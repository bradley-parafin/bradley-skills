"""List the parts of a Markdown draft that are hardest to read.

Usage: readability.py FILE [FILE ...]   (or pipe text on stdin)

Reports sentences over 25 words, paragraphs or list items over 80 words,
sentences with 3+ code names, and paragraphs that open with a code name.
Also prints a reading-ease score that counts each code name as one short word,
so identifiers don't drag the score, and code names per 100 words as a
separate jargon number. Advisory only: always exits 0.
See ../references/readability-research.md.
"""

import re
import sys

LONG_SENTENCE, VERY_LONG_SENTENCE, WALL, CODE_HEAVY = 25, 40, 80, 3
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+(?:\[[ xX]\]\s+)?")
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
CODE_RE = re.compile(r"<code>(.*?)</code>|`([^`]+)`", re.S)
TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")
BOLD_LABEL_RE = re.compile(r"^\s*(?:\*\*|<b>)([^*<]{1,40}?)\.(?:\*\*|</b>)")
SENT_SPLIT_RE = re.compile(r"(?<=[.!?])[\"”)]?\s+(?=[\"“(\[A-Z0-9Ⓒ])")
CODE = "Ⓒ"


def units(text):
    """Yield (line_number, text) for each paragraph, bullet, or numbered item."""
    cur, start, in_fence, in_page = None, 0, False, False
    for n, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            s = ""
        elif in_fence:
            continue
        if s.startswith("<page"):
            in_page = not s.endswith("</page>")
            s = ""
        elif in_page:
            in_page = not s.startswith("</page>")
            continue
        if not s or s.startswith(("#", "|", "<!--")) or s in ("<p>", "</p>", "---"):
            if cur:
                yield start, cur
            cur = None
            continue
        m = LIST_RE.match(raw)
        if m:
            if cur:
                yield start, cur
            cur, start = raw[m.end():], n
            continue
        if cur is None:
            start = n
        cur = f"{cur} {s}" if cur else s
    if cur:
        yield start, cur


def clean(unit):
    unit = LINK_RE.sub(r"\1", unit)
    unit = BOLD_LABEL_RE.sub(lambda m: m.group(1) + ":", unit)
    unit = CODE_RE.sub(lambda m: CODE + re.sub(r"\s+", "_", m.group(1) or m.group(2)) + CODE, unit)
    unit = TAG_RE.sub("", unit).replace("&amp;", "&")
    return re.sub(r"\s+", " ", unit).strip()


def words(text):
    return [w for w in (t.strip(".,;:!?\"'()[]“”*") for t in text.split()) if re.search(r"[A-Za-z0-9" + CODE + "]", w)]


def syllables(word):
    if word.startswith(CODE) or not re.search(r"[A-Za-z]", word):
        return 1
    word = word.lower()
    count = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e") and not word.endswith(("le", "ee")) and count > 1:
        count -= 1
    return max(1, count)


def preview(text, n=12):
    return " ".join(text.replace(CODE, "`").split()[:n]) + " …"


def report(name, text):
    findings, sentence_lengths = [], []
    all_words = []
    for line, raw in units(text):
        unit = clean(raw)
        unit_words = words(unit)
        if not unit_words:
            continue
        if len(unit_words) > WALL:
            findings.append((line, f"paragraph {len(unit_words)} words: split it ({preview(unit)})"))
        if unit_words[0].startswith(CODE):
            findings.append((line, f"opens with a code name: say what happens first ({preview(unit)})"))
        for sentence in SENT_SPLIT_RE.split(unit):
            sw = words(sentence)
            if not sw:
                continue
            sentence_lengths.append(len(sw))
            all_words += sw
            codes = sum(w.startswith(CODE) for w in sw)
            if len(sw) > VERY_LONG_SENTENCE:
                findings.append((line, f"sentence {len(sw)} words: split it ({preview(sentence)})"))
            elif len(sw) > LONG_SENTENCE:
                findings.append((line, f"sentence {len(sw)} words ({preview(sentence)})"))
            if codes >= CODE_HEAVY:
                findings.append((line, f"{codes} code names in one sentence ({preview(sentence)})"))
    if not sentence_lengths:
        return
    avg = sum(sentence_lengths) / len(sentence_lengths)
    over = 100 * sum(n > LONG_SENTENCE for n in sentence_lengths) / len(sentence_lengths)
    syl_per_word = sum(map(syllables, all_words)) / len(all_words)
    ease = 206.835 - 1.015 * avg - 84.6 * syl_per_word
    codes = 100 * sum(w.startswith(CODE) for w in all_words) / len(all_words)
    print(f"{name}: {len(sentence_lengths)} sentences, average {avg:.1f} words, {over:.0f}% over {LONG_SENTENCE}, "
          f"reading ease {ease:.0f} (code names as one word), {codes:.1f} code names per 100 words")
    for line, message in findings:
        print(f"  line {line}: {message}")


def main():
    paths = sys.argv[1:]
    if not paths:
        report("stdin", sys.stdin.read())
    for path in paths:
        with open(path, encoding="utf-8") as f:
            report(path, f.read())


if __name__ == "__main__":
    main()

"""Check a PR title/body or ticket text for writing mistakes a script can catch.

Usage: prose_check.py [--title TEXT] [--body TEXT | --body-file PATH]
Prints one finding per line and exits 1 when any finding is blocking.
"""

import argparse
import re
import sys

CHECKLIST = "~/Code/bradley-skills/skills/sound-human/references/pr-and-ticket-checklist.md"

FILLER = ["robust", "seamless", "seamlessly", "ensures", "leverages", "leverage", "comprehensive", "utilize"]
SESSION_LINK = re.compile(r"claude\.ai/code|claude://|chatgpt\.com/codex")
LITERAL_ESCAPE = re.compile(r"\\u[0-9a-fA-F]{4}")
MENTION = re.compile(r"(?<![\w`/.@-])@[A-Za-z][\w-]*")
BARE_PR = re.compile(r"(?<![\w/])(?:[a-z][\w-]*)?#\d{2,}\b")
BARE_ID = re.compile(r"\b[A-Z]{2,}(?:-[A-Z]{2,})*-(?:\d{2,}|[A-Z0-9]{3})\b")
NOT_YET = re.compile(r"\b(?:the next PR|a follow-?up(?: PR)?|in a follow-?up)\b", re.I)
NOW_WORDS = re.compile(r"\b(?:now|no longer|until now)\b", re.I)


def strip_code(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", " ", text)


def strip_links(text):
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", text)
    return re.sub(r"https?://\S+", " ", text)


def first_sentence(body):
    for block in re.split(r"\n\s*\n", body):
        line = block.strip()
        if not line or line.startswith(("#", "[", "<!--", "- [", "|", "🤖")):
            continue
        return re.split(r"(?<=[.!?])\s", line, maxsplit=1)[0]
    return ""


def check(title, body):
    findings = []

    def add(blocking, message):
        findings.append((blocking, message))

    for label, text in (("title", title), ("body", body)):
        if not text:
            continue
        if LITERAL_ESCAPE.search(text):
            add(True, f"{label}: literal \\uXXXX escape; type the real character")
        if SESSION_LINK.search(text):
            add(True, f"{label}: links an agent session; remove it")
        prose = strip_links(strip_code(text))
        for handle in sorted(set(MENTION.findall(prose))):
            add(True, f"{label}: {handle} notifies someone on GitHub; drop it or put it in backticks")
        for word in FILLER:
            if re.search(rf"\b{word}\b", prose, re.I):
                add(False, f"{label}: filler word \"{word}\"; say what happens instead")

    if title:
        if title.startswith("["):
            add(False, "title: write the ticket ID without brackets, e.g. `MXA-1234 Do the thing`")
        if len(title) > 80:
            add(False, f"title: {len(title)} chars; name only the main change")
        if NOW_WORDS.search(title):
            add(False, "title: \"now\"/\"no longer\" reads as already merged; use a plain verb")

    if body:
        prose = strip_links(strip_code(body))
        linked = " ".join(label + " " + url for label, url in re.findall(r"\[([^\]]*)\]\(([^)]*)\)", body))
        opening = first_sentence(strip_code(body))
        if opening and NOW_WORDS.search(opening):
            add(False, f"body: first sentence says \"now\"/\"no longer\"; start with what the PR does (\"Updates X to …\"): {opening[:90]}")
        for ref in sorted(set(BARE_PR.findall(prose)) - set(BARE_PR.findall(linked)) - {"#" + n for n in re.findall(r"/pull/(\d+)", linked)}):
            add(False, f"body: {ref} isn't linked; write it as [{ref}](url)")
        for ref in sorted(set(BARE_ID.findall(prose)) - set(BARE_ID.findall(linked))):
            add(False, f"body: {ref} isn't linked; link the ticket, Sentry issue, or incident")
        for phrase in sorted(set(m.group(0) for m in NOT_YET.finditer(prose))):
            add(False, f"body: \"{phrase}\" points at something unnamed; link it or name its ticket")
        readable = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", strip_code(body))
        for block in re.split(r"\n\s*\n|\n\s*(?:[-*+]|\d+\.)\s+", readable):
            block_words = block.split()
            if len(block_words) > 80:
                add(False, f"body: {len(block_words)}-word paragraph; split it ({' '.join(block_words[:8])} …)")
            for sentence in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(\[\"])", block):
                if len(sentence.split()) > 40:
                    add(False, f"body: {len(sentence.split())}-word sentence; split it ({' '.join(sentence.split()[:8])} …)")
        if body.count("—") > 2:
            add(False, f"body: {body.count('—')} em dashes; use periods or commas")
    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default="")
    parser.add_argument("--body", default="")
    parser.add_argument("--body-file")
    args = parser.parse_args()
    body = args.body
    if args.body_file:
        body = sys.stdin.read() if args.body_file == "-" else open(args.body_file, encoding="utf-8").read()
    findings = check(args.title, body)
    for blocking, message in findings:
        print(("BLOCK " if blocking else "check ") + message)
    if not findings:
        print("no findings; still read it against " + CHECKLIST)
    sys.exit(1 if any(b for b, _ in findings) else 0)


if __name__ == "__main__":
    main()

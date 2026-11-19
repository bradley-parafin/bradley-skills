# What makes text readable

The research behind the "Length and order" rules in `SKILL.md`. Most sources below are summaries or official style guidance; the primary studies weren't all read in full.

## Findings

| Finding | What it means for writing | Source |
|---|---|---|
| Readability formulas (Flesch, Flesch-Kincaid, Fog, SMOG) count only word and sentence length. | Use them as a warning light. They can't see jargon, order, or whether the ideas connect, and they misjudge technical docs. | AHRQ; Redish (2000) |
| Plain-language guides target 15–20 words per sentence on average. GOV.UK caps sentences at 25 words and paragraphs at five sentences. | Rewrite sentences over 25 words; split paragraphs over five sentences or about 80 words. | GOV.UK; ONS; Newcastle University |
| Often-quoted American Press Institute figures put comprehension near 90% at 14 words per sentence and under 10% at 43 or more. | Sentences over 40 words almost always need splitting. The study's method couldn't be checked, so treat the numbers as directional. | API, via secondary summaries |
| Readers scan web pages in F-shaped and layer-cake patterns: headings, then the first words of lines. | Put the point in the heading and the first sentence. Front-load key words. | Nielsen Norman Group |
| Cohesion predicts comprehension better than formulas. In McNamara's example, a more cohesive text scored *harder* on Flesch-Kincaid (11.2 vs 9.3) because linking words lengthen sentences. | Keep "because," "so," "then." Shorter isn't the goal; connected is. | Graesser et al. (2004), Coh-Metrix; McNamara |
| Readers expect familiar context at the start of a sentence and new information at the end. | Open with the actor or event the reader knows; put the new term or code name last. | Gopen & Swan (1990) |
| Each unfamiliar term costs effort, and formulas can't see it. Scoring code names as words moved one guide's Flesch reading ease from 51 to 35. | Cut code names the reader doesn't need to act; say what a thing does before naming it. | Measured on an internal developer guide, Nov 2026 |

## Rubric for a readability score

When asked to score a document, use this rubric and say it's a rubric built from these sources, not a published standard.

| Dimension | Points | Full marks when |
|---|---|---|
| Sentence length | 20 | Average 15–20 words or less, under 10% over 25, none over 40 |
| Paragraph size | 15 | No paragraph or list item over 80 words |
| Code names and jargon | 25 | Under 2 code names per 100 words, few sentences with 2+ |
| Word-level ease | 10 | Flesch reading ease 50+ with code names set aside |
| Structure and front-loading | 15 | Headings state the point; first sentences say what happens |
| Old before new | 10 | Paragraphs open with the actor or event, not a code name; one term per thing |
| Active voice | 5 | Under 10% passive |

## Sources

- [AHRQ: Use caution with readability formulas](https://www.ahrq.gov/talkingquality/resources/writing/tip6.html)
- [Redish (2000), readability formulas' limits, ACM](https://www.doi.org/10.1145/344599.344637)
- [How to measure readability (KP Washington)](https://prism.kpwashingtonresearch.org/background_to_plain_language/how_to_measure_readability.html)
- [NN/g: F-pattern in reading digital content](https://www.nngroup.com/videos/f-pattern-reading-digital-content/)
- [Newcastle University: readability](https://www.ncl.ac.uk/design-system/ux/editorial/readability/)
- [GOV.UK: why 25 words is our limit](https://insidegovuk.blog.gov.uk/2014/08/04/sentence-length-why-25-words-is-our-limit/)
- [GOV.UK: clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/)
- [ONS service manual: plain language](https://service-manual.ons.gov.uk/content/writing-for-users/plain-language)
- [What is the perfect sentence length (API figures)](https://medium.com/@scottydocs/what-is-the-perfect-sentence-length-4690ce8d5048)
- [Graesser et al. (2004), Coh-Metrix](https://pubmed.ncbi.nlm.nih.gov/15354684/)
- [Beyond readability formulas (McNamara cohesion example)](https://www.hoosieramwa.org/news/2014/10/15/beyond-readability-formulas-an-interesting-free-text-analysis-tool)
- [Gopen & Swan (1990), The Science of Scientific Writing](https://www.win.tue.nl/~wstomv/quotes/science-of-scientific-writing.html)

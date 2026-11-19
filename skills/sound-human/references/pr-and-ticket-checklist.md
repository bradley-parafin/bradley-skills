# PR and ticket checklist

Use this before you publish a PR title, PR description, PR comment, or Linear ticket. Write for a reviewer from another team who hasn't seen the chat, the ticket, or the branch.

## PR title

- Start with the ticket ID, no brackets: `MXA-7717 Skip the preview offer AAN if one went out in the last 30 days`.
- Say what the code does differently, with a plain verb. Don't reuse a commit subject, don't describe where code moved, and leave secondary changes for the description.
- No terms a reviewer would trip on ("stops accept", "SNS lands"). Say what happens.

## PR description

- Follow the repo's template and description check exactly (AGENTS.md, "PR templates and description validation"). Required headings and checkbox text stay word for word.
- First sentence: what this PR does, as a verb. "Updates X to …", "Adds …", "Deletes …". Not "X now …", "no longer", or "until now": it isn't merged.
- Next: why, in plain words. Who is affected and what goes wrong today. For a bug, name the code's real term and the one assumption that broke.
- Each bullet says what the piece does before it names the endpoint, table, or class.
- Link a domain term where it first appears if a reviewer outside the area wouldn't know it (for example, a payments term like "capture" or "settlement" → the team's developer guide). Only where it helps.
- Link every reference: PRs as `[api#123](url)`, tickets, Sentry issues, Slack threads. No bare IDs.
- Don't point at things that don't exist yet ("the next PR", "a follow-up"). Link the PR or name its ticket.
- Keep sentences under about 25 words and paragraphs under about 80. Split anything over 40 words. Keep the "because" and "so" that connect two facts.
- State only what you verified. Cut guesses about what a person or system will do.
- One word per actor: don't drift between customer, user, and account, or order and purchase.
- Testing says what you ran and what happened, in that order. Before and after for a bug. No pasted logs.
- No session links, no `@handles` you haven't checked are real people, no links to private Notion or tracker pages.
- No "robust", "seamless", "ensures", "leverages", "comprehensive".

## Linear tickets

- Use the create-ticket skill. The title names the work. One concern per ticket.
- Every line is a decision. No "consider", "either", "if needed", or "decide which".

## Before and after you publish

- Run `python3 ~/Code/bradley-skills/skills/sound-human/scripts/prose_check.py --title "<title>" --body-file <file>` and fix what it reports, unless a finding is wrong for this text.
- Read the draft once as that reviewer from another team. Rewrite any sentence you'd have to read twice.
- After publishing a PR description, read it back with `gh pr view` and wait for the description check to pass.

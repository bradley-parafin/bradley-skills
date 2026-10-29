---
name: create-ticket
description: Write or revise engineering tickets (Linear issues, GitHub issues, handoff tasks) that an engineer or agent can pick up and execute without making decisions the author could have made. Use when creating tickets, splitting work into tickets, scoping a migration into tickets, or reviewing existing tickets for open decisions, hedges, or noise. Applies /sound-human for clarity.
---

# Create Ticket

A ticket is an instruction, not a discussion. Whoever picks it up, often an agent, should be able to start work from the ticket alone, without making a call the author could have made and without asking what a line means.

If the author leaves a decision open, the implementer hands it to an agent, and the agent decides without the context the author had. Make every decision you can before writing.

## Before writing

1. **Verify the facts yourself.** Read the code, the config, and the live state (schedules, flags, data) that the ticket depends on. Do not copy claims from a subagent, a chat summary, or an older ticket without checking them.
2. **Make the decisions.** For each open question, pick the answer and state it. Defaults:
   - Migrations and refactors keep today's behavior unless the ticket explicitly changes it.
   - Reuse the existing pattern the codebase already follows.
   - Pick the smallest change that does the job.
3. **Escalate only real decisions.** If a question needs someone else (product, compliance, another team), ask that person now. If the ticket can't be written without the answer, the ticket waits, or the ticket says exactly who decides and blocks on it. Never write "decide which" for the implementer.
4. **Decide the shape of the batch.** One ticket per independently shippable change, usually one per PR or deploy unit. Only make a ticket a sub-issue of another when it is truly part of that issue's scope. A pilot ticket is not an umbrella for follow-on work; use the project or a dedicated parent.

## What goes in

- **Current state:** what exists today and where it runs, with the smallest useful code references (file and function) inline.
- **The change:** what to build or move, stated as a definite instruction.
- **Rules the implementer would otherwise break:** only the non-obvious ones, each with its reason. Examples: "keep the event object type and id the same, or the idempotency keys change and people get the email twice", "merge only after Kitchen deploys, because merging airflow-dags deploys immediately".
- **Done when:** observable results someone can check (a run in Toolbox, a log line, a count).
- **Links:** the ticket or PR that shows the pattern to follow, and real blockers as blocking relations.

## What stays out

Cut every line that fails the act-on test: *does this line make the implementer do something, or prevent a specific mistake?*

- **Open choices:** "either A or B", "decide which to keep", "consider", "you could also". Pick one.
- **Hedges:** "if needed", "if it's still needed", "where possible", "may want to". State the instruction or delete it.
- **Non-issues:** "X can't be passed, but nothing uses it, so use the default." If nothing has to change, say nothing.
- **Speculation:** guesses about future sharing, refactors, or abstractions the ticket doesn't ask for. Mention shared code only when it exists and the ticket should reuse it, by name.
- **Process narration:** how the scoping was done, which agent found what, history of the decision.
- **Unverified claims** and anything marked "inferred" or "probably".
- **Status that will go stale** (assignee, cycle, priority) unless the user asked for it.

Shared steps that apply to every ticket in a batch (for example "follow the pilot ticket's steps: register the campaign, switch the scheduled job, delete the legacy jobs after a few clean runs") are fine to repeat. Keep them short and identical across the batch.

## Writing

Apply `/sound-human` to every ticket. In particular:

- Open with the current behavior and the concrete change, not background.
- Name who acts and where: the DAG, the job, the selector, the service.
- Introduce a component by what it does the first time it appears.
- Say explicitly when a piece already exists, so nobody rebuilds it ("the selectors already look up the offer").
- Describe behavior instead of vague phrases like "other paths" or "special cases".
- Title: an imperative outcome under ~70 characters ("Run accept-offer drips through the Kitchen campaign job"), with the team's ticket conventions.

## Final pass

Before creating or saving, reread every ticket line by line as the implementer:

1. Does each line pass the act-on test?
2. Is there any choice, hedge, or "if" the author could resolve? Resolve it.
3. Would an agent with no chat history know where to start and how to tell it's done?
4. Run the `/sound-human` ambiguity pass.
5. When a reader flags a problem in one ticket, sweep the whole batch for the same problem before replying.

## Example

Before:

> The legacy jobs wrap the selector in a one-minute statement timeout. The campaign runner doesn't, so move the timeout into the selector if it's still needed.
>
> The selectors pick applications whose step started 24 to 48 hours ago. Either keep a daily schedule, or change the selectors to check what was already sent. A $0 limit is sent today, while LOC drops those, so decide which to keep.

After:

> The legacy jobs wrap the selector in a one-minute statement timeout. The campaign runner doesn't, so set the same timeout inside the selector.
>
> The selectors pick applications whose step started 24 to 48 hours ago, which only works because the DAG runs every day. Keep the campaign task on this DAG's daily schedule. Keep today's credit-limit rule: skip only merchants with no limit.

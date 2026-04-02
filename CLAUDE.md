# CLAUDE.md — DataBees Internship 2026

Project-specific instructions for Claude Code when working in this repository.

---

## Repo Structure

```
raw/          — Raw input data: meeting transcripts, syllabi, rough notes from anyone
live/         — Living documents updated every session (session notes, use cases, etc.)
action/       — Intern work artifacts: completed tasks, submissions, assignments
```

## How I Work With This Repo

- **raw/meeting-transcripts/** holds Otter.ai (or similar) transcript files from each session.
- After each session, read the transcript and summarize the discussion into **live/internship-sessions.md** under the correct session heading.
- The live document is the source of truth for what was covered, tasks assigned, and decisions made.

## Session Ordering

Sessions in `live/internship-sessions.md` are ordered **latest first** — the most recent session goes at the top, older sessions below. Always insert new sessions above existing ones, not at the bottom.

## Session Notes Workflow

When given a meeting transcript to process:

1. Read the full transcript from `raw/meeting-transcripts/`.
2. Identify the correct session in `live/internship-sessions.md` by date.
3. Fill in or update:
   - **Attendees** — include all speakers mentioned.
   - **Week Check-in** — what each intern worked on, any interesting discussions.
   - **Agenda sections** — summarize each agenda item discussed.
   - **Action Items** — clear table of tasks, who owns them, for next session.
4. Do not overwrite existing content that was pre-filled — merge and enrich it.
5. Keep summaries concise but complete enough for absentees to follow.

## Writing Style for Session Notes

- Use bullet points for intern check-ins (name + what they did).
- Use numbered headings within each session (### 1. ..., ### 2. ...).
- Use a markdown table for action items.
- Avoid padding — capture decisions and learnings, not every sentence.

## Key People

- **Sanjeev Kumar** — Mentor & Organizer (DE track lead)
- **Vinod** — Mentor (DA track)
- **Vivek Prasad** — Mentor (ML track)
- **Kousalya** — Organizer
- Interns: Suhash Raja, Filip Cedermark, Deepika Elangovan, Neha Doda, Asindu Gayangana, Nikolaos Biniaris, Elliot Eriksson

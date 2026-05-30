# Midweek Sync Progress

A running log of all intern midweek check-in calls. Latest first.

---

## Midweek Sync — May 27, 2026

**Attendees:** Kousalya, Filip Cedermark, Neha Doda
**Absent:** Suhash Raja, Deepika Elangovan, Asindu Gayangana, Elliot Eriksson, Nikolaos Biniaris

*Short 8-minute check-in. Low attendance; no blockers raised.*

### Intern Progress Updates

- **Filip Cedermark** — Continuing dbt work; no major new things to show. Planning to scale up — looking for larger datasets (API sources or public datasets) to move beyond small sample data and practice proper data modeling at scale.
- **Neha Doda** — Learning a lot; tried GitHub for the first time yesterday. Cloned the repo, created a fork, and raised a pull request to add her Power BI storage modes presentation to her `action/` folder. PR is visible in GitHub and awaiting Sanjeev's approval for merge.

### GitHub Q&A (Neha + Filip)

Filip screenshared to show Neha where to find pull requests in the repo (Code → Pull Requests tab). Confirmed Neha's PR is correctly submitted — it will merge once Sanjeev approves it. Correct workflow confirmed: clone repo → add files → fork → pull request.

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Review and approve Neha's PR (Power BI presentation) | Sanjeev | ASAP |
| Find larger dataset / API source for dbt modeling at scale | Filip | Next session |

---

## Midweek Sync — May 20, 2026

**Attendees:** Kousalya, Neha Doda, Filip Cedermark, Suhash Raja
**Absent:** Deepika Elangovan, Asindu Gayangana, Elliot Eriksson, Nikolaos Biniaris

*Short 11-minute check-in. No blockers raised; mostly status updates.*

### Intern Progress Updates

- **Neha Doda** — Busy week (Swedish classes + family commitments). Working on the Power BI storage modes presentation assigned by Sanjeev (import, direct query, composite). Also exploring Microsoft Fabric alongside internship work.
- **Filip Cedermark** — Moved from learning dbt to actively using it on the internship project. No concrete demo yet but making progress. Plans to reach out to Raj/Nikolaos to get credentials for a separate project that was discussed earlier. Will drop his GitHub username in the new group channel Raj created.
- **Suhash Raja** — Continuing with streaming and transformation work. Plans to share DABs deployment code in the repo from last week's progress.

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Drop GitHub username in Raj's new group channel | Filip | ASAP |
| Share DABs deployment code in repo | Suhash | ASAP |

---

## Midweek Sync — May 6, 2026

**Attendees:** Kousalya, Deepika Elangovan, Filip Cedermark, Neha Doda, Suhash Raja, Asindu Gayangana
**Absent:** Elliot Eriksson, Nikolaos Biniaris

### Intern Progress Updates

- **Deepika Elangovan** — Researched Databricks Asset Bundles + Terraform for CI/CD in data engineering. Key findings: Terraform handles infrastructure (catalog, storage, permissions); Databricks Asset Bundles handle pipeline/job deployment via YAML files and CLI — supports multi-environment setup (dev/test/stage/prod). Still doing hands-on; iterating with Claude-generated code and hitting some errors.
- **Filip Cedermark** — Set up dbt mid-last-week, going through the official intro course. Still getting familiar with practices and workflow. Will have something to show by Saturday. Offered to share dbt intro course link with Neha.
- **Neha Doda** — Started dbt last week; following mixed sources (YouTube, ChatGPT). Limited progress this week — busy with a task assigned by Raj.
- **Suhash Raja** — Recovering from fever/cold since last Friday. Plans to work on something the next day and have an update for Saturday.
- **Asindu Gayangana** — Completed sales pipeline (Medallion) through gold layer. Pipeline parameterized to support both daily incremental runs and historical backfill using the same code. Attempted to screen-share but had connectivity issues — deferred to Saturday (May 9) session.

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Send dbt intro course link to Neha | Filip | ASAP |
| Share Databricks Asset Bundles video link | Deepika → Asindu | ASAP |
| Present sales pipeline (Medallion, bronze→gold) | Asindu | Saturday May 9 |
| Have dbt progress to show | Filip | Saturday May 9 |

---

## Midweek Sync — April 29, 2026

**Attendees:** Kousalya, Filip Cedermark, Neha Doda, Asindu Gayangana, Raj Kumar *(dropped in briefly)*
**Absent:** Deepika Elangovan, Elliot Eriksson, Nikolaos Biniaris, Suhash Raja *(joined late)*

### Intern Progress Updates

- **Filip Cedermark** — Just installed dbt; going through the official intro course. Confirmed using Medallion architecture (bronze/silver/gold schemas set up). Plans to integrate dbt into the silver transformation layer. Confirmed dbt has a Databricks connector.
- **Asindu Gayangana** — Databricks 14-day trial expired; switched to Managed Tables (no external cloud connection). Using AutoLoader to load data to bronze (partitioned by load date), silver complete, gold not yet started. ~3 tables, millions of rows. Using Databricks built-in scheduler.
- **Neha Doda** — Connected dbt to Microsoft SQL Server locally.

### Raj Kumar's Inputs

- Role-specific stream split starting this week.
- Plans to use intern Medallion architecture pipelines for an internal MVP — confirmed Filip and Asindu have end-to-end Medallion set up.
- Will connect with Sanjeev on end-to-end output and scheduler integration.
- Wants 15-min 1:1s with all interns: Filip (Apr 30, in office), Asindu (Apr 29 at 2:30 via Slack), Deepika/Elliot/Nikolaos to be scheduled via Kousalya.

### Logistics

- Saturday Apr 26 session was cancelled (Sanjeev business trip). Next meeting: Wednesday May 6.

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| 1:1 with Filip | Raj | Apr 30 (in office) |
| 1:1 with Asindu | Raj | Apr 29 at 2:30 (Slack) |
| Schedule 1:1s with Deepika, Elliot, Nikolaos | Kousalya | This week |
| Connect with Sanjeev re: E2E output + scheduler | Raj | TBD |

---

## Midweek Sync — April 22, 2026

**Attendees:** Kousalya, Neha Doda, Filip Cedermark, Deepika Elangovan *(arrived after others had left)*
**Absent:** Suhash Raja, Asindu Gayangana, Elliot Eriksson, Nikolaos Biniaris

*Impromptu 12-minute call. Most interns saving updates for the Saturday session.*

### Intern Progress Updates

- **Filip Cedermark** — Recovering from a difficult personal week; picking up again. Has started looking into dbt more following Session 5's platform diversification discussion. Saving detailed updates for Saturday.
- **Neha Doda** — Has a cold; working remotely from India. Installed dbt locally and read about it — noted it uses SQL for data transformations, which complements her DA/Power BI background. Also explored Databricks (free edition) as a platform. Previously looked at Microsoft Fabric but found it has no free learning tier. Wants Sanjeev's guidance on whether to focus on dbt or Databricks first, or whether she can do both simultaneously. Filip's view: Databricks is an environment, dbt is a framework — they complement each other and can be done in parallel.
- **Deepika Elangovan** *(arrived after call ended)* — Was removed from the Slack workspace (free 14-day trial expired). Kousalya to follow up with Raj to get her re-added.

### Logistics

- Meeting timing to be decided at the Saturday (Apr 26) session when most members are present.

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Discuss dbt vs Databricks prioritisation with Sanjeev | Neha | Saturday session |
| Re-add Deepika to Slack — follow up with Raj | Kousalya | ASAP |
| Agree on fixed midweek sync timing | All | Saturday session |

---

## Midweek Sync — April 15, 2026

**Attendees:** Kousalya, Suhash Raja, Filip Cedermark, Neha Doda, Deepika Elangovan
**Absent:** Elliot Eriksson, Asindu Gayangana

### Onboarding — Neha (DA Track)

Suhash walked Neha through the internship program plan for the BA Analyst path:

- Month 1 focus: SQL (window functions, common queries) — practice via HackerRank and ChatGPT
- Can use her existing Microsoft SQL Server for hands-on work; alternatively sign up for Databricks Free Community Edition (browser-based)
- Filip pointed her to the GitHub repo and explained the `live/` folder for use cases and assignments
- Discussed uploading personal work under `action/` — each intern to create their own subfolder

### Intern Progress Updates

- **Filip Cedermark** — Slower week due to personal commitments. Implemented `Faker` (per Sanjeev's feedback) to generate synthetic customer event data; built a Delta table in Databricks and is practicing CDC patterns within a medallion architecture (bronze → silver). Next: deduplicate by most recent row per ID when moving data to the silver layer.
- **Suhash Raja** — Made progress ingesting data from Azure Storage. Learned about **Azure Access Connector for Databricks** — a service used to create credentials for Databricks to access Azure Storage. Once configured, Spark (`readStream` / `read`) automatically uses those credentials to load Delta tables in the bronze layer.
- **Deepika Elangovan** — Prepared a small PPT recap of her CI/CD with GitHub Actions demo (requested by Sanjeev). Also studied incremental ingestion concepts and Parquet vs Delta — new topics for her. Will demo at the Sunday session.

### Logistics

- Weekend session timing: moving from **Saturday → Sunday**, same time slot (9–10:30 AM) — Sanjeev confirmed Sunday works better; Kousalya to update the invite.
- Wednesday midweek sync timing: currently 4:30 PM; discussion on whether to revert to 3:30 PM Swedish time — to be decided at the Sunday session.

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Confirm weekend session moves to Sunday (same time) | Kousalya | Before Sunday |
| Discuss and agree on preferred Wednesday sync timing | All interns | Sunday session |
| Upload work artifacts to `action/` folder on GitHub | All interns | Ongoing |
| Demo: CI/CD with GitHub Actions | Deepika | Sunday session |

---

## Midweek Sync — April 8, 2026

**Attendees:** Kousalya, Elliot Eriksson, Suhash Raja, Asindu Gayangana, Deepika Elangovan, Neha Doda
**Absent:** Filip Cedermark (informed in advance)

### Intern Progress Updates

- **Suhash Raja** — Setting up data sources for Stage 1 (batch ingestion). Unsure which specific datasets to use from the use case (customers/orders DB, product catalog, store inventory). Exploring the GitHub action items.
- **Elliot Eriksson** — Hasn't started hands-on work yet; planning to begin that evening or the following day. New to Databricks; scoped out the ML tasks on GitHub.
- **Asindu Gayangana** — Built a batch pipeline in Databricks using CSV and Parquet files; created dimension tables (product, country, etc.) with ~3M records. Next step: streaming pipeline using an external API (Raspberry Pi / CoinGecko).
- **Deepika Elangovan** — Created a free-tier Databricks account, watched YouTube tutorials for onboarding. Used Faker library (via ChatGPT-generated code in VS Code) to generate sample data. Planning to import generated data into Databricks for hands-on work.

### Technical Discussion — Databricks AutoLoader (Asindu demo)

Asindu screen-shared to walk the team through AutoLoader (`spark.readStream` with `format("cloudFiles")`):

- **`inferSchema`** — auto-detects column types from source files (avoids everything loading as strings)
- **`schemaLocation`** — persists detected schema to a folder for reuse across runs
- **`schemaEvolutionMode`** — handles newly added columns in source files; use with `mergeSchema` to propagate new columns downstream without failing the pipeline

Asindu offered to upload a Databricks features comparison document to Slack and the GitHub repo for the team's reference.

### Data Sources Discussion

- Use case calls for: customers/orders DB, product catalog, store inventory, suppliers
- Consensus: interns can use any representative data (downloaded CSV, Faker-generated data, or free APIs)
- **CoinGecko API** suggested as a free streaming data source (price updates every ~30 min)
- **Faker library** confirmed usable for synthetic retail data generation

### GitHub Workflow Clarification

- Interns discussed whether to fork or push directly. Consensus: fork the repo and submit via **pull request** from a feature branch.

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Upload Databricks features comparison doc to Slack/repo | Asindu | ASAP |
| Begin hands-on pipeline work in Databricks | Elliot | This week |
| Finalize data source selection and start batch ingestion | Suhash | This week |
| Continue Faker data generation → import into Databricks | Deepika | This week |
| Read up on Parquet, Iceberg, Delta Lake, Hudi formats | All DE track | Before next Saturday session |

---

## Midweek Sync — April 1, 2026

**Attendees:** Kousalya, Elliot Eriksson, Filip Cedermark, Neha Doda, Asindu Gayangana, Vinod Kumar
**Absent:** Deepika Elangovan (Swedish class conflict), Suhash Raja

### Scheduling

Deepika flagged a conflict: Swedish class runs 1–4 PM on Wednesdays. Team discussed rescheduling future midweek syncs to **before 12 PM or after 4 PM**. All present confirmed flexibility. Neha noted she also has Swedish class 9–11 AM on Wednesdays, so 11 AM–12 PM or after 4 PM works for her.

### GitHub Access Issue

Interns had not yet received access to Sanjeev's GitHub repo. Elliot had tried messaging on Slack with no response. Kousalya and Vinod noted Sanjeev was likely busy and agreed to reach out via the group Slack channel to get the repo link shared before the weekend session.

### Intern Progress Updates

- **Elliot Eriksson** — Has been reading up on PySpark (found it interesting based on the distributed systems topic from the last session). No concrete tasks yet due to missing GitHub access.
- **Filip Cedermark** — Continued SQL study; started building a basic pipeline structure after last Saturday's session discussion. Set up file structure and began generating sample data in Databricks.
- **Asindu Gayangana** — Started building a pipeline in Databricks. Shared key distinction: free edition does not support streaming pipelines; 14-day premium trial does. Suggested using the free tier for the batch pipeline tasks.

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Share GitHub repo link / grant access to interns | Sanjeev (via Kousalya + Vinod follow-up) | Before Saturday session |
| Reschedule future midweek syncs (before 12 or after 4) | Kousalya | Next week |
| Continue pipeline setup and sample data generation | Filip | Saturday session |
| Explore Databricks free edition for batch pipeline work | Asindu | Saturday session |
| Read up on PySpark and clarify ML task scope | Elliot | Saturday session |

# Midweek Sync Progress

A running log of all intern midweek check-in calls. Latest first.

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

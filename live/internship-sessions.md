# Databee Internship 2026 — Session Notes

> Sessions are ordered **latest first** — most recent session at the top.

---

## Session 13 — June 27, 2026 *(upcoming)*

**Agenda:**

**Part 1 — Weekly sync & check-ins**

1. Week check-in — what did you work on? Blockers? Wins? *(2-week gap — Midsommar break)*
2. ~~Suhash — Slide deck: MV vs streaming table vs Delta table + DLT use case design with SCD 1 & 2~~ *(carried over Sessions 9–12)* → Session 13 target
3. Neha — 20-min storytelling session: present existing dashboard to group as business stakeholders *(carried over from Session 12)*
4. Deepika — MLflow progress + MLOps hands-on share-out

**Part 2 — Technical deep-dives**

5. Asindu — Large-scale Spark job: scale to 100–200 GB, simulate skewed joins, identify bottlenecks
6. Filip — Enhanced Faker generator + dbt pipeline at scale
7. Nikolaos — Expand Tableau dashboards + Databricks Genie AI integration for ad hoc analysis

**Standing items**

8. Sanjeev — Share Spark UI/DAG screenshots + logs for bottleneck analysis exercise *(carried over from Session 11)*

---

## Session 12 — June 13, 2026

**Attendees:** Sanjeev Kumar (mentor), Kousalya, Neha Doda, Suhash Raja, Deepika Elangovan, Asindu Gayangana, Nikolaos Biniaris
**Absent:** Filip Cedermark, Elliot Eriksson

**Agenda:**

**Part 1 — Weekly sync & check-ins**

1. Admin — Next week is Midsommar (June 20) — **no session**. Next session June 27. ✅ *(Kousalya to inform Raj + Slack)*
2. Week check-in — what did you work on? Blockers? Wins?
3. ~~Suhash — Slide deck: MV vs streaming table vs Delta table + DLT use case design with SCD 1 & 2~~ → *(not prepared; unit testing work instead — carry over)*
4. Deepika — MLOps progress ✅ *(pushed code to repo; started MLflow)*
5. ~~Nikolaos — Databricks widget parametrization~~ → *(pivoted to Tableau dashboards — see section 4)*

**Part 2 — Technical deep-dives**

6. ~~Neha — 20-min storytelling session~~ → *(deferred; was in Microsoft AI Skills event — carry over to Session 13)*
7. Asindu — 27–28 GB pipeline run + GitFlow / CI-CD branching discussion ✅
8. ~~Filip — Enhanced Faker~~ → *(absent)*

**Standing items**

9. ~~Sanjeev — Share Spark UI/DAG screenshots + logs~~ → *(carry over — action item confirmed)*

**Notes:**

---

### 1. Admin

- Raj organising an intern dinner next week (June 20 — Midsommar week). Sanjeev to try to join if travel permits.
- No session June 20. Kousalya to inform Raj + Slack channel.

---

### 2. Suhash — Config-Driven Development + Unit Testing

Built a config-driven pipeline scaffold: folder structure, logging utility, config loader, `add_metadata` utility. Wrote unit tests for logging and `config_load` (both passing). `add_metadata` test failing — error: "cannot create local Spark session" when running via pytest with Databricks Connect installed.

**Sanjeev debug session (screen share):**
- Root cause of the Spark session error: when Databricks Connect is installed, local `SparkSession.builder.getOrCreate()` is intercepted. Fix: add an environment check — if running locally (not on Databricks), instantiate a standalone local Spark session; if on Databricks, let the platform inject it automatically.
- Actual test failure spotted: `assert "ingestion_timestamp" in enriched.columns` — **data type mismatch**: `enriched.columns` returns a list of strings; the `in` check works, but the assertion message shows it's not found. Likely the column name differs or the DataFrame isn't being built correctly. Fix: use `assert "ingestion_timestamp" in enriched.columns` and verify the column is actually being added by the function before asserting.
- Test folder structure (unit/integration split) is correct. Integration tests intentionally empty — they run on cluster, not locally. Fine.
- DABs deployment is working — code deployed to Databricks workspace successfully.
- **Recommendation:** use Databricks Genie (built-in AI) for Databricks-specific troubleshooting rather than ChatGPT alone — it has more Databricks context.
- General principle: only Databricks Asset Bundles and declarative pipelines are Databricks-specific. Everything else (project structure, logging, config, testing) is standard software engineering.

---

### 3. Deepika — MLOps Progress

Pushed all existing code to internship repo. Started MLOps path:
- Covered ML lifecycle, tools landscape, MLOps vs DevOps distinction.
- Built a small end-to-end MLOps project for hands-on understanding.
- This week: exploring MLflow and Kubeflow. Kubeflow felt easier (has Kubernetes background). MLflow harder — YouTube example was too advanced.

→ **Sanjeev**: Start with MLflow — open source, Databricks-integrated, widely used in production. SageMaker is dominant in AWS world; Azure AI Foundry for Azure. Concept stays the same across frameworks; don't get blocked by framework choice. Find a simpler MLflow example first; build up from there.

---

### 4. Neha — Data Cleaning + Stakeholder Alignment (screen share)

Neha shared an Excel dataset (Swedish product/supplier data from a previous interview project — OKQ8 logistics). Questions about data cleaning: irregular spaces in product/supplier names, Swedish characters, abbreviations.

**Sanjeev's feedback:**
- As a DA/analytics engineer, **never clean or transform data without stakeholder sign-off**. The data belongs to the business, not the analyst.
- Correct process: take a sample → present to stakeholders → agree on what changes are acceptable → codify those changes as rules/test cases → apply.
- Thought process matters in interviews: if you left irregular spaces *intentionally* because you didn't have business confirmation, say that. Explain your reasoning. Interviewers value this more than "I cleaned everything I didn't like."
- If data is small (Excel-level), cleaning details don't affect performance. If data grows to GBs, think about layout optimization (partitioning keys, file format).

Storytelling session deferred to Session 13 (Neha was in Microsoft AI Skills event this week, no time to prepare). Neha also explored Fabric Eventhouse and Event Streams this week.

---

### 5. Asindu — GitFlow, CI-CD Branching, UI vs Local Dev, Views vs Tables

**GitFlow & feature branching (Sanjeev explanation):**
- General rule: create feature branch from **main** (production state) — you build on what is live, not on in-progress work from colleagues.
- Exception: if your feature directly depends on another in-progress feature, branch from **dev** or from that feature branch.
- Feature branches: delete after merging to main. Pull request → merge → delete branch is the clean pattern.
- Dev branch = production + latest additions. Main = production. Feature branches feed into dev via PRs; dev feeds into main after integration testing passes.
- **Recommended read for all interns: GitFlow workflow** — learn when to use main/dev/feature/release/hotfix branches.

**Databricks UI vs local IDE:**
- Both are valid. ~70% of Databricks users prefer UI development for fast iteration (prototype, run notebook, see output immediately).
- Hardcore data engineers often prefer local IDE for more control.
- Databricks UI supports full Git-based workflow: link folder to Git repo, pull, create branches, raise PRs — same as local.
- Key: pull at the start of every session regardless of where you work.

**Temporary views vs materialized tables (Asindu observed view re-running transformations each time):**

*Nikolaos explained first (correct):* views are always recomputed from source — always fresh, but slow for complex logic; tables are materialized — fast queries, but require a scheduled job to stay updated.

*Sanjeev expanded with the full framing:*
- **View** = window to the garden (recomputed every query, always fresh, no extra table to manage, slow on large data)
- **Materialized table** = the garden itself (pre-computed, stored, fast, extra maintenance overhead)
- Choice depends on data volume + query frequency: small data or infrequent queries → views fine. Large data or many users querying simultaneously → materialize. Paying for compute 100x vs paying for it once.

**Scale challenge:** Asindu ran 27–28 GB joins across 3 tables — completed in 2 seconds. → **Sanjeev**: 27 GB is too small for Spark to struggle. Targets to simulate real-world problems:
- Scale to **100–200 GB**.
- Write two join queries: one filtering *before* the join, one filtering *after* — compare performance.
- Simulate **data skew**: 26 GB for Sweden region, 1 GB for everything else. Partition by region. Observe slowness and uneven executor loads in Spark UI.

---

### 6. Nikolaos — Tableau Dashboards + Databricks Genie for Ad Hoc Analysis

Pivoted from widget parametrization. Built two Tableau dashboards on gold layer data:

**Dashboard 1 — Holiday Performance:**
- Holiday vs non-holiday average revenue per day
- Total revenue by holiday (bar) + order count (line) — combination chart
- Interactive action filters (click to drill down)
- Data powered by gold metric tables + Holidays API join

**Dashboard 2 — Customer Segmentation & Analytics:**
- RFM (Recency, Frequency, Monetary) analysis → customer segments: loyal, at-risk, lost, promising
- CLV (Customer Lifetime Value) by cohort + time-based segmentation
- Repeat purchase rate trend (0–40% — low for supply chain industry)
- Customer retention heat map
- Interactive filters throughout

**Sanjeev challenge: ad hoc queries (e.g. "show me Black Friday season metrics"):**
→ Nikolaos: if data exists in gold layer, add interactive Tableau filter → 1-day sprint for user. For AI-driven ad hoc → use **Databricks Genie**: train it with gold layer context, SQL query examples, window function templates, table descriptions. Monitor accuracy via Genie benchmarks (hallucination rate, response accuracy %).

**Sanjeev feedback:** Exactly the right answer. Customers are asking about AI-integrated dashboarding everywhere. Being able to say *"here's how I'd add Genie, here's how I'd train it, here's how I'd monitor accuracy"* is a differentiating answer in any interview. Always pair AI usage with quality monitoring — same principle as DQ frameworks, just applied to AI responses.

→ Broader message to all interns: AI should be positioned as a companion that makes you 10x productive, not a threat. Companies hiring now expect engineers to use AI effectively and show amplified output.

---

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Inform Raj + Slack: no session June 20 (Midsommar) | Kousalya | ASAP |
| Fix `add_metadata` unit test — resolve SparkSession instantiation + column assertion bug | Suhash | Next session |
| Prepare slide deck: MV vs streaming table vs Delta table *(4th carry-over)* | Suhash | Next session |
| Continue MLflow hands-on; find simpler example; build up from there | Deepika | Next session |
| Push MLflow experiment code to repo | Deepika | Next session |
| Prepare storytelling session: present existing dashboard to group as business stakeholders *(deferred)* | Neha | Next session |
| Scale pipeline to 100–200 GB; simulate skewed joins (Sweden skew scenario); observe Spark behaviour | Asindu | Next session |
| Expand Tableau dashboards + explore Databricks Genie integration for ad hoc analysis | Nikolaos | Next session |
| Start enhanced Faker generator using complex dataset as template *(carry-over)* | Filip | Next session |
| Share Spark UI/DAG screenshots + logs for bottleneck analysis exercise *(carry-over)* | Sanjeev | Before Session 13 |

---

## Session 11 — June 6, 2026

**Attendees:** Sanjeev Kumar (mentor), Kousalya, Neha Doda, Suhash Raja, Filip Cedermark, Asindu Gayangana
**Absent:** Deepika Elangovan, Nikolaos Biniaris, Elliot Eriksson

**Agenda:**

**Part 1 — Weekly sync & check-ins**

1. Week check-in — what did you work on? Blockers? Wins?
2. Neha — Direct Lake mode + Power BI Fabric Capacity pricing model PPT *(carried over Sessions 9 & 10)* ✅
3. ~~Suhash — Slide deck: MV vs streaming table vs Delta table + DLT use case design with SCD 1 & 2~~ → *(not prepared, carry over to Session 12)*
4. ~~Deepika — Multi-bundle DABs isolation validation + Terraform + DABs code to repo~~ → *(absent, carry over)*

**Part 2 — Technical deep-dives**

5. Asindu — DABs bundle creation + inferSchema research ✅ *(pivoted from metadata-driven demo)*
6. ~~Filip — Enhanced Faker generator + dbt scaled to large dataset~~ → *(busy week, carry over)*
7. ~~Nikolaos — Databricks widget parametrization~~ → *(absent, carry over)*
8. ~~Deepika — MLOps path kickoff~~ → *(absent, carry over)*
9. ~~Software licenses update~~ → *(not discussed)*

**Notes:**

---

### 1. Week Check-in

- **Filip Cedermark** — Very busy week (cousin's graduation, away Wed–Fri). Only worked Mon/Tue. Plan: found a larger, more complex multi-table open dataset → will write a generator using it as a structural template to boost volume while preserving schema complexity. Starting next week.
  → **Sanjeev**: No problem. Take your time.

- **Suhash Raja** — Continued unit/integration testing research (no slide deck yet). Learned: unit test = arrange sample data → run through transformation logic → assert outcome. Was using pandas for DataFrame assertions — queried whether that's the right approach. Also explored Spark logging and Spark UI concepts, unclear which interface is Spark UI in free Databricks (serverless). Also briefly explored Python virtual environments (UV, Poetry) and basic Python.
  → **Sanjeev**: Spark has its own testing framework — use that, not pandas. DQX is for *data quality in production*, not integration testing (corrected earlier confusion). Spark UI deep-dive in section 2. Also: research Databricks Permissions API for RLS/column masking in DABs.

- **Asindu Gayangana** — Created a DABs bundle on free edition: exported existing pipelines into bundle folder structure, assets auto-land in the correct folders. Researched `inferSchema` / info schema — found **not recommended for production**: scans source system at runtime, slows ingestion. Exploring cross-account DABs deployment using profiles + access tokens (two free edition accounts simulating dev → prod).
  → **Sanjeev**: Spot on about inferSchema. **Bronze principle:** land everything as strings — no schema concerns, full flexibility to reprocess later. Fix schema in silver. Good direction on DABs cross-account deployment. Scale pipeline to large data is the next priority.

- **Neha Doda** — Presented Direct Lake mode (verbal + screen share) and Microsoft Fabric Capacity pricing model (PPT). Has multiple finished Power BI dashboards (logistics, Spotify business performance) and wants to shift focus from building to **storytelling / stakeholder presentation**.
  → **Sanjeev**: Storytelling is a career-level skill. Will schedule a 20-min slot: Neha presents existing dashboard to the group as business stakeholders, group asks questions, Sanjeev grills and gives feedback. Neha to share dashboards + KPI pointers beforehand via Slack.

---

### 2. Spark UI & Debugging Deep-dive (Sanjeev screen share)

Triggered by Suhash's questions about Spark logging and which UI surface to use for debugging:

**Classic compute — full Spark UI:**
- Access: cluster page → **Spark UI** tab (not available on serverless).
- **Jobs tab:** run time, number of stages, total task count per job.
- **Stages tab:** shuffle read/write, input/output per stage.
- **Stage detail:** per-executor stats — spill to disk, shuffle bytes, partition balance. Reveals data skew (some executors doing far more work than others).
- **SQL/DataFrame tab — DAG:** the gold mine. Shows the full execution plan Spark built before running (lazy evaluation). Reveals: filter pushdown (or lack of it), join strategy (broadcast vs sort-merge), unnecessary shuffles, scans of millions of rows.
- **Structured Streaming tab:** input rate, processing rate, batch duration per streaming job.

**Serverless — Query Profile (simplified view):**
- Spark UI not exposed. Use **Query History → Query Profile** instead.
- Shows: total time, bytes/rows/files read, file pruning, disk spill.
- ~70% of debugging achievable from query profile alone.
- Databricks intentionally simplified this for SQL-first/DA users — query profile mimics the DB world familiar interface.

**Key read:** *Spark: The Definitive Guide* (shared in earlier sessions) — covers jobs/stages/tasks model, DAG, lazy evaluation. Essential for understanding what you're debugging.

**Upcoming exercise:** Sanjeev will share Spark UI screenshots + DAG logs. Interns to analyse and identify bottlenecks (slowness, shuffle overhead, spill, skew).

---

### 3. Neha — Direct Lake Mode

- Microsoft Fabric-only storage mode — not visible in standalone Power BI Desktop.
- Combines **Import** (fast, in-memory) and **Direct Query** (real-time, no scheduled refresh) benefits.
- Data must reside in OneLake (Microsoft Fabric); engine reads Delta files directly without a separate memory load step.
- Neha confirmed: Power BI Desktop only shows Import and Direct Query — Direct Lake requires a Fabric org license/trial.

---

### 4. Neha — Microsoft Fabric Capacity Pricing Model

**Old model problems:** 4 separate services (Synapse, ADLS, ADF, Power BI) = 4 bills, 4 admin portals, 4 security models, data movement costs between services, unpredictable total spend, per-user Power BI licensing on top.

**New Fabric F SKU model:**
- Unified platform: data engineering, data warehouse (SQL), real-time intelligence, data factory, Power BI all in one capacity.
- **F SKU range:** F2 → F2048.
- **F64 inflection point:** at F64+, all Power BI viewers included. Below F64 = $10/user/month surcharge for report viewers.
- F64+ unlocks all premium Power BI features.
- Pricing: pay-as-you-go (per SKU) or annual reservation (~41% discount).
- **Fabric Capacity Estimator** tool: input workload specs → recommends SKU with utilization estimate.
- Key finding from estimator: F128 scenario showed **43% unused capacity** — inherent weakness of capacity-based pricing.

**Sanjeev — pricing model comparison (important for customer conversations):**
- **Capacity-based (Fabric):** reserve upfront for a year, pay regardless of actual usage.
- **Compute-based (Databricks, Snowflake):** pay only for what you run; idle = $0. No reserved machines. Clusters scale 1→N, auto-shutdown when idle.
- The 43% unused Fabric capacity is a real commercial attack angle when talking to customers with variable workloads.
- Azure Databricks (first-party): pricing handled by Microsoft, slightly different model.

**Competitive landscape:**
- **Hyperscaler-native (cloud-locked):** Fabric (Azure), Redshift/Glue/SageMaker (AWS), BigQuery/Dataproc/Looker (GCP).
- **Cloud-agnostic:** Databricks, Snowflake, dbt — same code/jobs run on any cloud, no re-tooling on migration.
- Fabric is Microsoft's strategic response to Databricks/Snowflake: built on Delta + Spark notebooks, tight Power BI coupling to pull BI users into engineering. Microsoft moving P-tier (license-based) → F-tier (capacity-based).

---

### 5. Suhash — RLS & Column-Level Masking in Production

Suhash explored Row-Level Security (RLS) and Column-Level Masking (CLM) in the Databricks UI and asked: in production, do you define these in UI or via code/CI/CD?

→ **Sanjeev**: UI is for exploration only. In production: use **DABs + Unity Catalog Permissions API**. UC functions (used for CLM/RLS) should be definable in DABs — assign which service principal/user gets what access via the permissions API, not manual UI clicks. **Action:** research the Databricks Permissions API for programmatic RLS/CLM definition via CI/CD.

---

### 6. ARM Templates vs Terraform (Asindu's Q)

Asindu asked: for Azure Databricks, is ARM template sufficient for CI/CD infrastructure provisioning?

→ **Suhash**: ARM is Azure-only. Terraform is vendor-agnostic (AWS, Azure, GCP), more widely adopted across organisations. Learning Terraform transfers across clouds and companies — better investment.

---

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Share Spark UI/DAG screenshots + logs for bottleneck analysis exercise | Sanjeev | Before Session 12 |
| Share Databricks pricing calculator links | Sanjeev | ASAP |
| Schedule 20-min storytelling session for Neha | Sanjeev | Session 12 |
| Research Spark testing framework for unit testing Spark pipelines (not pandas) | Suhash | Next session |
| Research Databricks Permissions API for RLS/CLM setup via DABs/CI/CD | Suhash | Next session |
| Prepare slide deck: MV vs streaming table vs Delta table *(3rd carry-over)* | Suhash | Next session |
| Share existing Power BI reports via Slack + prepare KPI pointers before session | Neha | Before Session 12 |
| Continue DABs multi-account deployment (profiles + tokens, dev → prod simulation) | Asindu | Next session |
| Scale pipeline to large dataset (20–30 GB); practice Spark debugging | Asindu | Next session |
| Start enhanced Faker: complex multi-table dataset as template, boost volume | Filip | Next session |
| Validate multi-bundle DABs isolation (deploy-only timestamp test) + push Terraform/DABs code *(carry-over)* | Deepika | Next session |
| Begin MLOps path: MLflow foundations + experiment tracking *(carry-over)* | Deepika | Next session |
| Add Databricks widget parametrization to notebooks *(carry-over)* | Nikolaos | Next session |

---

## Session 10 — May 30, 2026

**Attendees:** Sanjeev Kumar (mentor), Kousalya, Neha Doda, Suhash Raja, Filip Cedermark, Deepika Elangovan, Asindu Gayangana, Nikolaos Biniaris, Rajkumar Rajagopal *(Raj — joined for check-ins and closing)*
**Absent:** Elliot Eriksson

**Agenda:**

**Part 1 — Weekly sync & admin**

1. Week check-in — what did you work on? Blockers? Wins?
2. Admin — Neha's PR merged ✅ *(Sanjeev merged before session)*
3. Sanjeev — Deepika's MLOps path *(shared and discussed)*
4. ~~Neha — Direct Lake mode + Power BI Fabric Capacity pricing model share-out~~ → *(research done, PPT not ready — carried over)*
5. Deepika — Live Terraform + DABs E2E demo: Databricks workspace on Azure ✅
6. Asindu — End-to-end pipeline demo with DQX plugged into silver layer ✅
7. Nikolaos — Databricks AI/BI dashboards *(pivoted from Tableau — see notes)*

**Part 2 — Technical deep-dives**

8. Suhash — DLT: materialized view vs streaming table vs Delta table *(conceptual; slide deck assigned for next session)*
9. Nikolaos — Metadata-driven DQ framework live walkthrough ✅
10. Filip — dbt progress + data scaling discussion ✅
11. ~~Suhash — Multi-job DABs mono-repo experiment~~ → *(partially covered via Deepika's demo)*

**Pre-session — Deliverables Submitted to Repo (as of May 30)**

| Intern | Deliverable | Location |
|---|---|---|
| **Deepika Elangovan** | CI/CD presentation deck (GitHub Actions overview) | `action/de-devops/CICD using Github Actions.pptx` |
| **Deepika Elangovan** | Full CI/CD demo app — FastAPI Gothenburg Weather app with Dockerfile, Kubernetes manifests, GitHub Actions CI + CD workflows | `action/de-devops/gothenburg_weather/` |
| **Filip Cedermark** | Faker-based synthetic data generator notebook (customer/order/CDC records) | `action/de-devops/filip/Sample Data Generator.ipynb` |
| **Nikolaos Biniaris** | Full medallion pipeline — bronze (CSV + Public Holidays API, overwrite & CDC), silver CDC (CRM + ERP + API), gold (fact_sales, dims, 5 aggregations), orchestration, metadata-driven DQ framework | `action/de-devops/nikolas/` |
| **Neha Doda** | Power BI storage modes presentation | *Merged this session* ✅ |
| **Suhash Raja** | DABs CI/CD workflow | *Pushed to separate branch — not merged to main* |
| **Asindu Gayangana** | *(nothing committed yet — pipeline in Databricks only)* | — |
| **Elliot Eriksson** | *(nothing committed yet)* | — |

**Notes:**

---

### 1. Week Check-in

- **Neha Doda** — Researched Direct Lake mode and Fabric Capacity pricing model (no PPT yet — carrying over). First GitHub experience: cloned repo, raised PR (merged). Built a small end-to-end project: pulled data from multiple sources, cleaned, transformed (tried dbt), created CSV files for Power BI. Has a data model ready. Cannot access Microsoft Fabric (no org ID, trial expired) — using DuckDB as intermediate store instead. Wants KPIs/business questions from Sanjeev to build a proper analytics engineering use case.
  → **Sanjeev**: Good investment in Git. Will define use case KPIs based on Neha's data model (ask Neha to commit data model to repo). Final goal: end-to-end AE demo (transform layer + Power BI visualization presented as if to a business user). DuckDB fine for now; alternative: dump data as Parquet to ADLS and import into Power BI.

- **Suhash Raja** — Researched materialized views vs streaming tables: MV used in aggregation/gold layer, automatically refreshed by Databricks on source changes; streaming tables for incremental load from streaming sources, used in silver, manually controlled. Went through Databricks Learning tutorial on SCD Type 1 & 2 in declarative pipelines — understood end-to-end flow. Q: should we partition in silver layer?
  → **Sanjeev**: Partitioning is not layer-specific — it's use-case driven. Purpose: improve read performance. Pitfalls: over-partitioning (too many small files), under-partitioning (no benefit), wrong partition key choice. No middle ground — either very good or very bad. Also read **liquid clustering** (Databricks' modern replacement for partitioning — more powerful, avoids partition pitfalls). For job clusters: DE specifies config in DABs/job definition; Databricks automatically provisions the cluster — no Docker image management needed. Next task: prepare a proper slide deck on MV vs streaming table vs Delta table + design a mid-complexity DLT use case with SCD 1&2.

- **Deepika Elangovan** — MLOps path shared by Sanjeev (see section 2). Multi-bundle DABs experiment: added a second bundle, both ran on every push. Added a condition to partially fix it. Still running both on deploy+run.
  → **Sanjeev**: The real test is `bundle deploy` only (not deploy+run) — check timestamps in the environment per project to verify only the changed bundle was updated. deploy+run is for UAT/dev integration testing, not production validation. Deepika to push clean code to repo after cleanup.

- **Asindu Gayangana** — Full pipeline demo (screen share): AutoLoader → bronze (partitioned by load\_date) → silver (backfill or incremental read stream, DQX validation, valid → silver, invalid → silver\_invalid, partitioned by order\_date, deduplicated by row\_id) → gold (partition replace). Workflow job with 3 tasks; bronze has retry logic (3x, 10-min delay) and timeout threshold. Parameter widgets control backfill vs stream mode — no hardcoding. DQX installed and functioning.
  → **Sanjeev**: Research `inferSchema` in production (important interview topic). Key feedback: think metadata-driven ingestion — instead of creating a new pipeline per source (e.g. campaign data), parameterize so a new source is onboarded by adding a config entry only, zero code changes. Sanjeev showed his own YAML-based metadata config (source path, target table, schema hints, DQ rules, derived columns) + for-loop in pipeline code that auto-creates DAG flows per config entry. CICD exists but needs more work — sync with Suhash and Deepika. Scale up: target 20–30 GB using Filip's Faker library.

- **Nikolaos Biniaris** — Decided against Tableau manual CSV export (wanted fully connected pipeline). Built Databricks AI/BI dashboards instead on gold business metrics. Dashboards cover: holiday vs non-holiday revenue, CLV by cohort, churn risk + RFM segmentation, product performance, time-based revenue trends (MoM, day-of-week patterns). All powered by pre-built gold metric tables — SQL queries are simple. Used AI assistant (Genie) to generate dashboard ideas and metric suggestions. Walked through metadata-driven DQ framework (see section 4).
  → **Sanjeev**: Great work. AI usage is expected — showcasing it in interviews is a positive signal. Always show you are managing the AI (reviewing output, not on autopilot). Tableau community ↔ Databricks free don't support direct connection — Raj offered to potentially purchase Tableau/Power BI licenses for a couple of months. Neha to check Power BI on Mac route for Nikolaos. Next step: add Databricks widget parameters to notebooks for full parametrization (like Asindu did).

- **Filip Cedermark** — Progress on dbt-core. Ready to scale. Dilemma: use own Faker generator (simple, 1 table, few columns, but infinitely scalable) vs Databricks sample dataset (1.5 GB, 10 tables, more complexity, but fixed size).
  → **Sanjeev**: Do both — enhance Faker generator: add ~10–12 columns + 1 complex nested column (struct/array) using Claude. Push updates so others can use it. Then scale to large volumes. Scale is non-negotiable before internship ends — Spark problems (shuffle, spill, skew) only surface at scale. 30% of production data has arrays/nested structures requiring explode/parse — good to cover. dbt-core is used in production; dbt Cloud adds packaging conveniences but not required for internship purposes.

---

### 2. Deepika's MLOps Path

Sanjeev shared a structured MLOps course plan covering:

1. **Foundations** — ML basics recap, MLOps vs DevOps distinctions
2. **Experiment tracking** — MLflow (open source, Databricks managed) and SageMaker (AWS). Other frameworks to explore: Vertex AI (Google), Snowflake Cortex
3. **Data & feature engineering** — Feature pipelines, feature stores, working with data scientists' outputs
4. **Model packaging & serving** — Model registry, deployment endpoints
5. **CI/CD for ML** — Applying CICD to model lifecycle (train → validate → register → serve)
6. **Orchestration of ML pipelines** — Scheduling, dependencies
7. **Model monitoring & observability** — Drift detection, performance tracking in production
8. **Capstone project** — Tying all stages end-to-end

Note: concept stays the same across frameworks; specific API names differ. Deepika to choose a framework (MLflow recommended as starting point given Databricks context).

---

### 3. Metadata-Driven Ingestion — Deep Dive (Sanjeev screen share)

Triggered by Asindu's pipeline demo and Suhash's follow-up question:

**Core principle:** A production-grade pipeline can onboard a new source without any code changes. Everything variable is externalized to a metadata config.

**Config structure (YAML/JSON file or config table):**
- Source path / type / format
- Target catalog, schema, table name
- Schema hints for key columns
- DQ expectations (e.g. `claim_id: not_null`)
- Derived/transformation column definitions

**Pipeline code:**
- Reads config at startup → loads all source definitions into memory
- Uses placeholders (variables) — no hardcoded table names, paths, or rules
- A for-loop iterates over config entries, creates a task/flow for each source automatically

**Config lifecycle (best practice):**
1. Developer writes new source config as YAML/JSON
2. CI/CD runs test cases against it (e.g. ping source, validate schema)
3. On pass → config upserted into config table in the warehouse
4. Pipeline reads config table at runtime

**Boundary:** Gold layer modeling is intentionally excluded — it requires business-specific logic that can't be fully genericized. Metadata-driven applies primarily to bronze → silver ingestion.

**Sanjeev's message:** *"A pipeline is only production-grade when it can onboard a new source without writing code."*

---

### 4. Nikolaos — Metadata-Driven DQ Framework Walkthrough

- DQ rules stored as column-level comments in Unity Catalog (e.g. `ALTER TABLE gold_fact_sales CHANGE COLUMN amount COMMENT 'DQ: non-negative'`)
- `spark.catalog.listColumns()` scans all column comments at runtime
- Utility function parses any comment containing `DQ:` → translates to enforcement rule (not_null, non-negative, date type, etc.)
- Output: `is_invalid` flag column per row → invalid rows → quarantine table with error description; clean rows pass through
- Adding DQ to a new table = add a comment. Zero code changes.

Connects back to metadata-driven theme: same principle as Sanjeev's ingestion config — rules live outside code.

**Sanjeev**: This is the right pattern. Start simple (bronze/silver parameterization for DE; DQ comment-driven checks for analytics engineering). Next step: add Databricks widget parameters for runtime control.

---

### 5. Unit Testing vs Integration Testing (CICD best practices)

Raised by Suhash during the metadata-driven discussion:

- **Unit tests**: each developer tests their own logic locally before pushing. Examples: ping config server, validate input/output with sample data, schema assertions.
- **Integration tests**: full pipeline tested in UAT/staging environment post-deployment. Tests how all components (bronze + silver + gold, from multiple developers) work together end-to-end.
- **deploy+run** in CI pipeline = integration test trigger in UAT/dev. Not used in production.
- **Production**: deploy only; jobs are scheduled via Databricks scheduler.

---

### 6. Deepika — Terraform + DABs E2E Live Demo

Two-repo architecture:
- **Platform repo** (Terraform): provisions all Azure infrastructure → exports workspace name, catalog name, secrets to Azure Key Vault
- **Data pipelines repo** (DABs): reads secrets from Key Vault → sets up Databricks workspace, schemas, jobs, bundles. Zero hardcoded values.

**Platform pipeline flow (GitHub Actions):** lint + security scan → Terraform init → Terraform plan → Terraform apply → export outputs to Key Vault

**Resources created by Terraform (5 modules):**
- Networking: VNet, subnets, NSG
- Workspace: Databricks workspace (SKU, network binding)
- Unity Catalog: metastore, bronze/silver/gold schemas
- Security: Key Vault, service principal (scoped: owner/contributor/reader)
- Compute: cluster (right VM SKU found for Sweden Central after many trials)

**DABs pipeline (data pipelines repo):** Two bundles — Customer ETL and Finance ETL. Condition added to prevent both running on every push. Challenge: deploy+run fires both; Sanjeev clarified real test is deploy-only with timestamp checks per project folder.

**Sanjeev's Q on `output.tf`:** outputs (e.g. bronze schema name) printed at end of Terraform apply run — comes from `outputs.tf` file in Terraform folder structure.

Deepika to push cleaned code to repo so others can reference it as a CI/CD + IaC template.

---

### 7. DLT vs Plain Spark — Context for All Interns

Sanjeev's framing when Suhash discussed DLT:
- **DLT (Declarative Pipelines)**: managed by Databricks — logging, observability, retries handled automatically. Developer focuses on logic only.
- **Plain Spark** (PySpark / Spark SQL / Scala): full control, more boilerplate, more flexibility.
- **Every platform has an equivalent**: Snowflake → Dynamic Tables; Azure Fabric → FDF (Fabric Data Factory); AWS → Glue ETL.
- Customers who want simplicity → declarative; those needing fine-grained control → plain Spark.
- Neither is universally better — choosing the right one is part of the engineer's job.

---

### 8. Closing — Raj's Remarks

- Progress and engagement across the group was strong despite fully remote setup.
- Recommendation: use midweek syncs more actively — resolve blockers between yourselves before bringing to Sanjeev; use the call to come to a consensus on what questions to escalate.
- Raj offered to explore purchasing Tableau / Power BI licenses for a couple of months.
- Sanjeev: all interns to drop desired software list in internship Slack channel (Power BI, Tableau, dbt Cloud if needed) — will evaluate budget with Raj.

---

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Prepare Direct Lake mode + Fabric Capacity pricing model PPT | Neha | Next session |
| Commit data model + dataset to repo for Sanjeev to derive KPIs | Neha | This week |
| Define analytics engineering use case KPIs for Neha | Sanjeev | This week |
| Explore Power BI on Mac option for Nikolaos | Neha | This week |
| Prepare slide deck: MV vs streaming table vs Delta table (pros/cons, use cases) | Suhash | Next session |
| Design mid-complexity DLT use case with SCD type 1 & 2 + justification for DLT over plain Spark | Suhash | Next session |
| Research liquid clustering in Databricks | Suhash | Next session |
| Validate multi-bundle DABs isolation: deploy-only test (check timestamps per project) | Deepika | Next session |
| Push clean Terraform + DABs code to repo (platform + data pipeline repos) | Deepika | Next session |
| Begin MLOps path (MLflow foundations + experiment tracking) | Deepika | Next session |
| Focus on metadata-driven ingestion: onboard new source via config only, no code changes | Asindu | Next session |
| Research `inferSchema` in production (pros/cons, when to use) | Asindu | Next session |
| Scale pipeline to 20–30 GB using Filip's Faker library | Asindu | Next session |
| Sync with Suhash + Deepika on CI/CD; push CI/CD code to repo | Asindu | Next session |
| Enhance Faker generator: expand to ~12 columns + add 1 complex nested struct/array column | Filip | Next session |
| Scale dbt pipeline to large dataset using enhanced Faker data | Filip | Next session |
| Add Databricks widget parameters to notebooks for full runtime parametrization | Nikolaos | Next session |
| Drop desired software licenses list in internship Slack channel | All interns | ASAP |
| Discuss Tableau / Power BI license purchase with Raj | Sanjeev | This week |

---

## Session 9 — May 23, 2026

**Attendees:** Sanjeev Kumar (mentor), Kousalya, Filip Cedermark, Neha Doda, Suhash Raja, Deepika Elangovan, Nikolaos Biniaris
**Absent:** Asindu Gayangana, Elliot Eriksson

**Agenda:**

**Part 1 — Weekly sync**

1. Week check-in — what did you work on? Blockers? Wins?
2. Neha — Power BI storage modes presentation: import vs direct query vs composite *(assigned Session 8)*
3. ~~Deepika — Live Terraform run: E2E Databricks workspace + Unity Catalog on Azure~~ → *(deferred — ran out of time; next session)*
4. ~~Asindu — End-to-end pipeline demo with DQX plugged into silver layer~~ → *(carried over — Asindu absent)*
5. ~~Nikolaos — Metadata-driven DQ framework live walkthrough~~ → *(carried over — not covered this session)*

**Part 2 — Technical deep-dives & presentations**

6. ~~Filip — dbt progress: incremental ingestion, SCD type 1 & 2, artifacts in Databricks~~ → *(carried over — still resolving setup errors)*
7. Suhash — DABs CI/CD deep-dive: mono-repo vs multi-repo, `databricks.yml` atomicity, deploy-run patterns *(organically covered)*
8. Nikolaos — Analytics engineering: gold layer business metrics in Spark SQL *(covered in check-in)*
9. ~~Sanjeev — Deepika's MLOps path~~ → *(carried over — Sanjeev to define by next session)*
10. ~~Sanjeev — Spark Definitive Guide: specific chapters for DE interns~~ → *(carried over)*
11. ~~Elliot — MLflow deep-dive: model logging, feature stores, serving endpoint~~ → *(carried over — Elliot absent)*

**Notes:**

---

### 1. Week Check-in

- **Filip Cedermark** — Slow week due to errors encountered when starting actual dbt usage on the internship project. Current blocker: dbt not recognizing the project file, preventing SQL models from running. Nothing concrete to show yet.
  → **Sanjeev**: Take time to fix the issue. Path confirmed: basic project → incremental ingestion → SCD type 1 & 2 → eventually collaborate with Suhash on dbt vs SDP comparison.

- **Neha Doda** — Prepared and delivered the Power BI storage modes presentation (see section 2). Also exploring Microsoft Fabric — learning Delta tables and the Lakehouse vs Warehouse distinction in Fabric using DP600 content (Aleksy's YouTube series).
  → **Sanjeev**: Fabric is a valid platform, used by many customers. Core analytical engineering concepts matter more than platform choice. dbt is the leading tool in this space — will cover once foundations are solid. Sanjeev to prepare a step-by-step analytics engineering path for Neha. Also: recommended Neha scroll through Sessions 1–3 notes in the repo to catch up on foundational concepts (structured/semi-structured data, file formats, Lakehouse) that were covered in common early sessions.
  → **New tasks**: research **Direct Lake mode** (4th Power BI mode, Fabric-specific) and the **Power BI Fabric Capacity pricing model** (replaced old A1/P1/P2 license model). Come prepared to discuss next session.

- **Suhash Raja** — Limited DE progress this week but pushed CI/CD workflow using DABs for deployment to a separate branch in the repo. Raised questions about production DABs patterns — addressed in section 3.
  → **Sanjeev**: Still pending: streaming tables vs materialized views vs Delta tables (pros/cons, use cases), SCD type 1 & 2 in DLT.

- **Deepika Elangovan** — Successfully completed end-to-end Terraform + DABs implementation: created Azure resources via Terraform (5 modules), then ran a medallion architecture ETL pipeline (bronze → silver → gold) on a sample CSV file via YAML config and GitHub Actions. Used Claude for code generation throughout.
  → **Sanjeev**: Excellent progress. Keep using Claude but always understand what it generates — it sometimes uses outdated provider versions. Always direct it explicitly (e.g. "use the latest version of this Terraform provider"). Plan to show a live run next session.
  → Also: Deepika is stepping into the **MLOps path** (confirmed). She hasn't spoken to Raj yet. Sanjeev to define MLOps plan by next week.

- **Nikolaos Biniaris** — Fixed pipeline issues and moved to the gold layer. Created a set of business metrics using Spark SQL on top of `fact_sales` (enriched with holiday API data) and dimension tables (products, customers). Metrics include: holiday sales performance, CLV (customer lifetime value), product performance, time-based trends, and operational KPIs.
  → **Sanjeev**: This is exactly the analytics engineering pattern — Neha should align with Nikolaos on this approach. For dashboarding: Databricks free edition and Tableau community edition don't support direct connection. Nikolaos's plan: export gold layer tables to CSV and manually import into Tableau.

---

### 2. Neha — Power BI Storage Modes Presentation

Neha presented a comparison of the three Power BI storage modes:

**Import Mode**
- Data is copied into Power BI's in-memory model
- Fastest query performance; no live connection needed; full DAX support (including time intelligence)
- Limitations: Pro license capped at 1 GB; data is not real-time; requires scheduled refresh

**Direct Query Mode**
- Every visual fires a live query directly to the source database
- Always up-to-date; no size limit (data stays in source); good for real-time dashboards
- Limitations: slower performance (round-trip to database per query); limited DAX support (time intelligence functions not available); source database must always be online; high load when many users query simultaneously

**Composite / Dual Mode**
- Combines both: some tables in import, others in direct query
- Recommended pattern: **fact tables → direct query** (frequently changing transactional data); **dimension tables → import** (rarely changing; benefit from refresh scheduling)
- Balances cost, performance, and freshness

**Comparison summary (Neha's table):** data storage location, speed, latency, memory usage, dataset size suitability, real-time capability, concurrent user handling, DAX support.

---

### 3. Post-Presentation Discussion — Direct Query Optimization & Caching

Sanjeev extended the storage modes discussion with production-level context:

**Optimizing direct query at Lakehouse scale:**
- When Power BI connects to a Lakehouse (Databricks, Snowflake, Fabric) in direct query mode, the fired SQL query needs to scan potentially terabytes of data.
- **Data layout optimization** is the engineer's responsibility:
  - **Partitioning** (Suhash explained): organize data in folders by a common filter column (e.g. date, country). A query for "last month" skips all other partitions — no full scan.
  - **Clustering / Liquid clustering**: like database indexing, co-locates related rows physically on disk. Speeds up point lookups and range scans.
- **Database-level caching** (production pattern):
  - Schedule the exact set of queries a critical dashboard fires (e.g. CEO dashboard) to run at 6 AM as a scheduled job on the warehouse.
  - Results are loaded into the database's disk cache. When users log in at 8 AM and click the dashboard, the query is already cached → near-instant response even in direct query mode.
  - Cache is invalidated as soon as the underlying table is updated → direct query fires again → re-cached. No stale data is ever returned.

**Nikolaos's question — why not use import with a trigger instead?**
- Import + trigger works well when data changes infrequently (e.g. daily batch).
- For streaming tables (data arriving every second/millisecond), continuous import re-runs would explode Power BI storage and cost.
- Direct query is more practical at scale and increasingly unavoidable given Power BI's Fabric Capacity pricing — customers often trade performance for cost savings by leaning on direct query.

**Mono-repo vs multi-repo — raised as conceptually parallel**: both import/direct query and mono/multi-repo are "flavors" — neither is universally correct; the right choice depends on scale, team structure, and cost constraints.

---

### 4. Suhash — DABs CI/CD Patterns (Screen Share)

Suhash shared his DABs deployment setup: single declarative pipeline job, workflow action with three steps: validate bundle → deploy bundle → run bundle job. Sparked a detailed production discussion:

**Mono-repo vs multi-repo:**
- **Mono-repo**: one root git repo with multiple project folders (`my_first_job/`, `my_second_job/`, etc.). All code in one place — easy to manage and navigate.
  - Risk: a code change in one folder accidentally triggers redeployment of all other jobs — a hard no in production.
- **Non-monorepo**: each project is its own separate git repo. No cross-contamination, but managing hundreds of repos becomes a nightmare.
- **Both patterns are used in production**; depends on team preference. Know the pros and cons of each.

**`databricks.yml` as the unit of modularity (key takeaway):**
- When `databricks.yml` lives **inside a project folder**, that folder becomes an atomic deployment unit. `databricks bundle deploy` on that folder only deploys that project — other folders are unaffected.
- When `databricks.yml` is at the **root level**, the entire repo is treated as one unit — any change deploys everything. This is the wrong pattern for multi-project mono-repos.
- Deepika: confirmed same architecture from her implementation; wants to experiment with a two-job setup to validate isolation.

**Deploy + run:**
- `deploy` + `run` together is a dev/QA pattern only — deploy and immediately trigger the job for integration testing.
- In production: deploy only; jobs are scheduled via Databricks job scheduler, not triggered by the deployment pipeline.

**DABs YAML auto-completion in VS Code:**
- Suhash asked about getting proper Databricks DABs YAML key auto-completion (Red Hat YAML extension was not recognizing Databricks-specific keys).
- Suggestion: install the **Databricks VS Code extension** — it understands `databricks.yml` schema and should provide context-aware completions.
- Deepika: also recommended **YAML Lint** as a fallback for syntax validation and indentation fixing.

---

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Research Direct Lake mode (Power BI / Fabric) and Fabric Capacity pricing model; compare with old license model | Neha | Next session |
| Push Power BI storage modes presentation to `action/` folder in GitHub | Neha | This week |
| Define analytics engineering step-by-step path for Neha | Sanjeev | Next session |
| Define Deepika's MLOps path | Sanjeev | Next session |
| Continue resolving dbt project file error; progress on incremental ingestion | Filip | Next session |
| Experiment with multi-job DABs mono-repo setup (two separate folders, each with own `databricks.yml`) | Suhash & Deepika | Next session |
| Read: streaming table vs materialized view vs Delta table (pros/cons, use cases); SCD type 1 & 2 in DLT | Suhash | Next session |
| Install Databricks VS Code extension for YAML auto-completion | Suhash | This week |
| Live Terraform + DABs E2E demo | Deepika | Next session |
| DQX pipeline demo (end-to-end with DQX in silver) | Asindu | Next session |
| Connect Tableau to gold layer (manual CSV export if needed); continue analytics engineering models | Nikolaos | Next session |

---

## Session 8 — May 16, 2026

**Attendees:** Sanjeev Kumar (mentor), Kousalya, Filip Cedermark, Neha Doda, Suhash Raja, Deepika Elangovan, Asindu Gayangana, Nikolaos Biniaris
**Absent:** Elliot Eriksson

**Agenda:**

**Part 1 — Weekly sync**

1. Week check-in — what did you work on? Blockers? Wins?
2. Deepika — E2E Databricks + Unity Catalog infra deployment demo (Terraform + GitHub Actions) *(committed for this session)*
3. ~~Filip — dbt silver layer demo: quarantine/dead-letter table with reason tags~~ → *(carried over — just started dbt yesterday)*
4. ~~Nikolaos — metadata-driven DQ framework walkthrough~~ → *(partially discussed; live demo deferred to next session)*
5. ~~Asindu — DQX data quality implementation in silver layer walkthrough~~ → *(practiced but not in pipeline yet — carried over)*
6. ~~Sanjeev — Deepika's MLOps path~~ → *(not covered — carried over)*
7. ~~Sanjeev — Spark Definitive Guide: specific chapters for DE interns to focus on~~ → *(not covered — carried over)*

**Part 2 — Technical deep-dives**

8. ~~Elliot — MLflow deep-dive: model logging, feature stores, serving endpoint~~ → *(carried over — Elliot absent)*

**Notes:**

---

### 1. Week Check-in

- **Filip Cedermark** — Spent the last two weeks learning dbt-core: reading material, setting up, connecting to Databricks environment. Started actual implementation yesterday. Using the Faker CDC generator he built previously as the data source — will now run all transformations through dbt instead of PySpark notebooks. Using the Databricks connector, so dbt runs on top of Databricks compute and creates materialized objects in the background.
  → **Sanjeev**: Confirmed dbt-core + Databricks connector means Databricks compute handles execution. Focus next on core dbt engineering concepts: incremental ingestion, data cleaning patterns, SCD type 1 & 2. Understand what artifacts dbt creates in Databricks (materialized views, tables, etc.) — as an engineer you're expected to know what the tool is doing underneath.

- **Neha Doda** — Covered all areas from the Power BI report doc: implemented static and dynamic RLS, time intelligence functions, drill-through, and page navigation. Ready to move to Tableau.
  → **Sanjeev**: Instead of presenting the dashboard next session, prepare a short presentation on Power BI connection/import modes — import, direct query, and composite — covering when to use each based on data size, latency requirements, and cost. Also research the old license-based pricing vs the new Fabric Capacity model; create a comparison including what Direct Lake is and why it matters. These are hot interview topics for analytics roles.

- **Suhash Raja** — Created a Databricks Workflow job and a declarative DLT pipeline for a single batch CSV load. Understands the difference between Workflow jobs and declarative pipelines (delta live tables). Deployed using Databricks Asset Bundles (DABs). Deployed to Databricks platform via GitHub Actions CI/CD. Using retail data from Databricks Marketplace; sticking with DBFS storage to avoid cloud costs.
  → **Sanjeev**: Collaborate with Deepika this week — she has strong DABs experience and has built a sample. Also connect with Filip on using his Faker library to generate 5–10 GB of data for high-volume pipeline testing. Go deeper into declarative pipelines: implement SCD type 1, SCD type 2, auto CDC; understand append flows, change flows, restart, backfill, and full refresh patterns. Read up on UC managed tables vs UC external tables, and the difference between streaming tables, materialized views, and Delta tables (pro/cons, which layer each belongs to). Build a full end-to-end pipeline covering ingestion → transformation → data quality in DLT.

- **Deepika Elangovan** — Started implementing Databricks infrastructure via Terraform but hit many errors. Azure portal access issues (Gmail vs Microsoft account conflict). Free trial expired — now on pay-as-you-go (spent ~57 SEK this week). Screen-shared architecture and slide deck covering: 5 Terraform modules (Compute, Networking, Security, Unity Catalog, Workspace), remote backend for state files (versioning + prevent state corruption), GitHub Actions CI/CD flow. Walked through Terraform commands (init, plan, apply, destroy). Issue: compute resource creation failing in Sweden Central region.
  → **Sanjeev**: Recommend Sweden Central first; West Europe is fine if unavailable. Great use of Claude for code generation — ensure you understand what every resource does, as interviews will test that. Nice to see architecture diagrams alongside the code. Plan to show a live run next session once issues are resolved.

- **Asindu Gayangana** — Limited progress this week. Focused on understanding CI/CD for Databricks but not yet confident. Tried both CLI and UI approaches. Plans to use two separate free-edition accounts (one for CI, one for CD). Has practiced DQX in a notebook but has not plugged it into the pipeline yet. Also created a manual architecture diagram using Roto.io.
  → **Sanjeev**: Next session — show full end-to-end pipeline demo with DQX plugged into the silver layer. Keep working on the CI/CD approach.

- **Nikolaos Biniaris** — Converted entire pipeline (bronze → gold) from `spark.read` to streaming with `trigger(availableNow=True)`. Made data quality checks metadata-driven using Databricks column-level comments: a comment like `DQ: not_null` on a column is picked up by a utility function that translates it into an actual DQ rule at runtime. Null/failed records are routed to a quarantine table; clean records pass downstream.
  → **Sanjeev**: Approach is close — the utility function that translates comment tags into SQL rules is the right idea, but wants to see it live next session to validate completeness. Also: Sanjeev had a chat with Raj — recommendation is for Nikolaos to spend ~50% of time on his existing strength (data analysis / visualization) and 50% on DE work. He has Tableau + Streamlit experience (no Power BI due to Mac). Next step: use Spark SQL to build gold layer data models (star schema) to serve dashboards. Also collaborate with Neha on visualization practices (RLS, time intelligence, KPIs, access control).

---

### 2. Analytics Engineering — Role Deep Dive

Discussion triggered by Neha's pivot toward Analytics Engineering and Suhash's question on the role:

- **Data Analyst**: receives clean data, builds reports and visualizations. Focus on KPIs, dashboards, front-end consumption.
- **Data Engineer**: handles high-volume ingestion and cleaning, agnostic to specific business domain. Serves downstream analysts and ML teams.
- **Analytics Engineer** (sits between the two): takes silver layer data, creates the final aggregated/gold layer for reporting, designs and schedules those pipelines, owns the semantic/data model. Uses tools like dbt for SQL-based transformations. Responsible for the reporting backend — the gold layer is the foundation of the BI tool.
  - Key point: the semantic layer in Power BI (measures, relationships) is typically the analytics engineer's domain.
  - dbt became popular precisely because it gave analysts a SQL-based, engineer-grade interface to own this layer independently.

Sanjeev's framing: visualization is the front end; analytics engineering is the back end of the DA role.

---

### 3. Deepika — Terraform + GitHub Actions Architecture (Screen Share)

Key highlights from the walkthrough:

- **5 Terraform modules**: Networking (VNet, subnets), Workspace (Databricks workspace), Unity Catalog, Security (service principals, role assignments), Compute (clusters)
- **Remote backend**: stores Terraform state in Azure Blob → enables versioning, prevents state file corruption when multiple people run pipelines simultaneously, supports rollback to previous state
- **State file comparison**: on `terraform plan`, Terraform compares the desired config against the current state file — shows what will be created, updated, or destroyed
- **Terraform Destroy**: deletes all resources in the managed resource group — no orphan resources as long as everything is within the same resource group
- **Standard commands**: `init` (initialize providers), `plan` (dry-run diff), `apply` (deploy), `destroy` (tear down)
- **Folder structure**: `main.tf` (what to build), `variables.tf` (parameterization — no hardcoding), `outputs.tf` (post-run output values, used by downstream pipeline runs), `provider.tf` (target cloud platform)
- **Architecture flow**: code pushed to GitHub → GitHub Actions retrieves secrets → Terraform pipeline runs → resources created in Azure resource group
- **Current blocker**: compute resource creation failing in Sweden Central; evaluating West Europe as fallback

**Sanjeev's note for all interns**: data engineers don't need to be Terraform experts, but should understand what resource groups, VNets, and IaC workflows are — it comes up in interviews and you'll interact with platform teams on these topics.

---

### 4. Specialization Strategy & Session Feedback

Sanjeev asked the group for feedback on the mixed-stream session format:

- **Suhash**: Weekly calls are valuable — hearing different personas' perspectives is useful. Wants more cross-team collaboration (e.g., Filip ↔ Suhash for dbt vs SDP comparison).
- **Deepika**: Finds it interesting — DE and CI/CD are entirely new for her; the breadth is a good foundation.
- **Neha**: Sometimes feels disconnected from deep DE topics, but passive listening still yields value. Acknowledged that CI/CD will eventually be relevant as her analytics engineering path matures.
- **Sanjeev's rationale**: As roles grow toward architect-level, broad awareness matters. Selfish reason for DE interns to hear BI content: as a data engineer you'll be asked about Power BI import modes — your consumers are analysts, so you need to understand their constraints. 200-level knowledge of adjacent domains is the goal.

**Specialization positioning (updated):**
- **Neha**: Analytics Engineering path — Power BI → analytics engineering (dbt / gold layer ownership)
- **Nikolaos**: Same path — Tableau/Streamlit → analytics engineering via Spark SQL gold layer models; continue streaming/DQ work in parallel
- **Filip & Suhash**: Future collaboration task — produce a structured dbt vs SDP comparison (Databricks pushes SDP when customers are unhappy with dbt, and vice versa; knowing both is a differentiator)

---

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Prepare Power BI presentation: import vs direct query vs composite mode (size, latency, cost tradeoffs) | Neha | Next session |
| Research Power BI pricing: license-based vs Fabric Capacity model + Direct Lake; create comparison | Neha | Next session / following |
| Start Tableau exploration | Neha | Ongoing |
| Collaborate with Deepika on DABs | Suhash | This week |
| Connect with Filip to get Faker library; generate 5–10 GB test data | Suhash | This week |
| Implement SCD type 1 & 2, auto CDC in declarative DLT pipelines | Suhash | Next session |
| Understand append flows, change flows, restart, backfill, full refresh in DLT | Suhash | Next session |
| Read: UC managed table vs UC external table; streaming table vs materialized view vs Delta table (pros/cons, use cases) | Suhash | Next session |
| Build full DLT pipeline: ingestion → transformation → data quality | Suhash | Next session |
| Continue dbt implementation; focus on incremental ingestion, SCD type 1 & 2, data cleaning | Filip | Next session |
| Research what artifacts dbt creates in Databricks | Filip | Next session |
| Collaborate with Suhash on DABs experience | Filip | This week |
| Resolve Azure compute issues (Sweden Central → West Europe); demo live Terraform run | Deepika | Next session |
| Plug DQX into pipeline; demo full end-to-end pipeline with DQX in silver layer | Asindu | Next session |
| Implement Databricks CI/CD (two free-account approach) | Asindu | Next session |
| Demo metadata-driven DQ framework (column-comment approach) live | Nikolaos | Next session |
| Start analytics engineering: build gold layer data models (star schema) in Spark SQL | Nikolaos | Next session |
| Collaborate with Neha on visualization practices (RLS, time intelligence, KPIs) | Nikolaos | Next session |

---

## Session 7 — May 9, 2026

**Attendees:** Sanjeev Kumar (mentor), Kousalya, Deepika Elangovan, Neha Doda, Suhash Raja, Asindu Gayangana
**Absent:** Filip Cedermark *(texted unable to join)*, Elliot Eriksson, Nikolaos Biniaris

**Agenda:**

**Part 1 — Weekly sync**

1. Week check-in — what did you work on? Blockers? Wins?
2. Session stream split — confirm DE+DevOps / ML / DA structure and logistics *(carried over)*
3. ~~Filip — dbt silver layer demo: quarantine/dead-letter table with reason tags~~ *(Filip absent — carried over)*
4. Deepika — CI/CD artifact separation: Bundles vs Terraform for catalog, schema & checkpoints *(pros/cons)*
5. ~~Nikolaos — metadata-driven DQ framework walkthrough~~ *(Nikolaos absent — carried over)*

**Part 2 — Technical deep-dives**

6. ~~Elliot — MLflow deep-dive: model logging, feature stores, serving endpoint~~ *(Elliot absent — carried over)*
7. Spark streaming optimization — rate limiting, `maxBytesPerTrigger`, `maxFilesPerTrigger`, partition pruning *(Asindu's `maxBytesPerPartition` issue + broader context)*
8. Spark Definitive Guide walkthrough — group reading/discussion session
   - Reference: [Spark: The Definitive Guide](https://analyticsdata24.wordpress.com/wp-content/uploads/2020/02/spark-the-definitive-guide40www.bigdatabugs.com_.pdf)

**Notes:**

---

### 1. Week Check-in

- **Neha Doda** — Started dbt basics: installation, setup, intro videos, CLI commands. Connected dbt to Microsoft SQL Server locally. Also assigned by Raj to write website content on data platform modernization (separate from internship tasks).
  → **Sanjeev**: Stay on DA track. Primary focus: Power BI (3+ years experience, PL-300 certified) — practice deeply (DAX, time intelligence, KPIs, access control, Power BI Service). dbt is the right tool for SQL-based transformations alongside BI. Also explore **Tableau** and **Looker Studio** — concepts are generic across tools. Raj has upcoming opportunities for dashboarding resources.
- **Deepika Elangovan** — Researched Databricks Asset Bundles (also referred to as Databricks Automation Bundles) + Terraform. Key findings: Terraform handles infrastructure (catalog, storage, permissions); DABs handle pipeline/job deployment via `databricks.yml`. Hitting errors with free edition; iterating with Claude for troubleshooting. Got accepted to **Chalmers Master's in Biomedical Engineering** (starts September) — wants to include ML/MLOps given it's part of her program. Wants to be included in MLOps track.
- **Suhash Raja** — No update (sick all week, now recovering). Revealed he already has **Databricks Associate Data Engineer certification** (taken Feb 2026, studied from Spark Definitive Guide + Raj's PySpark book). Plans to go full throttle on DE tasks this week.
- **Asindu Gayangana** — Updated PySpark pipeline: optimized for both daily incremental runs and backfill using same pipeline. Completed gold layer tables. Currently researching **Databricks DQX** for YAML-based data quality expectations in silver layer.

---

### 2. Stream Specialization — Paths Confirmed

Sanjeev recapped and confirmed specialization paths for each intern:

| Intern | Track | Focus |
|---|---|---|
| **Neha** | DA | Power BI (primary), dbt for transformations, Tableau / Looker Studio |
| **Deepika** | DevOps → MLOps | E2E Databricks infra (Terraform + DABs + Azure); MLOps path TBD |
| **Suhash** | DE (Databricks specialist) | SCD, CDC, incremental ingestion, Unity Catalog, DLT, Lakeflow, DABs; target DE Pro |
| **Asindu** | DE (Databricks + Spark) | DQX, Unity Catalog, AutoLoader, declarative pipelines, Lakeflow; read Spark Definitive Guide |
| **Nikolaos** | DA | Same dashboarding advice as Neha (confirmed by Sanjeev) |
| **Filip** | DE + dbt | dbt silver layer + quarantine table *(absent)* |
| **Elliot** | ML / Snowflake | MLflow, Snowflake Cortex *(absent)* |

**Key point from Sanjeev**: Strong data engineering fundamentals matter more than platform choice — any company will take you if your fundamentals are solid (Spark, CDC, SCD, medallion architecture). Databricks is a strong choice given market growth, but don't limit yourself.

---

### 3. Databricks Asset Bundles (DABs) — Technical Discussion

- DABs = implementation on top of Terraform, managed via `databricks.yml` YAML file
- **State management advantage over plain Terraform**: in a mono-repo with 10 projects, Terraform rebuilds the whole state on any change. DABs treat each sub-project atomically — one project's deployment doesn't affect others.
- DABs renamed to **Databricks Automation Bundles** in recent docs (some older docs still say Asset Bundles)
- Known limitation: inherited Terraform state issues still surface; Databricks actively working on engine changes
- **Deepika's new capstone task**: End-to-end Databricks workspace + Unity Catalog deployment on Azure using Terraform + GitHub Actions. Must include: security (VNet isolation, hub-and-spoke model), proper separation of infra vs pipeline deployments.
- Deepika confirmed she maintained separate infra and code pipelines in previous experience — relevant here.

---

### 4. Spark Streaming Rate Limiting

Deep-dive with Asindu and Suhash:

- **`maxFilesPerTrigger`**: limits files per micro-batch. E.g., 100 new files + `maxFilesPerTrigger=10` → 10 sequential batches of 10 files each
- Within each batch, Spark distributes files across workers in parallel (e.g., 4 workers → ~2.5 files each)
- Batches are **sequential**, processing within each batch is **parallel**
- Rationale: prevents overwhelming compute with massive data volumes in a single micro-batch; matches processing capacity to cluster size
- Asindu confirmed understanding of `maxFilesPerTrigger`; watermarking noted as advanced topic — not required now
- **Partition pruning**: Suhash familiar; `maxBytesPerTrigger` to be read up on

---

### 5. Spark Definitive Guide

- Sanjeev emphasized this book as essential for all DE interns — common interview questions come from it
- Suhash confirmed he has already read it (used it to prep for Databricks Associate certification)
- Suhash shared PDF in Slack; index accessible via Adobe bookmarks panel
- Sanjeev to define specific chapters for Asindu to focus on (too many chapters to read all)

---

### 6. Architecture Diagrams

Sanjeev: all interns should capture their pipeline designs as architecture diagrams.
- Interviewers frequently ask candidates to draw an end-to-end architecture on the spot
- As a DE, you will transition towards solution architecture thinking — knowing which tool fits which layer is essential
- Start now: whenever you design something end-to-end, create a proper diagram alongside it

---

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Review Power BI interview prep doc; identify areas to practice | Neha | Next session |
| Explore Tableau and Looker Studio | Neha | Ongoing |
| E2E Databricks + Unity Catalog infra deployment on Azure (Terraform + GitHub Actions); research VNet isolation / hub-and-spoke | Deepika | Next session |
| Define Deepika's MLOps path; share with her | Sanjeev | Next session |
| Implement SCD Type 1 & 2, CDC, incremental ingestion in Spark 3; scale with Filip's Faker library; include DABs | Suhash | Next session |
| Define Suhash's Databricks specialization plan (Unity Catalog, DLT, Lakeflow) | Sanjeev | Next session |
| Implement DQX in silver layer using YAML expectations | Asindu | Next session |
| Define Spark Definitive Guide chapters for Asindu | Sanjeev | Next session |
| Draw architecture diagram for current pipeline | All DE interns | Ongoing |

---

## Session 6 — April 25, 2026

**Attendees:** Sanjeev Kumar (mentor), Kousalya, Filip Cedermark, Suhash Raja, Deepika Elangovan, Neha Doda, Nikolaos Biniaris, Elliot Eriksson, Asindu Gayangana

**Agenda:**

**Part 1 — Weekly sync**

1. Week check-in — what did you work on? Blockers? Wins?
2. Meeting schedule — agree on a fixed recurring time going forward *(raised in Apr 22 midweek sync)*
3. Session stream split — confirm structure from Session 5 announcement:
   - DE + DevOps stream: Sanjeev leads
   - ML stream: mentor TBD (acting - Sanjeev)
   - DA stream: mentor TBD (acting - Sanjeev)
4. Neha — dbt vs Databricks focus: which to prioritise first? *(flagged in midweek sync — wants Sanjeev's guidance)*
5. Elliot — ML Use Case 1 demo *(carried over from Session 5)*
6. Intern presentations — carried over from Session 5:
   - Incrementalization & idempotency — pipeline design, backfill handling
   - `infer schema` vs fixed schema — production pros and cons *(Asindu leads)*
   - `AvailableNow` trigger — correct explanation *(Asindu leads)*
   - Scalar UDF vs vectorized / Pandas UDF — when to use each *(Nikolaos leads)*
7. Nikolaos — detailed pipeline code walkthrough *(carried over from Session 5)*

**Part 2 — Based on midweek sync (Apr 22)**

8. Action item check-ins from Session 5:
   - **Suhash** — Databricks CE → Azure ADLS connection attempt
   - **Filip** — Faker data-generation code shared with group? dbt progress?
   - **Deepika** — DQ checks in Silver layer; new PR raised?
   - **Elliot** — ML Use Case 1 PR raised?
9. Admin: Deepika's Slack removal *(free trial expired — Kousalya following up with Raj)*

**Notes:**

---

### 1. Week Check-in

- **Filip Cedermark** — Screenshared Faker-based CDC generator: generates customer records (ID, name, email, phone, city, purchase amount) with configurable row count; first batch always change_type = "insert"; second function updates random rows → change_type = "update" or "delete"; includes nulls for DQ practice. Silver partly done: null email → "unknown@example.com", null phone → "not available". Next: move to dbt; implement quarantine/dead-letter table with reason tagging (Sanjeev recommendation). Will push code to GitHub.
- **Suhash Raja** — No major update this week.
- **Neha Doda** — Started SQL roadmap from GitHub; installed MS SQL Server 2019. Explored dbt and Databricks Academy fundamentals. Has prior Microsoft Fabric experience.
  → **Sanjeev**: Stay on DA track; dbt is the right tool — gives analysts power to do SQL-based transformations (equivalent of what DE does in PySpark). Switching to full DE from zero would be too steep right now. Discuss with Raj if wanting to change track.
- **Elliot Eriksson** — Demoed ML Use Case 1 (see section 2). Also working on Use Case 2. Dropped early.
- **Deepika Elangovan** — Limited progress (volunteering this week). Ingested data into bronze (customers + orders); silver: trimming, normalization, null removal, column renaming. Plans to add advanced functions before next session.
  → **Sanjeev task**: Research CI/CD artifact separation — what belongs in pipeline deployment (Databricks Bundles/API) vs infrastructure deployment (Terraform): specifically catalog, schema, and checkpoint artifacts. Prepare a pros/cons argument.
- **Asindu Gayangana** — No major update (busy last two weeks).
- **Nikolaos Biniaris** — Implemented SCDs, full DQ framework (4 checks: uniqueness, not-null, FK relationships, accepted values), quarantine table with reason column, and business metric APIs (CLV, revenue by product, holiday impact, customer segments, country performance). Detailed walkthrough in section 3.

---

### 2. Elliot — ML Use Case 1 Demo (Counter-Strike round winner predictor)

- **Data & preprocessing**: Game state features (time left, players alive per team, etc.); binary labels (win=1/loss=0); 80/20 train/test split
- **Model**: Gradient Boosting Classifier; ROC AUC used for scoring
- **MLflow**: ~100 model runs via hyperparameter tuning; best model auto-selected. Accuracy improved from ~60% → ~80%
- **Sanjeev walkthrough of Databricks ML UI**: Showed Experiments + Models panel — all runs logged per iteration with metrics (precision, etc.); model can be registered and promoted; Serving section = deploy registered model to an endpoint for inference
- **Next steps for Elliot**: Explore MLflow in depth — model logging, feature stores, model serving. Also explore Snowflake Cortex (since now on Snowflake track).

---

### 3. Nikolaos — Pipeline Walkthrough & DQ Framework

Full pipeline: bronze → silver → dimensions → fact_sales → gold metrics → fact_sales_enriched (+ holidays API)

**DQ framework (modelled after dbt, without Great Expectations):**
- 4 checks: uniqueness of PKs, FK relationships, not-null on key columns, accepted values
- Single parameterized notebook — table name passed as job parameter; same notebook reused across all gold tables
- Quarantine table: broken rows with reason column (test type, failed count, pass rate)

**Sanjeev feedback:**
- Good reusable pattern; `.toPandas().toList()` for metadata table is fine for small metadata but flag as non-scalable if applied to data
- **Key next step — metadata-driven DQ framework**: Hardcoding column checks means every new table requires a code change → testing + deployment window + risk. Production standard: store check configs in a metadata table or JSON file → code reads config dynamically → no code change per new source onboarding
- **at-rest vs in-flight DQ**: current implementation reads data back after writing (at-rest). In-flight DQ (applied during write) is more efficient and lower latency. Research both; plan to migrate.

---

### 4. Technical Discussions

**infer schema vs fixed schema** (Suhash, Deepika, Asindu, Sanjeev):
- `inferSchema=True`: Spark samples a subset to auto-detect column types — risk of wrong inference (e.g., integer inferred but data later contains longs → truncation). Has happened in production.
- **Sanjeev's recommendation — mix and match**:
  - Give **schema hints** for critical columns (IDs, cost, dates) — Spark fixes those, infers the rest
  - In **bronze**: cast all columns to string (accepts everything, nothing dropped) + schema evolution enabled to capture new columns
  - In **silver+**: apply proper typed schema
  - Enable `mergeSchema=True` for schema evolution so new upstream columns are captured rather than silently dropped or failing the job
- **Asindu**: In bronze, schema inference + evolution is needed so new columns aren't lost for auditing. Sanjeev agreed but: risk of wrong type inference → prefer casting everything to string in bronze instead

**Scalar UDF vs Pandas (Vectorized) UDF** (Nikolaos, Suhash, Sanjeev):
- **Scalar UDF**: row-by-row; falls outside JVM → serialization/deserialization overhead; bypasses Catalyst optimizer. In some cases replacing a UDF with a native Spark function gives dramatic performance gains — this is one of the most common Spark optimization wins seen in production.
- **Pandas UDF**: chunk-based (processes batches of rows); stays within Spark execution model; significantly faster
- **Best practice**: Always prefer native Spark functions. Use UDF only when unavoidable. If unavoidable, use Pandas UDF.
- **When unavoidable**: custom ML inference per row (e.g., computer vision on IoT machine images — UDF fires model endpoint per image; switching to Pandas UDF → ~15K images processed in parallel per batch)
- UDFs unavoidable in ~20% of production cases; 80% can be replaced with native Spark functions

**AvailableNow trigger** (Asindu live demo, Sanjeev):
- `spark.readStream` polls source every 500ms by default — runs continuously
- `trigger(availableNow=True)`: converts streaming job to batch — reads all new files since last checkpoint, processes them in parallel, then stops. Checkpoint location handles incrementalization automatically.
- vs `spark.read` (batch): works fine but incrementalization must be handled manually (e.g., date-based directory structure + orchestrator passing current date)
- vs `trigger(once=True)` (deprecated): processes all data in a single batch — not parallel, inefficient for large datasets
- **Asindu's `maxBytesPerPartition` issue**: failing because source table is not partitioned — this option requires a partitioned source. To be covered in a dedicated Spark optimization session.
- Future sessions: dedicated deep-dive on rate limiting, `maxBytesPerTrigger`, `maxFilesPerTrigger`, partition pruning, and Spark optimization.

---

### 5. Logistics & Closing

- **Wednesday sync timing**: uncomfortable for several interns (Deepika: Swedish class; others joining late). To be resolved async via Slack.
- **Session stream split**: delayed due to logistics. Sanjeev handling all tracks for now; update coming via Slack.
- **Next session CANCELLED**: Sanjeev on business trip next weekend (returns Sunday evening). Session resumes in two weeks — **May 9**.

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Push Faker CDC data generator to GitHub repo | Filip | This week |
| Implement dbt silver layer with quarantine table and reason tags | Filip | Next session |
| Start dbt SQL learning roadmap | Neha | Ongoing |
| Research CI/CD artifact separation (Bundles/API vs Terraform for catalog, schema, checkpoints) — pros/cons | Deepika | Next session |
| Research at-rest vs in-flight DQ checks; build metadata-driven DQ framework | Nikolaos | Next session |
| Explore MLflow: model logging, feature stores, serving endpoint | Elliot | Next session |
| Post Slack poll for Wednesday midweek sync timing | Kousalya | This week |

---

## Session 5 — April 19, 2026

**Attendees:** Sanjeev Kumar (mentor), Kousalya, Filip Cedermark, Suhash Raja, Deepika Elangovan, Neha Doda, Nikolaos Biniaris, Elliot Eriksson
**Absent:** Asindu Gayangana

**Agenda:**

1. Week check-in — what did you work on? Blockers? Wins?
2. Intern Tech Platform & Specialization Map

   | Intern | Track | Specialization Focus | Primary Platform | Key Tools & Tech |
   |---|---|---|---|---|
   | **Suhash Raja** | DE + DevOps | Streaming ingestion, medallion architecture, infra provisioning | Databricks + Azure | Azure ADLS, Azure Data Factory, Terraform, Docker, GitHub Actions, PySpark, PL/SQL |
   | **Filip Cedermark** | DE + dbt | Data products, medallion architecture, CDC | Databricks + dbt | PySpark, Delta tables, Faker, dbt |
   | **Deepika Elangovan** | DE + DevOps | CI/CD pipelines, ETL/ELT, IaC integration | Databricks + Azure DevOps | Terraform, Kubernetes, Jenkins, GitHub Actions, PySpark, PowerShell |
   | **Neha Doda** | DA | BI dashboards, KPIs, SQL fundamentals | Power BI + Databricks (exploring) | Power BI (PL-300 certified), Excel, SQL, HackerRank |
   | **Asindu Gayangana** | DE | Advanced pipelines, CDC, Spark optimization | Databricks | Autoloader, Change Data Feed, PySpark, Kaggle data, Parquet, Azure Synapse (prior) |
   | **Nikolaos Biniaris** | DE | API integration, enriched retail pipelines | Databricks | PySpark, Pandas UDF, Public Holidays API, Weather API, Delta tables, Liquid Clustering |
   | **Elliot Eriksson** | ML | Supervised learning, synthetic data generation | Snowflake | MLflow, Snowflake ML, TensorFlow/PyTorch (exploring), PySpark, VS Code |

   > **Note:** Filip added **dbt** as second specialisation; Elliot switched from Databricks to **Snowflake**.

3. Deepika demo — CI/CD pipeline with GitHub Actions, Docker & Kubernetes *(carried over from Session 4)*
4. Architectural discussion — End-to-end data platform walkthrough *(Azure reference architecture)*
5. *(Carried over to next sessions)* Intern presentations — incrementalization, infer schema, AvailableNow trigger, UDFs; Elliot ML demo

**Notes:**

### 1. Week Check-in

- **Suhash Raja** — Connected Databricks to Azure ADLS using Azure Access Connector (managed identity service). Configured storage container access so Databricks reads ADLS automatically via Spark. Learned that Databricks creates a default Access Connector for Unity Catalog metadata — separate from the user-created one for data access. Sanjeev confirmed this distinction. Will also try connecting Databricks Community Edition (free tier) to ADLS.
- **Filip Cedermark** — Busy week (family matters), slightly behind. Switched to Faker for synthetic customer event data (fields: customer ID, name, email, phone, city, purchase amount, signup date). Planning to add CDC logic simulating email/city/order updates. Sanjeev asked Filip to share the Faker code with the group when ready so others can generate large-scale test data.
- **Deepika Elangovan** — Prepared CI/CD demo (presented in item 3). Working on Silver layer: removing nulls/duplicates, renaming columns. Plans to study window functions and Parquet vs Delta next. Sanjeev reminder: Silver is not done without data quality checks — add DQ before considering it complete.
- **Neha Doda** — Got onboarding guidance from Suhash and Filip during mid-week sync. Starting with SQL via the DA roadmap. Already holds Power BI PL-300 certification. Sanjeev directed her to the DA use case week-by-week plan in the repo.
- **Nikolaos Biniaris** — Implemented full CDC across bronze → silver → gold independently. Bronze: MERGE UPSERT by comparing primary key counts. Silver: watermark-based incremental inserts/updates. Gold: rebuilds dimensions/facts for new data. Raised and merged a PR to the main repo. Sanjeev: great example of the Git flow others should follow.
- **Elliot Eriksson** — Completed ML Use Case 1 in Databricks; needs to connect to GitHub and raise a PR. Watching Stanford ML lectures. Participating in a hackathon building a synthetic data model — plans to tie it into Use Case 2. Will demo if time permits.

---

### 2. Tech Platform Diversification

Sanjeev raised that the cohort is heavily Databricks + Azure focused and that **dbt** and **Snowflake** are widely used in the market with customer demand. Asked for volunteers:

- **Filip** → **dbt** (has prior internship experience with it; familiar with the concepts)
- **Elliot** → **Snowflake** (fully switching; had not progressed far in Databricks)

Others remain on Databricks and can add a second platform later. Sanjeev updated the tech platform table.

---

### 3. Deepika Demo — CI/CD with GitHub Actions, Docker & Kubernetes

**CI/CD overview:**
- CI/CD = Continuous Integration / Continuous Delivery (or Deployment)
- Continuous Delivery = requires manual approval before production deploy
- Continuous Deployment = fully automated all the way to production
- Common practice: auto-deploy to dev/test/staging; manual gate for production

**GitHub Actions:**
- Pipeline config lives in `.github/workflows/` as YAML files
- Triggered on push or PR merge to a configured branch
- Steps: checkout code → set Python version → install dependencies → Docker login → Docker build → Docker push
- Secrets (Docker Hub token, API key) stored as GitHub Secrets — never hardcoded in code

**Docker:**
- Dockerfile layers: base image → set workdir → copy requirements → `pip install` → copy source code → expose port → run command
- Image tagging convention: `<date>.<run-number>` (e.g. `19.4.2026.6`) — human-readable vs default SHA hashes

**Kubernetes:**
- Rolling deployment: new pod is created and verified healthy before old pod is terminated → zero downtime
- Key concepts: pod (runs containers), service (exposes app), deployment (desired state config), node (VM), control plane (cluster management)
- Minikube used locally for demo (GitHub Actions does not support Minikube; it's a local learning tool only)

**Live demo app:** FastAPI Gothenburg Weather app using OpenWeather API (temperature, humidity, wind, 5-day forecast). Showed: Docker pull from Hub, `kubectl apply -f deployment.yaml`, rolling pod update in real time.

**Azure deployment path shown (not live):** Service principal + AKS cluster name + resource group configured as GitHub Secrets, then same YAML apply approach.

**Q&A highlights:**
- *Elliot:* When deploying new code, do you need to restart the running process? → *Sanjeev:* Yes, unless using blue-green deployment. *Deepika:* Kubernetes rolling deployment handles this — new pod runs before old pod is terminated.
- *Sanjeev:* How much of this applies to MLOps? → *Deepika:* Limited MLOps experience, couldn't fully answer. Same CICD principles apply but MLOps has model-specific concerns.

---

### 4. Architectural Discussion — End-to-End Data Platform

Sanjeev walked through a full Azure-based reference architecture of a typical customer data platform — framed as essential interview knowledge for all tracks (DE, DA, ML, DevOps).

**Sources:**
- RDBMS/DWH (SQL Server, Synapse) — JDBC connections, CDC streams
- Sensors & IoT (wind farms, electricity meters, factory machines, Electrolux fridges) — continuous real-time streams
- Files/Logs (JSON, XML, audit logs, cybersecurity logs) — semi-structured
- Media/Unstructured (images, video) — fed to ML models (e.g. Northvolt predictive maintenance)
- Business Apps — structured/aggregated; ML typically consumes at gold/feature store level
- Multi-cloud — common in enterprise; involves egress cost, networking, private links

**Ingest — Batch vs Streaming:**
- Batch: hours/daily cadence, lower cost
- Near real-time: seconds to minutes; Real-time: <1 second (fraud detection, card tap)
- Interview tip: always reason about *why* streaming is needed — cost tradeoff is real; every interviewer will probe this
- Tools: Azure Event Hub / Data Factory, Databricks Structured Streaming, Snowflake Snowpipes, AWS Kinesis

**Orchestration (spans all layers):**
- Manages job dependencies and scheduling end-to-end (ingest → transform → gold → reverse ETL)
- Tools: Databricks Workflows, Azure Data Factory, Apache Airflow, AWS Glue ETL

**Data & AI Governance:**
- Non-negotiable for enterprise production: row/column-level security, access control, lineage
- Databricks: Unity Catalog; Snowflake: Horizon; Azure: Purview; cross-platform: Immuta (referential catalog)
- For ML: AI governance — model access audit, EU AI Act compliance
- Sanjeev: *"Any platform without fine-grained access control will fail enterprise customers"*

**Operational DB & Reverse ETL:**
- Low-latency serving (<100ms): LakeBase (Databricks managed Postgres), Snowflake equivalent
- Reverse ETL: pushing aggregated gold data back to operational DBs for fraud detection, credit checks, in-app real-time dashboards

**Collaboration / Data Sharing:**
- Delta Share (Databricks), Snowflake Marketplace — share data with third parties without copying it

**DevOps across all layers:**
- DevOps/MLOps applies everywhere — CI/CD for code changes, IaC for infrastructure, MLOps for model lifecycle

**GDPR vs Data Governance:**
- Data Governance = who has access to data at rest right now (access control, lineage)
- GDPR = regulatory compliance (right to be forgotten, data residency) — related but distinct

![Data Intelligence Platform Architecture](../images/lakehouse-architecture.png)

---

### 5. Closing & Next Steps

- **Session structure from next week:** Sessions split into specialised streams
  - DE + DevOps: Sanjeev leads
  - ML: separate mentor TBD (Elliot's stream)
  - DA: TBD — Sanjeev or another mentor
- Sanjeev to share the split session plan in the group channel before next week

**Carried over to future sessions:**
- Intern presentations: incrementalization & idempotency, infer schema vs fixed schema, AvailableNow trigger, Scalar vs Pandas UDF
- Elliot ML Use Case 1 demo
- Nikolaos detailed pipeline code walkthrough

### Action Items

| Task | Owner | Due |
|------|-------|-----|
| Try connecting Databricks CE to Azure ADLS | Suhash | Next session |
| Share Faker data-generation code with group | Filip | This week |
| Implement DQ checks in Silver layer | Deepika | Next session |
| Delete & re-upload demo files; raise new PR with latest changes | Deepika | This week |
| Study DA use case plan week-by-week | Neha | Ongoing |
| Raise PR for ML Use Case 1 code | Elliot | This week |
| Explore dbt | Filip | Ongoing |
| Explore Snowflake | Elliot | Ongoing |
| Share next week's split session plan with group | Sanjeev | Before next session |

---

## Session 4 — April 11, 2026

**Attendees:** Sanjeev Kumar (mentor), Elliot Eriksson, Suhash Raja, Deepika Elangovan, Nikolaos Biniaris, Asindu Gayangana

*Note: Filip not present.*

**Agenda:**

**Part 1 — Carried over from Session 3**
1. Week check-in — what did you work on? Blockers? Wins?
2. Parquet deep dive — why is it the backbone of big data?
3. Code sharing — Stage 1 progress; screen share what you have built so far
4. Architectural discussion — table formats (Delta, Iceberg, Hudi) deep dive and comparison; Lakehouse vs Data Lake vs Data Warehouse

   ![Data Intelligence Platform Architecture](../images/lakehouse-architecture.png)
5. ~~Deepika demo — CI/CD pipeline with GitHub Actions + Databricks~~ *(moved to Session 5 — PR raised, demo needs more prep)*

**Part 2 — Based on midweek sync (Apr 8)**
- Git workflow recap — quick walkthrough of feature branch → PR flow
- Data sources Q&A — clarify what datasets to use per stage (Faker, Kaggle, CoinGecko API, Raspberry Pi IoT simulator)
- ~~Catch up with Filip & Nikolaos — hear about their progress and see if there is anything the group can help with~~ *(Filip absent; Nikolaos covered in check-in)*

**Notes:**

### 1. Week Check-in

- **Elliot Eriksson** — Chose Databricks as ML platform. Currently working on a simple supervised learning project to learn how Databricks works. Has Git set up but hasn't pushed code yet — waiting until something is complete.
- **Suhash Raja** — Studied window functions and CTEs. Attempted to set up source data but hit connectivity issues between local machine and Azure. Exploring Kafka + Kubernetes → Databricks as a pipeline topology. Sanjeev flagged to not stay stuck — ask for help early. Will set up Git repo.
- **Deepika Elangovan** — Set up Databricks platform. Generated synthetic data using Faker (orders.csv + customers.csv, ~5,000 rows). Uploaded to Databricks and read using PySpark. Studied Spark architecture, DAG, lazy evaluation, DataFrames, and ELT vs ETL hybrids. Raised a PR for CI/CD work (used fork method instead of direct clone — Sanjeev confirmed both approaches are fine). Will demo CI/CD next session.
- **Nikolaos Biniaris** — Joined CSV sources and enriched with API data. Initially used a weather API for order enrichment but hit rate limits (~900 records/day cap). Switched to a **Public Holidays API** to enrich orders by country — goal is to analyse whether sales correlate with public holidays. Screen-shared pipeline showing parallel ingestion (CSV + API) and Silver join on the date column.
- **Asindu Gayangana** — Parameterized pipeline scripts using Databricks task parameters passed into notebooks. Created a DIM_DATE table directly to Silver (skipped Bronze — justified as a one-time static load). For other sources, used AutoLoader (`readStream` + `cloudFiles`) with schema inference, schema evolution mode, `maxFilesPerTrigger`, and CDC. Screen-shared code. Had a detailed discussion on incrementalization, infer schema, and the AvailableNow trigger (see section 3).

---

### 2. Parquet Deep Dive

Group discussion — interns shared what they researched:

- **Suhash** — Columnar format stores data column-by-column rather than row-by-row. Since values in a column share the same type, compression is very efficient. Only selected columns are read — not the entire row.
- **Nikolaos** — Validated the column pruning behaviour: selecting 2 of 20 columns reads only those 2 columns; the other 18 are skipped entirely by the engine. This can reduce query time from hours to seconds at scale.
- **Asindu** — Added that Parquet is OLAP-optimised. Per-column compression is more effective because each column has a uniform data type. Parquet also stores min/max statistics per column chunk, enabling predicate pushdown and file pruning without reading the data itself.

**Sanjeev expanded:**
- Parquet compression algorithms (Snappy, ZSTD) can compress data 10x or more — a file that is 100 MB on disk could expand to 10 GB in memory.
- In contrast, CSV/text compression is far less efficient because data types are mixed per row.
- **Open table formats (Delta, Iceberg, Hudi)** are not new file formats — they are Parquet underneath, but with an additional **metadata layer** (JSON/Avro sidecar files) that stores: min/max statistics per column, deletion vectors, schema versions, and partition metadata.
- When a query runs against a 1 TB table split across 10,000 Parquet files, the metadata layer allows **data skipping** — the engine reads the metadata first and prunes irrelevant files before touching any data files.
- **Task for next session:** Research what specific problems Delta/Iceberg/Hudi solve that raw Parquet cannot handle on its own.

---

### 3. Code Screen Shares & Technical Discussion

**Nikolaos — API Ingestion & Parallel Pipeline**
- Ingesting CSV and Public Holidays API in parallel Databricks tasks.
- Silver layer joins the two sources on the date column to enrich orders with holiday flags.
- Hit weather API rate limits earlier — good real-world lesson on API ingestion design.
- **Sanjeev's advice on API ingestion in interviews:** Be able to articulate that API ingestion is viable but comes with trade-offs — rate limits, scalability (will the API handle a 10x increase in calls?), and whether batch pull vs event-driven push is the right model.
- **Spark UDFs vs pure Python for APIs:** Nikolaos correctly avoided Spark UDFs for API calls. Key reasons: UDFs fall outside the JVM and lose Catalyst optimiser benefits; they are row-by-row unless vectorized; serialisation/deserialisation overhead.
- **Sanjeev assigned research:** Compare **scalar UDF** vs **vectorized UDF (Pandas UDF)** — why the vectorised variant is faster and when each should be used.

**Asindu — Parameterized AutoLoader Pipeline**
- Task parameters passed from Databricks Workflow into notebook widgets — good production pattern for reusability.
- DIM_DATE created directly to Silver without Bronze — valid for one-time static reference tables.
- For transactional sources, used AutoLoader (`readStream + cloudFiles`) with:
  - `inferSchema = true` — auto-detects column types; if disabled, everything reads as string.
  - `schemaEvolutionMode` — handles upstream schema changes without failing the job.
  - `maxFilesPerTrigger` — limits how many files are processed per micro-batch (scalability control).
- **Sanjeev's questions (to research for next session):**
  - `inferSchema true` vs manually defining a fixed schema — what production problems can each cause?
  - `AvailableNow` trigger — Asindu's explanation was partially correct; Sanjeev clarified: if you use `readStream`, the job would normally run continuously (24/7). `AvailableNow` tells the streaming API to process all available data *now* and then stop — making a streaming job behave like a scheduled batch job.
- AutoLoader handles idempotency automatically via checkpoint locations — it tracks which files have already been processed and only ingests new arrivals.
- **Sanjeev noted:** Even without AutoLoader, incrementalization can be achieved using batch APIs — interns should understand both approaches.

**General points raised by Sanjeev:**
- All interns should push code to Git using the **feature branch → PR** workflow. Treat the internship repo like a production delivery to a customer.
- Asindu's Git invite had expired — Sanjeev to re-add.
- Session time of 1 hour is proving short given the screen-sharing depth. Sanjeev will discuss extending sessions with Kousalya.

---

### 4. Architectural Discussion — Lakehouse Introduction *(partial)*

- **Deepika** summarised: Data Warehouse holds processed/structured data; Data Lake holds raw + semi-structured data; Lakehouse is a combination of both for advanced analytics.
- **Sanjeev** began the evolution narrative: started with traditional Data Warehouses (Oracle, SQL Server) → limitations led to the Data Lake concept → *(transcript cut off here)*
- The group discussed the key differences between the three paradigms — Data Warehouse, Data Lake, and Lakehouse — and how the Lakehouse addresses the weaknesses of both predecessors.
- Discussion touched on how the Lakehouse architecture is **scalable** (built on object stores like S3/ADLS, compute and storage scale independently) and **ACID compliant** (enabled by open table formats like Delta Lake, Iceberg, and Hudi, which bring transactional guarantees on top of Parquet). *(Full discussion not captured in transcript — to be continued in Session 5.)*

---

### Action Items for Next Session

| # | Task | Who |
|---|------|-----|
| 1 | Research incrementalization patterns — simulate incremental data arrival and test that pipeline only ingests new files; research idempotency and backfill handling | All interns |
| 2 | Research what problems Delta / Iceberg / Hudi solve on top of raw Parquet — come ready to discuss | All interns |
| 3 | Push code to Git repo using feature branch → PR workflow | All interns |
| 4 | Understand Lakehouse architecture — differences between Data Warehouse, Data Lake, and Lakehouse; how Lakehouse achieves scalability and ACID compliance | All interns |
| 5 | Research `infer schema true` vs fixed schema — what production issues can each cause? | Asindu |
| 6 | Research `AvailableNow` trigger — explain correctly next session | Asindu |
| 7 | Research scalar UDF vs vectorized / Pandas UDF — explain the difference and when to use each | Nikolaos |
| 8 | Prepare CI/CD demo (GitHub Actions + Databricks) for Session 5 | Deepika |
| 9 | Resolve Azure connectivity issue; implement incremental ingestion pipeline | Suhash |
| 10 | Continue supervised learning project in Databricks; push code to Git | Elliot |
| 11 | Re-add Asindu to repo (invite expired); discuss session time extension with Kousalya | Sanjeev |

---

## Session 3 — April 4, 2026

**Attendees:** Sanjeev Kumar (mentor), Kousalya (organizer), Suhash Raja, Filip Cedermark, Asindu Gayangana, Elliot Eriksson, Deepika Elangovan, Nikolaos Biniaris

*Note: Easter weekend — some interns had limited availability; Filip left early.*

**Agenda:**
1. Repo walkthrough — structure, CLAUDE.md, branching strategy
2. Week check-in & platform check-in
3. Use case progress & live demos
4. Architectural discussion — file formats & table formats

**Notes:**

### 1. Repo Walkthrough

Sanjeev walked through the repo structure for interns who had just cloned it:

- `raw/` — raw inputs including meeting transcripts. Interns can commit their own midweek sync transcripts here as a progress tracker.
- `live/` — living documents (session notes, use cases, topics list). All interns have read/write access; suggest edits via PRs.
- `action/` — intern work artifacts. Each intern creates their own subfolder under their stream (e.g. `action/DE-DevOps/your-name/`). Treat it as a monorepo.
- `CLAUDE.md` — key config file for AI-assisted workflows. Changes should go through PRs, not direct commits to main.
- Branching strategy: `feature/*` → `dev` → `staging` → `main` (GitFlow lite). All interns should create feature branches and submit PRs.

---

### 2. Week Check-in & Platform Check-in

- **Suhash Raja** — Started SQL basics (DDL) in Databricks. Chose **Databricks** (free enterprise edition). Has not cloned the repo yet; plans to do so post-session.
- **Filip Cedermark** — Getting set up on Databricks; file structure setup was trickier than expected. Used ChatGPT to generate sample data and landed it in Databricks. Planning to look at Stage 2 (CDC) next. Sanjeev recommended switching to the **Faker library** for reusable, scalable data generation in Databricks.
- **Asindu Gayangana** — Built a pipeline in Databricks using a 5M-row Kaggle dataset. Used **Autoloader** for Bronze ingestion. Set up **Change Data Feed (CDF)** on the Bronze table — manually modified data via SQL, then extracted changed records using version history (max version). Loaded dimension tables; still needs to join the fact table for Silver. Also researched Spark internals: worker nodes, partitions, ideal partition sizes, on-heap memory (execution + storage). Could not fully understand off-heap memory.
- **Elliot Eriksson** — Read about Spark and PySpark; drew diagrams of how it works. Confirmed he's on the **ML track**. Planning to use VS Code + PySpark. Sanjeev pointed out ML platform options: Databricks (MLflow), Snowflake (Cortex), AWS (SageMaker), Azure ML.
- **Deepika Elangovan** — Created Databricks account (Azure free trial exhausted). Watching YouTube tutorials on data ingestion. Has an existing GitHub CI/CD repo. Sanjeev asked her to demo CI/CD pipeline to the group using GitHub Actions + Databricks integration. Also mentioned **Databricks Asset Bundles** and **Terraform** as tools to explore.
- **Nikolaos Biniaris** — Shared screen showing Databricks. Ingested CRM/ERP data (customers, products, sales + dimension data — 6 tables) using both Python and SQL notebooks. Chose not to partition at Bronze (no date columns; dates stored as strings). Researched partitioning in Databricks vs standard Spark. Asked about handling multiple source types (CSV + API) — Sanjeev showed how to build parallel Databricks workflow tasks for independent sources. Also asked about API ingestion; Sanjeev directed him to research **Spark UDFs** and their trade-offs.

---

### 3. Architectural Discussion — File Formats & Table Formats

**Structured vs Semi-structured vs Unstructured data:**
- **Unstructured** (images, binary blobs) — no schema, slowest to process.
- **Semi-structured** (JSON, XML) — schema loosely coupled (xsd for XML); can be processed without schema.
- **Structured** (tabular, Parquet, Delta) — schema tightly bound; fastest for engines to process.

**Open Source vs Proprietary formats:**
- Proprietary: Oracle, Teradata, Snowflake's internal formats — require licenses.
- OSS: Parquet, Delta, Iceberg, Hudi, Avro, ORC — free to use; any engine or platform can adopt them.
- Interview tip: being able to reference OSS technologies (Apache Spark, MLflow, Iceberg) rather than only vendor tools shows platform-agnostic depth.

**Object stores:** S3, ADLS, GCS — where all data lives as files (called "objects"). Bronze/Silver/Gold data all lives here.

**Parquet:**
- The bread and butter of the big data world. Columnar format. Foundation of almost every modern data platform.
- **Task for interns:** research *why* Parquet is so important and what problem it solves. Discuss in midweek sync.

**Open Table Formats — Delta, Iceberg, Hudi:**
- All three are built on top of Parquet but add a metadata layer.
- Key features added: ACID transactions, time travel, schema enforcement, versioning, upsert/merge support.
- Delta Lake: created by Databricks engineers, then open sourced. Liquid clustering is a Delta innovation, also open sourced.
- Iceberg and Hudi: alternative open table formats with similar capabilities.
- Discussion to continue next session with deeper comparison.

**Streaming source tip (for Suhash's question):**
- **Raspberry Pi Azure IoT Web Simulator** — free, browser-based tool that generates IoT data and writes to Azure IoT Hub. Can be pointed at Databricks Structured Streaming or ADF for practice with real streaming ingestion.

---

### Action Items for Next Session

| # | Task | Who |
|---|------|-----|
| 1 | Research why Parquet is the backbone of big data — come ready to discuss in midweek sync and Session 4 | All interns |
| 2 | Clone the repo; create your own folder under `action/` for your stream | All interns |
| 3 | Start Stage 1 (batch ingestion) in Databricks | Suhash |
| 4 | Switch data generation to Faker library; explore Stage 2 (CDC) | Filip |
| 5 | Complete Silver fact table join; commit code to `action/` folder | Asindu |
| 6 | Choose ML platform (Databricks / SageMaker / Azure ML); start ML use case | Elliot |
| 7 | Commit CI/CD demo (GitHub Actions + Databricks) to internship repo; explore Databricks Asset Bundles and Terraform | Deepika |
| 8 | Build parallel Databricks workflow (CSV + API sources); read about Spark UDFs and their trade-offs | Nikolaos |

---

## Session 2 — March 28, 2026

**Attendees:** Suhash Raja, Filip Cedermark, Deepika Elangovan, Neha Doda, Kousalya (organizer), Sanjeev Kumar (mentor), Vivek Prasad (mentor), Vinod (mentor), Asindu Gayangana, Nikolaos Biniaris, Elliot Eriksson

**Agenda:**
1. Week check-in — what did you work on? Anything to share?
2. Platform — use and registration
3. Use cases defined per stream
4. Architectural discussion



**Notes:**

### 1. Week Check-in

Interns shared what they worked on since Session 1:

- **Suhash + group** — Reviewed the shared presentation slides; had a midweek check-in among themselves to compare tools and skills.
- **Filip Cedermark** — Refreshed SQL fundamentals on HackerRank (basic and advanced queries). Also attended a Snowflake AI/agentic event (got in last-minute via a colleague's spare spot).
- **Deepika Elangovan** — Recapped SQL basics; had not used SQL since joining Accenture, so focused on getting back up to speed with small queries.
- **Asindu Gayangana** — Worked on SQL and PySpark; focused on window functions and complex joins. Subscribed to a Spark Playground for hands-on practice.
- **Nikolaos Biniaris** — Practised SQL heavily (window functions, joins). Asked a good question: *how much do we need to manage clustering ourselves in Snowflake vs Databricks?* Sanjeev explained predictive optimization — both platforms can auto-manage clustering, but Databricks gives manual control if needed.
- **Elliot Eriksson** — Limited prior experience with data lifecycle; had done minor data cleaning projects (null/duplicate removal) including a cancer-identification ML project.

Sanjeev's advice to the group: attend platform meetups (Databricks, AWS, Microsoft, Snowflake) beyond big paid events — look up smaller user groups and meetups on meetup.com.

---

### 2. Platform — Use and Registration

Sanjeev walked through how to choose a platform to implement the use cases:

- All major cloud platforms offer free/trial accounts: **Azure (ADF)**, **AWS (Glue)**, **Databricks (Lakeflow Designer / Serverless SQL — now unlimited free tier)**, **Snowflake**.
- Recommended approach — start easy, then go deeper:
  - **Phase 1:** Drag-and-drop tools (ADF, Glue, Lakeflow Designer) — implement the use case with minimal code to understand the concepts.
  - **Phase 2:** Re-implement the same use case in **pure PySpark** — this is the target skill for data engineers.
- Failures/errors encountered along the way will surface important Spark internals worth discussing in sessions.
- **Task:** Each intern to pick a platform, spin up a trial account, and report back next session which platform they chose.

---

### 3. Architectural Discussion

#### 1. Data Lifecycle
The journey every piece of data takes through a modern data platform:

- **Ingestion** — Pull raw data from source systems (databases, APIs, flat files, streams) and land it as-is into storage (Bronze layer). No transformation yet.
- **Cleaning** — Remove nulls, duplicates, invalid records. Standardize formats (dates, currency, casing). This produces a trusted, queryable Silver layer.
- **Transformation** — Apply business logic: joins, aggregations, KPI calculations, data modelling (Star Schema). This is the Gold layer — ready for consumption. dbt owns this step.
- **Serving** — Expose the clean, modelled data to end consumers: dashboards (Power BI / Tableau), APIs, ML models, or self-serve querying (Databricks Genie).

#### 2. Distributed Systems
Why we can't just use a single machine for large data:

- A single machine has limits on CPU, RAM, and disk — at scale, data doesn't fit
- Distributed systems split work across many nodes (computers) that work in parallel
- Key concepts: partitioning (splitting data), fault tolerance (handling node failures), coordination (who does what)
- Examples in the wild: Hadoop (HDFS), Kafka (streaming), Cassandra (NoSQL), and the Spark cluster itself
- The trade-off: more complexity, but linear scalability

#### 3. Distributed Engines
The processing layer that runs on top of distributed systems:

- **Apache Spark / PySpark** — The dominant batch + streaming engine. Processes data in-memory across a cluster. Used for Silver → Gold transformations at scale.
- **Apache Flink** — Real-time stream processing. Lower latency than Spark Streaming.
- **Databricks** — Managed Spark platform with optimizations (Delta Engine, Photon). What most enterprises run today.
- **dbt** — Not distributed itself, but pushes transformation logic down into the warehouse engine (Snowflake, BigQuery, Redshift) which is distributed underneath.

#### 4. File Formats
How data is physically stored on disk — this matters for performance:

| Format | Type | Pros | Best For |
|---|---|---|---|
| CSV | Row-based | Human readable, universal | Small files, quick sharing |
| JSON | Row-based | Flexible schema, API native | Raw ingestion, semi-structured data |
| Parquet | Columnar | Fast reads, great compression | Analytics, data warehouses |
| Avro | Row-based | Schema evolution, compact | Kafka streaming, Hadoop |
| Delta | Columnar + ACID | Versioning, time travel, ACID | Production pipelines (Databricks) |
| ORC | Columnar | Optimized for Hive/Hadoop | Legacy Hadoop stacks |

Key takeaway: **use Parquet or Delta for anything going into a pipeline**. CSV/JSON only at the ingestion boundary.

---

### 4. Use Cases Defined per Stream

Each intern now has a defined use case that will be their north star through the internship. These are end-to-end projects that build progressively each month.

**Sanjeev - DE**

**Use Case: Smart Retail Analytics & AI-Powered Recommendation Engine**

A retail company operates both online and offline stores. They receive raw data from multiple sources — transactional databases, REST APIs, and flat files — and need an end-to-end data platform to power business reporting, customer intelligence, and an AI-assisted product recommendation system.

**Data Sources:**
- Customer & Orders DB → PostgreSQL (OLTP) — ingested via Python + SQLAlchemy
- Product catalog → REST API (paginated JSON) — ingested via Python Requests
- Store inventory & suppliers → CSV files (daily drops) — processed via Pandas / PySpark
- User clickstream / behavior → JSON logs — processed via PySpark

**Pipeline Stages:**

- **Stage 1 — Extract (Bronze):** Ingest from all sources into cloud storage (S3/Azure Blob), partitioned by ingestion date. Raw data stored as-is.
- **Stage 2 — Silver (Cleaning & Enrichment):** Remove nulls, duplicates, invalid records. Standardize timestamps and currency. Join orders → customers → products. Deduplicate using SQL Window Functions (ROW_NUMBER). Use CTEs for readable transformation logic.
- **Stage 3 — Data Modeling:** Design a Star Schema (fact_orders + dim_customer, dim_product, dim_date, dim_store). Load into a cloud warehouse (Snowflake / BigQuery / Redshift).
- **Stage 4 — Gold Layer with dbt:** Build dbt models for business metrics — revenue by product, customer lifetime value, customer segments (High/Mid/Low), store performance, inventory health. Add dbt tests (not_null, unique, custom SQL).
- **Stage 5 — Scale with PySpark:** Re-implement Silver → Gold transformations in PySpark. Handle millions of rows with partitioning, caching. Compare Pandas vs PySpark for scale.
- **Stage 6 — Orchestration with Airflow:** Daily DAG at 10 AM — extract → silver → gold → dbt run → notify. Add retry logic, failure alerts, backfill support, data quality sensor tasks.
- **Stage 7 — AI Layer (RAG + Vector DB):** Embed product descriptions → store in Pinecone or pgvector. Build a RAG pipeline for semantic product search and personalized recommendations using purchase history.
- **Stage 8 — CI/CD & Production Hardening:** GitHub Actions pipeline (lint → test → staging → prod). Environment-based dbt profiles. Bash scripts for health checks and backfills. Full documentation and architecture diagram.


**Approach 1 — Cloud Native:** Python → S3/Azure Blob → Snowflake/BigQuery → dbt → Airflow → pgvector/Pinecone → GitHub Actions

**Approach 2 — PySpark Stack:** Python + PySpark → Parquet/HDFS → PostgreSQL or Databricks → dbt → Airflow (local) → pgvector → GitHub Actions


**Vinod - DA**

SQL Internship - Setup and Week 1 Tasks

1. SQL Setup Steps
   - Install Microsoft SQL Server 2019 Developer Edition.
   - Install SQL Server Management Studio (SSMS).
   - Download the AdventureWorks sample database backup file (.bak).
   - Open SSMS and connect to the SQL Server instance.
   - Right click on Databases and select Restore Database.
   - Choose Device and select the downloaded .bak file.
   - Complete the restore process and create the database.
   - Run a sample query to confirm the setup is working.

2. Week 1 SQL Practice Questions
   - Get all records where FirstName starts with A and ends with n
   - Find people whose LastName length is more than 6 characters
   - Get records where FirstName contains ar but not at the start
   - Fetch records where FirstName is exactly 5 characters long
   - Find people where FirstName is equal to LastName
   - Get records where FirstName has no vowels
   - Find people whose LastName starts with same letter as FirstName
   - Get records where FirstName starts with M and LastName ends with r
   - Find people where FirstName starts with J or LastName starts with S but BusinessEntityID is less than 100
   - Get records where FirstName contains a and does not contain e
   - Find people where FirstName starts with A or B and LastName contains son
   - Find names where second letter is a
   - Find names where third letter is r
   - Get names where FirstName starts and ends with same letter
   - Find names that contain exactly one a
   - Get names that contain at least two a characters
   - Find records where FirstName is in John, David, Mary and BusinessEntityID is between 50 and 200
   - Get records where FirstName is not in James, Robert and LastName starts with B
   - Find people where BusinessEntityID is between 10 and 100 and FirstName starts with a vowel
   - Get records where ID is between 1 and 300 but exclude even numbers
   - Find people where FirstName starts with S and LastName ends with n or contains ar
   - Get records where FirstName starts with a vowel and LastName does not start with a vowel
   - Find people where FirstName length is greater than 5 and LastName length is less than 5
   - Get records where FirstName contains a and LastName contains e and BusinessEntityID is less than 150
   - Find people where FirstName starts with A or LastName ends with e and FirstName does not contain z and BusinessEntityID is between 10 and 200
   - Find people where FirstName has exactly two vowels and LastName starts with same letter as FirstName and ID is not between 50 and 100
   - Find people where FirstName contains ar only once and LastName length is greater than FirstName length


**Vivek - ML**
TBU

---

### Action Items for Next Session

| # | Task | Who |
|---|------|-----|
| 1 | Read about distributed systems, distributed engines, and file formats. Prepare an architecture diagram of how Spark works (driver, workers, partitioning, fault tolerance) — explain it to the group. | All interns |
| 2 | Sign up for a trial platform of your choice (Azure/AWS/Databricks/Snowflake). Report back which platform you chose. | All interns |
| 3 | Start on Stage 1 of your assigned use case using the chosen platform. | DE / DevOps interns |
| 4 | Sanjeev to refine the use case document and share the repo with the group. | Sanjeev |
| 5 | Sanjeev to update DevOps and ML use case sections. | Sanjeev |
| 6 | Continue midweek check-in among yourselves. Drop blockers/questions in Slack. | All interns |

---

## Session 1 — March 21, 2026

**Attendees:** Sanjeev Kumar (mentor), Suhash Raja, Filip Cedermark, Deepika Elangovan, Neha Doda, Kousalya (organizer)

**Agenda:**
1. Introductions (experience, expectations, fun fact)
2. Structure of sessions — discussion
3. Common session plan for all streams

**Notes:**

Session structure agreed:
- Saturday 1-hour sessions (mentors unavailable on weekdays)
- First month: common sessions for all streams covering foundational topics
- 4 streams planned: DA, DE, DevOps/Infra, ML/Analytics

Intern introductions & stream assignments:

- **Suhash Raja** — Major: DE + DevOps. 10 yrs IT (PL/SQL, Splunk, Docker, Terraform, GitHub Actions). Databricks Associate certified.
- **Filip Cedermark** — Major: Data Engineering. Vocational AI/ML school, 17-week internship at Postnode (PySpark/Databricks), consulting bootcamp.
- **Deepika Elangovan** — Major: DE + DevOps. 4 yrs DevOps at Accenture (Azure, CI/CD, Terraform, Kubernetes). Wants to expand into DE.
- **Neha Doda** — Major: DA (primary), interested in DA + DE combo. Power BI, PL-300 certified (Jan 2026), end-to-end BI background.

Key discussion points:
- AI philosophy: build foundational knowledge first, use AI as a companion — not vibe-coding from day one
- AI impact on DA roles discussed (Databricks Genie/AI BI); Neha's DA + DE combo recommended as a strong skillset
- Vinod (mentor) intro not completed — transcript cut off

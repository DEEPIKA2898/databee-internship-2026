# Use Case — Data Science & Machine Learning

**Track Lead:** Vivek Prasad

---

> This document covers the foundational ideas you need before you start building. Don't try to memorise all of this upfront — read through once.

---

## Stream 1: Python, Math & ML Fundamentals

### Python Basics for ML

- **Functions and loops** — you'll use these constantly. Get comfortable writing reusable functions instead of copy-pasting code blocks.
- **Lists and dictionaries** — most data in ML passes around as one of these before it hits a dataframe.
- **Virtual environments** — always work inside a virtual environment (`python -m venv env`). This keeps your project's dependencies isolated and avoids the classic "it works on my machine" problem.
- **pip** — how you install libraries. `pip install pandas scikit-learn` is how you get started on almost every project.

### Math You Actually Need at This Stage

- **Mean and average** — the most basic way to summarise a set of numbers. If your model predicts house prices, the mean error tells you how far off it is on average.
- **What a percentage tells you** — if 20 out of 100 customers churned, the churn rate is 20%. Simple, but you'll use this to understand your data before touching any model.
- **Correlation** — when one thing goes up, does another tend to go up or down with it? You don't need to calculate it by hand; just understand what it means when someone says "age and salary are positively correlated."

### What is Machine Learning?

In normal programming you write rules: *if age > 60 and balance < 500, flag as at-risk.*
In machine learning you give the computer examples (lots of past customers + whether they actually churned) and it figures out the rules on its own.

Three types you should know:

- **Supervised learning** — you give labelled examples (input + correct answer). The model learns to predict the answer for new inputs. This is what 90% of beginner projects use.
- **Unsupervised learning** — no labels. The model finds patterns in the data on its own, like grouping similar customers together.
- **Reinforcement learning** — the model learns by trial and error. Think chess engines. Ignore this for now.

### The ML Workflow

Every project, regardless of complexity, follows the same basic steps:

```
Get Data → Clean It → Prepare Features → Train Model → Evaluate → (Deploy)
```

1. **Get data** — CSV file, database, API, whatever. At beginner level it's usually a CSV.
2. **Clean it** — remove rows with missing values, fix obvious errors, drop columns you don't need.
3. **Prepare features** — convert everything into numbers (models only understand numbers). "Male/Female" becomes 0/1, categories become encoded numbers.
4. **Train a model** — feed the prepared data to an algorithm. It adjusts its internal parameters until predictions are as close to the correct answers as possible.
5. **Evaluate** — check how well it performs on data it has never seen before.
6. **Deploy** — make it available so others can use it. Don't worry about this step on your first project.

### Features and Labels

- A **feature** is an input the model uses to make a prediction. Example: customer age, number of products purchased, account tenure.
- A **label** is what you're trying to predict. Example: will this customer churn? (yes/no)

> Good features matter more than a complex model. Start simple.

### Training vs Testing Split

You never evaluate a model on the same data you trained it on — that's like giving students the exam questions in advance.

Standard practice: split your data before you do anything else.

- **Training set (~80%)** — the model learns from this
- **Test set (~20%)** — you check performance on this, only after training is done

If you skip this step, your model will look great on paper and fail in real use.

---

## Stream 2: Deep Learning & Frameworks

At beginner level you don't need to build neural networks yet. But you should understand what they are.

### Neural Networks

A neural network is a chain of simple calculations applied one after another. Each "layer" takes inputs, multiplies them by weights, adds a bias, and passes the result to the next layer. Through training, the weights get adjusted until the output matches the correct answers as closely as possible.

That's it. The complexity comes from having many layers and millions of weights — not from any single step being complicated.

### Why Frameworks Exist

Writing all those calculations from scratch for every project would be impractical. Frameworks like **PyTorch** and **TensorFlow** give you pre-built building blocks — define your architecture, feed in data, call `.fit()` or a training loop, and the framework handles the math.

At this stage: just know they exist and that **PyTorch** is the more widely used one in research and industry right now.

### Saving a Model

Once trained, a model is just a set of numbers (weights). Saving a model means writing those numbers to a file. Loading a model means reading them back so you can use the model without retraining.

In scikit-learn:
```python
joblib.dump(model, 'model.pkl')   # save
joblib.load('model.pkl')          # load
```

---

## Stream 3: Cloud Platforms & Deployment

### Docker — One Idea to Understand

A Docker container packages your code, your Python version, and all your libraries into one self-contained unit. It runs identically on your laptop, your colleague's machine, and a cloud server.

The reason this matters: "it works on my machine but not on the server" is one of the most common problems in software. Docker eliminates it.

You write a `Dockerfile` that describes what to install and how to run your app. Then `docker build` creates the image and `docker run` starts it.

### Batch vs Real-Time Inference

- **Batch inference** — run predictions on a whole dataset at once, typically on a schedule. Example: every Monday morning, score all customers for churn risk and save results to a file.
- **Real-time inference** — a running service that responds to individual requests instantly. Example: a user opens the app, and within milliseconds the system recommends products.

---

## Stream 4: MLOps Basics

### Why Not Just Use a Notebook Forever?

Notebooks are great for exploring data. But they're hard to schedule, hard to test, and hard for other people to run reliably. Once your code works in a notebook, the next step is converting it to a plain Python script that can be run from the command line and triggered automatically.

### Experiment Tracking

When you try different model settings (more trees, different learning rate, etc.) it's easy to forget which combination gave the best result. **MLflow** solves this by logging every run with its parameters and metrics so you can compare them in a visual dashboard.

### What is Model Drift?

A model trained on last year's data might become less accurate over time because the world changes. Customer behaviour shifts, prices change, new patterns emerge. This is called **model drift** — and it's why models need to be retrained periodically, not just once.

---

## Quick Reference — Libraries

| Library | What it does |
|---|---|
| `pandas` | Load and manipulate tabular data (CSVs, DataFrames) |
| `numpy` | Fast numerical operations on arrays |
| `scikit-learn` | Classical ML models, preprocessing, evaluation metrics |
| `matplotlib` | Basic charts and plots |
| `joblib` | Save and load trained models |
| `mlflow` | Track experiments, log metrics, compare runs |

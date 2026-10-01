# Project Setup & Execution Guide

Welcome to the **HDB Resale Price Prediction & Streamlit Deployment** project! Follow these steps to run the code locally in VS Code and deploy your app to the cloud.

---

## Phase 1: Fork & Clone the Project

### Step 1: Fork the repository
1. Sign in to GitHub and go to: https://github.com/flexfengfeng/6m-data-c3.2-HDB_price_predictor
2. Click **Fork** (top right), then **Create fork**. You now have your own copy at `https://github.com/<your-username>/6m-data-c3.2-HDB_price_predictor`.

### Step 2: Clone to VS Code
1. On **your fork's** page, click the green **Code** button and copy the HTTPS URL.
2. Open **VS Code**.
3. Open the command palette (`Ctrl + Shift + P` on Windows, `Cmd + Shift + P` on Mac), type `Git: Clone`, and press Enter.
4. Paste the URL and choose a folder to save the project in.
5. When VS Code asks, click **Open**.

---

## Phase 2: Set Up Your Python Environment

### Step 1: Open the VS Code terminal
Press ``Ctrl + ` `` (backtick) on Windows or ``Cmd + ` `` on Mac.

### Step 2: Create the lesson environment
`environment.yml` describes the environment: Python 3.12 plus every package in `requirements-dev.txt`. This includes everything in `requirements.txt` (pandas, scikit-learn, Streamlit, ...) and the notebook tools. Versions are pinned so your model loads correctly on Streamlit Cloud later.

```bash
conda env create -f environment.yml
conda activate hdb_project
```

Your terminal prompt should now start with `(hdb_project)`.

### Step 3: Register the environment as a notebook kernel (one-time)
```bash
python -m ipykernel install --user --name hdb_project --display-name "Python (hdb_project)"
```

---

## Phase 3: Build and Compare the Models

### Step 1: Work through the notebook
1. Open `hdb_price_model.ipynb` in VS Code.
2. Click **Select Kernel** (top right), then **Jupyter Kernel** > **Python (hdb_project)**. You can also pick **Python Environments** > **hdb_project**.
3. Run the cells from top to bottom (**Run All** or `Shift + Enter` cell by cell). Read the explanations and discuss the questions.

The notebook takes about 1 to 2 minutes to run fully. Cross-validating the tree models is the slowest part.

### Step 2: Train the final model
```bash
python model.py
```

This trains all three models, prints a comparison table, and saves the best model:

```
Chosen model: Gradient Boosting (lowest cross-validated RMSE)
Saved models/hdb_price_model.joblib (0.7 MB) and models/model_card.json
```

---

## Phase 4: Run the Web App Locally

```bash
streamlit run app.py
```

Your browser opens at http://localhost:8501. Try:
- The **Predict a price** tab: pick a town, flat type, size, storey and lease year, then click **Predict resale price**.
- The **Model comparison** tab: see how the three models scored.

Press `Ctrl + C` in the terminal to stop the app.

---

## Phase 5: Push Your Changes to GitHub

Streamlit Cloud runs the code and model **from your GitHub repo**, so commit the trained model files too:

```bash
git add .
git commit -m "Train HDB price model"
git push
```

---

## Phase 6: Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and click **Continue with GitHub**.
2. Click **Create app** (top right), then choose to deploy from a GitHub repo.
3. Fill in:
   * **Repository:** your fork, e.g. `<your-username>/6m-data-c3.2-HDB_price_predictor`
   * **Branch:** `main`
   * **Main file path:** `app.py`
4. Open **Advanced settings** and set **Python version** to **3.12** (the same version you trained with).
5. Click **Deploy**. The first build takes a few minutes while packages install from `requirements.txt`.

You now have a public URL you can share!

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | Activate the environment (`conda activate hdb_project`). In the notebook, check the selected kernel is **Python (hdb_project)**. If packages are still missing, run `conda env update -f environment.yml --prune`. |
| `CondaValueError: prefix already exists` | The environment already exists. Run `conda activate hdb_project`, or remove it with `conda env remove -n hdb_project` and create it again. |
| App says **"No trained model found"** | Run `python model.py` first. On Streamlit Cloud, check `models/hdb_price_model.joblib` and `models/model_card.json` were pushed to GitHub. |
| Errors or warnings about scikit-learn versions when loading the model | The app is using a different scikit-learn version from the one you trained with. Keep the versions in `requirements.txt` pinned, then retrain and push. |
| You changed the features in `hdb_features.py` | Retrain with `python model.py`, update the inputs in `app.py`, then commit and push again. |

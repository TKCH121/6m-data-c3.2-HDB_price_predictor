# Singapore HDB Resale Price Predictor

Build a machine learning model that predicts the resale price of a Singapore HDB flat, then deploy it as a Streamlit web app.

You will train and compare three regression models, **Linear Regression**, **Random Forest** and **Gradient Boosting**, pick the best one with cross-validation, and put it online for anyone to use.

## What you will learn

- Turn raw columns into model features (for example, `"10 TO 12"` becomes storey `11`)
- One-hot encode text columns inside a scikit-learn `Pipeline`
- Train and explain three regression algorithms
- Evaluate models with MAE, RMSE and R², and compare them fairly with 5-fold cross-validation
- Weigh accuracy against model size, speed and interpretability when choosing a model to deploy
- Save a model, load it in a Streamlit app, and deploy the app to Streamlit Community Cloud

## Project structure

```
├── hdb_price_model.ipynb      # Teaching notebook: EDA, 3 models, comparison (start here)
├── hdb_features.py            # Shared feature engineering (used by training AND the app)
├── model.py                   # Script: trains all 3 models, picks the best, saves it
├── app.py                     # Streamlit web app
├── data/
│   └── hdb_resale_2017_2019.csv
├── models/
│   ├── hdb_price_model.joblib # Saved model (created by model.py)
│   └── model_card.json        # Scores for every model + metadata the app uses
├── requirements.txt           # Packages for training and the app (used by Streamlit Cloud)
├── requirements-dev.txt       # Adds notebook tools (matplotlib, seaborn, ipykernel)
└── setup.md                   # Step-by-step setup and deployment guide
```

## Workflow

1. **Explore and experiment** in `hdb_price_model.ipynb`.
2. **Train for real** with `python model.py`. It repeats the notebook's modelling steps, picks the model with the lowest cross-validated RMSE, and writes it to `models/`.
3. **Serve** with `streamlit run app.py`.
4. **Deploy** by pushing to GitHub and connecting the repo to Streamlit Community Cloud.

Full instructions: [setup.md](setup.md).

## Data

50,432 HDB resale transactions from **January 2017 to May 2019**, originally from [data.gov.sg](https://data.gov.sg) (via [this mirror](https://github.com/kohjiaxuan/Predicting-HDB-Price-with-Machine-Learning)). A copy is kept in `data/` so the project works offline.

Features used: `town`, `flat_type`, `floor_area_sqm`, `storey` (midpoint of `storey_range`), `lease_commence_date`. Target: `resale_price`.

## Results

Output of `python model.py` (80/20 train/test split, `random_state=42`):

| Model | CV RMSE (S$) | CV R² | Test MAE (S$) | Test RMSE (S$) | Test R² | File size |
|---|---|---|---|---|---|---|
| Linear Regression | 60,245 | 0.846 | 46,726 | 60,521 | 0.848 | < 0.1 MB |
| Random Forest | 36,661 | 0.943 | 25,096 | 35,624 | 0.947 | ~26 MB |
| **Gradient Boosting** (deployed) | **36,121** | **0.945** | 26,192 | 35,814 | 0.947 | ~0.7 MB |

Both tree models beat Linear Regression by a wide margin, because price depends on features in non-linear ways (for example, an extra square metre is worth more in some towns than others). Gradient Boosting has the lowest cross-validated RMSE, so it is deployed. It is also about 35 times smaller than the Random Forest. Random Forest has a slightly lower test MAE, which is a good reminder that we **choose with cross-validation, not the test set**.

For comparison, the original version of this project used Linear Regression on three numeric columns only (no town or flat type) and reached R² ≈ 0.54.

## Limitations

- Prices reflect the **2017 to 2019** market, not today's prices. See exercise 5 in the notebook to retrain on fresh data.
- The model ignores exact location within a town (block, distance to MRT, and so on), so similar-looking flats can differ from the estimate by tens of thousands of dollars.
- Very rare flat types (1 ROOM, MULTI-GENERATION) have few training examples, so predictions for them are less trustworthy.

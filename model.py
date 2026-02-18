import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("ai_job_replacement_2020_2026.csv")

# Drop unwanted column
if "job_id" in df.columns:
    df = df.drop("job_id", axis=1)

# Create target category
df["ai_replacement_category"] = pd.cut(
    df["ai_replacement_score"],
    bins=3,
    labels=["Low", "Medium", "High"]
)
df = df.drop("ai_replacement_score", axis=1)

# Features & Target
X = df.drop("ai_replacement_category", axis=1)
y = df["ai_replacement_category"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Identify Columns
cat_cols = ['job_role', 'industry', 'country']
num_cols = X.select_dtypes(include=['number']).columns

# Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", "passthrough", num_cols)
    ]
)

# Full Pipeline with SMOTE for balance
model = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("smote", SMOTE(random_state=42)),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train and Save
model.fit(X_train, y_train)
joblib.dump(model, "model.joblib", compress=3)


print("✅ Model trained and saved as model.joblib")
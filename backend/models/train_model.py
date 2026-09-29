import os, joblib, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from backend.config import Config
from backend.risk import risk_score, label

def train_model(n=4000, seed=42):
    rng = np.random.RandomState(seed)
    X = np.column_stack([rng.uniform(5, 200, n), rng.uniform(295, 335, n), rng.uniform(0.2, 0.95, n),
                         rng.uniform(0.1, 3.5, n), rng.randint(0, 4, n)])
    y = np.array([label(s) for s in risk_score(*X.T)])
    le = LabelEncoder(); ye = le.fit_transform(y)
    Xtr, Xte, ytr, yte = train_test_split(X, ye, test_size=0.2, random_state=seed, stratify=ye)
    clf = RandomForestClassifier(n_estimators=150, random_state=seed).fit(Xtr, ytr)
    print(f"Held-out accuracy vs rule-based labels: {clf.score(Xte, yte):.3f}")
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    joblib.dump({"model": clf, "encoder": le}, Config.MODEL_PATH)
    return clf, le

if __name__ == "__main__":
    train_model()

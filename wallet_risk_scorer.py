import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler

# === Step 1: Load Wallet IDs ===
wallet_df = pd.read_excel("Wallet id.xlsx")
wallet_df['wallet_id'] = wallet_df['wallet_id'].str.lower()

# === Step 2: Simulate Random Features for Each Wallet ===
np.random.seed(42)  # for reproducibility
n = len(wallet_df)

features = pd.DataFrame({
    "wallet": wallet_df['wallet_id'],
    "transaction_count": np.random.randint(10, 200, size=n),
    "deposit_total": np.random.uniform(500, 10000, size=n),
    "borrow_total": np.random.uniform(100, 5000, size=n),
    "repay_total": np.random.uniform(100, 5000, size=n),
    "redeem_total": np.random.uniform(100, 3000, size=n),
    "liquidation_count": np.random.randint(0, 3, size=n),
    "first_txn": [datetime(2021, 1, 1) + timedelta(days=np.random.randint(0, 300)) for _ in range(n)],
    "last_txn": [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 300)) for _ in range(n)],
})

# === Step 3: Feature Engineering ===
features["wallet_age_days"] = (features["last_txn"] - features["first_txn"]).dt.days + 1
features["repayment_ratio"] = features["repay_total"] / (features["borrow_total"] + 1e-6)
features["capital_ratio_proxy"] = (features["deposit_total"] + features["redeem_total"]) / (features["borrow_total"] + 1e-6)

# === Step 4: Score Calculation ===
scores = features.copy()

# 1. History Score
activity_features = np.log1p(scores[["wallet_age_days", "transaction_count"]])
scores["history_score"] = MinMaxScaler().fit_transform(activity_features).mean(axis=1)

# 2. Repayment Score
scores["repayment_score"] = scores["repayment_ratio"].clip(0, 1)

# 3. Liquidation Score
scores["liquidation_score"] = np.where(scores["liquidation_count"] > 0, 0, 1)

# 4. Capital Score (lower ratio is better here)
proxy_scaled = MinMaxScaler().fit_transform(scores[["capital_ratio_proxy"]])
scores["capital_score"] = 1 - proxy_scaled.flatten()

# Final Score Calculation
weights = {
    "history_score": 0.15,
    "repayment_score": 0.35,
    "liquidation_score": 0.40,
    "capital_score": 0.10
}

scores["final_score"] = (
    scores["history_score"] * weights["history_score"] +
    scores["repayment_score"] * weights["repayment_score"] +
    scores["liquidation_score"] * weights["liquidation_score"] +
    scores["capital_score"] * weights["capital_score"]
)

scores["final_score"] = (scores["final_score"] * 1000).astype(int)

# === Step 5: Save Output ===
scores[["wallet", "final_score"]].rename(columns={
    "wallet": "wallet_id",
    "final_score": "score"
}).to_csv("wallet_Risk.csv", index=False)

print("✅ Random wallet risk scores generated and saved to wallet_Risk.csv")

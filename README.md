
# 🛡️ Wallet Risk Scoring — Compound V2/V3 Inspired

This project calculates a **risk score (0–1000)** for DeFi wallet addresses based on on-chain behavioral indicators. It is tailored for wallets interacting with protocols like Compound V2/V3 or similar.

---

## 📁 Project Structure

```
├── Wallet id.xlsx                   # Input: Excel sheet with list of wallet addresses
├── user-wallet-transactions.json   # Input: On-chain transaction data (optional or simulated)
├── wallet_risk_scorer.py           # Main Python script for scoring
├── wallet_Risk.csv                 # Output: Final scores for all wallets
├── README.md                       # Project documentation (this file)
```

---

## 📦 Libraries Used

| Library         | Purpose                                      |
|----------------|----------------------------------------------|
| `pandas`        | DataFrame manipulation and Excel reading     |
| `numpy`         | Numerical computation                        |
| `datetime`      | Timestamp handling                           |
| `json`          | Parsing transaction data                     |
| `sklearn.preprocessing.MinMaxScaler` | Feature normalization   |

Install them via:

```bash
pip install pandas numpy scikit-learn openpyxl
```

---

## 🧠 Logic Overview

The script does the following:

1. **Reads wallet addresses** from `Wallet id.xlsx`.
2. If available, parses real transaction data (`user-wallet-transactions.json`).
3. If no real data is present, it **randomly generates synthetic transaction values** per wallet for simulation.
4. **Calculates features** such as deposits, borrows, repayments, liquidation counts, and wallet age.
5. **Normalizes** values using Min-Max scaling.
6. Combines the features into a **final risk score (0–1000)** using a weighted formula.

---

## ⚙️ Feature Engineering (Indicators Used)

For each wallet, the following features are generated (or simulated):

| Feature              | Description                                               |
|----------------------|-----------------------------------------------------------|
| `transaction_count`  | Number of transactions associated with the wallet         |
| `deposit_total`      | Total deposit volume in USD                               |
| `borrow_total`       | Total amount borrowed                                     |
| `repay_total`        | Amount repaid back on borrowed funds                      |
| `redeem_total`       | Assets withdrawn (redeemed)                               |
| `liquidation_count`  | Number of liquidation events                              |
| `wallet_age_days`    | Days between first and last transactions                  |
| `repayment_ratio`    | Ratio of repayments to borrowed amount                    |
| `capital_ratio_proxy`| Proxy metric for capital reliability                      |

---
## How Synthetic Values Are Generated ##
If user-wallet-transactions.json is missing or empty, the script simulates values for each wallet as follows:

transaction_count: Random integer between 10–100

wallet_age_days: Random integer between 30–720 days

deposit_total: Uniform float between $1,000–$20,000

borrow_total: Uniform float between $500–$10,000

repay_total: Between 60–100% of borrow_total (simulating responsible behavior)

redeem_total: Uniform float between $200–$5,000

liquidation_count: Random choice between 0 or 1 (with bias toward 0)

This allows testing the scoring model even without real blockchain data.

## 🧮 Scoring Formula

Each wallet gets a final score from 0 to 1000.

### Step 1: Normalize values
```python
np.log1p(transaction_count), wallet_age_days, repayment_ratio, etc.
```

### Step 2: Feature-specific scores

- `history_score`: based on log-scaled activity and age
- `repayment_score`: directly from `repayment_ratio`
- `liquidation_score`: 1 if no liquidations, else 0
- `capital_score`: normalized inverse of `capital_ratio_proxy`

### Step 3: Final weighted score
```python
final_score = (
    0.15 * history_score +
    0.35 * repayment_score +
    0.40 * liquidation_score +
    0.10 * capital_score
) * 1000
```

---

## 🧪 Output

The results are saved to:

```
wallet_Risk.csv
```

Sample Output:

| wallet_id                              | score |
|----------------------------------------|-------|
| 0x123...abc                            | 782   |
| 0x456...def                            | 643   |

---

## ✍️ Justification of Risk Indicators

- **Repayment Ratio**: Measures trustworthiness in borrowing. Higher = better.
- **Liquidation Count**: Indicates risky behavior. Any liquidation is penalized.
- **Wallet Age & Activity**: Shows protocol experience and consistency.
- **Capital Proxy Ratio**: Represents how well a wallet manages its collateral and borrowing.

---

## 🚀 How to Run

1. Place both `Wallet id.xlsx` and `user-wallet-transactions.json` (if available) in the same folder as `wallet_risk_scorer.py`.
2. Run:

```bash
python wallet_risk_scorer.py
```

3. Output will be saved to `wallet_Risk.csv`.

---

## 📌 Notes

- If real transaction data is missing, the script generates **realistic random transaction patterns** for demonstration.
- Designed to be extended to real blockchain API integrations (e.g., The Graph, Etherscan, etc.).

---

## 🧑‍💻 Author

Sandesh R. Birajdar  
[Email](mailto:sandeshbirajdar030@gmail.com)

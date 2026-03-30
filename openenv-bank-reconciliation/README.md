# Bank Reconciliation Environment

An OpenEnv-compliant AI training environment for reconciling Indian bank statements.

## Why This Environment?

Indian bank statements often contain cryptic UPI (Unified Payments Interface) transaction references that are difficult to parse:

- **UPI format**: `UPI-9182XXXX@paytm.okhdfc`
- **NEFT format**: `NEFT/123456/raun`
- **Merchant codes**: Short codes that need decoding

This environment trains AI agents to:
1. Categorize transactions (Food, Travel, Utilities, Shopping, Unknown)
2. Decode cryptic UPI references to identify merchants
3. Flag duplicates and anomalies in bank statements

## Observation Space

| Field | Type | Description |
|-------|------|-------------|
| transactions | List[Transaction] | Batch of 10 unresolved transactions |
| resolved_count | int | Number of transactions resolved so far |
| episode_step | int | Current step in the episode |
| context_hints | Dict[str, str] | Time/amount patterns from statement |

### Transaction Model
- `id`: Unique transaction ID
- `amount`: Transaction amount (INR)
- `merchant_raw`: Raw merchant string (e.g., "UPI-9182XXXX@paytm")
- `timestamp`: Transaction datetime
- `upi_ref`: UPI reference if applicable
- `account_type`: "debit" or "credit"

## Action Space

| Field | Type | Description |
|-------|------|-------------|
| transaction_id | str | ID of transaction to process |
| assigned_category | str | Category: Food, Travel, Utilities, Shopping, Unknown |
| merchant_label | str | Human-readable merchant name |
| flag_type | str | None, "duplicate", or "anomaly" |

## Tasks

### Task 1: Categorize (Easy)
- **Description**: Categorize 10 transactions with clear merchant names
- **Difficulty**: Easy
- **Grading**: Exact match of assigned_category to ground_truth
- **Expected Baseline**: TBD

### Task 2: Decode UPI (Medium)
- **Description**: Decode 10 cryptic UPI transaction IDs and assign merchant labels
- **Difficulty**: Medium
- **Grading**: Fuzzy string match between merchant_label and ground_truth
- **Expected Baseline**: TBD

### Task 3: Full Reconciliation (Hard)
- **Description**: Full reconciliation with 30 transactions, including 3 duplicates and 2 anomalies
- **Difficulty**: Hard
- **Grading**: 40% category accuracy + 30% duplicate detection + 30% anomaly detection
- **Expected Baseline**: TBD

## Running Locally

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run FastAPI Server
```bash
uvicorn api.main:app --host 0.0.0.0 --port 7860
```

### API Endpoints
- `GET /tasks` - List available tasks and action schema
- `POST /reset` - Reset environment with task type
- `POST /step` - Take an action
- `GET /state` - Get current state
- `POST /grader` - Grade completed episode
- `POST /baseline` - Run OpenAI baseline (requires OPENAI_API_KEY)

## Running with Docker

### Build
```bash
docker build -t bank-reconciliation-env .
```

### Run
```bash
docker run -p 7860:7860 bank-reconciliation-env
```

## Baseline Scores

| Task | gpt-4o-mini | Human (TBD) |
|------|-------------|-------------|
| categorize | TBD | TBD |
| decode_upi | TBD | TBD |
| full_reconciliation | TBD | TBD |

## Environment Details

- **Max steps per episode**: 60
- **Batch size**: 10 transactions
- **Random seed**: 42 (for reproducibility)
- **No real bank data**: All data is synthetic using Faker

## Supported Merchants

| Merchant | Category |
|----------|----------|
| SWIGGY | Food |
| ZOMATO | Food |
| IRCTC | Travel |
| AMAZON | Shopping |
| FLIPKART | Shopping |
| NETFLIX | Utilities |
| BESCOM | Utilities |
| BBNL | Utilities |
| PHONEPE | Unknown |
| PAYTM | Unknown |

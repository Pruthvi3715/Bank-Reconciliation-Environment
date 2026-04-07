import random
import uuid
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict
from faker import Faker

from .models import Transaction, MERCHANT_CATEGORIES

fake = Faker()
Faker.seed(42)
random.seed(42)

MERCHANTS = list(MERCHANT_CATEGORIES.keys())
BANKS = ["hdfc", "icici", "sbi", "axis", "kotak", "yesbank"]
UPI_SUFFIXES = ["oksbi", "okhdfc", "okicici", "okaxis", "okkotak"]


def generate_upi_ref(merchant: str) -> str:
    format_type = random.choice(["numeric", "merchant_code", "neft"])

    if format_type == "numeric":
        number = "".join([str(random.randint(0, 9)) for _ in range(10)])
        bank = random.choice(BANKS)
        suffix = random.choice(UPI_SUFFIXES)
        return f"UPI-{number}@{bank}.{suffix}"

    elif format_type == "merchant_code":
        code = (
            merchant[:4].lower()
            if random.random() > 0.5
            else f"m{random.randint(1000, 9999)}"
        )
        bank = random.choice(BANKS)
        suffix = random.choice(UPI_SUFFIXES)
        return f"UPI-{code}@{bank}.{suffix}"

    else:
        ref = f"NEFT/{random.randint(100000, 999999)}"
        partial_name = fake.first_name().lower()[:4]
        return f"{ref}/{partial_name}"


def generate_amount(merchant: str, is_anomaly: bool = False) -> float:
    base_amounts = {
        "SWIGGY": (80, 600),
        "ZOMATO": (100, 800),
        "IRCTC": (50, 3000),
        "AMAZON": (200, 5000),
        "FLIPKART": (150, 4000),
        "NETFLIX": (399, 799),
        "BESCOM": (200, 2000),
        "BBNL": (300, 1500),
        "PHONEPE": (50, 1000),
        "PAYTM": (50, 2000),
    }

    min_amt, max_amt = base_amounts.get(merchant, (100, 1000))
    amount = random.uniform(min_amt, max_amt)

    if is_anomaly:
        amount *= 10

    return round(amount, 2)


def generate_clear_transaction(seed: int) -> Tuple[Transaction, str, str]:
    random.seed(seed)
    fake.seed_instance(seed)

    merchant = random.choice(MERCHANTS)
    category = MERCHANT_CATEGORIES[merchant]
    amount = generate_amount(merchant)

    transaction = Transaction(
        id=str(uuid.uuid4()),
        amount=amount,
        merchant_raw=merchant,
        timestamp=datetime.now() - timedelta(days=random.randint(0, 30)),
        upi_ref=None,
        account_type=random.choice(["debit", "credit"]),
    )

    return transaction, category, merchant


def generate_upi_transaction(seed: int) -> Tuple[Transaction, str, str]:
    random.seed(seed)
    fake.seed_instance(seed)

    merchant = random.choice(MERCHANTS)
    category = MERCHANT_CATEGORIES[merchant]
    amount = generate_amount(merchant)
    upi_ref = generate_upi_ref(merchant)

    transaction = Transaction(
        id=str(uuid.uuid4()),
        amount=amount,
        merchant_raw=upi_ref,
        timestamp=datetime.now() - timedelta(days=random.randint(0, 30)),
        upi_ref=upi_ref,
        account_type=random.choice(["debit", "credit"]),
    )

    return transaction, category, merchant


def generate_mixed_transaction(
    seed: int, is_upi: bool = True
) -> Tuple[Transaction, str, str]:
    if is_upi:
        return generate_upi_transaction(seed)
    return generate_clear_transaction(seed)


def generate_full_statement(
    num_transactions: int = 30,
    seed: int = 42,
    inject_duplicates: int = 3,
    inject_anomalies: int = 2,
    clear_only: bool = False,
) -> Tuple[
    List[Transaction], Dict[str, str], Dict[str, str], List[Tuple[str, str]], List[str]
]:
    random.seed(seed)
    fake.seed_instance(seed)

    transactions = []
    ground_truth_categories = {}
    ground_truth_merchants = {}
    duplicates = []
    anomalies = []

    if clear_only:
        num_clear = num_transactions
        num_upi = 0
    else:
        num_clear = num_transactions // 3
        num_upi = num_transactions - num_clear

    for i in range(num_clear):
        transaction, category, merchant = generate_clear_transaction(seed + i)
        transactions.append(transaction)
        ground_truth_categories[transaction.id] = category
        ground_truth_merchants[transaction.id] = merchant

    for i in range(num_upi):
        transaction, category, merchant = generate_upi_transaction(seed + num_clear + i)
        transactions.append(transaction)
        ground_truth_categories[transaction.id] = category
        ground_truth_merchants[transaction.id] = merchant

    if inject_duplicates > 0 and len(transactions) >= 4:
        available_indices = list(range(len(transactions)))
        for _ in range(inject_duplicates):
            if len(available_indices) < 2:
                break
            idx1, idx2 = random.sample(available_indices, 2)
            available_indices.remove(idx1)
            available_indices.remove(idx2)

            dup_transaction = Transaction(
                id=str(uuid.uuid4()),
                amount=transactions[idx1].amount,
                merchant_raw=transactions[idx1].merchant_raw,
                timestamp=transactions[idx1].timestamp
                + timedelta(hours=random.randint(1, 12)),
                upi_ref=transactions[idx1].upi_ref,
                account_type=transactions[idx1].account_type,
            )
            transactions.append(dup_transaction)
            ground_truth_categories[dup_transaction.id] = ground_truth_categories[
                transactions[idx1].id
            ]
            ground_truth_merchants[dup_transaction.id] = ground_truth_merchants[
                transactions[idx1].id
            ]
            duplicates.append((transactions[idx1].id, dup_transaction.id))

    if inject_anomalies > 0:
        for _ in range(inject_anomalies):
            if not transactions:
                break
            idx = random.randint(0, len(transactions) - 1)
            original = transactions[idx]

            anomaly_transaction = Transaction(
                id=str(uuid.uuid4()),
                amount=original.amount * 10,
                merchant_raw=original.merchant_raw,
                timestamp=original.timestamp + timedelta(days=1),
                upi_ref=original.upi_ref,
                account_type=original.account_type,
            )
            transactions.append(anomaly_transaction)
            ground_truth_categories[anomaly_transaction.id] = ground_truth_categories[
                original.id
            ]
            ground_truth_merchants[anomaly_transaction.id] = ground_truth_merchants[
                original.id
            ]
            anomalies.append(anomaly_transaction.id)

    random.shuffle(transactions)

    return (
        transactions,
        ground_truth_categories,
        ground_truth_merchants,
        duplicates,
        anomalies,
    )


def get_context_hints(transactions: List[Transaction]) -> dict:
    if not transactions:
        return {}

    amounts = [t.amount for t in transactions]
    merchants = [
        t.merchant_raw
        for t in transactions
        if not t.merchant_raw.startswith("UPI")
        and not t.merchant_raw.startswith("NEFT")
    ]

    hints = {}
    if amounts:
        hints["avg_amount"] = str(round(sum(amounts) / len(amounts), 2))
        hints["max_amount"] = str(max(amounts))
        hints["min_amount"] = str(min(amounts))

    if merchants:
        most_common = max(set(merchants), key=merchants.count)
        hints["common_merchant"] = most_common

    return hints

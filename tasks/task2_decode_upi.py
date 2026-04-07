from env import BankReconciliationEnv, grade_task


class Task2DecodeUpi:
    """Medium: Decode 10 cryptic UPI transaction IDs and assign merchant labels."""

    name = "decode_upi"
    description = "Decode 10 cryptic UPI transaction IDs and assign merchant labels"
    difficulty = "medium"
    expected_score = "TBD"

    def __init__(self, seed: int = 42):
        self.env = BankReconciliationEnv(seed=seed)

    def reset(self):
        return self.env.reset(seed=self.env._seed, task_type="decode_upi")

    def step(self, action):
        return self.env.step(action)

    def grade(self):
        return grade_task(
            self.name,
            self.env.state.resolved_transactions,
            self.env.state,
        )

    def get_info(self):
        return {
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty,
            "action_schema": {
                "transaction_id": "str",
                "assigned_category": "Food | Travel | Utilities | Shopping | Unknown",
                "merchant_label": "str (decoded merchant name)",
                "flag_type": "None",
            },
        }

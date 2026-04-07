from env import BankReconciliationEnv, grade_task


class Task1Categorize:
    """Easy: Categorize 10 transactions with clear merchant names."""

    name = "categorize"
    description = "Categorize 10 transactions that all have clear merchant names"
    difficulty = "easy"
    expected_score = "TBD"

    def __init__(self, seed: int = 42):
        self.env = BankReconciliationEnv(seed=seed)

    def reset(self):
        return self.env.reset(seed=self.env._seed, task_type="categorize")

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
                "merchant_label": "str (human readable name)",
                "flag_type": "None",
            },
        }

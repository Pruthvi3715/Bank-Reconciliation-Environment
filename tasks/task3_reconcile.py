from env import BankReconciliationEnv, grade_task


class Task3Reconcile:
    """Hard: Full reconciliation - categorize + decode + flag duplicates and anomalies."""

    name = "full_reconciliation"
    description = (
        "Full reconciliation: categorize + decode + flag 3 duplicates "
        "and 2 anomalies hidden in 30 transactions"
    )
    difficulty = "hard"
    expected_score = "TBD"

    def __init__(self, seed: int = 42):
        self.env = BankReconciliationEnv(seed=seed)

    def reset(self):
        return self.env.reset(seed=self.env._seed, task_type="full")

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
                "merchant_label": "str",
                "flag_type": "None | duplicate | anomaly",
            },
        }

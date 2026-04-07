"""Run baseline and save results to a file."""
import json
from baseline.inference import run_all_tasks

results = run_all_tasks()

print("\n=== FINAL RESULTS ===")
for task, result in results.items():
    print(f"{task}: score={result['score']}, "
          f"resolved={result['resolved']}/{result['total']}, "
          f"steps={result['steps']}")

with open("baseline_results.json", "w") as f:
    json.dump(results, f, indent=2)
    print("\nResults saved to baseline_results.json")

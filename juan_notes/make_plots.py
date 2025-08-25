import json
import csv
from pathlib import Path

# where your results live
results_dir = Path("../results")
output_csv = Path("../results/results_summary.csv")

rows = []

for json_file in results_dir.rglob("*.json"):
    with open(json_file, "r") as f:
        data = json.load(f)

    params = data.get("params", {})
    results = data.get("results", {})

    # detect type (upload vs search) from filename
    if "upload" in json_file.name:
        row = {
            "dataset": params.get("dataset"),
            "engine": params.get("engine"),
            "experiment": params.get("experiment"),
            "type": "upload",
            "parallel": params.get("parallel"),
            "upload_time": results.get("upload_time"),
            "total_time": results.get("total_time"),
        }
    else:  # search
        row = {
            "dataset": params.get("dataset"),
            "engine": params.get("engine"),
            "experiment": params.get("experiment"),
            "type": "search",
            "parallel": params.get("parallel"),
            "mean_time": results.get("mean_time"),
            "p95_time": results.get("p95_time"),
            "p99_time": results.get("p99_time"),
            "rps": results.get("rps"),
            "mean_precisions": results.get("mean_precisions"),
            "total_time": results.get("total_time"),
        }

    row["file"] = str(json_file.relative_to(results_dir))
    rows.append(row)

# write to CSV
fieldnames = sorted({k for row in rows for k in row.keys()})
with open(output_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote summary to {output_csv}")

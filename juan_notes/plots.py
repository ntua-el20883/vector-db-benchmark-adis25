import pandas as pd
import matplotlib.pyplot as plt

# Load results summary
csv_path = "./results/results_summary.csv"
df = pd.read_csv(csv_path)

# Convert times from seconds to ms where appropriate
df["mean_time_ms"] = df["mean_time"] * 1000
df["p95_time_ms"] = df["p95_time"] * 1000

def show_table(dataset):
    subset = df[df["dataset"] == dataset][
        ["dataset", "engine", "type", "upload_time", "mean_time_ms", "p95_time_ms", "rps", "mean_precisions"]
    ]
    print(subset.to_string(index=False))

# Example: show glove-100-angular comparison
show_table("glove-100-angular")

# --- Visualization ---

# 1. Upload times comparison
upload = df[df["type"] == "upload"]
plt.figure(figsize=(10,5))
for dataset in upload["dataset"].unique():
    subset = upload[upload["dataset"] == dataset]
    plt.bar([f"{dataset}\n{engine}" for engine in subset["engine"]], subset["upload_time"])
plt.ylabel("Upload Time (s)")
plt.title("Upload Times by Dataset and Engine")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 2. Mean query latency comparison
search = df[df["type"] == "search"]
plt.figure(figsize=(10,5))
for dataset in search["dataset"].unique():
    subset = search[search["dataset"] == dataset]
    plt.bar([f"{dataset}\n{engine}" for engine in subset["engine"]], subset["mean_time_ms"])
plt.ylabel("Mean Latency (ms)")
plt.title("Query Latency by Dataset and Engine")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 3. Throughput vs accuracy scatter
plt.figure(figsize=(8,6))
for engine in search["engine"].unique():
    subset = search[search["engine"] == engine]
    plt.scatter(subset["rps"], subset["mean_precisions"], label=engine)
plt.xlabel("Queries per second (RPS)")
plt.ylabel("Mean Precision")
plt.title("Throughput vs Accuracy")
plt.legend()
plt.grid(True)
plt.show()

# Save cleaned summary for LaTeX/Markdown tables
df.to_csv("./results/results_summary_clean.csv", index=False)


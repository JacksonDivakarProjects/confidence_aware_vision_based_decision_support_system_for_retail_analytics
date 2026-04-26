import matplotlib.pyplot as plt
import numpy as np

metrics = ["Flip Rate", "Stability Score"]
baseline = [12, 0.977]
confidence = [12, 0.977]

x = np.arange(len(metrics))
width = 0.35

plt.figure(figsize=(4.5, 3))

plt.bar(x - width/2, baseline, width, label="Baseline")
plt.bar(x + width/2, confidence, width, label="Confidence-Aware")

plt.xticks(x, metrics)
plt.ylabel("Value")
plt.legend(frameon=False)

plt.tight_layout()
plt.savefig("fig3_decision_metrics.png", dpi=300)
plt.close()

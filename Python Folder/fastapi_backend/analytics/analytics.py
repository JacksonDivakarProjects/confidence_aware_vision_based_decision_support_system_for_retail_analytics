import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pymysql
import warnings

# =========================
# SUPPRESS WARNING (clean)
# =========================
warnings.filterwarnings("ignore", category=UserWarning)

# ==================================================
# GLOBAL CONFIDENCE SETTINGS
# ==================================================

CONFIDENCE_POWER = 1.0
CONFIDENCE_MIN = 0.5


def safe_float(x, default=0.0):
    if x is None or not np.isfinite(x):
        return default
    return float(x)

# ==================================================
# DATA LOADING (pymysql only)
# ==================================================

def load_data():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="53787",
        database="age_gender_db"
    )

    query = """
        SELECT
            face_uid,
            gender,
            age_range,
            confidence,
            first_seen,
            last_seen
        FROM person_detection
    """

    df = pd.read_sql(query, conn)
    conn.close()

    df["first_seen"] = pd.to_datetime(df["first_seen"])
    df["last_seen"] = pd.to_datetime(df["last_seen"])

    df["session_seconds"] = (
        df["last_seen"] - df["first_seen"]
    ).dt.total_seconds()

    df["hour"] = df["first_seen"].dt.hour
    df["date"] = df["first_seen"].dt.date

    # FIX: remove deprecated warning
    df["time_bucket"] = df["first_seen"].dt.floor("1min")

    return df

# ==================================================
# BASELINE ANALYTICS
# ==================================================

def compute_kpis_baseline(df):
    daily = df.groupby("time_bucket")["face_uid"].nunique().sort_index()

    decisions = (daily > daily.mean()).astype(int)
    transitions = decisions.iloc[1:] != decisions.iloc[:-1].values
    flip_rate = int(transitions.sum())

    stability = 1 - flip_rate / max(len(decisions) - 1, 1)

    return {
        "total_footfall": int(df["face_uid"].nunique()),
        "decision_flip_rate": flip_rate,
        "avg_daily_footfall": round(safe_float(daily.mean()), 2),
        "avg_session_seconds": round(safe_float(df["session_seconds"].mean()), 2),
        "daily_variance": round(safe_float(daily.var()), 2),
        "stability_score": round(safe_float(stability), 3),
        "num_days": int(len(daily))
    }

# ==================================================
# CONFIDENCE ANALYTICS
# ==================================================

def compute_kpis_confidence(df):
    daily_count = df.groupby("time_bucket")["face_uid"].nunique().sort_index()
    daily_conf = df.groupby("time_bucket")["confidence"].mean().clip(lower=CONFIDENCE_MIN)

    mean_conf = safe_float(daily_conf.mean(), 1.0)
    effective_signal = daily_count * (daily_conf ** CONFIDENCE_POWER)

    decisions = (effective_signal > effective_signal.mean()).astype(int)
    transitions = decisions.iloc[1:] != decisions.iloc[:-1].values
    flip_rate = int(transitions.sum())

    stability = 1 - flip_rate / max(len(decisions) - 1, 1)

    return {
        "avg_session_seconds": round(df["session_seconds"].mean(), 2),
        "decision_flip_rate": flip_rate,
        "num_days": int(len(effective_signal)),
        "total_footfall_weighted": round(safe_float(effective_signal.sum() / mean_conf), 2),
        "avg_daily_footfall_weighted": round(safe_float(effective_signal.mean() / mean_conf), 2),
        "daily_variance_weighted": round(safe_float(effective_signal.var() / (mean_conf ** 2)), 2),
        "stability_score": round(safe_float(stability), 3),
    }

# ==================================================
# TREND
# ==================================================

def compute_trend(df):
    daily = (
        df.groupby("time_bucket")["face_uid"]
        .nunique()
        .reset_index(name="visitors")
        .sort_values("time_bucket")
    )

    daily["time_index"] = np.arange(len(daily))

    model = LinearRegression().fit(daily[["time_index"]], daily["visitors"])
    slope = float(model.coef_[0])

    return {
        "slope": round(slope, 4),
        "interpretation": (
            "Stable demand" if abs(slope) < 0.1
            else "Increasing demand" if slope > 0
            else "Decreasing demand"
        )
    }

# ==================================================
# MASTER (FRONTEND-COMPATIBLE KEYS)
# ==================================================

def compute_all_insights():
    df = load_data()

    return {
        "baseline": compute_kpis_baseline(df),
        "confidence_aware": compute_kpis_confidence(df),
        "trend": compute_trend(df)
    }

# ==================================================
# DEBUG
# ==================================================

if __name__ == "__main__":
    results = compute_all_insights()

    print("\n=== DEBUG STRUCTURE ===")
    print(results)

    print("\n=== BASELINE ===")
    for k, v in results.get("baseline", {}).items():
        print(f"{k}: {v}")

    print("\n=== CONFIDENCE ===")
    for k, v in results.get("confidence_aware", {}).items():
        print(f"{k}: {v}")

    print("\n=== TREND ===")
    for k, v in results.get("trend", {}).items():
        print(f"{k}: {v}")
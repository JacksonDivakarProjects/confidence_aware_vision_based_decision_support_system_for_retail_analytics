import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pymysql
# --------------------------------------------------
# DATA LOADING & PREPARATION
# --------------------------------------------------










def load_data(path="data/footfall.csv"):
    """
    Loads footfall session-level data and prepares derived columns.
    """
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

    # Convert timestamps
    df["first_seen"] = pd.to_datetime(df["first_seen"])
    df["last_seen"] = pd.to_datetime(df["last_seen"])

    # Derived columns
    df["session_seconds"] = (
        df["last_seen"] - df["first_seen"]
    ).dt.total_seconds()

    df["hour"] = df["first_seen"].dt.hour
    df["date"] = df["first_seen"].dt.date

    return df


# --------------------------------------------------
# KPI INSIGHTS
# --------------------------------------------------

def compute_kpis(df):
    """
    Core KPIs for dashboard
    """
    total_visitors = df["face_uid"].nunique()

    avg_session = df["session_seconds"].mean()

    daily_counts = df.groupby("date")["face_uid"].nunique()
    avg_daily_footfall = daily_counts.mean()

    peak_hour_series = df.groupby("hour")["face_uid"].nunique()
    peak_hour = int(peak_hour_series.idxmax())
    peak_hour_footfall = int(peak_hour_series.max())

    return {
        "total_visitors": int(total_visitors),
        "avg_daily_footfall": round(avg_daily_footfall, 2),
        "avg_session_seconds": round(avg_session, 2),
        "peak_hour": peak_hour,
        "peak_hour_footfall": peak_hour_footfall
    }


# --------------------------------------------------
# DEMOGRAPHIC INSIGHTS
# --------------------------------------------------

def compute_demographics(df):
    """
    Age and gender distribution
    """
    age_dist = (
        df.groupby("age_range")["face_uid"]
        .nunique()
        .sort_values(ascending=False)
    )

    gender_dist = (
        df.groupby("gender")["face_uid"]
        .nunique()
    )

    age_pct = (age_dist / age_dist.sum() * 100).round(2).to_dict()
    gender_pct = (gender_dist / gender_dist.sum() * 100).round(2).to_dict()

    top_age_group = age_dist.idxmax()

    return {
        "top_age_group": top_age_group,
        "age_distribution_pct": age_pct,
        "gender_distribution_pct": gender_pct
    }


# --------------------------------------------------
# ENGAGEMENT INSIGHT (DWELL TIME)
# --------------------------------------------------

def compute_engagement(df):
    """
    Average dwell time by age group
    """
    dwell_by_age = (
        df.groupby("age_range")["session_seconds"]
        .mean()
        .round(2)
        .to_dict()
    )

    return {
        "avg_dwell_time_by_age": dwell_by_age
    }


# --------------------------------------------------
# PARETO INSIGHT (80–20 RULE)
# --------------------------------------------------

def compute_pareto(df):
    """
    Identifies how many hours contribute to 80% of footfall
    """
    hourly_counts = (
        df.groupby("hour")["face_uid"]
        .nunique()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    hourly_counts["cum_pct"] = (
        hourly_counts["count"].cumsum()
        / hourly_counts["count"].sum()
        * 100
    )

    top_hours = hourly_counts[hourly_counts["cum_pct"] <= 80]
    top_hours_pct = len(top_hours) / len(hourly_counts) * 100

    return {
        "top_hours_percentage": round(top_hours_pct, 2),
        "footfall_contribution_pct": 80
    }


# --------------------------------------------------
# TREND ESTIMATION (LINEAR REGRESSION)
# --------------------------------------------------

def compute_trend(df):
    """
    Long-term demand trend using linear regression
    """
    daily = (
        df.groupby("date")["face_uid"]
        .nunique()
        .reset_index(name="visitors")
    )

    daily["time_index"] = np.arange(len(daily))

    X = daily[["time_index"]]
    y = daily["visitors"]

    model = LinearRegression()
    model.fit(X, y)

    slope = float(model.coef_[0])

    if abs(slope) < 0.1:
        interpretation = "Stable demand"
    elif slope > 0:
        interpretation = "Increasing demand"
    else:
        interpretation = "Decreasing demand"

    return {
        "slope": round(slope, 4),
        "interpretation": interpretation
    }


# --------------------------------------------------
# VOLATILITY INSIGHT
# --------------------------------------------------

def compute_volatility(df):
    """
    Measures demand stability using coefficient of variation
    """
    daily_counts = df.groupby("date")["face_uid"].nunique()

    mean = daily_counts.mean()
    std = daily_counts.std()

    cv = std / mean if mean > 0 else 0

    return {
        "coefficient_of_variation": round(cv, 3),
        "stability": "Stable" if cv < 0.5 else "Volatile"
    }


# --------------------------------------------------
# MASTER FUNCTION (FOR FASTAPI)
# --------------------------------------------------

def compute_all_insights(path="data/footfall.csv"):
    """
    Single call used by FastAPI
    """
    df = load_data(path)

    return {
        "kpis": compute_kpis(df),
        "demographics": compute_demographics(df),
        "engagement": compute_engagement(df),
        "pareto": compute_pareto(df),
        "trend": compute_trend(df),
        "volatility": compute_volatility(df)
    }

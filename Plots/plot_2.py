
import pymysql
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

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
    df["time_bucket"] = df["first_seen"].dt.floor("1T")
    return df

df= load_data()
print(df.head())

# df is your dataframe
df["time_bucket"] = pd.to_datetime(df["time_bucket"])

# Aggregate footfall per time bucket
agg = (
    df.groupby("time_bucket")["face_uid"]
    .nunique()
    .reset_index(name="footfall")
    .sort_values("time_bucket")
)

# Create time index for regression
agg["time_index"] = np.arange(len(agg))


plt.figure(figsize=(5, 3))

plt.hist(
    agg["footfall"],
    bins=10,
    edgecolor="black"
)

plt.yscale("log")

plt.xlabel("Footfall Count per Time Bucket")
plt.ylabel("Frequency (log scale)")

plt.tight_layout()
plt.savefig("fig4_footfall_distribution.png", dpi=300)
plt.close()

from fastapi import FastAPI
from analytics.analytics import compute_all_insights
from fastapi.middleware.cors import CORSMiddleware


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

DATA_PATH = r"C:\Users\Admin\Documents\Project Folder\Python Folder\fastapi_backend\synthetic_data\face_analytics_small_data.csv"

# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------



from analytics.analytics import compute_all_insights
from llm_recommendor.llm_recommendor import call_llm_recommendation







app = FastAPI(
    title="Retail Footfall Analytics API",
    description="Exposes aggregated footfall insights for frontend consumption",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Retail Footfall Analytics API is live"
    }


@app.post("/recommendations/chat")
def chat_recommendation(question: str):
    """
    Chat-style recommendation endpoint
    """
    insights = compute_all_insights(DATA_PATH)

    # Only pass SAFE aggregated fields
    llm_context = {
        "kpis": insights["kpis"],
        "pareto": insights["pareto"],
        "trend": insights["trend"],
        "demographics": insights["demographics"],
        "engagement": insights["engagement"]
    }

    answer = call_llm_recommendation(llm_context, question)

    return {
        "question": question,
        "recommendation": answer
    }


@app.get("/insights")
def get_all_insights():
    """
    Returns all computed insights as a single response.
    """
    return compute_all_insights(DATA_PATH)


@app.get("/insights/kpis")
def get_kpis():
    return compute_all_insights(DATA_PATH)["kpis"]


@app.get("/insights/demographics")
def get_demographics():
    return compute_all_insights(DATA_PATH)["demographics"]


@app.get("/insights/engagement")
def get_engagement():
    return compute_all_insights(DATA_PATH)["engagement"]


@app.get("/insights/pareto")
def get_pareto():
    return compute_all_insights(DATA_PATH)["pareto"]


@app.get("/insights/trend")
def get_trend():
    return compute_all_insights(DATA_PATH)["trend"]


@app.get("/insights/volatility")
def get_volatility():
    return compute_all_insights(DATA_PATH)["volatility"]



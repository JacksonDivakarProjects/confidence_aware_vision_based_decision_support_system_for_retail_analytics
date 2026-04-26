from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from analytics.analytics import compute_all_insights
from llm_recommendor.llm_recommendor import call_llm_recommendation


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="Retail Footfall Analytics API",
    description="Confidence-aware retail decision support API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "Retail Footfall Analytics API is live"
    }


# --------------------------------------------------
# CORE INSIGHTS
# --------------------------------------------------

def get_insights():
    return compute_all_insights()


# --------------------------------------------------
# INSIGHTS ENDPOINTS (FIXED KEYS)
# --------------------------------------------------

@app.get("/insights")
def get_all_insights():
    return get_insights()


@app.get("/insights/baseline")
def get_baseline_insights():
    return get_insights().get("baseline", {})


@app.get("/insights/confidence")
def get_confidence_insights():
    return get_insights().get("confidence_aware", {})


@app.get("/insights/trend")
def get_trend():
    return get_insights().get("trend", {})


# --------------------------------------------------
# LLM RECOMMENDATION (FIXED STRUCTURE)
# --------------------------------------------------

@app.post("/recommendations/chat")
def chat_recommendation(question: str):

    insights = get_insights()

    llm_context = {
        "baseline_kpis": insights.get("baseline", {}),
        "confidence_kpis": insights.get("confidence_aware", {}),
        "trend": insights.get("trend", {})
    }

    answer = call_llm_recommendation(llm_context, question)

    return {
        "question": question,
        "baseline_kpis": llm_context["baseline_kpis"],
        "confidence_kpis": llm_context["confidence_kpis"],
        "trend": llm_context["trend"],
        "recommendation": answer
    }
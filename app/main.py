from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(
    title="AI Adaptive Diagnostic Engine",
    description="Adaptive testing system that adjusts question difficulty based on student performance",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/")
def root():
    """
    Root endpoint with API information.
    """
    return {
        "message": "AI Adaptive Diagnostic Engine",
        "version": "1.0.0",
        "endpoints": {
            "start_session": "POST /start-session",
            "next_question": "GET /next-question/{session_id}",
            "submit_answer": "POST /submit-answer",
            "generate_plan": "POST /generate-plan",
            "get_session": "GET /session/{session_id}"
        }
    }

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

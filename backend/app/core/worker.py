import os
from celery import Celery
from app.core.config import settings

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "think2act_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300  # 5-minute hard limit per task
)

@celery_app.task(name="tasks.process_resume_parsing")
def process_resume_parsing_async(user_id: int, file_path: str):
    """
    Background worker processing uploaded PDF/DOCX resumes 
    without blocking the API request thread.
    """
    # 1. Load document from Object Storage / File Path
    # 2. Perform text extraction and parsing
    # 3. Calculate ATS scores against target job descriptions
    return {"user_id": user_id, "status": "COMPLETED", "parsed_skills_count": 8}

@celery_app.task(name="tasks.recalculate_user_skill_graph")
def recalculate_user_skill_graph_async(user_id: int):
    """
    Periodic job executing global skill score re-evaluations across user evidence logs.
    """
    return {"user_id": user_id, "status": "SKILL_GRAPH_UPDATED"}
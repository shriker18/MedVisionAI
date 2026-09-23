from fastapi import APIRouter, HTTPException

from app.services.database import get_analyses, get_analysis


router = APIRouter()


@router.get("/")
def history():
    return {
        "analyses": get_analyses()
    }


@router.get("/{analysis_id}")
def analysis_history(analysis_id: int):
    result = get_analysis(analysis_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    return result
from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.config import ALLOWED_IMAGE_TYPES, MAX_FILE_SIZE_MB
from app.services.image_validation import validate_image
from app.services.vision import vision_service
from app.services.database import save_analysis

router = APIRouter()


@router.post("/image")
async def analyze_image(
    file: UploadFile = File(...),
    question: str | None = None,
):

    # Check the declared content type
    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="Missing content type."
        )

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image type."
        )

    image_bytes = await file.read()

    try:
        # Verify that the uploaded bytes contain a valid image
        metadata = validate_image(
            image_bytes,
            MAX_FILE_SIZE_MB,
        )

        # Send the validated image to MedGemma
        raw_analysis = vision_service.analyze(
            image_bytes,
            question,
        )
        analysis_id = save_analysis(
    filename=file.filename,
    metadata=metadata,
    model="google/medgemma-1.5-4b-it",
    question=question,
    analysis=raw_analysis,
)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {exc}",
        )

    return {
    "id": analysis_id,
    "filename": file.filename,
    "metadata": metadata,
    "model": "google/medgemma-1.5-4b-it",
    "question": question,
    "analysis": raw_analysis,
    "limitations": [
        "AI-generated output.",
        "Not a medical diagnosis.",
        "Requires qualified clinical review.",
    ],
}
    
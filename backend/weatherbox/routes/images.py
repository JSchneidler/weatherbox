from typing import Literal, Optional
import io

from fastapi import APIRouter, Query, Path
from fastapi.responses import StreamingResponse
from sqlmodel import col, func, select
from PIL import Image

from weatherbox.db import get_session
from weatherbox.models import TimelapseImage
from weatherbox.timelapse import IMAGE_DIR

router = APIRouter()


@router.get("")
def get_images(
    page: int = Query(1, description="Page number for pagination"),
    limit: int = Query(10, description="Number of evenly spaced data points to return"),
    start_date: Optional[str] = Query(
        None, description="Start date in ISO format (e.g., 2024-01-01T00:00:00Z)"
    ),
    end_date: Optional[str] = Query(
        None, description="Start date in ISO format (e.g., 2024-01-01T00:00:00Z)"
    ),
):
    """
    Get the list of images captured by the camera.
    """
    base_query = select(TimelapseImage)

    if start_date:
        base_query = base_query.where(TimelapseImage.timestamp >= start_date)
    if end_date:
        base_query = base_query.where(TimelapseImage.timestamp <= end_date)

    session = get_session()

    # Get the total count to calculate sampling interval
    count_query = select(func.count(col(TimelapseImage.id))).select_from(TimelapseImage)
    if base_query.whereclause is not None:
        count_query = count_query.where(base_query.whereclause)
    total_count = session.exec(count_query).all()[0]

    query = base_query.offset((page - 1) * limit).limit(limit)
    images = session.exec(query).all()

    return {
        "total_count": total_count,
        "total_pages": (total_count + limit - 1) // limit,  # Ceiling division
        "page": page,
        "limit": limit,
        "images": images,
    }


@router.get("/{image_id}")
def get_image(
    image_id: int = Path(..., description="The ID of the image to get"),
    size: Literal["small", "medium", "large"] = Query(
        "small", description="Size of the image to return (small, medium, large)"
    ),
    format: Literal["jpeg", "png"] = Query(
        "jpeg", description="Format of the image to return (jpeg, png)"
    ),
    quality: int = Query(
        80,
        description="Quality of the image to return (0-100)",
        ge=0,
        le=100,
    ),
):
    """
    Get a specific image by its ID.
    """
    session = get_session()
    image = session.get(TimelapseImage, image_id)

    if not image:
        return {"error": "Image not found"}, 404

    img = Image.open(f"{IMAGE_DIR}/{image.file_name}")

    if size == "small":
        img = img.resize((320, 240))
    elif size == "medium":
        img = img.resize((640, 480))
    elif size == "large":
        img = img.resize((1280, 960))

    # Convert to bytes
    img_buffer = io.BytesIO()
    img.save(img_buffer, format=format, quality=quality, optimize=True)
    img_buffer.seek(0)

    return StreamingResponse(img_buffer, media_type=f"image/{format.lower()}")

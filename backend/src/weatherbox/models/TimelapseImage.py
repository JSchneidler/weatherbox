from typing import Optional

from sqlmodel import Field, SQLModel


class TimelapseImage(SQLModel, table=True):
    """An image from a timelapse."""

    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str = Field(index=True, nullable=False)
    file_name: str = Field(max_length=255, nullable=False)

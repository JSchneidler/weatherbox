import pytest


@pytest.fixture(scope="module")
def db_connection():
    """Fixture to set up a database connection."""
    from sqlalchemy import create_engine
    from sqlmodel import Session

    database_url = "sqlite:///weatherbox-test.db"
    engine = create_engine(database_url, echo=True)

    with Session(engine) as session:
        yield session


def test_database(db_connection):
    """Test the database connection and basic operations."""
    from sqlmodel import select
    from weatherbox.models.TimelapseImage import TimelapseImage

    with db_connection as session:
        new_image = TimelapseImage(
            timestamp="2025-06-02T23:49:43", file_name="test_image.jpg"
        )

        session.add(new_image)
        session.commit()

        statement = select(TimelapseImage).where(
            TimelapseImage.file_name == "test_image.jpg"
        )
        results = session.exec(statement).all()

        assert len(results) == 1
        assert results[0].file_name == "test_image.jpg"

        session.delete(new_image)
        session.commit()

        statement = select(TimelapseImage).where(
            TimelapseImage.file_name == "test_image.jpg"
        )
        results = session.exec(statement).all()
        assert len(results) == 0

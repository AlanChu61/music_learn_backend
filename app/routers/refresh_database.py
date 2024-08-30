from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import models, crud, database

router = APIRouter()


@router.post("/refresh-database")
def refresh_database(db: Session = Depends(database.get_db)):
    print("Refreshing database")
    try:
        # Drop all tables
        models.Base.metadata.drop_all(bind=database.engine)

        # Recreate all tables
        models.Base.metadata.create_all(bind=database.engine)

        # Insert dummy data
        crud.create_dummy_data(db)

        return {"message": "Database has been refreshed with dummy data"}

    except SQLAlchemyError as e:
        # Log the error details to the server logs
        print(f"Database error occurred: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while refreshing the database"
        )

    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

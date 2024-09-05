from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .. import models, crud, database

router = APIRouter()


@router.post("/refresh-database")
def refresh_database(db: Session = Depends(database.get_db)):
    try:
        models.Base.metadata.drop_all(bind=database.engine)
        models.Base.metadata.create_all(bind=database.engine)
        crud.create_dummy_data(db)
        return {"message": "Database has been refreshed with dummy data"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500, detail=f"Database error occurred: {str(e)}"
        )

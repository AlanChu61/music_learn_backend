from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Submission, User, Course
from ..crud import get_current_user
import shutil

router = APIRouter()


@router.post("/upload-file/")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file_path = f"uploads/{current_user.id}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    submission = Submission(
        user_id=current_user.id,
        course_id=current_user.courses[0].id,
        file_url=file_path,
    )
    db.add(submission)
    db.commit()
    return {"message": "File uploaded successfully"}


@router.get("/download-file/{submission_id}")
def download_file(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="File not found")

    # 檢查用戶是否有權限下載文件
    return {"file_url": submission.file_url}

import os
from fastapi import HTTPException, UploadFile

class FileValidator:
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
    ALLOWED_EXTENSIONS = {'.txt'}
    ALLOWED_CONTENT_TYPES = {'text/'}

    @classmethod
    def validate_file_presence(cls, file: UploadFile):
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

    @classmethod
    def validate_file_extension(cls, filename: str):
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail="Only .txt files are supported"
            )

    @classmethod
    def validate_content_type(cls, content_type: str):
        if content_type and not any(content_type.startswith(ct) for ct in cls.ALLOWED_CONTENT_TYPES):
            raise HTTPException(
                status_code=400, 
                detail="File must be a text file"
            )

    @classmethod
    def validate_file_size(cls, size: int):
        if size > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail="File size exceeds 5MB limit"
            )
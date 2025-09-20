from fastapi import HTTPException, UploadFile
from .validators import FileValidator

class FileProcessor:
    @staticmethod
    async def read_and_validate_file(file: UploadFile) -> str:
        try:
            content = await file.read()
            
            # Double-check file size after reading
            FileValidator.validate_file_size(len(content))
            
            return content.decode('utf-8')
            
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400, 
                detail="File is not a valid text file (UTF-8 encoding required)"
            )
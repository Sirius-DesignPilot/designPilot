from fastapi import HTTPException, status, UploadFile
import filetype


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# Desteklenen MIME tipleri
ACCEPTED_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/pjpeg",
    "image/vnd.dwg",
    "application/acad",
    "application/x-acad",
    "application/autocad",
}

# Desteklenen uzantılar
ACCEPTED_EXTENSIONS = {"png", "jpg", "jpeg", "dwg"}


def validate_file(file: UploadFile):
    
    if file.content_type.lower() not in ACCEPTED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported MIME type: {file.content_type}",
        )

    
    file_info = filetype.guess(file.file)

    if file_info is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unable to detect file type",
        )

    extension = file_info.extension.lower()
    if extension not in ACCEPTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file extension: {extension}",
        )

    
    file.file.seek(0, 2)  # move pointer to end
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 5MB limit",
        )

    return True

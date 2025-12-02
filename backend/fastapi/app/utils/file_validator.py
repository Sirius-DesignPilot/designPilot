from fastapi import HTTPException,status
from typing import IO
import filetype


def validate_file_size(file:IO):
    FILE_SIZE=5242880#5 Mb

    accepted_file_types=["image/png","image/jpeg","image/jpg","image/vnd.dwg",
                         "application/autocad_dwg","dwg"]

    file_info=filetype.guess(file.file)
    if file_info is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="unable to determine file type"
        )
    detected_content_type=file_info.extension.lower()

    if(
    file.content_type not in accepted_file_types
        or detected_content_type not in accepted_file_types
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="unsupported file type",
        )
    detected_content_type=file_info.extension.lower()
    if(
        file.content_type not in accepted_file_types
        or detected_content_type not in accepted_file_types
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="unsupported file type"
        )
    real_file_size=0
    for chunk in file.file:
        real_file_size+=len(chunk)
        if real_file_size>FILE_SIZE:
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,detail="Too large")

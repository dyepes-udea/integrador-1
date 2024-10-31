from fastapi import File, HTTPException, UploadFile, status


async def check_mime_type_csv_xlsx(
    file: UploadFile = File(...),
) -> tuple[bytes, str]:
    if file.content_type != "text/csv" and \
        file.content_type != "application/vnd.ms-excel" and \
        file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Extension",
        )
    return await file.read(), file.filename.split(".")[-1]

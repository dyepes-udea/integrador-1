from io import BytesIO
from typing import Callable

from fastapi import Depends, HTTPException, status
from pandas import DataFrame, read_csv, read_excel

from app.api.endpoints.dependencies.file import check_mime_type_csv_xlsx


def file_to_dataframe(
    required_columns: list[str],
) -> Callable[[bytes], DataFrame]:
    def wrapper(
        result: tuple[bytes, str] = Depends(check_mime_type_csv_xlsx),
    ) -> DataFrame:
        file_bytes, extension = result
        file_bytes_io = BytesIO(file_bytes)
        try:
            data: DataFrame
            if extension == "csv":
                data = read_csv(
                    file_bytes_io,
                    header=0,
                    na_filter=False,
                    keep_default_na=False,
                    usecols=required_columns,
                )
            else:
                data = read_excel(
                    file_bytes_io,
                    header=0,
                    na_filter=False,
                    keep_default_na=False,
                    usecols=required_columns,
                )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "one or more specified columns do not exist in "
                    f"the file: {', '.join(required_columns)}"
                ),
            )
        return data
    return wrapper
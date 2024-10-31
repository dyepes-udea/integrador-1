from pydantic import BaseModel, ConfigDict


class CreateProgramSubject(BaseModel):
    subject_id: int = ...
    program_id: int = ...


class ProgramSubject(CreateProgramSubject):
    model_config = ConfigDict(from_attributes=True)

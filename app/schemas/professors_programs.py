from pydantic import BaseModel, ConfigDict


class CreateProfessorProgram(BaseModel):
    professor_id: int = ...
    program_id: int = ...


class ProfessorProgram(CreateProfessorProgram):
    model_config = ConfigDict(from_attributes=True)

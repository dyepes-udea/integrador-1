from pandas import DataFrame
from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import InvestorCRUD
from app.repositories.postgresql.tables import Investor as InvestorTable
from app.schemas.entities import CreateEntity
from app.schemas.errors import MassiCreationError
from app.services.projects import project_service
from app.services.entities import entity_service
from app.schemas.investors import (
    InvestorFilters,
    CreateInvestor,
    Investor,
    InCreateInvestor,
    MassiCreationResult,
)


class InvestorService:
    def __init__(self) -> None:
        self.__crud = InvestorCRUD(table=InvestorTable)

    def get_all(
        self, *, session: Session, filters: InvestorFilters,
    ) -> list[Investor]:
        new_fielters = filters.model_dump(
            exclude={"skip", "limit", "project_code", "entity_code"},
            exclude_defaults=True,
        )

        if filters.project_code:
            project = project_service.get_by_code(
                session=session, code=filters.project_code,
            )
            new_fielters["project_id"] = project.id

        if filters.entity_code:
            entity = entity_service.get_by_code(
                session=session, code=filters.entity_code,
            )
            new_fielters["entity_id"] = entity.id

        investors = self.__crud.get_all(
            session=session,
            skip=filters.skip,
            limit=filters.limit,
            filters=new_fielters,
        )
        return [Investor.model_validate(investor) for investor in investors]
    
    def create(
        self, *, session: Session, new_investor: CreateInvestor,
    ) -> Investor:
        project = project_service.get_by_code(
            session=session,
            code=new_investor.project_code,
        )
        entity = entity_service.get_or_create(
            session=session,
            code=new_investor.entity_code,
            new_entity=CreateEntity(
                code=new_investor.entity_code,
                name=new_investor.entity_name,
            ),
        )
        investor = self.__crud.create(
            session=session,
            model=InCreateInvestor(
                project_id=project.id,
                entity_id=entity.id,
                **new_investor.model_dump(
                    exclude={
                        "project_code",
                        "entity_code",
                        "entity_name",
                    },
                ),
            ),
        )
        return Investor.model_validate(investor)
    
    def create_per_dataframe(
        self, *, session: Session, data: DataFrame,
    ) -> MassiCreationResult:
        errors = []
        investors = []
        for i, row in data.iterrows():
            try:
                new_investor = CreateInvestor(
                    type=row["Tipo"],
                    amount=row["Total fresco"],
                    kind=row["Total en especie"],
                    project_code=row["Proyecto"],
                    entity_code=row["Código del aportante"],
                    entity_name=row["Aportante"],
                )
                investor = self.create(
                    session=session, new_investor=new_investor,
                )
                investors.append(investor)
            except Exception as e:
                errors.append(MassiCreationError(row=i+1, error=str(e)))
        return MassiCreationResult(investors=investors, errors=errors)


investor_service = InvestorService()

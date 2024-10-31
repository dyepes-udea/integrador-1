from app.repositories.postgresql.database import postgresql


def get_db():
    session = postgresql.session()
    try:
        yield session
    finally:
        session.close()

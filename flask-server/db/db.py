from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, URL

class Base(DeclarativeBase):
    pass

def create_engine_instance(db_url: URL | None = None, echo: bool = False):
    """Creates an SQLAlchemy engine and initializes the database. Returns the engine instance."""
    if db_url is None: 
        db_url = URL.create(
            drivername="sqlite+pysqlite",
            database="instance/test.db",
        )
    engine = create_engine(str(db_url), echo=echo)
    Base.metadata.create_all(engine)
    return engine


if __name__ == "__main__":
    engine = create_engine_instance()
    
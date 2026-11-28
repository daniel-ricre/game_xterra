from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///game.db"

engine = create_engine(DATABASE_URL)


@event.listens_for(engine, "connect")
def _fk_pragma_on_connect(dbapi_conn, _):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from game.models.save import Save
    from game.models.player import PlayerState
    # import game.models.world     # noqa: F401
    from game.database.base import Base
    Base.metadata.create_all(bind=engine)
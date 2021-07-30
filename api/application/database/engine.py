from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.utils import get_params

def session_factory():
    params = get_params()
    username = params["USERNAME"]
    password = params["PASSWORD"]
    hostname = params["HOSTNAME"]
    port = params["PORT"]
    database = params["DATABASE"]

    db_engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

    def get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    return get_db

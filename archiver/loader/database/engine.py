from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager


def session_factory(username, password, hostname, port, database):
	"""Database session factory to generate engine context"""

	engine = create_engine(f"postgresql://{username}:{password}@{hostname}:{port}/{database}")
	Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

	@contextmanager
	def get_engine():
		try:
			db = Session()
			yield db
		finally:
			db.commit()
			db.flush()
			db.close()

	return get_engine

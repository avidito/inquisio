from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine():
	engine = create_engine("postgresql://report_admin:admin@localhost:5432/report")
	Session = sessionmaker(bind=engine)
	return Session()
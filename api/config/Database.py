from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

print("Insertion check")


class DataBase:
    
    print("Database class working")
    # Replace with your own MySQL connection details
    DATABASE_URL = "mysql+pymysql://root:Z%40nec2014@192.168.1.5:3306/smart_attendance_system"

    # SQLAlchemy engine
    engine = create_engine(DATABASE_URL, echo=True)

    # SessionLocal for dependency injection
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Base class for ORM models
    Base = declarative_base()

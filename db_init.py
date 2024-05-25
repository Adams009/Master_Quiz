from app import app, db
from app.models import User, Category, Question
from sqlalchemy import inspect

# Import all model classes here
from app.models import *

with app.app_context():
    # Get a list of all model classes
    model_classes = [cls for cls in db.Model.__subclasses__()]

    # Get an instance of the SQLAlchemy Inspector
    inspector = inspect(db.engine)

    # Check if tables already exist
    existing_tables = inspector.get_table_names()

    # Create tables that don't exist
    to_create = [cls.__table__ for cls in model_classes if cls.__tablename__ not in existing_tables]

    if to_create:
        for table in to_create:
            table.create(bind=db.engine, checkfirst=True)
        print(f"Created tables: {', '.join(cls.__tablename__ for cls in model_classes if cls.__tablename__ not in existing_tables)}")
    else:
        print("All tables already exist.")

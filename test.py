from app import app, db
from app.models import User, Category, Question
from sqlalchemy import inspect

# Import all model classes here
from app.models import *

# Ensure the application context is available for database operations
with app.app_context():
    # Add categories
    cat1 = Category(name='General Knowledge', description='General knowledge questions.')
    cat2 = Category(name='Science', description='Science-related questions.')
    db.session.add(cat1)
    db.session.add(cat2)
    db.session.commit()

    # Add questions
    q1 = Question(category_id=cat1.id, question_text='What is the capital of France?', correct_answer='Paris', wrong_answers='London,Rome,Berlin')
    q2 = Question(category_id=cat2.id, question_text='What is the chemical symbol for water?', correct_answer='H2O', wrong_answers='O2,CO2,He')
    db.session.add(q1)
    db.session.add(q2)
    db.session.commit()

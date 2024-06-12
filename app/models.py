from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

# User model definition, which includes user information and password management methods
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Method to set the password, hashing it before storing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method to check the password, comparing the hash with the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

     # Representation method for debugging purposes
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
# Category model definition, representing categories of questions
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256))

     # Representation method for debugging purposes
    def __repr__(self):
        return '<Category {}>'.format(self.name)
    
# Question model definition, representing individual questions in categories
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    question_text = db.Column(db.String(256), nullable=False)
    correct_answer = db.Column(db.String(128), nullable=False)
    wrong_answers = db.Column(db.String(256), nullable=False)
    category = db.relationship('Category', back_populates='questions')

    # Representation method for debugging purposes
    def __repr__(self):
        return '<Question {}>'.format(self.question_text)
    
# UserProgress model definition, tracking user progress through questions
class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    is_answered = db.Column(db.Boolean, default=False)
    is_correct = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='progress')
    question = db.relationship('Question', back_populates='progress')

     # Static method to get all progress entries for a specific user
    @staticmethod
    def get_user_progress(user_id):
        return UserProgress.query.filter_by(user_id=user_id).all()

    # Static method to get the number of correct answers for a specific user
    @staticmethod
    def get_correct_answers_count(user_id):
        return UserProgress.query.filter_by(user_id=user_id, is_correct=True).count()

    # Static method to get the total number of answered questions for a specific user
    @staticmethod
    def get_total_answers_count(user_id):
        return UserProgress.query.filter_by(user_id=user_id, is_answered=True).count()

     # Representation method for debugging purposes
    def __repr__(self):
        return '<UserProgress User:{} Question:{}>'.format(self.user_id, self.question_id)

# Define the relationship between models, so that the database can be queried
Category.questions = db.relationship('Question', order_by=Question.id, back_populates='category')
User.progress = db.relationship('UserProgress', order_by=UserProgress.id, back_populates='user')
Question.progress = db.relationship('UserProgress', order_by=UserProgress.id, back_populates='question')

# User loader function for Flask-Login to get user by ID
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


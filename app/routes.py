from flask import render_template, redirect, url_for, flash, request, session, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
import random, requests, html
from app.models import Category, Question, UserProgress
from urllib.parse import urlsplit


# Function to get questions from the Open Trivia Database API
def get_pool(amt,cat):
    url = f'https://opentdb.com/api.php?amount={amt}&category={cat}'
    response = requests.get(url).json()
    return response

# Function to shuffle a list of multiple choice answers
def shuffled(multiple):
    random.shuffle(multiple)
    return multiple

# Add enumerate function to Jinja2 context processors
@app.context_processor
def enumerate_fun():
    return dict(enumerate=enumerate)


# Route to display all categories, requires login
@app.route('/categories')
@login_required
def categories():
    categories = Category.query.all()
    return render_template('categories.html', title='Categories', categories=categories)

# Route to display a specific category and its questions, requires login
@app.route('/category/<int:category_id>')
@login_required
def category(category_id):
    category = Category.query.get_or_404(category_id)
    questions = Question.query.filter_by(category_id=category_id).all()
    return render_template('category.html', title=category.name, category=category, questions=questions)

# Route to display and handle the question answering logic, requires login
@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question(question_id):
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct = user_answer == question.correct_answer
        user_progress = UserProgress(user_id=current_user.id, question_id=question.id, is_answered=True, is_correct=correct)
        db.session.add(user_progress)
        db.session.commit()
        flash('Correct!' if correct else 'Wrong!', 'success' if correct else 'danger')
        return redirect(url_for('categories'))
    wrong_answers = question.wrong_answers.split(',')
    return render_template('question.html', title='Question', question=question, wrong_answers=wrong_answers)

# Route to handle user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations {}, you are now a registered user!'.format(user.username), 'success')
        return redirect(url_for('index'))
    
    else:
        for error in form.errors.values():
            if error:
                flash(f"something went wrong: {error}",'danger')
    return render_template('register.html', title='Register', form=form)


# Route to handle user login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# Route to handle user logout, requires login
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Route to display user progress, requires login
@app.route('/progress')
@login_required
def progress():
    user_progress = UserProgress.get_user_progress(current_user.id)
    correct_answers_count = UserProgress.get_correct_answers_count(current_user.id)
    total_answers_count = UserProgress.get_total_answers_count(current_user.id)
    return render_template('progress.html', title='Progress', user_progress=user_progress, correct_answers_count=correct_answers_count, total_answers_count=total_answers_count)


# Route for the home page, which handles category selection and question amount input
@app.route('/',methods=['GET','POST'])
@app.route('/index/', methods=['GET','POST'])
@login_required
def index():
    if request.method == 'POST':
        cat = 10
        category_chosen = request.form.get('category')
       
        for key in session.keys():
            if session[key] == session[category_chosen]:
                cat = int(category_chosen)
        

        amount = int(request.form.get('question'))

        return redirect(url_for('quiz',amount = amount, cat = cat))
    
    
    session['10'] = "Any category"
    session['9'] = "General Knowledge"
    session['27'] = "Animals"
    session['21'] = "Sports"
    session['24'] = "Politics"
    session['18'] = "Computer"
    
    return  render_template('index.html')


# Route to handle the quiz logic, fetching questions and evaluating answers
@app.route('/quiz/<int:cat>/<int:amount>', methods=['GET','POST'])
def quiz(cat,amount):
    All_answer = request.form
    score = 0

   
    for key in All_answer.keys():
        user_idx = int(key)
        user_response_value = All_answer[key]
        correct_answer = session['questions'][user_idx].get('correct_answer')
       
        if user_response_value == correct_answer:
            score += 1
        return redirect(url_for('result', score=score, amount=amount))

    fetch_data = get_pool(cat=cat,amt=amount)
    trivia_data = fetch_data.get('results')
    if trivia_data:
        questions = []

        for data in trivia_data:
            question = html.unescape(data.get('question'))
            answer = html.unescape(data.get('correct_answer'))
            multiple_question = html.unescape(data.get('incorrect_answers'))
            multiple_question.extend([answer])

            shuffle = shuffled(multiple_question)
            questions.append({
                'Question': question,
                'choices': shuffle,
                'correct_answer': answer
            })

        session['questions'] = questions
        print(f"Session questions: {session['questions']}")
        return render_template('quiz.html', questions=questions)
    else:
        return "No trivia data found. Please try again later."


# Route to display quiz results
@app.route('/result/<int:amount>/<int:score>', methods=['GET','POST'])
def result(amount,score):
    divide = amount/2
    if score < divide:
        flash(f'Your Score is Poor! Try Harder', 'alert')
    elif divide <= score < amount:
        flash(f'Your Score is Good! Keep it up', 'alert')
    else:
        flash(f'Congratulations!!! Your Score is Superb', 'alert')
    



    return render_template('result.html', amount=amount,score=score)


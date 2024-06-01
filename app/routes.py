from flask import render_template, redirect, url_for, flash, request, session, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
import random, requests, html






def get_pool(amt,cat):
    url = f'https://opentdb.com/api.php?amount={amt}&category={cat}'
    response = requests.get(url).json()
    return response

def shuffled(multiple):
    random.shuffle(multiple)
    return multiple


@app.context_processor
def enumerate_fun():
    return dict(enumerate=enumerate)



@app.route('/categories')
def categories():
    return 'Browse Categories'

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
        if not next_page or urlsplit(next_page)[0]!= '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/',methods=['GET','POST'])
@app.route('/index/', methods=['GET','POST'])
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


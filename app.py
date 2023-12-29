from flask import Flask, request, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.debug = True

app.config['SECRET_KEY'] = 'password'

toolbar = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    """Shows home page"""
    # title = satisfaction_survey.title
    # instructions = satisfaction_survey.instructions
    # questions = satisfaction_survey.questions
    return render_template('home.html', survey=survey)

@app.route('/survey_start')
def start_survey():
   """Reset response cache for new survey, redirect to first question"""

   responses = []

   return redirect('/questions/0')

@app.route('/questions/<int:idx>')
def questions_page(idx):
    """Shows survey questions"""

    question = survey.questions[idx]

    """ Prevent user from skipping questions """
    if (idx != len(responses)):
        flash("Please complete all questions in order", "ERROR")
        return redirect(f"/questions/{len(responses)}")
    
    if (idx > len(survey.questions)):
       flash(f"Invalid question id: {idx}", "ERROR")
       return redirect(f"/questions/{len(responses)}")

    return render_template("survey.html",question=question, question_num=idx)

@app.route('/answer', methods=["POST"])
def answer_redirect():
    """Upon submission, save answer, increase queston index or send to endscreen"""
    answer = request.form['answer']

    responses.append(answer)
    if (answer == null):
       return redirect('/')

    if (len(responses) == len(survey.questions)):
        return redirect("/end")
    else:
     return redirect(f"/questions/{len(responses)}")
    
@app.route('/end')
def end_survey():
   """Return thank you page at end of survey"""
   return render_template("end.html")

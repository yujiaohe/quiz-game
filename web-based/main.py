from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from data import QuizData

app = Flask(__name__)
app.config["SECRET_KEY"] = "dafjadjfa%^*dakfhad35r4adhfad@m"
Bootstrap(app)
question_data = []


class DefineForm(FlaskForm):
    category = SelectField(label="Select Category:",
                           choices=QuizData.get_categories(),
                           validators=[DataRequired()])
    type = SelectField(label="Select Type:",
                       choices=[("multiple", "Multiple Choice"),
                                ("boolean", "True/False")],
                       validators=[DataRequired()])
    difficulty = SelectField(label="Select Difficulty:",
                             choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
                             validate_choice=[DataRequired()])
    amount = SelectField(label="Number of Questions: ",
                         choices=list(range(5, 51, 5)),
                         validate_choice=[DataRequired()])

    submit = SubmitField(label="Start")


@app.route("/", methods=["GET", "POST"])
def home():
    define_form = DefineForm()
    if define_form.validate_on_submit():
        quiz_data = QuizData(amount=define_form.amount.data,
                             type=define_form.type.data,
                             category_id=define_form.category.data,
                             difficulty=define_form.difficulty.data)
        global question_data
        question_data = quiz_data.get_questions()
        return render_template("quiz.html", ques=question_data, ques_num=0, score=0)
    return render_template("index.html", form=define_form)


@app.route("/quiz")
def quiz():
    question_num = int(request.args.get("ques_num"))
    score = int(request.args.get("score"))
    user_answer = request.args.get("ans")
    if user_answer:
        # user checked answer
        is_correct = None
        if question_data[question_num]["correct_answer"] == user_answer:
            score += 1
            is_correct = True

        return render_template("quiz.html", ques=question_data, ques_num=question_num, score=score,
                               is_correct=is_correct, ans=user_answer)
    else:
        # 3s later go to next question
        if question_num < len(question_data):
            return render_template("quiz.html", ques=question_data, ques_num=question_num, score=score)
        else:
            # last question
            percent = round(score / len(question_data) * 100, 2)
            return render_template("final_score.html", score=score, ques=question_data, pct=percent)


if __name__ == "__main__":
    app.run(debug=True)

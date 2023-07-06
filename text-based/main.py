from data import question_data
from question_model import Question
from quiz_brain import QuizBrain

question_back = []
for item in question_data:
    new_q = Question(item["text"], item["answer"])
    question_back.append(new_q)

quiz = QuizBrain(question_back)

while quiz.still_has_questions():
    quiz.next_question()

print("You've completed the quiz.")
print(f"Your final score was: {quiz.score}/{quiz.question_number}.")
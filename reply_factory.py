
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    user_answers=session.get("user_answer",[])
    current_question=PYTHON_QUESTION_LIST[current_question_id]
    if answer not in current_question["options"]:
        return False ," Invalid , Please Choose again from options"
    user_answer={"question_id": current_question_id,"answer":answer,"id_correct":answer==current_question["correct_answer"]}
    user_answers.append(user_answer)
    session["user_answers"]=user_answers
    
    return True, "" 



def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id <len(PYTHON_QUESTION_LIST)-1:
        next_id=current_question_id+1
        next_quetion =PYTHON_QUESTION_LIST[next_id]["question"]
        return next_quetion, next_id
    else:
        return None, -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    user_answers=session.get("user_answer",[])
    score = 0
    for user_answer in user_answers:
        if user_answer.is_correct:
            score += 1

    # Calculate the user's percentage
    percentage = (score / len(quiz.questions)) * 100

    # Generate the final response
    final_response = f"You got {score} out of {len(PYTHON_QUESTION_LIST)} questions correct. That's {percentage:.2f}%!"

    # Add some personalized feedback based on the user's score
    if percentage >= 90:
        final_response += " You're a quizzing superstar!"
    elif percentage >= 70:
        final_response += " Not bad, keep practicing!"
    elif percentage >= 50:
        final_response += " You're getting there, try again!"
    else:
        final_response += " Maybe you should try this quiz again later?"

    # Return the final response
    return final_response

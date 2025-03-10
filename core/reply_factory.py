
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
    if current_question_id == None: 
        session["answers"] = []
    else:
        options = PYTHON_QUESTION_LIST[current_question_id]["options"]
        if answer in options:
            session["answers"].append({"question_id" : current_question_id , "answer":answer})
        else:
            return False, "You have answered wrong"
        
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id = -1
    next_question = ""
    if (current_question_id == None):
        next_question_id = 0
    else:
        next_question_id=current_question_id+1
    if (next_question_id < len(PYTHON_QUESTION_LIST)): 
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question_text'] + "<br>" +  str(PYTHON_QUESTION_LIST[next_question_id]['options'])
   
    return next_question, next_question_id


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers_list = session.get("answers")
    score = 0
    for answer in answers_list:
        question_id = answer['question_id']
        correct_answer = PYTHON_QUESTION_LIST[question_id]['answer']
        if correct_answer == answer['answer']:
            score= score + 1
    return f"You have score: {score} out of {len(PYTHON_QUESTION_LIST)}"


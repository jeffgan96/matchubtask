from flask import Flask
from flask import request

app = Flask(__name__)

#storage of questions as a {id: question} map
questions_db = {}

#store user answers. {uid: {qid: answer}} map
user_answers = {}

counter = 0


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/new_question', methods=['POST'])
def new_question():
    question = request.args.get('question')
    if question is None:
        return 'question params is required.', 400
    new_id = str(generateUUID())
    #add the new question into our db
    questions_db[new_id] = question

    return 'question successfully added. question=' + question + ' qid=' + str(len(questions_db))

@app.route('/answer_question', methods=['POST'])
def answer():
    ans = request.args.get('answer')
    qid = request.args.get('qid')
    uid = request.args.get('uid')

    if ans is None or qid is None or uid is None:
        return 'One or more required params are missing: [answer, qid, uid]', 400

    #make sure this question exists
    if qid not in questions_db:
        return 'Sorry. Unable to find the question with qid=' + qid, 400

    #create a new entry for first timers
    if uid not in user_answers:
        user_answers[uid] = {}

    user_answers[uid][qid] = ans

    return 'successfully answered question. uid=' + uid + " qid=" + qid + " ans=" + ans

@app.route('/get_answered_questions', methods=['GET'])
def get_answered_qns():
    uid = request.args.get('uid')
    if uid is None or uid not in user_answers:
        return 'uid required or not found.', 400
    result = ''

    user_keys = list(user_answers[uid])
    print(len(user_keys))
    for key in user_keys:
        #ignore questions already removed
        if key not in questions_db:
            user_answers[uid].pop(key, None)
            continue
        result += 'qid=' + key + ' ans=' + user_answers[uid][key] + '\n'

    return result

@app.route('/delete_question', methods=['POST'])
def delete_question():
    qid = request.args.get('qid')
    if qid is None or qid not in questions_db:
        return 'Unable to find the question.', 400
    questions_db.pop(qid, None)
    return 'Successfully deleted question qid=' + qid

#ideally this should generate a UUID
#this is required because we lazily delete qids in user_answers so there is a possibility of data sync error
#if a qid is answered but subsequently the question is removed and a new question with the same qid is stored
def generateUUID():
    global counter
    counter += 1
    return counter

#Submission for MatcHub task
#Author: Jeff Gan
#Date 23 October 2021

How to set up:
set/export FLASK_APP=app (if prompted)
set/export FLASK_ENV=development (if prompted)
flask run

======================================================================
#APIs supported             API type            Query params
#/new_question              [POST]              question
#/answer_question           [POST]              qid, uid, answer
#/get_answered_questions    [GET]               uid
#/delete_question           [POST]              qid
=======================================================================

#Overview, assumptions made and thought process:
Using the APIs supported, users can create new questions and answer questions using their uid (User id)
To "edit" answers after submission, the same API for answering question can be reused. Deleting answers after submission
is unsupported but its trivial. Im not very sure what to make use of the choices.csv and questions.csv (am i supposed to read
in csv as input?) so i put that aside and made this based on my own understanding of the task. There is some simple
error handling done (e.g checking if the question is valid).

Data structures used:
map/dict of {qid: question} for questions list
map/dict of {uid: {qid, answer}} for user answers

Time complexity of operations:
/new_question - O(1). we're adding to a dict
/answer_question - O(1). we're storing/updating to a dict
/remove question - O(1). we're removing from a dict
/get_answered_questions - amortised O(number of questions answered). If a series of answers are made and subsequent questions
are deleted, the first operation incurs a cost in order of number of total questions, but subsequent ones incur a cost of
number of questions answered.

Why use uid and qid:
reduce overhead. sending long strings over network and for comparison is computationally expensive

How are questions being deleted:
when a question is marked for deletion, we can remove it from the questions list in O(1). However, if we want to remove
it from the user answers, we need to traverse over the whole dict in O(q) time which is expensive. We could instead store
user answers with qid as key instaed of uid but then that would incur a problem of O(q) query time for getting user answers
for a particular uid.
Instead, the choice i made here was to do lazy evaluation. Only when get_user_answers (or whenever we need data sync)
will we remove deleted questions from the user answers list. A potential problem is that if a qid is reused and the answers for
the previous question is not removed, then we will end up "answering" the new question with the prev answer. to prevent
this,we need uuids that are not repeated.

Sample Test:
1. http://127.0.0.1:5000/new_question?question=q1                                                   [POST]
2. http://127.0.0.1:5000/new_question?question=q2                                                   [POST]
3. http://127.0.0.1:5000/new_question?question=q3                                                   [POST]
4. http://127.0.0.1:5000/answer_question?uid=1&qid=1&answer=answer1                                 [POST]
5. http://127.0.0.1:5000/answer_question?uid=1&qid=2&answer=answer2                                 [POST]
6. http://127.0.0.1:5000/get_answered_questions?uid=1 (we should see 2 questions being answered)    [GET]
7. http://127.0.0.1:5000/delete_question?qid=1                                                      [POST]
8. http://127.0.0.1:5000/get_answered_questions?uid=1 (we should see 1 question being answered)     [GET]

Estimated time taken: 2-3hrs
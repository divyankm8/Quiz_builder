from fastapi import FastAPI
from pydantic import BaseModel
from pyrebase import pyrebase
import os

path = os.path.dirname(__file__) + '\serviceAccountCredentials.json'
config = {
  "apiKey": "AIzaSyDILELhuoBCcDEMXLX8ocLI0V-6jWBR7I8",
  "authDomain": "test1-81c27.firebaseapp.com",
  "databaseURL": "https://test1-81c27-default-rtdb.firebaseio.com",
  "storageBucket": "test1-81c27.appspot.com",
  "serviceAccount": path
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
#print(db.child("users").shallow().get().val())

class userDetails(BaseModel):
    email: str
    name: str
class Email(BaseModel):
    email: str
class Quiz(BaseModel):
    userId: str
    quizTitle: str
    noOfQuestions: int
    questions: list
    options: list
    correct: list
class QuizLink(BaseModel):
    quizLink: str
class Answer(BaseModel):
    quizLink: str
    submitted: list


app = FastAPI()

@app.post("/createUser")
async def createUser(user: userDetails):
    db.child('users').child(usersHash(user.email)).set({'name': user.name, 'quiz': [True]})
    return {'message': 'Success'}

@app.post('/getUser')
async def getUser(data: Email):
    return {'name': db.child('users').child(usersHash(data.email)).get().val()['name']}

@app.post('/createQuiz')
async def createQuiz(newQuiz: Quiz):
    newLink = generateLink()
    db.child('quiz').child(newLink).set(newQuiz.dict())
    quizList = db.child('users').child(usersHash(newQuiz.userId)).get().val()['quiz']
    quizList.append(newLink)
    db.child('users').child(usersHash(newQuiz.userId)).update({'quiz': quizList})
    return {'link': newLink}

@app.post('/fetchQuiz')
async def fetchQuiz(emailId: Email):
    quizList = db.child('users').child(usersHash(emailId.email)).get().val()['quiz'][1:]
    result = []
    for link in quizList:
        result.append({'quizLink': link, 'quizTitle': db.child('quiz').child(link).get().val()['quizTitle']})
    return {'quiz': result}

@app.post('/deleteQuiz')
async def deleteQuiz(link: QuizLink):
    userId = usersHash(db.child('quiz').child(link.quizLink).get().val()['userId'])
    quizList = db.child('users').child(userId).get().val()['quiz']
    quizList.remove(link.quizLink)
    db.child('users').child(userId).update({'quiz': quizList})
    db.child('quiz').child(link.quizLink).remove()
    return {'message': 'Success'}

@app.post('/getQuiz')
async def getQuiz(link: QuizLink):
    quiz = db.child('quiz').child(link.quizLink).get().val()
    if quiz != None:
        return {'message': 'Success', 'quiz': {'quizTitle': quiz['quizTitle'], 'noOfQuestions': str(quiz['noOfQuestions']), 'questions': quiz['questions'], 'options': quiz['options']}}
    else:
        return {'message': 'Error'}

@app.post('/evaluateQuiz')
async def evaluateQuiz(answer: Answer):
    quiz = db.child('quiz').child(answer.quizLink).get().val()
    ansList = quiz['correct']
    marks = 0
    for (index, val) in enumerate(ansList):
        a, b = set(val), set(answer.submitted[index])
        if a.issubset(b) and b.issubset(a):
            marks += 1 
    return {'marks': str(marks), 'total': str(quiz['noOfQuestions'])}

def generateLink():
    counter = ['0', '0', '0', '0', '0', '0']
    quiz = db.child('quiz').shallow().get().val()
    while True:
        if (''.join(counter) in quiz):
            counter = nextLink(counter)
        else:
            break
    return ''.join(counter)

def nextLink(link):
    values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in range(-1, -7, -1):
        if values.index(link[i]) < 35:
            link[i] = values[values.index(link[i]) + 1]
            return link

def usersHash(email):
    userId = []
    for letter in email:
        if letter == '.':   userId.append('!')
        else:   userId.append(letter)
    return ''.join(userId)

def reverseHash(userId):
    email = []
    for letter in userId:
        if letter == '!':   email.append('.')
        else:   email.append(letter)
    return ''.join(email)

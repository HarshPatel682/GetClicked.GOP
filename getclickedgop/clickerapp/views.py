from django.shortcuts import render
from django.http import HttpResponse
import cgi
import os
import subprocess
import json
import ast
from django.contrib.auth import authenticate, login, logout
from models import *

def index(request):
    return HttpResponse("Welcome to GetClicked.GOP!")

def testpost(request):
    try:
        text = "This is what the server got as part of the POST:\n" + cgi.escape(str(request.POST))
    except:
        text = "Something went wrong, so this is just static text."
    return HttpResponse(text)

def deploy(request):
    #text = subprocess.check_output('touch /home/bitnami/public/DEPLOY', stderr=subprocess.STDOUT, shell=True)
    text = subprocess.check_output('w', stderr=subprocess.STDOUT, shell=True)
    return HttpResponse(text)

def createuser(request):
    result = {}
    if "username" not in request.POST:
        result["success"] = False
        result["comment"] = "A username was not supplied."
        return HttpResponse(json.dumps(result))
    elif "password" not in request.POST:
        result["success"] = False
        result["comment"] = "A password was not supplied."
        return HttpResponse(json.dumps(result))
    username = request.POST["username"]
    password = request.POST["password"]
    if len(User.objects.filter(username=username)) != 0:
        result["success"] = False
        result["comment"] = "That username is already taken."
        return HttpResponse(json.dumps(result))
    User.objects.create_user(username, None, password)
    result["success"] = True
    result["comment"] = "A new user was successfully created."
    return HttpResponse(json.dumps(result))

def loginuser(request):
    result = {}
    if "username" not in request.POST:
        result["success"] = False
        result["comment"] = "A username was not supplied."
        return HttpResponse(json.dumps(result))
    elif "password" not in request.POST:
        result["success"] = False
        result["comment"] = "A password was not supplied."
        return HttpResponse(json.dumps(result))
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is None:
        result["success"] = False
        result["comment"] = "The username and password combination was not recognized."
        return HttpResponse(json.dumps(result))
    else:
        result["success"] = True
        result["comment"] = "The user has been logged in successfully."
        login(request, user)
        return HttpResponse(json.dumps(result))

def logoutuser(request):
    result = {}
    logout(request)
    result["success"] = True
    return HttpResponse(json.dumps(result))

def createsection(request):
    result = {}
    if not request.user.is_authenticated:
        result["success"] = False
        result["comment"] = "There is no user currently logged in."
        return HttpResponse(json.dumps(result))
    if not "name" in request.POST:
        result["success"] = False
        result["comment"] = "A section name was not supplied."
        return HttpResponse(json.dumps(result))
    name = request.POST["name"]
    if len(Section.objects.filter(name=name)) != 0:
        result["success"] = False
        result["comment"] = "That section name is already taken."
        return HttpResponse(json.dumps(result))
    section = Section(instructor=request.user, name=name)
    section.save()
    result["success"] = True
    result["comment"] = "A new section was created successfully"
    return HttpResponse(json.dumps(result))

def sectionsasinstructor(request):
    result = {}
    if not request.user.is_authenticated:
        result["success"] = False
        result["comment"] = "There is no user currently logged in."
        result["sections"] = []
        return HttpResponse(json.dumps(result))
    sections = []
    for section in Section.objects.filter(instructor=request.user):
        sections.append(section.name)
    sections.sort()
    result["success"] = True
    result["comment"] = "Sections where the user is an instructor were found successfully."
    result["sections"] = sections
    return HttpResponse(json.dumps(result))

def enrollinsection(request):
    result = {}
    if not request.user.is_authenticated:
        result["success"] = False
        result["comment"] = "There is no user currently logged in."
        return HttpResponse(json.dumps(result))
    if not "section" in request.POST:
        result["success"] = False
        result["comment"] = "A section name was not supplied."
        return HttpResponse(json.dumps(result))
    section_name = request.POST["section"]
    if len(Section.objects.filter(name=section_name)) == 0:
        result["success"] = False
        result["comment"] = "There is no section with that name."
        return HttpResponse(json.dumps(result))
    section = Section.objects.get(name=section_name)
    if len(StudentSection.objects.filter(student=request.user,section=section)) != 0:
        result["success"] = False
        result["comment"] = "The user is already enrolled in that section."
        return HttpResponse(json.dumps(result))
    student_section = StudentSection(student=request.user,section=section)
    student_section.save()
    result["success"] = True
    result["comment"] = "The student was enrolled in the section successfully."
    return HttpResponse(json.dumps(result))

def sectionsasstudent(request):
    result = {}
    if not request.user.is_authenticated:
        result["success"] = False
        result["comment"] = "There is no user currently logged in."
        result["sections"] = []
        return HttpResponse(json.dumps(result))
    sections = []
    for student_section in StudentSection.objects.filter(student=request.user):
        sections.append(student_section.section.name)
    sections.sort()
    result["success"] = True
    result["comment"] = "Sections where the user is a student were found successfully."
    result["sections"] = sections
    return HttpResponse(json.dumps(result))

def createquestion(request):
    request_json = json.loads(request.body)
    body_data = json.loads(request.body)
    txt = subprocess.check_output('echo ' + str(body_data) + ' >> ~/posted', stderr=subprocess.STDOUT, shell=True)
    result = {}
    if not request.user.is_authenticated:
        result["success"] = False
        result["comment"] = "There is no user currently logged in."
        return HttpResponse(json.dumps(result))
    if not "section" in request_json:
        result["success"] = False
        result["comment"] = "A section name was not supplied."
        return HttpResponse(json.dumps(result))
    section_name = request_json["section"]
    if len(Section.objects.filter(name=section_name)) == 0:
        result["success"] = False
        result["comment"] = "There is no section with that name."
        return HttpResponse(json.dumps(result))
    section = Section.objects.get(name=section_name)
    if section.instructor != request.user:
        result["success"] = False
        result["comment"] = "The user is not the section's instructor."
        return HttpResponse(json.dumps(result))
    if not "label" in request_json:
        result["success"] = True
        result["comment"] = "The question text was not supplied."
        return HttpResponse(json.dumps(result))
    label = request_json["label"]
    if not "responses" in request_json:
        result["success"] = False
        result["comment"] = "The question responses were not supplied."
        return HttpResponse(json.dumps(result))
    responses = []
    try:
        raw_responses = request_json["responses"]
        for raw_response in raw_responses:
            response_text = raw_response[0]
            response_is_correct = raw_response[1]
            responses.append([response_text, response_is_correct])
    except Exception, e:
        result["success"] = False
        result["comment"] = str(e)#"The response set was not able to be parsed."
        return HttpResponse(json.dumps(result))
    
    question = Question(section=section, label=label)
    question.save()
    for response in responses:
        mcanswer = MCAnswer(question=question, label=response[0], is_correct=response[1])
        mcanswer.save()
    result["success"] = True
    result["comment"] = "A new question was added successfully."
    return HttpResponse(json.dumps(result))

def answerquestion(request):
    result = {}
    if not request.user.is_authenticated:
        result["success"] = False
        result["comment"] =  "There is no user currently logged in."
        return HttpResponse(json.dumps(result))
    if not "questionid" in request.POST:
        result["success"] = False
        result["comment"] = "A question id was not supplied."
        return HttpResponse(json.dumps(result))
    question_id = request.POST["questionid"]
    if len(Question.objects.filter(id=question_id)) == 0:
        result["success"] = False
        result["comment"] = "There is no question with that id."
        return HttpResponse(json.dumps(result))
    question = Question.objects.get(id=question_id)
    if len(StudentSection.objects.filter(student=request.user, section=question.section)) == 0:
        result["success"] = False
        result["comment"] = "The user is not enrolled in the appropriate section."
        return HttpResponse(json.dumps(result))
    if not "label" in request.POST:
        result["success"] = False
        result["comment"] = "No answer choice was provided."
        return HttpResponse(json.dumps(result))
    label = request.POST["label"]
    if len(MCAnswer.objects.filter(question=question, label=label)) == 0:
        result["success"] = False
        result["comment"] = "The answer choice is not valid."
        return HttpResponse(json.dumps(result))
    answer = MCAnswer.objects.get(question=question, label=label)
    # Delete the previous response if one exists
    if len(MCResponse.objects.filter(student=request.user, question=question)) != 0:
        MCResponse.objects.get(student=request.user, question=question).delete()
    mcresponse = MCResponse(student=request.user, question=question, response=answer)
    mcresponse.save()
    result["success"] = True
    result["comment"] = "Answer choice recorded successfully."
    return HttpResponse(json.dumps(result))

def getquestionsbysection(request):
    result = {"questions": [-1, "", False, ""]}
    if not request.user.is_authenticated:
        result["success"] = False
        result["comment"] =  "There is no user currently logged in."
        return HttpResponse(json.dumps(result))
    if not "section" in request.POST:
        result["success"] = False
        result["comment"] = "A section name was not supplied."
        return HttpResponse(json.dumps(result))
    section_name = request.POST["section"]
    if len(Section.objects.filter(name=section_name)) == 0:
        result["success"] = False
        result["comment"] = "There is no section with that name."
        return HttpResponse(json.dumps(result))
    section = Section.objects.filter(name=section_name)
    if len(StudentSection.objects.filter(student=request.user, section=section)) == 0:
        result["success"] = False
        result["comment"] = "The user is not enrolled in that section."
        return HttpResponse(json.dumps(result))
    questions = Question.objects.filter(section=section)
    question_list = []
    for question in questions:
        id = question.id
        label = question.label
        has_answered = len(MCResponse.objects.filter(student=request.user, question=question)) == 1
        answer = ""
        if has_answered:
            answer = MCResponse.objects.get(student=request.user, question=question).response.label
        question_list.append([id, label, has_answered, answer])
    result["success"] = True
    result["comment"] = "Questions in the specified section were retrieved successfully."
    result["questions"] = question_list
    return HttpResponse(json.dumps(result))

def getquestiondetail(request):
    result = {"answers": [], "questionid": -1, "hasanswered": False, "chosenanswer": ""}
    if not request.user.is_authenticated:
        result["success"] = False
        result["comment"] =  "There is no user currently logged in."
        return HttpResponse(json.dumps(result))
    if not "questionid" in request.POST:
        result["success"] = False
        result["comment"] = "A question id was not supplied."
        return HttpResponse(json.dumps(result))
    question_id = request.POST["questionid"]
    if len(Question.objects.filter(id=question_id)) == 0:
        result["success"] = False
        result["comment"] = "There is no question with that id."
        return HttpResponse(json.dumps(result))
    question = Question.objects.get(id=question_id)
    if len(StudentSection.objects.filter(student=request.user, section=question.section)) == 0:
        result["success"] = False
        result["comment"] = "The user is not enrolled in that section."
        return HttpResponse(json.dumps(result))
    answers = MCAnswer.objects.filter(question=question)
    answer_choices = [answer.label for answer in answers]
    has_answered = len(MCResponse.objects.filter(student=request.user, question=question)) == 1
    answer = ""
    if has_answered:
        answer = MCResponse.objects.get(student=request.user, question=question).response.label
    result["success"] = True
    result["comment"] = "Question detail was successfully retrieved."
    result["answers"] = answer_choices
    result["questionid"] = question_id # Echo the question id for convenience
    result["hasanswered"] = has_answered
    result["chosenanswer"] = answer
    result["label"] = question.label
    return HttpResponse(json.dumps(result))

def getgradeinfo(request):
    result = {"csv" : ""}
    if not request.user.is_authenticated:
        result["success"] = False
        result["comment"] =  "There is no user currently logged in."
        return HttpResponse(json.dumps(result))
    if not "section" in request.POST:
        result["success"] = False
        result["comment"] = "A section name was not supplied."
        return HttpResponse(json.dumps(result))
    section_name = request.POST["section"]
    if len(Section.objects.filter(name=section_name)) == 0:
        result["success"] = False
        result["comment"] = "There is no section with that name."
        return HttpResponse(json.dumps(result))
    section = Section.objects.get(name=section_name)
    if section.instructor != request.user:
        result["success"] = False
        result["comment"] = "The user is not the section's instructor."
        return HttpResponse(json.dumps(result))
    students = [student_section.student for student_section in StudentSection.objects.filter(section=section)]
    questions = [question for question in Question.objects.filter(section=section)]
    students.sort(key=lambda student: student.username)
    questions.sort(key=lambda question: question.label)
    # Format:
    # student name,question label,chosen answer,is answer correct?
    csv = ""
    for student in students:
        for question in questions:
            try:
                response = MCResponse.objects.get(student=student, question=question).response
                answer = response.label
                is_correct = response.is_correct
            except:
                answer = ""
                is_correct = False
            csv += student.username + "," + question.label + "," + answer + "," + str(is_correct) + "\n"
    result["success"] = True
    result["comment"] = "Successfully generated csv."
    result["csv"] = csv
    return HttpResponse(json.dumps(result))

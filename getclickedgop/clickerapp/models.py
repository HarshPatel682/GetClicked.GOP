from __future__ import unicode_literals

from django.db import models

SHORT_STRING_LENGTH = 50
LONG_STRING_LENGTH  = 1000
MULTIPLE_CHOICE = 1
SHORT_ANSWER = 2

# Create your models here.
# An instructor has a name, password hash, and password salt.
class Instructor(models.Model):
    name = models.CharField(max_length=SHORT_STRING_LENGTH)
    password_hash = models.CharField(max_length=SHORT_STRING_LENGTH)
    password_salt = models.CharField(max_length=SHORT_STRING_LENGTH)

# A student has a name, password hash, and password salt.
class Student(models.Model):
    name = models.CharField(max_length=SHORT_STRING_LENGTH)
    password_hash = models.CharField(max_length=SHORT_STRING_LENGTH)
    password_salt = models.CharField(max_length=SHORT_STRING_LENGTH)

# A section has an instructor and a name
class Section(models.Model):
    instructor = models.ForeignKey(Instructor)
    name = models.CharField(max_length=SHORT_STRING_LENGTH)

# Associates students with sections    
class StudentSection(models.Model):
    student = models.ForeignKey(Student)
    section = models.ForeignKey(Section)

# A game has a section and a name    
class Game(models.Model):
    section = models.ForeignKey(Section)
    name = models.CharField(max_length=SHORT_STRING_LENGTH)

# A question has a game, a type (either MULTIPLE_CHOICE or SHORT_ANSWER), and a position specifying
# that it is the nth question in the associated game
class Question(models.Model):
    game = models.ForeignKey(Game)
    type = models.IntegerField()
    position = models.IntegerField()

# A MCAnswer has a question, a label, and an indication of whether it is correct or not
class MCAnswer(models.Model):
    question = models.ForeignKey(Question)
    label = models.CharField(max_length=SHORT_STRING_LENGTH)
    is_correct = models.BooleanField()

# A text/free-form response has a student, a question, and a string response
class TextResponse(models.Model):
    student = models.ForeignKey(Student)
    question = models.ForeignKey(Question)
    response = models.CharField(max_length=LONG_STRING_LENGTH)

# An MCResponse has a student, a question, and an MCAnswer as a response
class MCResponse(models.Model):
    student = models.ForeignKey(Student)
    question = models.ForeignKey(Question)
    response = models.ForeignKey(MCAnswer)


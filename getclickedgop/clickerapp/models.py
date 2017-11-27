from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

SHORT_STRING_LENGTH = 50
LONG_STRING_LENGTH  = 1000
MULTIPLE_CHOICE = 1
SHORT_ANSWER = 2

# Create your models here.

# A section has an instructor and a name
class Section(models.Model):
    instructor = models.ForeignKey(User)
    name = models.CharField(max_length=SHORT_STRING_LENGTH, null=True)

# Associates students with sections    
class StudentSection(models.Model):
    student = models.ForeignKey(User)
    section = models.ForeignKey(Section)

# Only multiple choice questions for now
class Question(models.Model):
    section = models.ForeignKey(Section, default=None)
    label = models.CharField(max_length=LONG_STRING_LENGTH, null=True)

# A MCAnswer has a question, a label, and an indication of whether it is correct or not
class MCAnswer(models.Model):
    question = models.ForeignKey(Question)
    label = models.CharField(max_length=SHORT_STRING_LENGTH, null=True)
    is_correct = models.BooleanField()

# An MCResponse has a student, a question, and an MCAnswer as a response
class MCResponse(models.Model):
    student = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    response = models.ForeignKey(MCAnswer)


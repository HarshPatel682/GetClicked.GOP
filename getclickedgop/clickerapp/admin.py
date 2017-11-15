from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Section)
admin.site.register(StudentSection)
admin.site.register(Game)
admin.site.register(Question)
admin.site.register(MCAnswer)
admin.site.register(TextResponse)
admin.site.register(MCResponse)

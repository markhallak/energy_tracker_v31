from django.contrib import admin
# Register your models here.
from questions.models import Question, QuestionCategory
# Register your models here.
"""class QuestionAdmin(admin.ModelAdmin):
    pass"""

admin.site.register(Question)
admin.site.register(QuestionCategory)

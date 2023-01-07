from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from questions.models import Question

# Each  time the user answers the survey, there will be a diagnosis
class Diagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(_("Creation date"), auto_now=False, auto_now_add=True)
    score = models.FloatField(_("score"))

    def __str__(self):
        return self.id

# Per each diagnosis, the app stores the answers
class Answers(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.BooleanField()
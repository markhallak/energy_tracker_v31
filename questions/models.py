from django.db import models

# Create your models here.
class QuestionCategory(models.Model):
    name = models.CharField(max_length = 100)
    description =  models.TextField()
    def __str__(self):
            return self.name
            
class Question(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    category = models.ForeignKey(QuestionCategory,on_delete=models.CASCADE)
    score_yes = models.FloatField()
    score_no = models.FloatField()

    def __str__(self):
            return self.name


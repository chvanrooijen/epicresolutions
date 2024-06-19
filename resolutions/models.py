from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Cause(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Resolution(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    positive_action = models.CharField(max_length=200)
    trigger = models.CharField(max_length=200)
    goal = models.CharField(max_length=200)
    incentive = models.CharField(max_length=200)
    negative_action = models.CharField(max_length=200)
    def __str__(self):
        return self.positive_action

from django.db import models


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name'] # order by name


class Cause(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Resolution(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    causes = models.ManyToManyField(Cause)
    positive_action = models.CharField(max_length=200)
    trigger = models.CharField(max_length=200)
    goal = models.CharField(max_length=200)
    incentive = models.CharField(max_length=200)
    negative_action = models.CharField(max_length=200)

    def __str__(self):
        return self.positive_action

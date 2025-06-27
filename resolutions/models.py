from django.db import models
import re


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name'] # order by name


class Domain(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


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
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=200, blank=True)  # User-friendly label
    related_resolutions = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.label if self.label else self.positive_action
    
    @property
    def display_label(self):
        """Return the label if available, otherwise use positive_action"""
        return self.label if self.label else self.positive_action

    def get_article(self, word):
        return 'an' if word[0].lower() in 'aeiou' else 'a'

    def capitalize_sentence(self, sentence):
        return sentence[0].upper() + sentence[1:]

    def capitalize_i(self, sentence):
        # Use regex to find standalone "i" and capitalize it, including cases with contractions
        return re.sub(r'\bi\b(?=\s|$|\'m|\'ve|\'ll|\'d|\'re|\'s|\'t)', 'I', sentence)

    def to_sentence(self):
        causes = ', '.join(cause.name.lower() for cause in self.causes.all())
        article = self.get_article(self.role.name.lower())
        sentence = (f"As {article} {self.role.name.lower()}, i {self.positive_action.lower()}, "
                    f"{self.trigger.lower()}, to {self.goal.lower()}, and {self.incentive.lower()}, "
                    f"rather than {self.negative_action.lower()}. "
                    f"Causes: {causes}.")
        sentence = self.capitalize_sentence(sentence)
        return self.capitalize_i(sentence)
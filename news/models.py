from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200)

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-pub_date']
    
class Comment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField('date published')
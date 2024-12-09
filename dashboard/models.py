from django.db import models
from django.utils import timezone

# Create your models here.
class PDFDownloadLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    roles = models.ManyToManyField('resolutions.Role')
    resolutions = models.ManyToManyField('resolutions.Resolution')
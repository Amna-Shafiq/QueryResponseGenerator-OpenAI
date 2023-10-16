from django.db import models

class Question(models.Model):
    query = models.CharField(max_length=300)
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.query
from django.db import models

class Subscriber(models.Model):
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=70)

    def __str__(self):
        return self.name
    
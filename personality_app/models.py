from django.db import models

# Create your models here.

class TwitterUser(models.Model):
    username = models.CharField(max_length=100)
    # Add other fields as needed

    # Personality traits
    openness = models.FloatField()
    conscientiousness = models.FloatField()
    extraversion = models.FloatField()
    agreeableness = models.FloatField()
    neuroticism = models.FloatField()

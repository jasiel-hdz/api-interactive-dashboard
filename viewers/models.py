from django.db import models

class Viewer(models.Model):
    location_id = models.IntegerField()
    period_start = models.DateTimeField()
    period_start_date = models.DateField()
    period_start_time = models.TimeField()
    
    very_happy = models.FloatField()
    happy = models.FloatField()
    neutral = models.FloatField()
    unhappy = models.FloatField()
    very_unhappy = models.FloatField()
    
    gender = models.IntegerField()
    age = models.IntegerField()
    dwell_time_in_tenths_of_sec = models.IntegerField()
    attention_time_in_tenths_of_sec = models.IntegerField()
    age_value = models.IntegerField()
    
    def __str__(self):
        return str(self.location_id)
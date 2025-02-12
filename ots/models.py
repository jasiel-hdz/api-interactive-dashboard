from django.db import models

class OTS(models.Model):
    location_id = models.IntegerField()
    period_start = models.DateTimeField()
    period_start_date = models.DateField()
    period_start_time = models.TimeField()
    ots_count = models.IntegerField()
    duration = models.IntegerField()
    watcher_count = models.IntegerField()
    
    def __str__(self):
        return str(self.location_id)
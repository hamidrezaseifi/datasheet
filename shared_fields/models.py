from django.db import models


class ActionLog(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    action = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.message} by {self.user or 'Anonymous'} at {self.created_at}"

    class Meta:
        db_table = 'action_log'
        managed = True

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

from jobs.models import Job


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    applied_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Application by {self.user.username} for {self.job.title}"

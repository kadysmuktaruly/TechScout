from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    posted_date = models.DateTimeField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_remote = models.BooleanField(default=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs", null=True, blank=True)


    def __str__(self):
        return self.title
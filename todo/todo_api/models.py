from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.CharField(max_length = 100)
    time = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    status = models.BooleanField(default = False, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.task    

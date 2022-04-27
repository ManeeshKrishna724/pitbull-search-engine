from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Search(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    search = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.search)


class FreezeHistory(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    freeze_history = models.BooleanField(default=False)
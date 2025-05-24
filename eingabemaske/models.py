# eingabemaske/models.py
from django.db import models


class UserData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'eingabe'

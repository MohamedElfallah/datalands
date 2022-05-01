from django.db import models

# Create your models here.

class Freecodecamp(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(blank=True, null=True, )
    link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'freecodecamp'
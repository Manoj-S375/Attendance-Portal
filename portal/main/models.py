from django.db import models

# Create your models here.
class Login(models.Model):
    uid = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'login'

class Detail(models.Model):
    regno = models.IntegerField(primary_key=True)
    rname = models.CharField(max_length=10)
    dob = models.DateField()
    course = models.CharField(max_length=10)
    ryear = models.CharField(max_length=7)
    address = models.CharField(max_length=20)
    phone = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'detail'

class Attend(models.Model):
    regno = models.CharField(max_length = 12)
    subj = models.CharField(max_length = 3)
    adate = models.DateField()

    class Meta:
        db_table = 'attend'
        constraints = [
            models.UniqueConstraint(fields = ['regno','subj','adate'], name = 'key')
        ]
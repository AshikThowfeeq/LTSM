from django.db import models

class datatable(models.Model):
    roll_no = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    email_id = models.CharField(max_length=100,primary_key=True)
    batch = models.CharField(max_length=50)
    mentor_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.email_id

class attendancetable(models.Model):
    email_id = models.ForeignKey(datatable, on_delete=models.CASCADE,related_name='datas')
    date = models.DateField(null=True)
    hour_1 = models.BooleanField(default=False)
    hour_2 = models.BooleanField(default=False)
    hour_3 = models.BooleanField(default=False)
    hour_4 = models.BooleanField(default=False)
    hour_5 = models.BooleanField(default=False)
    hour_6 = models.BooleanField(default=False)
    hour_7 = models.BooleanField(default=False)
    hour_8 = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.email_id.email_id}, {self.date}"
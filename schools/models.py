from django.db import models
from faker import Faker
import uuid

class School(models.Model):
    name        = models.CharField(max_length=20)
    maxStudent  = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        fake = Faker()
        # User Faker to populate empty School Name
        if bool(self.name) == False:
            self.name = fake.company()[:20]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Student(models.Model):
    firstName = models.CharField(max_length=20)
    lastName  = models.CharField(max_length=20)
    studentId = models.CharField(max_length=20, unique=True, editable=False) 
    school    = models.ForeignKey(School, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        fake = Faker()
        # User Faker to random Name for Empty field
        if bool(self.firstName) == False: self.firstName = fake.name().split()[0][:20]
        if bool(self.lastName)  == False: self.lastName  = fake.name().split()[1][:20]
        if bool(self.studentId) == False: self.studentId = uuid.uuid4().hex[:20]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.firstName+' '+self.lastName
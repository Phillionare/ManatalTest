from django.db import models
import uuid

class School(models.Model):
    name        = models.CharField(max_length=20)
    maxStudent  = models.IntegerField()

    def save(self, *args, **kwargs):
        # we can validate the duplicate for StudentId here if nessessary but will cause of performance
        if self.studentId is None:
            self.studentId = uuid.uuid4().hex[:20]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Student(models.Model):
    firstName = models.CharField(max_length=20)
    lastName  = models.CharField(max_length=20)
    studentId = models.CharField(max_length=20, unique=True, editable=False) 
    school    = models.ForeignKey(School, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # we can validate the duplicate for StudentId here if nessessary but will cause of performance
        if self.studentId is None:
            self.studentId = uuid.uuid4().hex[:20]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.firstName+' '+self.lastName
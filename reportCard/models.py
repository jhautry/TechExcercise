from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)
    grade = models.FloatField(default=-1)
    def __unicode__(self):
        return "%s: %.2f"%(self.name, self.grade)

class Assignment(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    possible = models.IntegerField(default=0)
    def __unicode__(self):
        return "%s: %d/%d"%(self.name, self.points, self.possible)

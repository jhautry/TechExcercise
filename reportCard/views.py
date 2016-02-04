from django.shortcuts import render
from django.http import HttpResponse

from reportCard.models import Course, Assignment


# Create your views here.
def index(request):
    updateGrades()
    courseList = Course.objects.all()
    courseListText = "<p>List of courses:</p><p>"
    for c in courseList:
        if c.grade == -1:
	    courseListText += "{}: No grade - <a href=\"http://jhautrytechex.ddns.net:8000/{}\">Edit Course</a> - <a href=\"http://google.com\">Delete</a><br>".format(c.name, c.id)
        else:
	    courseListText += "{}: ".format(c.name) + "{0:.2f}%".format(c.grade*100) + " - <a href=\"http://jhautrytechex.ddns.net:8000/{}\">Edit Course</a> - <a href=\"http://google.com\">Delete</a><br>".format(c.id)
    courseListText += """</p><p>
    <form>
    New Course: <input type="text" name="newCourse"> 
    <input type="submit" value="Create">
    </form>
    </p>"""
    return HttpResponse(courseListText)

def assignList(request, c_id):
    aList = Assignment.objects.filter(course_id=c_id)
    cName = (Course.objects.get(id=c_id)).name
    output = "<p>List of assignments for {}:</p><p>".format(cName)
    for a in aList:
	output += "{}: {}/{} - <a href=\"http://google.com\">Delete</a><br>".format(a.name, a.points, a.possible)
    output += """</p><p>
    <form>
    New Assignment: <input type="text" name="newCourse">
    <input type="submit" value="Create">
    </form>
    </p>"""
    return HttpResponse(output)

def updateGrade(c_id):
    assignmentList = Assignment.objects.filter(course_id=c_id)
    totalpoints = 0
    totalposs = 0
    for a in assignmentList:
	totalpoints += a.points
	totalposs += a.possible
    if totalposs == 0:
	updatedGrade = -1
    else:
        updatedGrade = float(totalpoints)/float(totalposs)
    Course.objects.filter(id=c_id).update(grade=updatedGrade)

def updateGrades():
    courseList = Course.objects.all()
    for c in courseList:
	updateGrade(c.id)

from django.shortcuts import render
from django.http import HttpResponse

from reportCard.models import Course, Assignment


# Create your views here.
def index(request):
    newCourseName = request.GET.get("newcourse", None)
    if newCourseName != "" and newCourseName != None:
        addCourse(newCourseName)
    deleteCourseID = request.GET.get("delete", None)
    if deleteCourseID != None:
	remCourse(deleteCourseID)
    updateGrades()
    courseList = Course.objects.all()
    courseListText = "<p>List of courses:</p><p>"
    for c in courseList:
        if c.grade == -1:
	    courseListText += "{}: No grade - <a href=\"http://jhautrytechex.ddns.net:8000/{}\">Edit Course</a> - <a href=\"http://jhautrytechex.ddns.net:8000/?delete={}\">Delete</a><br>".format(c.name, c.id, c.id)
        else:
	    courseListText += "{}: ".format(c.name) + "{0:.2f}%".format(c.grade*100) + " - <a href=\"http://jhautrytechex.ddns.net:8000/{}\">Edit Course</a> - <a href=\"http://jhautrytechex.ddns.net:8000/?delete={}\">Delete</a><br>".format(c.id, c.id)
    courseListText += """</p><p>
    <form>
    New Course: <input type="text" name="newcourse" size="20"> 
    <input type="submit" value="Create">
    </form>
    </p>"""
    return HttpResponse(courseListText)

def assignList(request, c_id):
    newAssignName = request.GET.get("newassign", None)
    newAssignPnts = request.GET.get("points", None)
    newAssignPoss = request.GET.get("poss", None)
    if newAssignName != None and newAssignPnts != None and newAssignPoss != None:
	addAssign(newAssignName, int(newAssignPnts), int(newAssignPoss), c_id)
    deleteAssignID = request.GET.get("delete", None)
    if deleteAssignID != None:
        remAssign(deleteAssignID)
    aList = Assignment.objects.filter(course_id=c_id)
    cName = (Course.objects.get(id=c_id)).name
    output = "<p>List of assignments for {}:</p><p>".format(cName)
    for a in aList:
	output += "{}: {}/{} - <a href=\"http://jhautrytechex.ddns.net:8000/{}/?delete={}\">Delete</a><br>".format(a.name, a.points, a.possible, c_id, a.id)
    output += """</p><p>
    <form>
    New Assignment: <input type="text" name="newassign" size="20"><br>
    score: <input type="text" name="points" size="4"> out of <input type="text" name="poss" size="4">
    <input type="submit" value="Create">
    </form>
    </p><p><a href=\"http://jhautrytechex.ddns.net:8000/\">Back to main</a></p>"""
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

def addCourse(n):
    temp = Course(name=n)
    temp.save()

def remCourse(i):
    temp = Course.objects.get(id=i)
    temp.delete()

def addAssign(n, score, poss, c):
    temp = Assignment(name=n, points=score, possible=poss, course_id=c)
    temp.save()

def remAssign(i):
    temp = Assignment.objects.get(id=i)
    temp.delete()

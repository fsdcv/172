from django.http import HttpResponse
from django.shortcuts import render
from stu_app.models import student, course
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def studentlist(request):
    students = student.objects.all()
    return render(request, 'studentlist.html', {'student_list': students})

def courselist(request):
    courses = course.objects.all()
    return render(request, 'courselist.html', {'course_list': courses})

# def register(request):
#     if request.method == "POST":
#         sid = request.POST.get("student")
#         cid = request.POST.get("course")
#         student_obj = student.objects.get(id=sid)
#         course_obj = course.objects.get(id=cid)
        
#         # Checking if the student is already enrolled in the course
#         if student_obj.courses.filter(id=cid).exists():
#             resp = "<h1>Student with USN %s has already enrolled for the %s</h1>" % (student_obj.usn, course_obj.courseCode)
#             return HttpResponse(resp)
        
#         student_obj.courses.add(course_obj)
#         resp = "<h1>Student with USN %s successfully enrolled for the course with course code %s</h1>" % (student_obj.usn, course_obj.courseCode)
#         return HttpResponse(resp)
    
#     else:
#         students_list = student.objects.all()
#         courses_list = course.objects.all()
#         return render(request, 'register.html', {'student_list': students_list, 'course_list': courses_list})

def register(request):
    if request.method == "POST":
        sid = request.POST.get("student")
        cid = request.POST.get("course")
        try:
            student_obj = student.objects.get(id=sid)
            course_obj = course.objects.get(id=cid)
            
            # Checking if the student is already enrolled in the course
            if student_obj.courses.filter(id=cid).exists():
                message = "Student with USN %s has already enrolled for the %s" % (student_obj.usn, course_obj.courseCode)
                return JsonResponse({'message': message, 'status': 'error'})
            
            student_obj.courses.add(course_obj)
            message = "Student with USN %s successfully enrolled for the course with course code %s" % (student_obj.usn, course_obj.courseCode)
            return JsonResponse({'message': message, 'status': 'success'})
        
        except student.DoesNotExist or course.DoesNotExist:
            return JsonResponse({'message': 'Invalid student or course ID', 'status': 'error'})
    
    else:
        students_list = student.objects.all()
        courses_list = course.objects.all()
        return render(request, 'register.html', {'student_list': students_list, 'course_list': courses_list})

def enrolledStudents(request):
    if request.method == "POST":
        cid = request.POST.get("course")
        course_obj = course.objects.get(id=cid)
        enrolled_students = course_obj.student_set.all()
        return render(request, 'enrolledlist.html', {'course': course_obj, 'student_list': enrolled_students})
    
    else:
        courses_list = course.objects.all()
        return render(request, 'enrolledlist.html', {'Course_List': courses_list})

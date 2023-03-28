from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from university.models import *
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime

# Create your views here.



def main(request):
    return render(request,"login.html")


def allocatestaff(request):
    return render(request,"allocate staff.html")


def clgregist(request):
    return render(request,"college register.html")

def studentregist(request):
    ob = course.objects.all()
    return render(request,"student register.html",{'val':ob})

def staffregist(request):
    ob1 = college.objects.all()
    ob = department.objects.filter(clgid__lid__id=request.session['lid'])
    return render(request,"staff register.html",{'val':ob,'val1':ob1})


def addcomplaint(request):
    ob = complaint.objects.all()
    return render(request,"complaint.html",{'val':ob})

def examschedule(request):
    ob = subject.objects.all()
    return render(request,"Exam.html",{'val':ob})

def adddepartment(request):
    ob=college.objects.all()
    return render(request,"department.html",{'val':ob})


def addcourse(request):
    return render(request,"course.html")


def request_ans(request):
    return render(request,"request answer.html")


def addresult(request):
    return render(request,"Result.html")


def req_revaluation(request):
    return render(request,"Revaluation.html")


def addsubject(request):
    ob = course.objects.all()
    return render(request,"subject.html",{'val':ob})


def uploadanswer(request):
    # ob1=course.objects.all()
    ob = student.objects.all()
    obj = subject.objects.all()
    return render(request,"upload answersheet.html",{'val':ob,'val1':obj})

def adminallocatestaff(request):
    ob = staff.objects.all()

    return render(request,"adminallocatestaff.html",{'val':ob})

def view_allocatestaff(request):
    return render(request,"view/allocate staff.html")

def clg_details(request):
    ob = college.objects.all()
    return render(request,"view/COLLEGE DETAILS.html",{'val':ob})

def view_staff(request):
    return render(request,"view/STAFF.html")

def view_student(request):
    ob = course.objects.all()
    return render(request,"view/STUDENT.html",{'val':ob})

def view_exam(request):
    obj= course.objects.all()


    return render(request,"view/EXAM.html",{'val1':obj})



def search(request):
    subject_id = request.POST['select']
    obj = course.objects.all()
    ob1=exam.objects.filter(subject_id__course_id__id=subject_id)

    return render(request, "view/EXAM.html",{'val':ob1,'val1':obj})

def view_department(request):
    ob = department.objects.all()
    return render(request,"view/DEPARTMENT.html",{'val':ob})

def view_course(request):
    ob = course.objects.all()
    return render(request,"view/view course.html",{'val':ob})

def view_subject(request):
    ob = subject.objects.all()
    return render(request,"view/view subject.html",{'val':ob})

def view_answersheet(request):
    return render(request,"view/REQUESTOF ANSWER.html")

def view_result(request):
    ob = result.objects.all()
    return render(request,"view/RESULT.html",{'val':ob})

def view_revaluation(request):
    return render(request,"view/REVALUATION.html")

def view_complaint(request):
    ob = complaint.objects.filter(replay='pending')
    return render(request,"view/COMPLAINT.html",{'val':ob})


def view_stdcomplaint(request):
    ob = complaint.objects.filter(student_id__lid__id=request.session['lid'])
    return render(request,"view/view stdcomplaint.html",{'val':ob})

def admin(request):
    return render(request,"admin.html")

def stafpage(request):
    return render(request,"staff.html")

def myclg(request):
    return render(request,"college.html")

def stud(request):
    return render(request,"student.html")


def clgreg(request):
    college_name = request.POST['name']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['Pin']
    phone = request.POST['Phone']
    email = request.POST['Email']
    us = request.POST['username']
    pw = request.POST['password']

    ob = login()
    ob.username = us
    ob.password = pw
    ob.utype = 'college'
    ob.save()

    fob = college()
    fob.college_name = college_name
    fob.place = place
    fob.post = post
    fob.pin = pin
    fob.phone = phone
    fob.email = email
    fob.lid = ob
    fob.save()

    return HttpResponse('''<script>alert("Registration Successfull");window.location='/'</script> ''')


# def logn(request):
#     username=request.POST['username']
#     password=request.POST['password']
#     ob=login.objects.get(username=username,password=password)
#     if ob.utype =='admin':
#         return redirect('/admin')
#     elif ob.utype=='college':
#         request.session['lid']=ob.id
#         return redirect('/college')
#     elif ob.utype=='staff':
#         request.session['lid']=ob.id
#
#         return redirect('/staff')
#     elif ob.type=='student':
#         request.session['lid']=ob.id
#
#         return redirect('/student')
#     else:
#         return HttpResponse('''<script>alert("Invalid");window.location='/'</script> ''')

def logn(request):
    username=request.POST['username']
    password=request.POST['password']
    try:
        ob=login.objects.get(username=username,password=password)
        if ob.utype == 'admin':
            return HttpResponse('''<script>alert("welcome  to adminhome ");window.location='/admin'</script>''')
        elif ob.utype == 'college':
            request.session['lid'] = ob.id
            return HttpResponse('''<script>alert("welcome college ");window.location='/myclg'</script>''')
        elif ob.utype == 'staff':
            request.session['lid'] = ob.id
            return HttpResponse('''<script>alert("welcome staff ");window.location='/stafpage'</script>''')
        elif ob.utype == 'student':
            request.session['lid']=ob.id
            return HttpResponse('''<script>alert("welcome student ");window.location='/stud'</script>''')
        else:
            return HttpResponse('''<script>alert("invalid ");window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert("invalid ");window.location='/'</script>''')


def stfreg(request):
    name = request.POST['name']
    place = request.POST['Place']
    gender=request.POST['radiobutton']
    post = request.POST['Post']
    department_id = request.POST['select']

    pin = request.POST['Pin']
    phone = request.POST['Phone']
    email = request.POST['Email']
    us = request.POST['username']
    pw = request.POST['password']

    ob = login()
    ob.username = us
    ob.password = pw
    ob.utype = 'staff'
    ob.save()

    sob = staff()
    sob.name = name
    sob.place = place
    sob.gender = gender
    sob.post = post
    sob.college_id = college.objects.get(lid__id=request.session['lid'])
    sob.department_id=department.objects.get(id=department_id)
    sob.pin = pin
    sob.phone = phone
    sob.email = email
    sob.lid = ob
    sob.save()

    return HttpResponse('''<script>alert("Registration Successfull");window.location='/staffregist'</script> ''')


def stdreg(request):
    name = request.POST['name']
    place = request.POST['Place']
    gender=request.POST['radiobutton']
    post = request.POST['Post']
    course_id = request.POST['select']
    pin = request.POST['Pin']
    phone = request.POST['Phone']
    email = request.POST['Email']
    us = request.POST['username']
    pw = request.POST['password']

    ob = login()
    ob.username = us
    ob.password = pw
    ob.utype = 'student'
    ob.save()

    sob = student()
    sob.name = name
    sob.place = place
    sob.gender = gender
    sob.post = post
    sob.pin = pin
    sob.phone = phone
    sob.email = email
    sob.course_id = course.objects.get(id=course_id)
    sob.lid = ob
    sob.save()

    return HttpResponse('''<script>alert("Registration Successfull");window.location='/'</script> ''')


def exambtn(request):
    date = request.POST['date']
    time = request.POST['time']
    subject_id=request.POST['select']

    eob = exam()
    eob.date = date
    eob.time = time
    eob.subject_id=subject.objects.get(id=subject_id)
    eob.save()

    return HttpResponse('''<script>alert("Registration Successfull");window.location='/'</script> ''')

def deptbtn(request):
    dept = request.POST['dept']
    clg = request.POST['select']

    dob = department()
    dob.dept = dept
    dob.clgid=college.objects.get(id=clg)

    dob.save()

    return HttpResponse('''<script>alert("department added");window.location='/view_department'</script> ''')


def coursebtn(request):
    course_name = request.POST['course']
    course_code = request.POST['code']
    department_id = request.POST['select']

    dob = course()
    dob.course_name = course_name
    dob.course_code = course_code
    dob.department_id=department.objects.get(id=department_id)

    dob.save()

    return HttpResponse('''<script>alert("course added");window.location='/view_course'</script> ''')


def subjbtn(request):
    subject1 = request.POST['subject']
    semester = request.POST['select']
    course_id = request.POST['select']

    dob = subject()
    dob.subject = subject1
    dob.semester = semester
    dob.course_id=course.objects.get(id=course_id)

    dob.save()

    return HttpResponse('''<script>alert("subject added");window.location='/view_subject'</script> ''')


def delete(request,id):
    ob=subject.objects.get(id=id)
    ob.delete()

    return HttpResponse('''<script>alert("subject deleted");window.location='/view_subject'</script> ''')



def complaintbtn(request):
    postcomplaint = request.POST['Complaint']

    ob = complaint()
    ob.datetime = datetime.today()
    ob.postcomplaint = postcomplaint
    ob.replay = "pending"

    ob.student_id = student.objects.get(lid_id=request.session['lid'])
    ob.save()

    return HttpResponse('''<script>alert("complaint added");window.location='/view_stdcomplaint'</script> ''')


def reply(request,id):
    request.session['cid']=id
    return render(request,"replay.html")

def compreply(request):
    replay = request.POST['replay']

    ob = complaint.objects.get(id=request.session['cid'])
    ob.replay=replay

    ob.save()

    return HttpResponse('''<script>alert("send Successfull");window.location='/view_complaint'</script> ''')


def updanswer(request):
    answerpapper = request.FILES['file']
    ans=FileSystemStorage()
    a=ans.save(answerpapper.name,answerpapper)
    student_id = request.POST['select']
    subject_id = request.POST['select']


    ob = answersheet()
    ob.datetime = datetime.today()
    ob.student_id = student.objects.get(id=student_id)
    ob.subject_id = subject.objects.get(id=subject_id)
    ob.answerpapper = a
    ob.save()

    return HttpResponse('''<script>alert("send Successfull");window.location='/'</script> ''')









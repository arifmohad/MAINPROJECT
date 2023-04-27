from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from university.models import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from datetime import datetime
from django.db import connection
# Create your views here.



def main(request):
    return render(request,"loginindex.html")


def allocatestaff(request):
    ob = staff_allocation.objects.all()
    return render(request,"allocate staff.html",{'val':ob})


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
    ob = department.objects.all()
    return render(request,"course.html",{'val':ob})


def request_ans(request):
    ob = request_answersheet.objects.filter(student_id__lid__id=request.session['lid'])
    return render(request,"stdreqanswer.html",{'val':ob})

def request_ansadd(request):
    ob = answersheet.objects.filter(student_id__lid__id=request.session['lid'])
    return render(request,"view/REQUESTOF ANSWER.html",{'val':ob})


def addresult(request):
    return render(request,"Result.html")


def req_revaluation(request):
    return render(request,"Revaluation.html")


def addsubject(request):
    ob = course.objects.all()
    return render(request,"subject.html",{'val':ob})


def searchcrs(request):
    dep = request.GET['dep']
    sob = student.objects.filter(course_id__department_id__clgid__lid__id=request.session['lid'],course_id__id=dep)
    data = []
    for r in sob:
        row = {"id": r.id, "name": r.name}
        data.append(row)
    res = {"res": data}
    print(res)
    print(res)
    return JsonResponse(res)

def uploadanswer(request):
    ob1=course.objects.all()
    ob = student.objects.all()
    obj = exam.objects.all()
    return render(request,"upload answersheet.html",{'val':ob,'val1':obj,'v':ob1})

def adminallocatestaff(request):
    obj = exam.objects.all()
    result=[]
    for i in obj:
        obans=answersheet.objects.filter(exam_id__id=i.id)
        cans=len(obans)

        ob = staff_allocation.objects.filter(answersheet_id__exam_id__id=i.id)
        rcount=cans-len(ob)
        i.count=rcount
        print(i.subject_id.subjects)
        if i.count>0:
            result.append(i)

    return render(request,"adminallocatestaff.html",{'val':ob,'val1':result})

def allocstf(request,id):
    request.session['eid']=id
    ob = staff.objects.all()
    return render(request,"allocation2.html",{'val':ob})


def view_ansrequest(request):
    ob = request_answersheet.objects.all()
    return render(request,"view ansrequest.html",{'val':ob})

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

def view_adminexam(request):
    obj=exam.objects.all()



    return render(request,"view/view_examadmin.html",{'val':obj})

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
    return render(request,"admin index.html")

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

    return HttpResponse('''<script>alert("Registration Successfull");window.location='/clg_details'</script> ''')


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
    username=request.POST['uname']
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
    regno= request.POST['rgno']
    name = request.POST['name']
    father_name = request.POST['fname']
    mother_name = request.POST['mname']
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
    sob.regno = regno
    sob.name = name
    sob.father_name = father_name
    sob.mother_name = mother_name
    sob.place = place
    sob.gender = gender
    sob.post = post
    sob.pin = pin
    sob.phone = phone
    sob.email = email
    sob.course_id = course.objects.get(id=course_id)
    sob.lid = ob
    sob.save()

    return HttpResponse('''<script>alert("Registration Successfull");window.location='/studentregist'</script> ''')


def exambtn(request):
    date = request.POST['date']
    time = request.POST['time']
    subject_id=request.POST['select']

    eob = exam()
    eob.date = date
    eob.time = time
    eob.subject_id=subject.objects.get(id=subject_id)
    eob.save()

    return HttpResponse('''<script>alert("exam schedule added");window.location='/view_adminexam'</script> ''')

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
    department_id = request.POST['select']

    dob = course()
    dob.course_name = course_name
    dob.department_id=department.objects.get(id=department_id)

    dob.save()

    return HttpResponse('''<script>alert("course added");window.location='/view_course'</script> ''')


def subjbtn(request):
    subjects = request.POST['subject']
    semester = request.POST['select1']
    course_id = request.POST['select']

    dob = subject()
    dob.subjects = subjects
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

def approve(request,id):
    obj=request_answersheet.objects.get(id=id)
    obj.status='approved'
    obj.save()
    return redirect('/view_ansrequest')

def reject(request,id):
    obj=request_answersheet.objects.get(id=id)
    obj.status='rejected'
    obj.save()
    return redirect('/view_ansrequest')


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
    student_id = request.POST['select1']
    exam_id = request.POST['select3']

    ob = answersheet()
    ob.student_id = student.objects.get(id=student_id)
    ob.exam_id = exam.objects.get(id=exam_id)
    ob.answerpapper = a
    ob.date=datetime.today()
    ob.save()
    return HttpResponse('''<script>alert("send Successfull");window.location='/uploadanswer'</script> ''')


def admin_staffaloc(request):
    sno = request.POST['sheetnum']
    sid = request.POST['select']
    eid=request.session['eid']
    obstaff=staff.objects.get(id=sid)

    with connection.cursor() as cursor:
        cursor.execute("SELECT `id` FROM `university_answersheet` WHERE `id` NOT IN(SELECT `answersheet_id_id` FROM `university_staff_allocation`) AND `exam_id_id`="+str(eid)+" LIMIT "+str(sno))
        row = cursor.fetchall()
        print(row,"++++++++++++++++++++++++++++++++++++")
        for i in row:
            obans=answersheet.objects.get(id=i[0])
            ob=staff_allocation()
            ob.staff_id=obstaff
            ob.answersheet_id=obans
            ob.datetime=datetime.today()
            ob.score='0'
            ob.status='pending'
            ob.save()
    return HttpResponse('''<script>alert("allocated");window.location='/allocstf'</script> ''')


def staffaloc(request):
    score = request.POST['subject']
    status = request.POST['select']
    answersheet_id = request.POST['select']
    staff_id = request.POST['select']
    dob = staff_allocation()
    dob.score = score
    dob.status = status
    dob.datetime = datetime.today()

    dob.answersheet_id = staff_allocation.objects.get(id=answersheet_id)
    dob.staff_id = staff_allocation.objects.get(id=staff_id)

    dob.save()

    return HttpResponse('''<script>alert("subject added");window.location='/'</script> ''')


def reqansbtn(request):
    subjects = request.POST['select']
    ob = request_answersheet()
    ob.datetime = datetime.today()
    ob.status = "pending"
    ob.answersheet_id = answersheet.objects.get(id=subjects)
    ob.student_id = student.objects.get(lid_id=request.session['lid'])
    ob.save()

    return HttpResponse('''<script>alert("reques successs");window.location='/request_ans'</script> ''')









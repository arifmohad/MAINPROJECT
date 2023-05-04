import base64

import os
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from university.AESCLASS import encrypt, decrypt
from university.models import *
from django.http import HttpResponse, JsonResponse, request
from django.shortcuts import redirect
from datetime import datetime
from django.db import connection
# Create your views here.
import hashlib
import boto
import boto.s3
import sys
from boto.s3.key import Key



AWS_ACCESS_KEY_ID = 'AKIAVTA624LZIZKAIXO3'
AWS_SECRET_ACCESS_KEY = 'jPUOKXCYy1JyFnLxIyotub+rW+2gVtFe1zgKdH9h'


def main(request):
    return render(request,"loginindex.html")

@login_required(login_url='/')
def allocatestaff(request,id):
    ob = staff_allocation.objects.get(id=id)
    request.session['stalid']=id
    return render(request,"allocate staff.html",{'val':ob})

@login_required(login_url='/')
def revallocatestaff(request,id):
    ob = stafrevalallocation.objects.get(id=id)
    request.session['stalid']=id
    return render(request,"revalmark.html",{'val':ob})

@login_required(login_url='/')
def allocatestaffbtn(request):
    score=request.POST['Score']
    status=request.POST['Status']
    ob=staff_allocation.objects.get(id=request.session['stalid'])
    ob.score=score
    ob.status=status
    ob.save()
    return HttpResponse('''<script>alert("updated");window.location='/stfwork'</script>''')

@login_required(login_url='/')
def revallocatestaffbtn(request):
    score=request.POST['Score']
    status=request.POST['Status']

    ob=stafrevalallocation.objects.get(id=request.session['stalid'])

    ob.status=status
    ob.save()
    aid=ob.revaluation_id.answersheet_id.id
    aob=staff_allocation.objects.get(answersheet_id__id=aid)
    if int(aob.score)<int(score):
        aob.score=score
        aob.save()

    return HttpResponse('''<script>alert("updated");window.location='/stfrevwork'</script>''')



@login_required(login_url='/')
def clgregist(request):
    return render(request,"college register.html")


@login_required(login_url='/')
def studentregist(request):
    # department_id
    ob=staff.objects.get(lid__id=request.session['lid'])
    did=ob.department_id.id
    ob = course.objects.filter(department_id__id=did)
    return render(request,"student register.html",{'val':ob})


@login_required(login_url='/')
def staffregist(request):
    ob1 = college.objects.all()
    ob = department.objects.filter(clgid__lid__id=request.session['lid'])
    return render(request,"staff register.html",{'val':ob,'val1':ob1})

@login_required(login_url='/')
def addcomplaint(request):
    ob = complaint.objects.all()
    return render(request,"complaint.html",{'val':ob})
@login_required(login_url='/')
def examschedule(request):
    ob = subject.objects.values('subjects','course_id__course_name').distinct()
    print(ob,"===================")
    return render(request,"Exam.html",{'val':ob})
@login_required(login_url='/')
def adddepartment(request):
    ob=college.objects.all()
    return render(request,"department.html",{'val':ob})

@login_required(login_url='/')
def addcourse(request):
    ob = department.objects.all()
    return render(request,"course.html",{'val':ob})

@login_required(login_url='/')
def request_ans(request):
    ob = request_answersheet.objects.filter(student_id__lid__id=request.session['lid'])
    return render(request,"stdreqanswer.html",{'val':ob})


@login_required(login_url='/')
def request_ansadd(request):
    ob = answersheet.objects.filter(student_id__lid__id=request.session['lid'])
    return render(request,"view/REQUESTOF ANSWER.html",{'val':ob})

@login_required(login_url='/')
def addresult(request):
    return render(request,"Result.html")

@login_required(login_url='/')
def req_revaluation(request):
    ob = stafrevalallocation.objects.filter(revaluation_id__answersheet_id__student_id__lid__id=request.session['lid'])

    return render(request,"Revaluation.html",{'val':ob})

@login_required(login_url='/')
def addsubject(request):
    ob = course.objects.all()
    return render(request,"subject.html",{'val':ob})

@login_required(login_url='/')
def searchcrs(request):
    dep = request.GET['dep']
    sob = student.objects.filter(course_id__department_id__clgid__lid__id=request.session['lid'],course_id__id=dep)
    data = []
    for r in sob:
        row = {"id": r.id, "name": r.name,"rno":r.regno}
        data.append(row)
    res = {"res": data}
    print(res)
    print(res)
    return JsonResponse(res)

@login_required(login_url='/')
def uploadanswer(request):
    ob1=course.objects.filter(department_id__clgid__lid=request.session['lid'])
    ob = student.objects.all()
    obj = exam.objects.filter(subject_id__course_id__department_id__clgid__lid=request.session['lid'])
    return render(request,"upload answersheet.html",{'val':ob,'val1':obj,'v':ob1})
@login_required(login_url='/')
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

@login_required(login_url='/')
def allocstf(request,id):
    request.session['eid']=id
    ob = staff.objects.all()
    return render(request,"allocation2.html",{'val':ob})

@login_required(login_url='/')
def view_ansrequest(request):
    ob = request_answersheet.objects.all()
    return render(request,"view ansrequest.html",{'val':ob})
@login_required(login_url='/')
def view_allocatestaff(request):
    ob = staff_allocation.objects.all()
    return render(request,"view/allocate staff.html",{'val':ob})
@login_required(login_url='/')
def clg_details(request):
    ob = college.objects.all()
    return render(request,"view/COLLEGE DETAILS.html",{'val':ob})



@login_required(login_url='/')
def view_staff(request):
    return render(request,"view/STAFF.html")
@login_required(login_url='/')
def view_student(request):
    ob = student.objects.filter(staff_id__lid__id=request.session['lid'])
    return render(request,"view/STUDENT.html",{'val':ob})


@login_required(login_url='/')
def view_exam(request):
    obj= course.objects.all()


    return render(request,"view/EXAM.html",{'val1':obj})

@login_required(login_url='/')
def view_examstaff(request):
    obj= course.objects.all()


    return render(request,"view/staffviewexam.html",{'val1':obj})


@login_required(login_url='/')
def view_examstudent(request):
    obj= course.objects.all()


    return render(request,"view/view exam student.html",{'val1':obj})

@login_required(login_url='/')
def view_adminexam(request):
    obj=exam.objects.all()



    return render(request,"view/view_examadmin.html",{'val':obj})

@login_required(login_url='/')
def search(request):
    subject_id = request.POST['select']
    obj = course.objects.all()
    ob1=exam.objects.filter(subject_id__course_id__id=subject_id)

    return render(request, "view/EXAM.html",{'val':ob1,'val1':obj})

@login_required(login_url='/')
def searchstaff(request):
    subject_id = request.POST['select']
    obj = course.objects.all()
    ob1=exam.objects.filter(subject_id__course_id__id=subject_id)


    return render(request, "view/staffviewexam.html",{'val':ob1,'val1':obj})

@login_required(login_url='/')
def searchstud(request):
    subject_id = request.POST['select']
    obj = course.objects.all()
    ob1=exam.objects.filter(subject_id__course_id__id=subject_id)


    return render(request, "view/view exam student.html",{'val':ob1,'val1':obj})


@login_required(login_url='/')
def searchresult(request):
    subject_id = request.POST['select']
    obj = course.objects.all()
    ob1=staff_allocation.objects.filter(answersheet_id__exam_id__subject_id__course_id__id=subject_id,answersheet_id__student_id__course_id__department_id__clgid__lid__id=request.session['lid'],status='finish')


    return render(request, "view/clgviewresult.html",{'val':ob1,'val1':obj})


@login_required(login_url='/')
def view_department(request):
    ob = department.objects.all()
    return render(request,"view/DEPARTMENT.html",{'val':ob})

@login_required(login_url='/')
def view_course(request):
    ob = course.objects.all()
    return render(request,"view/view course.html",{'val':ob})

@login_required(login_url='/')
def view_subject(request):
    ob = subject.objects.all()
    return render(request,"view/view subject.html",{'val':ob})

@login_required(login_url='/')
def view_answersheet(request):
    return render(request,"view/REQUESTOF ANSWER.html")

@login_required(login_url='/')
def view_result(request):
    ob = staff_allocation.objects.filter(answersheet_id__student_id__lid__id=request.session['lid'],status='finish')
    res=[]
    for i in ob:
        obb=revaluation.objects.filter(answersheet_id__id=i.answersheet_id.id)
        if(len(obb)>0):
            i.st="y"
        else:
            i.st="n"
        res.append(i)
    print(res[0].st,"============")
    print(res,"============")
    print(res,"============")
    return render(request,"view/RESULT.html",{'val':res})

@login_required(login_url='/')
def view_revaluation(request):
    return render(request,"view/REVALUATION.html")

@login_required(login_url='/')
def view_complaint(request):
    ob = complaint.objects.filter(replay='pending')
    return render(request,"view/COMPLAINT.html",{'val':ob})

@login_required(login_url='/')
def clgresult(request):
    obj=course.objects.all()
    ob = staff_allocation.objects.filter(answersheet_id__student_id__course_id__department_id__clgid__lid__id=request.session['lid'],status='finish')
    return render(request,"view/clgviewresult.html",{'val':ob,'val1':obj})

@login_required(login_url='/')
def stfresult(request):
    obj=course.objects.all()
    ob = staff_allocation.objects.filter(answersheet_id__student_id__staff_id__lid__id=request.session['lid'],status='finish')
    return render(request,"view/stfviewresult.html",{'val':ob,'val1':obj})

@login_required(login_url='/')
def view_stdcomplaint(request):
    ob = complaint.objects.filter(student_id__lid__id=request.session['lid'])
    return render(request,"view/view stdcomplaint.html",{'val':ob})

@login_required(login_url='/')
def stfwork(request):
    ob = staff_allocation.objects.filter(staff_id__lid__id=request.session['lid'])

    return render(request,"staff works.html",{'val':ob})

@login_required(login_url='/')
def stfrevwork(request):
    ob = stafrevalallocation.objects.filter(staff_id__lid__id=request.session['lid'])
    return render(request,"staffrevalworks.html",{'val':ob})




@login_required(login_url='/')
def admin(request):
    return render(request,"admin index.html")
@login_required(login_url='/')
def stafpage(request):
    return render(request,"staffindex.html")
@login_required(login_url='/')
def myclg(request):
    return render(request,"collegeindex.html")
@login_required(login_url='/')
def stud(request):
    return render(request,"student index.html")






@login_required(login_url='/')
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
            request.session['lid'] = ob.id
            ob1=auth.authenticate(username='admin',password='admin')
            auth.login(request,ob1)
            return HttpResponse('''<script>alert("welcome  to adminhome ");window.location='/admin'</script>''')
        elif ob.utype == 'college':
            request.session['lid'] = ob.id
            ob1 = auth.authenticate(username='admin', password='admin')
            auth.login(request, ob1)
            return HttpResponse('''<script>alert("welcome college ");window.location='/myclg'</script>''')
        elif ob.utype == 'staff':
            request.session['lid'] = ob.id
            ob1 = auth.authenticate(username='admin', password='admin')
            auth.login(request, ob1)
            return HttpResponse('''<script>alert("welcome staff ");window.location='/stafpage'</script>''')
        elif ob.utype == 'student':
            request.session['lid']=ob.id
            ob1 = auth.authenticate(username='admin', password='admin')
            auth.login(request, ob1)
            return HttpResponse('''<script>alert("welcome student ");window.location='/stud'</script>''')
        else:
            return HttpResponse('''<script>alert("invalid ");window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert("invalid ");window.location='/'</script>''')

@login_required(login_url='/')
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

@login_required(login_url='/')
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
    sob.staff_id = staff.objects.get(lid__id=request.session['lid'])
    sob.course_id = course.objects.get(id=course_id)
    sob.lid = ob
    sob.save()

    return HttpResponse('''<script>alert("Registration Successfull");window.location='/studentregist'</script> ''')



def stdpass(request):

    return render(request, "update password.html")


@login_required(login_url='/')
def stdpasschange(request):
    oldpass = request.POST['oldpass']
    newpassword = request.POST['password']
    cnfpassword = request.POST['cpassword']
    try:
        ob=login.objects.get(password=oldpass,id=request.session['lid'])
        if  newpassword == cnfpassword:
            ob.password=newpassword
            ob.save()
            return HttpResponse('''<script>alert("change password");window.location='/stdntprofile'</script> ''')
        else:
            return HttpResponse('''<script>alert("mismatch password");window.location='/stdntprofile'</script> ''')
    except:
        return HttpResponse('''<script>alert("incorrect old password");window.location='/stdntprofile'</script> ''')



@login_required(login_url='/')
def exambtn(request):
    date = request.POST['date']
    time = request.POST['time']
    subject_id=request.POST['select']
    sob=subject.objects.filter(subjects=subject_id)
    for i in sob:
        eob = exam()
        eob.date = date
        eob.time = time
        eob.subject_id=subject.objects.get(id=i.id)
        eob.save()
    return HttpResponse('''<script>alert("exam schedule added");window.location='/view_adminexam'</script> ''')

@login_required(login_url='/')
def deptbtn(request):
    dept = request.POST['dept']
    clg = request.POST['select']

    dob = department()
    dob.dept = dept
    dob.clgid=college.objects.get(id=clg)

    dob.save()

    return HttpResponse('''<script>alert("department added");window.location='/view_department'</script> ''')

@login_required(login_url='/')
def coursebtn(request):
    course_name = request.POST['course']
    department_id = request.POST['select']

    dob = course()
    dob.course_name = course_name
    dob.department_id=department.objects.get(id=department_id)

    dob.save()

    return HttpResponse('''<script>alert("course added");window.location='/view_course'</script> ''')

@login_required(login_url='/')
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

@login_required(login_url='/')
def delete(request,id):
    ob=subject.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("subject deleted");window.location='/view_subject'</script> ''')

def deletestudent(request,id):
    ob=student.objects.get(id=id)
    ob.delete()

    return HttpResponse('''<script>alert("student deleted");window.location='/view_student'</script> ''')

@login_required(login_url='/')
def complaintbtn(request):
    postcomplaint = request.POST['Complaint']

    ob = complaint()
    ob.datetime = datetime.today()
    ob.postcomplaint = postcomplaint
    ob.replay = "pending"

    ob.student_id = student.objects.get(lid_id=request.session['lid'])
    ob.save()

    return HttpResponse('''<script>alert("complaint added");window.location='/view_stdcomplaint'</script> ''')

@login_required(login_url='/')
def approve(request,id):
    obj=request_answersheet.objects.get(id=id)
    obj.status='approved'
    obj.save()
    return redirect('/view_ansrequest')


@login_required(login_url='/')
def reject(request,id):
    obj=request_answersheet.objects.get(id=id)
    obj.status='rejected'
    obj.save()
    return redirect('/view_ansrequest')

@login_required(login_url='/')
def reply(request,id):
    request.session['cid']=id
    return render(request,"replay.html")


@login_required(login_url='/')
def compreply(request):
    replay = request.POST['replay']

    ob = complaint.objects.get(id=request.session['cid'])
    ob.replay=replay
    ob.save()
    return HttpResponse('''<script>alert("send Successfull");window.location='/view_complaint'</script> ''')

@login_required(login_url='/')
def updanswer(request):
    answerpapper = request.FILES['file']

    ans=FileSystemStorage()

    a=ans.save(answerpapper.name,answerpapper)



    student_id = request.POST['select1']
    exam_id = request.POST['select3']
    key = "qsdrt"
    ob=answersheet.objects.filter(exam_id__id=exam_id,student_id__id=student_id)
    if len(ob)==0:
        ob = answersheet()
        ob.student_id = student.objects.get(id=student_id)
        ob.exam_id = exam.objects.get(id=exam_id)
        ob.answerpapper = a
        ob.date=datetime.today()
        ob.hashvalue=""
        ob.save()




        sha256_hash = hashlib.sha256()



        print(a,"path=========================")
        with open(r"C:\main project\university_exam_evaluation\media/"+a, "rb") as imageFile:
            for byte_block in iter(lambda: imageFile.read(4096), b""):
                sha256_hash.update(byte_block)
            print(sha256_hash.hexdigest())
        with open(r"C:\main project\university_exam_evaluation\media/" + a, "rb") as imageFile:
            stri = base64.b64encode(imageFile.read()).decode('utf-8')
            enc1 = encrypt(stri, key).decode('utf-8')

            fh = open(r"C:\main project\university_exam_evaluation\media/"+a, "wb")
            fh.write(base64.b64decode(enc1))
            fh.close()

        hashval=str(sha256_hash.hexdigest())
        ob.hashvalue = hashval
        ob.save()

        bucket_name = 'samplebucket1riit'
        conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
                               AWS_SECRET_ACCESS_KEY)

        bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)

        testfile = r"C:\main project\university_exam_evaluation\media/"+a

        namef = a

        def percent_cb(complete, total):
            sys.stdout.write('.')
            sys.stdout.flush()

        k = Key(bucket)
        k.key = namef
        k.set_contents_from_filename(testfile,
                                     cb=percent_cb, num_cb=10)




        return HttpResponse('''<script>alert("send Successfull");window.location='/uploadanswer'</script> ''')
    else:
        return HttpResponse('''<script>alert("already uploaded");window.location='/uploadanswer'</script> ''')

@login_required(login_url='/')
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
    return HttpResponse('''<script>alert("allocated");window.location='/adminallocatestaff'</script> ''')

def admin_revalstaffaloc(request):
    sno = request.POST['sheetnum']
    sid = request.POST['select']
    eid=request.session['eid']
    obstaff=staff.objects.get(id=sid)

    with connection.cursor() as cursor:
        cursor.execute("SELECT `id` FROM `university_revaluation` WHERE `id` NOT IN(SELECT `revaluation_id_id` FROM `university_stafrevalallocation`) AND `answersheet_id_id` IN(SELECT `id` FROM `university_answersheet` WHERE `exam_id_id`="+str(eid)+") LIMIT "+str(sno))
        row = cursor.fetchall()
        print(row,"++++++++++++++++++++++++++++++++++++")
        for i in row:
            obans=revaluation.objects.get(id=i[0])
            ob=stafrevalallocation()
            ob.staff_id=obstaff
            ob.revaluation_id=obans
            ob.datetime=datetime.today()
            ob.status='pending'
            ob.save()
    return HttpResponse('''<script>alert("allocated");window.location='/revalallocatestaff'</script> ''')

@login_required(login_url='/')
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

@login_required(login_url='/')
def reqansbtn(request):
    subjects = request.POST['select']
    ob = request_answersheet()
    ob.datetime = datetime.today()
    ob.status = "pending"
    ob.answersheet_id = answersheet.objects.get(id=subjects)
    ob.student_id = student.objects.get(lid_id=request.session['lid'])
    ob.save()

    return HttpResponse('''<script>alert("reques successs");window.location='/request_ans'</script> ''')


@login_required(login_url='/')
def user_pay_proceed1(request):
    id=request.session['aid']
    ob=revaluation()
    ob.datetime = datetime.today()
    ob.status = "pending"
    ob.answersheet_id = answersheet.objects.get(id=id)
    ob.save()
    return HttpResponse('''<script>alert("reques successs");window.location='/view_result'</script> ''')

@login_required(login_url='/')
def user_pay_proceed(request,id):
    request.session['aid']=id
    import razorpay
    amount = "10000"
    request.session['pay_amount'] = amount
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create({'amount': amount+"00", 'currency': "INR", 'payment_capture': '1'})
    # qry = "select * from user where lid=%s"
    # res = selectone(qry, session['lid'])
    ob=student.objects.filter(lid__id=request.session['lid'])
    return render(request,'UserPayProceed.html', {'p':payment,'val':ob})







@login_required(login_url='/')
def revalallocatestaff(request):
    obj = exam.objects.all()
    result=[]
    for i in obj:
        obans=revaluation.objects.filter(answersheet_id__exam_id__id=i.id)
        cans=len(obans)

        ob = stafrevalallocation.objects.filter(revaluation_id__answersheet_id__exam_id__id=i.id)
        rcount=cans-len(ob)
        i.count=rcount

        if i.count>0:
            result.append(i)

    return render(request,"revalallocation.html",{'val':ob,'val1':result})

@login_required(login_url='/')
def revalallocstf(request,id):
    request.session['eid']=id
    ob = staff.objects.all()
    return render(request,"revalallocationstaff.html",{'val':ob})

@login_required(login_url='/')
def download(request,id):
    ob = staff_allocation.objects.get(id=id)

    path=r"C:\main project\university_exam_evaluation\media\\"+str(ob.answersheet_id.answerpapper)
    key = "qsdrt"
    #
    hv=ob.answersheet_id.hashvalue
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as imageFile:
            stri = base64.b64encode(imageFile.read()).decode('utf-8')
            print(stri)


            dec2 = decrypt(stri, key).decode('utf-8')


            fh1 = open(r"C:\main project\university_exam_evaluation\media\\d_"+str(ob.answersheet_id.answerpapper), "wb")
            fh1.write(base64.b64decode(dec2))
            fh1.close()
    with open(r"C:\main project\university_exam_evaluation\media\\d_"+str(ob.answersheet_id.answerpapper), "rb") as imageFile:
        for byte_block in iter(lambda: imageFile.read(4096), b""):
            sha256_hash.update(byte_block)
        print(sha256_hash.hexdigest())

    hashval = str(sha256_hash.hexdigest())

    if hv==hashval:
        return render(request,"view/clic here to download.html",{'v':"d_"+str(ob.answersheet_id.answerpapper)})
    else:
        return HttpResponse('''<script>alert("the hash value not same");window.location='/stfwork'</script> ''')



@login_required(login_url='/')
def downloadrev(request,id):
    ob = stafrevalallocation.objects.get(id=id)
    path=r"C:\main project\university_exam_evaluation\media\\"+str(ob.revaluation_id.answersheet_id.answerpapper)
    key = "qsdrt"
    #
    hv = ob.revaluation_id.answersheet_id.hashvalue
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as imageFile:
                stri = base64.b64encode(imageFile.read()).decode('utf-8')
                print(stri)


                dec2 = decrypt(stri, key).decode('utf-8')


                fh1 = open(r"C:\main project\university_exam_evaluation\media\\d_"+str(ob.revaluation_id.answersheet_id.answerpapper), "wb")
                fh1.write(base64.b64decode(dec2))
                fh1.close()
    with open(r"C:\main project\university_exam_evaluation\media\\d_" + str(ob.revaluation_id.answersheet_id.answerpapper),
              "rb") as imageFile:
        for byte_block in iter(lambda: imageFile.read(4096), b""):
            sha256_hash.update(byte_block)
        print(sha256_hash.hexdigest())

    hashval = str(sha256_hash.hexdigest())

    if hv == hashval:
        return render(request, "view/clic here to download.html",{'v': "d_" + str(ob.revaluation_id.answersheet_id.answerpapper)})
    else:
        return HttpResponse('''<script>alert("the hash value not same");window.location='/stfrevwork'</script> ''')



@login_required(login_url='/')
def downloadstd(request,id):
    ob = request_answersheet.objects.get(id=id)
    path=r"C:\main project\university_exam_evaluation\media\\"+str(ob.answersheet_id.answerpapper)
    key = "qsdrt"
    #
    with open(path, "rb") as imageFile:
                stri = base64.b64encode(imageFile.read()).decode('utf-8')
                print(stri)


                dec2 = decrypt(stri, key).decode('utf-8')


                fh1 = open(r"C:\main project\university_exam_evaluation\media\\d_"+str(ob.answersheet_id.answerpapper), "wb")
                fh1.write(base64.b64decode(dec2))
                fh1.close()
    return render(request,"view/clic here to download.html",{'v':"d_"+str(ob.answersheet_id.answerpapper)})


@login_required(login_url='/')
def clgprofile(request):
    ob = college.objects.filter(lid__id=request.session['lid'])
    return render(request,"view/clg profile.html",{'val':ob})

@login_required(login_url='/')
def stfprofile(request):
    ob = staff.objects.filter(lid__id=request.session['lid'])
    return render(request,"view/stf profile.html",{'val':ob})

@login_required(login_url='/')
def stdntprofile(request):
    ob = student.objects.filter(lid__id=request.session['lid'])
    return render(request,"view/student profile.html",{'val':ob})

def logout(request):
    auth.logout(request)
    return HttpResponse('''<script>alert("log out");window.location='/'</script> ''')



def paschange(request):
    auth.logout(request)
    return HttpResponse('''<script>alert("log out");window.location='/'</script> ''')









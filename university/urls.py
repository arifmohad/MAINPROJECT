from django.urls import path

from university import views

urlpatterns=[
    path('',views.main,name="main"),
    path('logn', views.logn, name="logn"),
    path('allocatestaff',views.allocatestaff,name="allocatestaff"),
    path('clgregist',views.clgregist,name="clgregist"),
    path('studentregist',views.studentregist,name="studentregist"),
    path('staffregist',views.staffregist,name="staffregist"),
    path('addcomplaint',views.addcomplaint,name="addcomplaint"),
    path('examschedule',views.examschedule,name="examschedule"),
    path('adddepartment',views.adddepartment,name="adddepartment"),
    path('addcourse',views.addcourse,name="addcourse"),
    path('request_ans',views.request_ans,name="request_ans"),
    path('addresult',views.addresult,name="addresult"),
    path('req_revaluation',views.req_revaluation,name="req_revaluation"),
    path('addsubject',views.addsubject,name="addsubject"),
    path('uploadanswer',views.uploadanswer,name="uploadanswer"),
    path('view_allocatestaff',views.view_allocatestaff,name="view_allocatestaff"),
    path('clg_details',views.clg_details,name="clg_details"),
    path('view_staff',views.view_staff,name="view_staff"),
    path('view_student',views.view_student,name="view_student"),
    path('view_exam',views.view_exam,name="view_exam"),
    path('view_department',views.view_department,name="view_department"),
    path('view_course',views.view_course,name="view_course"),
    path('view_subject',views.view_subject,name="view_subject"),
    path('view_answersheet',views.view_answersheet,name="view_answersheet"),
    path('view_result',views.view_result,name="view_result"),
    path('view_revaluation',views.view_revaluation,name="view_revaluation"),
    path('view_complaint',views.view_complaint,name="view_complaint"),
    path('view_stdcomplaint',views.view_stdcomplaint,name="view_stdcomplaint"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('adminallocatestaff', views.adminallocatestaff, name="adminallocatestaff"),
    path('allocstf', views.allocstf, name="allocstf"),

    path('clgreg',views.clgreg,name="clgreg"),
    path('stfreg',views.stfreg,name="stfreg"),
    path('stdreg',views.stdreg,name="stdreg"),
    path('deptbtn', views.deptbtn, name="deptbtn"),
    path('compreply', views.compreply, name="compreply"),
    path('exambtn', views.exambtn, name="exambtn"),
    path('reply/<int:id>', views.reply, name="reply"),
    path('coursebtn', views.coursebtn, name="coursebtn"),
    path('subjbtn', views.subjbtn, name="subjbtn"),
    path('complaintbtn', views.complaintbtn, name="complaintbtn"),
    path('search', views.search, name="search"),
    path('updanswer', views.updanswer, name="updanswer"),
    path('searchcrs', views.searchcrs, name="searchcrs"),
    path('view_adminexam', views.view_adminexam, name="view_adminexam"),
    path('staffaloc', views.staffaloc, name="staffaloc"),
    path('reqansbtn', views.reqansbtn, name="reqansbtn"),


    path('admin',views.admin,name="admin"),
    path('stafpage',views.stafpage,name="stafpage"),
    path('myclg',views.myclg,name="myclg"),
    path('stud',views.stud,name="stud"),



]
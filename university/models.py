from django.db import models

# Create your models here.

class login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    utype=models.CharField(max_length=100)






class college(models.Model):
    lid=models.ForeignKey(login,on_delete=models.CASCADE)
    college_name=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.IntegerField()
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100) 


class department(models.Model):
    dept = models.CharField(max_length=100)
    clgid = models.ForeignKey(college, on_delete=models.CASCADE)

class course(models.Model):
    department_id=models.ForeignKey(department,on_delete=models.CASCADE)
    course_name=models.CharField(max_length=100)


class subject(models.Model):
    course_id=models.ForeignKey(course,on_delete=models.CASCADE)
    subjects=models.CharField(max_length=100)
    semester=models.IntegerField()   




class student(models.Model):
    lid=models.ForeignKey(login,on_delete=models.CASCADE)
    course_id=models.ForeignKey(course,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    regno = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    pin=models.IntegerField()
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100)


class staff(models.Model):
    lid=models.ForeignKey(login,on_delete=models.CASCADE)
    college_id=models.ForeignKey(college,on_delete=models.CASCADE)
    department_id=models.ForeignKey(department,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100)





class exam(models.Model):
    subject_id=models.ForeignKey(subject,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()

class answersheet(models.Model):
    student_id = models.ForeignKey(student, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(exam,on_delete=models.CASCADE)
    answerpapper = models.FileField()
    date = models.DateField()



class staff_allocation(models.Model):
    staff_id=models.ForeignKey(staff,on_delete=models.CASCADE)
    answersheet_id=models.ForeignKey(answersheet,on_delete=models.CASCADE)
    datetime=models.DateField()
    score=models.CharField(max_length=100)
    status=models.CharField(max_length=100)




class complaint(models.Model):
    student_id=models.ForeignKey(student,on_delete=models.CASCADE)
    datetime=models.DateField()
    postcomplaint=models.CharField(max_length=100)
    replay=models.CharField(max_length=100)






class request_answersheet(models.Model):
    student_id=models.ForeignKey(student,on_delete=models.CASCADE)
    answersheet_id=models.ForeignKey(answersheet,on_delete=models.CASCADE)
    datetime=models.DateField()
    status=models.CharField(max_length=100)


class revaluation(models.Model):
    answersheet_id=models.ForeignKey(answersheet,on_delete=models.CASCADE)
    datetime=models.DateField()
    status=models.CharField(max_length=100)


class stafrevalallocation(models.Model):
    revaluation_id=models.ForeignKey(revaluation,on_delete=models.CASCADE)
    staff_id=models.ForeignKey(staff,on_delete=models.CASCADE)
    datetime = models.DateField()
    status = models.CharField(max_length=100)



    

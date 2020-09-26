from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, department=None,password=None,**kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            first_name = first_name,
            last_name  = last_name,
            department = department,
            email      = self.normalize_email(email),
            username   = username
        )



        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            first_name = first_name,
            last_name  = last_name,
            email      = self.normalize_email(email),
            password   = password,
            username   = username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email           = models.EmailField(max_length=50, unique=True)
    username        = models.CharField(max_length=25, unique=True)
    first_name      = models.CharField(max_length=15)
    last_name       = models.CharField(max_length=15)
    department      = models.CharField(max_length=15, blank=True, null=True)
    date_joined     = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)


    is_student      = models.BooleanField(default=False)
    is_teacher      = models.BooleanField(default=False)


    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyUserManager()


    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def name(self):
        return self.first_name+' '+self.last_name





class Teacher(User):
    subject = models.CharField(max_length=15)

    def name(self):
        return self.first_name+' '+self.last_name



class Student(User):
    sap_id      = models.BigIntegerField(primary_key=True)
    division    = models.CharField(max_length=1)

    def name(self):
        return self.first_name+' '+self.last_name


class McqExam(models.Model):
	exam_topic=models.CharField(max_length=20)
	#teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
	def __str__(self):
		return self.exam_topic

	def get_absolute_url(self):
		return reverse("account:list")

class Question(models.Model):
	mcq_exam=models.ForeignKey(McqExam,on_delete=models.CASCADE,related_name='mcq_exam')
	question=models.CharField(max_length=300)
	option_1=models.CharField(max_length=300)
	option_2=models.CharField(max_length=300)
	option_3=models.CharField(max_length=300)
	option_4=models.CharField(max_length=300)
	correct_ans=models.CharField(max_length=1)

	def __str__(self):
		return self.question

	def get_absolute_url(self):
		return reverse("account:list")







class Student_Response(models.Model):
	question=models.ForeignKey(Question,on_delete=models.CASCADE)
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	student_response=models.CharField(max_length=1)

	def __str__(self):
		return 'response'


class Results(models.Model):
    mcq_exam=models.ForeignKey(McqExam,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    obtained_marks=models.CharField(max_length=9)
    total_marks=models.CharField(max_length=9)

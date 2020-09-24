from rest_framework import serializers
from account.models import *
from django.contrib.auth.hashers import make_password

class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'is_student', 'sap_id','username','division','password']

        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}



    def newsave(self):
        student=Student(email=self.validated_data['email'],username=self.validated_data['username'],sap_id=self.validated_data['sap_id'],first_name=self.validated_data['first_name'],last_name=self.validated_data['last_name'],is_student=self.validated_data['is_student'])
        password=self.validated_data['password']
        student.set_password(password)
        student.save()
        return student



class TeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'email', 'is_teacher','username','subject','password']

        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}



    def newsave(self):
        teacher=Teacher(email=self.validated_data['email'],username=self.validated_data['username'],first_name=self.validated_data['first_name'],last_name=self.validated_data['last_name'],is_teacher=self.validated_data['is_teacher'])
        password=self.validated_data['password']
        teacher.set_password(password)
        teacher.save()
        return teacher






class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=10)
    password = serializers.CharField(style={"input_type": "password"})

from rest_framework import serializers
from account.models import *

class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=['mcq_exam','question','option_1','option_2','option_3','option_4','correct_ans','id']

class CreateChpSerializer(serializers.ModelSerializer):
    question=CreateQuestionSerializer(many=False,read_only=True)

    class Meta:
        model = McqExam
        fields ="__all__"



class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student_Response
        fields=['question','student','student_response']

class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Results
        fields=['student','obtained_marks','total_marks']

class ResultsSerializerStudent(serializers.ModelSerializer):
    class Meta:
        model=Results
        fields=['mcq_exam','student','obtained_marks','total_marks']

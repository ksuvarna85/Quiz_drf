from rest_framework import serializers
from account.models import *


class CreateChpSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqExam
        fields =['id','exam_topic']

class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=['mcq_exam','question','option_1','option_2','option_3','option_4','correct_ans','id']


class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student_Response
        fields=['question','student','student_response']

class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Results
        fields=['student','obtained_marks','total_marks']

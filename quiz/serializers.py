from rest_framework import serializers
from account.models import *


class CreateChpSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqExam
        fields =['exam_topic','id']

class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=['mcq_exam','question','option_1','option_2','option_3','option_4','correct_ans','id']

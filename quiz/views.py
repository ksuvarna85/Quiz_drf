from django.shortcuts import render
from quiz.serializers import *
from account.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ExamTopicList(APIView):
    permission_classes = [IsAuthenticated]


    def get_object(self, pk):
        try:
            return McqExam.objects.get(pk=pk)
        except McqExam.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        exam=McqExam.objects.all()
        serializer=CreateChpSerializer(exam,many=True)
        x=request.user.is_student
        print(x)
        if x:
            return Response("you r a student")
        else:

            return Response(serializer.data)

    def post(self,request,pk):
        serializer=CreateChpSerializer(data=request.data)
        #print(serializer)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            data={
            "id":user.id,
            "Exam topic":user.exam_topic


            }
            x=request.user.is_student
            if x:
                return Response("you r a student")
            else:

                return Response(data)



    def delete(self,request,pk):
        exam=self.get_object(pk=pk)
        x=request.user.is_student
        if x:
            return Response("you r a student")
        else:

            exam.delete()
            return Response("deleted successfully")


class ExamDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk,q_pk):
        question=McqExam.objects.get(id=pk)
        question=Question.objects.filter(mcq_exam=question)
        print(question)
        serializer=CreateQuestionSerializer(question,many=True)
        x=request.user.is_student
        if x:
            return Response("you r a student")
        else:

            return Response(serializer.data)

    def post(self,request,pk,q_pk):

        serializer=CreateQuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            user=serializer.save()
            data={
            "id":user.id,
            "Question":user.question,
            "option 1":user.option_1,
            "option 2":user.option_2,
            "option 3":user.option_3,
            "option 4":user.option_4,
            "correct_ans":user.correct_ans,
            }
            x=request.user.is_student
            if x:
                return Response("you r a student")
            else:


                return Response(data)

    def put(self, request,pk,q_pk):
        question = Question.objects.get(id=q_pk)
        print(question)
        serializer = CreateQuestionSerializer(question, data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            data={
            "id":user.id,
            "Question":user.question,
            "option 1":user.option_1,
            "option 2":user.option_2,
            "option 3":user.option_3,
            "option 4":user.option_4,
            "correct_ans":user.correct_ans,
            }

            x=request.user.is_student
            if x:
                return Response("you r a student")
            else:
                return Response(data)







    def delete(self, request,pk,q_pk):
        question = Question.objects.get(id=q_pk)
        x=request.user.is_student
        if x:
            return Response("you r a student")
        else:

            question.delete()
            return Response("Deleated successfully")

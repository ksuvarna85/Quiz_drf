from django.shortcuts import render
from quiz.serializers import *
from account.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from quiz.permissions import *
from rest_framework import viewsets
# Create your views here.
class ExamTopicList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user=User.objects.get(id=self.request.user.id).email
        teacher=Teacher.objects.get(email=user)
        return teacher
    def get_queryset(self):
        try:

            teacher=self.get_object()

            return McqExam.objects.filter(teacher=teacher)
        except McqExam.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        exam=self.get_queryset()
        print(exam)
        teacher=self.get_object()


        data=[]

        for i in exam:
            lst2=[]
            question=Question.objects.filter(mcq_exam=i)

            for j in question:

                data3={
                "id":j.id,
                "question":j.question,
                "option_1":j.option_1,
                "option_2":j.option_2,
                "option_3":j.option_3,
                "option_4":j.option_4,
                "correct_ans":j.correct_ans,

                }
                lst2.append(data3)

            data2={
            "id":i.id,
            "teacher":teacher.first_name +" "+ teacher.last_name,
            "exam_topic":i.exam_topic,
            "question":lst2,
            }
            data.append(data2)


        x=request.user.is_student
        print(x)
        if x:
            return Response("you r a student")
        else:

            return Response(data)

    def post(self,request,pk):
        x=request.user.is_student
        if x:
            return Response("you r a student")
        else:
            exam_topic=request.data.get("exam_topic")
            if exam_topic is None:
                data={
                "Message":"incorrect key please enter the key as exam_topic"
                }
                return Response(data)

            teacher=self.get_object()

            mcq_exam=McqExam.objects.create(exam_topic=exam_topic,teacher=teacher)
            mcq_exam.save()
            serializer=CreateChpSerializer(mcq_exam)
            return Response(serializer.data)




    def delete(self,request,pk):
        try:
            exam=exam=McqExam.objects.get(pk=pk)
        except McqExam.DoesNotExist:
            raise Http404

        x=request.user.is_student
        if x:
            return Response("you r a student")
        else:

            exam.delete()
            return Response("deleted successfully")


class ExamDetails(APIView):
    permission_classes = [IsAuthenticated,TestDetails]

    def get(self,request,pk):
        question=McqExam.objects.get(id=pk)
        question=Question.objects.filter(mcq_exam=question)
        #print(question)
        serializer=CreateQuestionSerializer(question,many=True)
        x=request.user.is_student
        if x:
            return Response("you r a student")
        else:

            return Response(serializer.data)

    def post(self,request,pk):
        x=request.user.is_student
        if x:
            return Response("you r a student")
        else:
            mcq_exam=McqExam.objects.get(pk=pk)
            question=Question.objects.create(mcq_exam=mcq_exam,
                                        question=request.data.get('question'),
                                        option_1=request.data.get('option_1'),
                                        option_2=request.data.get('option_2'),
                                        option_3=request.data.get('option_3'),
                                        option_4=request.data.get('option_4'),
                                        correct_ans=request.data.get('correct_ans')  )
            question.save()
            serializer=CreateQuestionSerializer(question)
            return Response(serializer.data)



class QuestionDetails(APIView):
    permission_classes = [IsAuthenticated,TestDetails]


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

    def put(self, request,pk,q_pk):
        question = Question.objects.get(id=q_pk)
        try:
            data={
            'question':request.data['question'],
            'option_1':request.data['option_1'],
            'option_2':request.data['option_2'],
            'option_3':request.data['option_3'],
            'option_4':request.data['option_4'],
            'correct_ans':request.data['correct_ans'],
            'mcq_exam':pk

            }
        except:
            return Response("Required fields not availabel")

        print(request.data)
        serializer = CreateQuestionSerializer(question, data=data)
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


            return Response(data)

    def delete(self, request,pk,q_pk):
        question = Question.objects.get(id=q_pk)
        x=request.user.is_student
        if x:
            return Response("you r a student")
        else:


            question.delete()
            return Response("Deleated successfully")

class TeacherResultsView(APIView):
    def get_queryset(self,pk):
        try:
            mcq_exam=McqExam.objects.get(pk=pk)
            results=Results.objects.filter(mcq_exam=mcq_exam)
            return results
        except:
            return -1

    def get(self,request,pk):

        results=self.get_queryset(pk)
        if results==-1:
            return Response("Details Not Found")
        print(results)
        serializer=ResultsSerializer(results,many=True)
        if request.user.is_student:
            return Response("you r a student")
        else:
            return Response(serializer.data)

#STUDENT Quiz


class StudentResponse(APIView):
    permission_classes = [IsAuthenticated,Students]

    def get_serializer_class(self):
        if self.request.method=='POST':
            return StudentResponseSerializer
        else:

            return ResultsSerializerStudent
    def post(self,request,pk):
        lst1=[]
        mcq_exam=McqExam.objects.get(pk=pk)
        question=Question.objects.filter(mcq_exam=mcq_exam)

        for i in question:
            lst1.append(i.question)

        lst2=[]

        for i in request.data.values():
            if i=="":
                lst2.append(0)
                continue
            lst2.append(i)
        print(lst2)


        if len(lst1)!=len(lst2):
            while(len(lst1)!=len(lst2)):
                lst2.append(0)
        d=[]

        for i in range(0,len(lst1)):

            mcq_exam=McqExam.objects.get(pk=pk)
            if i==0:
                question=Question.objects.filter(mcq_exam=mcq_exam)
            req_question=question.first()


            user=User.objects.get(email=request.user)
            student=Student.objects.get(email=user)
            if Student_Response.objects.filter(question=req_question,student=student).exists():
                return Response("already answered")
            else:
                response=Student_Response.objects.create(question=req_question,student=student,student_response=lst2[i])


                print(question)

                response.save()
                serializer=self.get_serializer_class()
                serializer=serializer(response)
                d.append(serializer.data)

                question=question.exclude(question=req_question)



        return Response(d)

    def get(self,request,pk):
        question_ans=McqExam.objects.get(pk=pk)
        student_email=Student.objects.get(email=request.user)
        #print(question_ans)
        student_ans=Student_Response.objects.filter(student=student_email)
        #print(student_ans)
        #print(question_ans)
        count=0
        count_correct=0

        questions=Question.objects.filter(mcq_exam=question_ans)
        print(question_ans)

        for i in questions:
            question_ans=Question.objects.get(question=i).correct_ans
            student_ans=Student_Response.objects.get(student=student_email,question=i).student_response
            #print(student_ans+'     '+question_ans)
            if int(student_ans)==int(question_ans):
                count_correct=count_correct+1
            count=count+1
        chp_name=McqExam.objects.get(id=pk)
        #print(x)
        student_result=Results(mcq_exam=chp_name,student=student_email,obtained_marks=count_correct,total_marks=count)
        if Results.objects.filter(mcq_exam=chp_name,student=student_email).exists():
            user=Results.objects.get(mcq_exam=chp_name,student=student_email,obtained_marks=count_correct,total_marks=count)
            serializer=self.get_serializer_class()
            serializer=serializer(user)


            return Response(serializer.data)

        else:
            student_result.save()
            user=Results.objects.get(mcq_exam=chp_name,student=student_email,obtained_marks=count_correct,total_marks=count)
            serializer=ResultsSerializerStudent(user)

            return Response(serializer.data)
class StudentQuestionView(APIView):
    permission_classes = [IsAuthenticated,Students]

    def get_queryset(self,pk):
        try:
            mcq_exam=McqExam.objects.get(pk=pk)
            question=Question.objects.filter(mcq_exam=mcq_exam)
            return question
        except:
            return -1


    def get(self,request,pk):

        question=self.get_queryset(pk)
        if question==-1:
            return Response("Exam Topic Not Found")
        data=[]
        for i in question:
            d={
            "id":i.id,
            "Question":i.question,
            "option_1":i.option_1,
            "option_2":i.option_2,
            "option_3":i.option_3,
            "option_4":i.option_4,
            }
            data.append(d)

        return Response(data)

class ExamTopicStudent(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_student:
            return McqExam.objects.all()
        else:
            user=User.objects.get(id=self.request.user.id).email
            teacher=Teacher.objects.get(email=user)
            return McqExam.objects.filter(teacher=teacher)


    serializer_class=CreateChpSerializer

    permission_classes = (IsAuthenticated,)

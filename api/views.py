from rest_framework import generics
from rest_framework.views import APIView
from .serializer import UserSerializer, QuizSerializer, ChatHistorySerializer, LessonSerializer, LessonTitleSerializer, GoalsSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, ChatHistory, Lesson, Goals

from .gen_model import generate_quiz, chatbot, generate_lesson
from .util import create_lesson_from_ai_response, get_lessons_titles

# Create your views here.
from django.http import JsonResponse


class UserViewSet(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
    

class QuizViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class QuizView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    

class GenerateQuizView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, topic):
        response = generate_quiz(topic)
        response['topic'] = topic
        response['user'] = request.user 
        serializer = QuizSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        try:
            history = user.chat_history.msg[-10:]
        except:
            if not user.chat_history:
                chat = ChatHistory.objects.create(user=user)
                chat.save()
            history = user.chat_history.msg
        response = chatbot(request.data['message'],history)

        user.chat_history.msg.append(
        {
            "role": "user",
            "parts":[{"text":f"{request.data['message']}"}]
        })
        user.chat_history.msg.append({
            "role": "model",
            "parts":[{"text":f"{response}"}]
        }
        )
        user.chat_history.save()
        return Response({'msg': {"role": "model", "parts": [{"text": response}]}}, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        try:
            history = user.chat_history.msg[:10]
        except:
            if not user.chat_history:
                chat = ChatHistory.objects.create(user=user)
                chat.save()
            history = user.chat_history.msg
        return Response(history, status=status.HTTP_200_OK)
    def delete(self, request):
        user = request.user
        user.chat_history.msg = []
        user.chat_history.save()
        return Response({}, status=status.HTTP_200_OK)


class lessonsView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Lesson.objects.filter(user=request.user).delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        lessons = get_lessons_titles(request.user)
        serializer = LessonTitleSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LessonsListView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class GoalsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Goals.objects.filter(user=request.user).delete()
        Goals.objects.create(user=request.user,data = request.data)
        Lesson.objects.filter(user=request.user).delete()
        content = generate_lesson(request.data)
        create_lesson_from_ai_response(content,request.user)
        lessons = get_lessons_titles(request.user)
        serializer = LessonTitleSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request):
        Goals.objects.filter(user=request.user).delete()
        Goals.objects.create(user=request.user,data = request.data)
        Lesson.objects.filter(user=request.user).delete()
        content = generate_lesson(request.data)
        create_lesson_from_ai_response(content,request.user)
        lessons = get_lessons_titles(request.user)
        serializer = LessonTitleSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def get(self, request):
        goals = Goals.objects.filter(user=request.user).first()
        if not goals:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        serializer = GoalsSerializer(goals)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, topic):
        '''
            use Gemini to get a verse to be recited
        '''

class RecitationCorrectionView(APIView):
    permission_classes = [IsAuthenticated]

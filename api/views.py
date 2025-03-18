from rest_framework import generics
from rest_framework.views import APIView
from .serializer import UserSerializer, QuizSerializer, ChatHistorySerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, ChatHistory

from .gen_model import generate_quiz, chatbot
# Create your views here.
from django.http import JsonResponse


class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Quiz, Lesson
from .models import ChatHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = '__all__'


class LessonTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'lesson_number', 'title', 'is_completed']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
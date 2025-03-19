from django.db import models

# Create your models here.


class Quiz(models.Model):
    topic = models.CharField(max_length=100, null=True, blank=True)
    question = models.CharField(max_length=300)
    options = models.JSONField()
    answer = models.CharField(max_length=1,choices=[
        ('a', 'a'),
        ('b', 'b'),
        ('c', 'c'),
        ('d', 'd'),
    ])
    evidence = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_answer = models.CharField(max_length=1, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question
    

class ChatHistory(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='chat_history')
    msg = models.JSONField(default=list)

    def __str__(self):
        return f'{self.user}, {self.msg}'



class Lesson(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    lesson_number = models.IntegerField()
    content = models.TextField()
    is_completed = models.BooleanField(default=False)
    estimated_time = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
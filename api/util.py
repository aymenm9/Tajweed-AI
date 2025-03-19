from .models import Lesson


def create_lesson(lesson_data):
    lesson = Lesson.objects.create(**lesson_data)
    lesson.save()


def create_lesson_from_ai_response(lessons_data,user):
    for lesson_data in lessons_data:
        lesson_data['user'] = user
        create_lesson(lesson_data)


def get_lessons_titles(user):
    return Lesson.objects.filter(user=user).values('id','title','lesson_number','is_completed').order_by('lesson_number')

def get_lessons_titles_completed(user):
    return Lesson.objects.filter(user=user).values('id','title','lesson_number','is_completed').filter(is_completed=True).order_by('lesson_number')

def get_lessons_titles_uncompleted(user):
    return Lesson.objects.filter(user=user).values('id','title','lesson_number','is_completed').filter(is_completed=False).order_by('lesson_number')
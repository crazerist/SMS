from django.http.response import HttpResponse
from django.shortcuts import render, reverse, redirect

from user.models import Student, Teacher
from constants import INVALID_KIND


def get_user(request, kind):
    """

    :param request:
    :param kind: teacher or student
    :return: return Teacher instance or Student instance
    """
    if request.session.get('kind', '') != kind or kind not in ["student", "teacher"]:
        return None

    if len(request.session.get('user', '')) != 10:
        return None

    uid = request.session.get('user')
    if kind == "student":
        # 找到对应学生
        grade = uid[:4]
        number = uid[4:]
        student_set = Student.objects.filter(grade=grade, number=number)
        if student_set.count() == 0:
            return None
        return student_set[0]
    else:
        # 找到对应老师
        department_no = uid[:3]
        number = uid[3:]
        teacher_set = Teacher.objects.filter(department_no=department_no, number=number)
        if teacher_set.count() == 0:
            return None
        return teacher_set[0]


# Create your views here.
def home(request, kind):
    if kind == "teacher":
        return teacher_home(request)
    elif kind == "student":
        return student_home(request)
    return HttpResponse(INVALID_KIND)


def teacher_home(request):
    kind = "teacher"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind=kind)

    info = {
        "name": user.name,
        "kind": kind
    }

    context = {
        "info": info
    }

    return render(request, 'course/nav.html', context)

def student_home(request):
    kind = "student"
    user = get_user(request, kind)

    if not user:
        return redirect('login', kind = kind)

    info = {
        "name": user.name,
        "kind": kind
    }

    context = {
        "info": info
    }

    return render(request, 'course/nav.html', context)

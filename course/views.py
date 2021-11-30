from django.http.response import HttpResponse
from django.shortcuts import render, reverse, redirect
from django.db.models import Q
from user.models import Student, Teacher
from constants import INVALID_KIND, INVALID_REQUEST_METHOD
from .forms import CourseForm, ScheduleForm
from .models import Course, Schedule, StudentCourse

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
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    is_search = False
    search_key = ""
    if request.method == "POST":
        search_key = request.POST.get("search")
        if search_key:
            is_search = True

    context = {"info": info}
    q = Q(teacher=user)
    if is_search:
        q = q & Q(name__icontains=search_key)
        context["search_key"] = search_key

    context["course_list"] = Course.objects.filter(q).order_by('status')

    return render(request, 'course/teacher/home.html', context)


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

def create_course(request):
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.status = 1
            obj.teacher = user

            obj.save()
            return redirect(reverse("course", kwargs={"kind": "teacher"}))
    elif request.method == 'GET':
        form = CourseForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    return render(request, 'course/teacher/create_course.html', {'info': info, 'form': form})

def create_schedule(request, course_id):
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    course = Course.objects.get(pk=course_id)

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()

            return redirect(reverse("view_detail", kwargs={"course_id": course_id}))
    elif request.method == 'GET':
        form = ScheduleForm()
    else:
        return HttpResponse(INVALID_REQUEST_METHOD)

    return render(request, 'course/teacher/create_schedule.html', {'info': info, 'form': form, "course": course})

def delete_schedule(request, schedule_id):
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    schedule = Schedule.objects.get(pk=schedule_id)

    course_id = request.GET.get("course_id") or schedule.course.id

    schedule.delete()

    return redirect(reverse("view_detail", kwargs={"course_id": course_id}))

def handle_course(request, course_id, handle_kind):
    """
    :param request:
    :param course_id:
    :param handle_kind:
            1: "开始选课",
            2: "结束选课",
            3: "结课",
            4: "给分完成"
    :return:
    """
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    course = Course.objects.get(pk=course_id)
    if course.status == handle_kind and course.status < 5:
        if course.status == 4:
            scs = StudentCourse.objects.filter(course=course)
            all_given = True
            res = ""
            for sc in scs:
                if sc.scores is None:
                    all_given = False
                    res += "<div>%s 未打分</div>" % sc.student

            if all_given:
                course.status += 1
                course.save()
                return redirect(reverse("view_detail", kwargs={"course_id": course.id}))
            else:
                return HttpResponse(res)
        else:
            course.status += 1
            course.save()

    course_list = Course.objects.filter(teacher=user)
    return render(request, 'course/teacher/home.html', {'info': info, 'course_list': course_list})

def view_detail(request, course_id):
    user = get_user(request, "teacher")
    if not user:
        return redirect(reverse("login", kwargs={"kind": "teacher"}))

    info = {
        "name": user.name,
        "kind": "teacher",
    }

    course = Course.objects.get(pk=course_id)
    c_stu_list = StudentCourse.objects.filter(course=course)
    sche_list = Schedule.objects.filter(course=course)

    context = {
        "info": info,
        "course": course,
        "course_students": c_stu_list,
        "schedules": sche_list
    }

    if course.status == 5:
        sorted_cs_list = sorted(c_stu_list, key=lambda cs: cs.scores)
        context["sorted_course_students"] = sorted_cs_list

    return render(request, "course/teacher/course.html", context)

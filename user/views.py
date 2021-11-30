from audioop import reverse

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from constants import INVALID_KIND
from user.forms import StuLoginForm, TeaLoginForm
from user.cbvs import CreateStudentView, CreateTeacherView, UpdateStudentView, UpdateTeacherView
from user.models import Student, Teacher


def home(request):
    return render(request, "user/login_home.html")

def login(request, kind):
    if kind not in ["teacher", "student"]:
        return HttpResponse(INVALID_KIND)

    if request.method == 'POST':
        if kind == "teacher":
            form = TeaLoginForm(data=request.POST)
        else:
            form = StuLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]
            if len(uid) != 10:
                form.add_error("uid", "账号长度必须为10")
            else:
                if kind == "teacher":
                    department_no = uid[:3]
                    number = uid[3:]
                    object_set = Teacher.objects.filter(department_no=department_no, number=number)
                else:
                    grade = uid[:4]
                    number = uid[4:]
                    object_set = Student.objects.filter(grade=grade, number=number)
                if object_set.count() == 0:
                    form.add_error("uid", "该账号不存在.")
                else:
                    user = object_set[0]
                    if form.cleaned_data["password"] != user.password:
                        form.add_error("password", "密码不正确.")
                    else:
                        request.session['kind'] = kind
                        request.session['user'] = uid
                        request.session['id'] = user.id

                        return redirect("course", kind=kind)

            return render(request, 'user/login_detail.html', {'form': form, 'kind': kind})
    else:
        context = {'kind': kind}
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            if kind == "teacher":
                form = TeaLoginForm({"uid": uid, 'password': '12345678'})
            else:
                form = StuLoginForm({"uid": uid, 'password': '12345678'})
        else:
            if kind == "teacher":
                form = TeaLoginForm()
            else:
                form = StuLoginForm()
        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')

        return render(request, 'user/login_detail.html', context)


def register(request, kind):
    func = None
    if kind == "student":
        func = CreateStudentView.as_view()
    elif kind == "teacher":
        func = CreateTeacherView.as_view()

    if func:
        return func(request)
    else:
        return HttpResponse(INVALID_KIND)

def logout(request):
    if request.session.get("kind", ""):
        del request.session["kind"]
    if request.session.get("user", ""):
        del request.session["user"]
    if request.session.get("id", ""):
        del request.session["id"]
    return redirect("login")


def update(request, kind):
    func = None
    if kind == "student":
        func = UpdateStudentView.as_view()
    elif kind == "teacher":
        func = UpdateTeacherView.as_view()
    else:
        return HttpResponse(INVALID_KIND)

    pk = request.session.get("id")
    if pk:
        context = {
            "name": request.session.get("name", ""),
            "kind": request.session.get("kind", "")
        }
        return func(request, pk=pk, context=context)

    return redirect("login")

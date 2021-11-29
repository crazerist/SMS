from django.shortcuts import render
from django.http.response import HttpResponse
from constants import INVALID_KIND
from user.forms import StuLoginForm, TeaLoginForm
from user.cbvs import CreateStudentView, CreateTeacherView

def home(request):
    return render(request, "user/login_home.html")

def login(request, *args, **kwargs):
    if not kwargs or kwargs.get("kind", "") not in ["student", "teacher"]:
        return HttpResponse(INVALID_KIND)

    kind = kwargs["kind"]
    context = {'kind': kind}

    if request.method == 'POST':
        if kind == "teacher":
            form = TeaLoginForm(data=request.POST)
        else:
            form = StuLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]

            temp_res = "hello, %s" % uid
            return HttpResponse(temp_res)
        else:
            context['form'] = form
    elif request.method == 'GET':
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            data = {"uid":uid, 'password': '12345678'}
            if kind == "teacher":
                form = TeaLoginForm(data)
            else:
                form = StuLoginForm(data)
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

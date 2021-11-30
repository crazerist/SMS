from django.shortcuts import reverse, redirect
from django.views.generic import CreateView
from django.views.generic import UpdateView
from user.forms import StuUpdateForm


from user.forms import StuRegisterForm, TeaRegisterForm

from user.models import Student, Teacher
import random


class CreateStudentView(CreateView):
    model = Student
    form_class = StuRegisterForm
    # fields = "__all__"
    template_name = "user/register.html"
    success_url = "login"

    def form_valid(self, form):
        # 学生注册时选定年级自动生成学号
        grade = form.cleaned_data["grade"]
        # order_by默认升序排列，number前的负号表示降序排列
        student_set = Student.objects.filter(grade=grade).order_by("-number")
        if student_set.count() > 0:
            last_student = student_set[0]
            new_number = str(int(last_student.number) + 1)
            for i in range(6 - len(new_number)):
                new_number = "0" + new_number
        else:
            new_number = "000001"

        # Create, but don't save the new student instance.
        new_student = form.save(commit=False)
        # Modify the student
        new_student.number = new_number
        # Save the new instance.
        new_student.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_student

        uid = grade + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'student'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))


    def get_context_data(self, **kwargs):
        context = super(CreateStudentView, self).get_context_data(**kwargs)
        context["kind"] = "student"

        return context





class CreateTeacherView(CreateView):
    model = Teacher
    form_class = TeaRegisterForm
    template_name = "user/register.html"
    success_url = "login"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # 老师注册时随机生成院系号, 院系号范围为[0,300)
        department_no = random.randint(0, 300)
        # 把非三位数的院系号转换为以0填充的三位字符串，如1转换为'001'
        department_no = '{:0>3}'.format(department_no)
        teacher_set = Teacher.objects.filter(department_no=department_no).order_by("-number")
        if teacher_set.count() > 0:
            last_teacher = teacher_set[0]
            new_number = int(last_teacher.number) + 1
            new_number = '{:0>7}'.format(new_number)
        else:
            new_number = "0000001"

        # Create, but don't save the new teacher instance.
        new_teacher = form.save(commit=False)
        # Modify the teacher
        new_teacher.department_no = department_no
        new_teacher.number = new_number
        # Save the new instance.
        new_teacher.save()
        # Now, save the many-to-many data for the form.
        form.save_m2m()

        self.object = new_teacher

        uid = department_no + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'teacher'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))

    def get_context_data(self, **kwargs):
        context = super(CreateTeacherView, self).get_context_data(**kwargs)
        context["kind"] = "teacher"

        return context

class UpdateStudentView(UpdateView):
    model = Student
    form_class = StuUpdateForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "student"
        return context

    def get_success_url(self):
        return reverse("course", kwargs={"kind": "student"})


class UpdateTeacherView(UpdateView):
    model = Teacher
    form_class = TeaRegisterForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateTeacherView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "teacher"
        return context

    def get_success_url(self):
        return reverse("course", kwargs={"kind": "teacher"})


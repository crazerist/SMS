from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.shortcuts import render, reverse, redirect

# Relative import of GeeksModel
from .models import Schedule, StudentCourse
from .forms import ScoreForm


class ScoreUpdateView(UpdateView):
    model = StudentCourse
    form_class = ScoreForm
    template_name = 'course/teacher/score.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        title = "给分"
        if request.GET.get("update"):
            title = "修改成绩"

        info = {}
        return_url = reverse("course", kwargs={"kind": "teacher"})
        if self.object:
            teacher = self.object.course.teacher
            info = {
                "name": teacher.name,
                "kind": "teacher",
            }
            return_url = reverse("view_detail", kwargs={"course_id": self.object.course.id})

        return self.render_to_response(self.get_context_data(info=info, title=title, return_url=return_url))

    def get_success_url(self):
        if self.object:
            return reverse("view_detail", kwargs={"course_id": self.object.course.id})
        else:
            return reverse("course", kwargs={"kind": "teacher"})

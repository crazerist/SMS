from django import forms
from .models import Course, Schedule, StudentCourse


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ['status', 'teacher']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ["course"]

class ScoreForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ["student", "course", "scores", "comments"]

    student = forms.CharField(label="学生", disabled=True)
    # course = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    course = forms.CharField(label="课程", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['student'] = self.instance.student
        self.initial['course'] = self.instance.course

    def clean_student(self):
        return self.initial['student']

    def clean_course(self):
        return self.initial['course']

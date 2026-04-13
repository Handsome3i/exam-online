from django.contrib import admin
from .models import Exam, Question, Option, ExamRecord, AnswerDetail


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    show_change_link = True


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'question_count', 'duration_minutes', 'is_published', 'created_by', 'created_at']
    list_filter = ['is_published', 'created_at']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['order', 'content', 'question_type', 'score', 'exam']
    list_filter = ['exam', 'question_type']
    inlines = [OptionInline]


@admin.register(ExamRecord)
class ExamRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'total_score', 'is_submitted', 'started_at', 'submitted_at']
    list_filter = ['exam', 'is_submitted']

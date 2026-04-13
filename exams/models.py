from django.db import models
from django.conf import settings


class Exam(models.Model):
    title = models.CharField('试卷名称', max_length=200)
    description = models.TextField('试卷说明', blank=True, default='')
    duration_minutes = models.IntegerField('考试时长(分钟)', default=60)
    is_published = models.BooleanField('已发布', default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='创建人', related_name='created_exams'
    )
    pass_score = models.IntegerField('及格分数', default=60)
    total_score = models.IntegerField('总分', default=100)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = '试卷'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    TYPE_CHOICES = [('single', '单选'), ('multi', '多选')]
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', verbose_name='所属试卷')
    order = models.IntegerField('题号', default=0)
    question_type = models.CharField('题型', max_length=10, choices=TYPE_CHOICES, default='single')
    content = models.TextField('题干')
    score = models.IntegerField('分值', default=5)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'
        ordering = ['order']

    def __str__(self):
        return f'Q{self.order}: {self.content[:30]}'

    def get_options(self):
        return self.options.all().order_by('label')


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', verbose_name='所属题目')
    label = models.CharField('选项标签', max_length=5)
    content = models.TextField('选项内容')
    is_correct = models.BooleanField('是否正确答案', default=False)

    class Meta:
        verbose_name = '选项'
        verbose_name_plural = '选项'
        ordering = ['label']

    def __str__(self):
        return f'{self.label}. {self.content[:30]}'


class ExamRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        verbose_name='考生', related_name='exam_records'
    )
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='试卷', related_name='records')
    answers = models.JSONField('作答记录', default=dict)
    total_score = models.IntegerField('得分', default=0)
    is_submitted = models.BooleanField('已交卷', default=False)
    started_at = models.DateTimeField('开始时间', auto_now_add=True)
    submitted_at = models.DateTimeField('交卷时间', null=True, blank=True)

    class Meta:
        verbose_name = '考试记录'
        verbose_name_plural = '考试记录'
        ordering = ['-started_at']
        unique_together = ['user', 'exam']

    def __str__(self):
        return f'{self.user.username} - {self.exam.title} - {self.total_score}分'

    @property
    def passed(self):
        return self.total_score >= self.exam.pass_score


class AnswerDetail(models.Model):
    record = models.ForeignKey(ExamRecord, on_delete=models.CASCADE, related_name='details', verbose_name='考试记录')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='题目')
    selected_options = models.JSONField('选择的选项', default=list)
    is_correct = models.BooleanField('是否正确', default=False)
    earned_score = models.IntegerField('得分', default=0)

    class Meta:
        verbose_name = '答题详情'
        verbose_name_plural = '答题详情'

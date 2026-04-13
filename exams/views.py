from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Exam, ExamRecord, AnswerDetail
from .forms import ExamCreateForm, ExamEditForm
from .utils import parse_exam_excel


@login_required
def exam_list(request):
    if request.user.is_admin():
        exams = Exam.objects.all()
    else:
        exams = Exam.objects.filter(is_published=True)

    exam_data = []
    records_map = {}
    if not request.user.is_admin():
        for record in ExamRecord.objects.filter(user=request.user):
            records_map[record.exam_id] = record

    for exam in exams:
        exam_data.append({
            'exam': exam,
            'record': records_map.get(exam.id),
        })

    return render(request, 'exams/exam_list.html', {'exam_data': exam_data})


@login_required
def exam_create(request):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('exams:exam_list')

    if request.method == 'POST':
        form = ExamCreateForm(request.POST, request.FILES)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            excel_file = request.FILES['excel_file']
            try:
                count = parse_exam_excel(excel_file, exam)
                messages.success(request, f'试卷创建成功，共导入 {count} 道题目')
            except Exception as e:
                exam.delete()
                messages.error(request, f'Excel 解析失败：{e}')
                return render(request, 'exams/exam_create.html', {'form': form})
            return redirect('exams:exam_list')
    else:
        form = ExamCreateForm()
    return render(request, 'exams/exam_create.html', {'form': form})


@login_required
def exam_edit(request, exam_id):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('exams:exam_list')

    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        form = ExamEditForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, '试卷更新成功')
            return redirect('exams:exam_list')
    else:
        form = ExamEditForm(instance=exam)
    return render(request, 'exams/exam_edit.html', {'form': form, 'exam': exam})


@login_required
def exam_delete(request, exam_id):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('exams:exam_list')

    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, '试卷已删除')
    return redirect('exams:exam_list')


@login_required
def exam_publish(request, exam_id):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('exams:exam_list')

    exam = get_object_or_404(Exam, id=exam_id)
    exam.is_published = not exam.is_published
    exam.save()
    status = '已发布' if exam.is_published else '已取消发布'
    messages.success(request, f'试卷 {status}')
    return redirect('exams:exam_list')


@login_required
def exam_preview(request, exam_id):
    if not request.user.is_admin():
        messages.error(request, '权限不足')
        return redirect('exams:exam_list')

    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.prefetch_related('options').all()
    return render(request, 'exams/exam_preview.html', {'exam': exam, 'questions': questions})


@login_required
def exam_start(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, is_published=True)
    record, created = ExamRecord.objects.get_or_create(
        user=request.user, exam=exam,
        defaults={'started_at': timezone.now()}
    )
    if record.is_submitted:
        messages.info(request, '您已完成该考试')
        return redirect('exams:exam_result', exam_id=exam_id)
    return redirect('exams:exam_take', exam_id=exam_id)


@login_required
def exam_take(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, is_published=True)
    record = get_object_or_404(ExamRecord, user=request.user, exam=exam)

    if record.is_submitted:
        return redirect('exams:exam_result', exam_id=exam_id)

    questions = exam.questions.prefetch_related('options').all()
    elapsed = (timezone.now() - record.started_at).total_seconds()
    remaining = max(0, exam.duration_minutes * 60 - elapsed)

    return render(request, 'exams/exam_take.html', {
        'exam': exam,
        'record': record,
        'questions': questions,
        'remaining_seconds': int(remaining),
    })


@login_required
def exam_submit(request, exam_id):
    if request.method != 'POST':
        return redirect('exams:exam_take', exam_id=exam_id)

    exam = get_object_or_404(Exam, id=exam_id)
    record = get_object_or_404(ExamRecord, user=request.user, exam=exam)

    if record.is_submitted:
        return redirect('exams:exam_result', exam_id=exam_id)

    questions = exam.questions.prefetch_related('options').all()
    total_score = 0
    answers_data = {}

    for question in questions:
        key = f'question_{question.id}'
        if question.question_type == 'multi':
            selected = request.POST.getlist(key)
        else:
            val = request.POST.get(key)
            selected = [val] if val else []

        correct_labels = set(
            opt.label for opt in question.options.all() if opt.is_correct
        )
        selected_set = set(selected)
        is_correct = selected_set == correct_labels and len(selected_set) > 0
        earned = question.score if is_correct else 0
        total_score += earned

        answers_data[str(question.id)] = list(selected)

        AnswerDetail.objects.create(
            record=record,
            question=question,
            selected_options=list(selected),
            is_correct=is_correct,
            earned_score=earned,
        )

    record.answers = answers_data
    record.total_score = total_score
    record.is_submitted = True
    record.submitted_at = timezone.now()
    record.save()

    return redirect('exams:exam_result', exam_id=exam_id)


@login_required
def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    record = get_object_or_404(ExamRecord, user=request.user, exam=exam)

    if not record.is_submitted:
        return redirect('exams:exam_take', exam_id=exam_id)

    details = record.details.select_related('question').prefetch_related('question__options').all()

    return render(request, 'exams/exam_result.html', {
        'exam': exam,
        'record': record,
        'details': details,
    })

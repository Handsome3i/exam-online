import openpyxl
from .models import Exam, Question, Option


def parse_exam_excel(file, exam):
    """
    解析考题 Excel 文件并写入数据库。
    Excel 格式：
      列1: 题目序号（仅每题首行有值）
      列2: 题目（仅每题首行有值）
      列3: 选项设置（每行一个选项）
      列4: 答案（仅首行，多选用 ；分隔）
      列5: 类型（单选/多选，仅首行）
      列6: 涉及标准部分（可选）

    每道题跨多行，选项占一行一个；题号/题干/答案/类型仅在该题第一行出现。
    """
    wb = openpyxl.load_workbook(file)
    ws = wb.active

    questions_data = []
    current = None

    for row in ws.iter_rows(min_row=2, max_col=6, values_only=True):
        seq, title, option_text, answer, qtype, _ref = row

        if seq is not None and title is not None:
            if current:
                questions_data.append(current)
            type_map = {'单选': 'single', '多选': 'multi'}
            answers = []
            if answer:
                answers = [a.strip() for a in str(answer).replace('；', ';').split(';')]
            current = {
                'order': int(seq),
                'content': str(title).strip(),
                'question_type': type_map.get(str(qtype).strip(), 'single') if qtype else 'single',
                'options': [],
                'answers': answers,
            }

        if current and option_text:
            current['options'].append(str(option_text).strip())

    if current:
        questions_data.append(current)

    score_per_question = exam.total_score // max(len(questions_data), 1)
    remainder = exam.total_score - score_per_question * len(questions_data)

    for i, qdata in enumerate(questions_data):
        score = score_per_question + (1 if i < remainder else 0)
        question = Question.objects.create(
            exam=exam,
            order=qdata['order'],
            content=qdata['content'],
            question_type=qdata['question_type'],
            score=score,
        )
        labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for j, opt_text in enumerate(qdata['options']):
            is_correct = opt_text in qdata['answers']
            Option.objects.create(
                question=question,
                label=labels[j] if j < len(labels) else str(j + 1),
                content=opt_text,
                is_correct=is_correct,
            )

    return len(questions_data)

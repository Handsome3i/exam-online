from django import forms
from .models import Exam


class ExamCreateForm(forms.ModelForm):
    excel_file = forms.FileField(
        label='上传考题Excel文件',
        help_text='支持 .xlsx 格式，列顺序：题目序号、题目、选项、答案、类型、标准部分',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx,.xls'}),
    )

    class Meta:
        model = Exam
        fields = ['title', 'description', 'duration_minutes', 'pass_score', 'total_score']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入试卷名称'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '可选，试卷说明'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'pass_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ExamEditForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'duration_minutes', 'pass_score', 'total_score', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'pass_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from exams.models import Exam
from exams.utils import parse_exam_excel

User = get_user_model()


class Command(BaseCommand):
    help = '从 Excel 文件导入考题创建试卷'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Excel 文件路径')
        parser.add_argument('--title', type=str, default='语音转录模块考试', help='试卷标题')
        parser.add_argument('--duration', type=int, default=30, help='考试时长(分钟)')
        parser.add_argument('--total', type=int, default=100, help='总分')
        parser.add_argument('--pass-score', type=int, default=60, help='及格分')

    def handle(self, *args, **options):
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            self.stderr.write('请先创建管理员账号: python manage.py createsuperuser')
            return

        exam = Exam.objects.create(
            title=options['title'],
            duration_minutes=options['duration'],
            total_score=options['total'],
            pass_score=options['pass_score'],
            created_by=admin,
            is_published=True,
        )

        with open(options['filepath'], 'rb') as f:
            count = parse_exam_excel(f, exam)

        self.stdout.write(self.style.SUCCESS(
            f'成功导入试卷「{exam.title}」，共 {count} 道题'
        ))

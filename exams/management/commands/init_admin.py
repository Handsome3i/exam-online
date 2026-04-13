from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = '确保管理员账号存在'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            u = User.objects.create_superuser('admin', 'admin@exam.com', 'admin123')
            u.role = 'admin'
            u.first_name = '管理员'
            u.save()
            self.stdout.write(self.style.SUCCESS('Admin created: admin / admin123'))
        else:
            self.stdout.write('Admin already exists')

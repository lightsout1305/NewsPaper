from django.core.management.base import BaseCommand, CommandError

from news_project.models import Post


class Command(BaseCommand):
    help = 'Удаляет все статьи и новости из выбранной категории'

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Выберите категорию (Politics, Economy, Art, IT, Sports, Other:')
        answer = input().lower()
        if answer:
            self.stdout.write(f'Вы действительно хотите удалить весь материал по категории {answer}?')
            answer1 = input().lower()
            if answer1 == 'да':
                Post.objects.filter(categories__category_name=f'{answer}').delete()
                self.stdout.write(self.style.SUCCESS(f"Материал в категории '{answer}' успешно удален"))
            else:
                self.handle()
            return
        else:
            self.stdout.write(self.style.ERROR("Отказано в доступе"))




from django.core.management.base import BaseCommand

from dotick.tasks.application import advance_task_lifecycle


class Command(BaseCommand):
    help = "Advance active Task time states at the current UTC instant."

    def handle(self, *args, **options):
        changed = advance_task_lifecycle()
        self.stdout.write(self.style.SUCCESS(f"Advanced {changed} Task lifecycle state(s)."))

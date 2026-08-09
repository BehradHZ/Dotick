from django.contrib import admin

from core.models import Event, Routine, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "user_status", "due_date", "deadline", "deadline_enabled"]
    list_filter = ["user_status", "deadline_enabled"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "start_time", "end_time"]


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ["title", "user_status", "period_end"]
    list_filter = ["user_status"]

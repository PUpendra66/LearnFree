from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'price', 'duration')
    search_fields = ('title', 'instructor')
    list_filter = ('price', 'duration')

from django import template
from django.utils import timezone

from attendances.models import AttendanceBook

register = template.Library()


@register.filter
def is_late(student, attendance_book):
    return attendance_book.is_late(student)

@register.filter
def absent_students(classroom, day=None):
    if day is None:
        day = timezone.now()

    n_students = classroom.students.count()
    try:
        attbook = classroom.attendancebook_set.get(day=day)
    except AttendanceBook.DoesNotExist:
        return n_students # all absent

    return n_students - attbook.students.count()

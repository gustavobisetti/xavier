# -*- coding: utf-8 -*-

from datetime import date

from django import forms
from django import http
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404
from django.utils.text import capfirst
from django.utils.translation import ugettext


from accounts.models import Student
from classes.models import Class
from xavier.views import ModelView

from .models import Attendance, AttendanceBook


class AttendanceBookView(ModelView):
    base_template = 'attendances/base.html'
    paginate_by = 20

    def get_class_rooms(self, request):
        return Class.objects.filter(
            period__school=self.get_current_school(request)
        )

    def get_attendance_book(self, classroom, day):
        if not isinstance(day, date):
            year, month, month_day = day.split('-')
            day = date(int(year), int(month), int(month_day))
        if not isinstance(classroom, Class):
            classroom = Class.objects.get(pk=classroom)
        attendance_book, _ = AttendanceBook.objects.get_or_create(
            classroom=classroom,
            day=day,
        )
        return attendance_book

    def get_query_set(self, request, *args, **kwargs):
        # Filter items only from current school
        qs = super(ModelView, self).get_query_set(request, *args, **kwargs)
        current_school = self.get_current_school(request)
        return qs.filter(classroom__period__school=current_school)

    def additional_urls(self):
        return [
            (r'^take-attendance/(?P<classroom>\d+)/$', self.take_attendance),
            (r'^take-attendance/(?P<classroom>\d+)/(?P<student>\d+)$', self.ajax_take_attendance),
        ]

    def take_attendance(self, request, classroom):
        if not self.adding_allowed(request):
            return self.response_adding_denied(request)

        classroom = get_object_or_404(Class, pk=classroom)
        day = request.GET.get('day', date.today())
        attendance_book = self.get_attendance_book(classroom, day)
        context = {
            'title': ugettext('Attendances'),
            'subtitle': unicode(classroom),
            'classroom': classroom,
            'attendance_book': attendance_book
        }

        return self.render(
            request,
            template='attendances/take_attendance.html',
            context=self.get_context(request, context)
        )

    def ajax_toggle_attendance(self, request):
        if request.is_ajax():
            try:
                attendance_book_id = int(request.GET.get('attendance_book'))
                attendance_book = AttendanceBook.objects.get(pk=attendance_book_id)
                student_id = int(request.GET.get('student'))
                student = Student.objects.get(pk=student_id)
            except ValueError:
                return http.HttpResponse(status=400)
            except ObjectDoesNotExist:
                return http.HttpResponse(status=400)
            attendance, created = Attendance.objects.get_or_create(
                attendance_book=attendance_book,
                student=student,
            )
            if not created:
                attendance.delete()
            return http.HttpResponse(status=200)
        return http.HttpResponse(status=400)

    def ajax_toggle_late_status(self, request):
        if request.is_ajax():
            try:
                attendance_book_id = int(request.GET.get('attendance_book'))
                attendance_book = AttendanceBook.objects.get(pk=attendance_book_id)
                student_id = int(request.GET.get('student'))
                student = Student.objects.get(pk=student_id)
            except ValueError:
                return http.HttpResponse(status=400)
            except ObjectDoesNotExist:
                return http.HttpResponse(status=400)
            attendance = Attendance.objects.get(
                attendance_book=attendance_book,
                student=student,
            )
            is_late = attendance.is_late
            attendance.is_late = False if is_late else True
            attendance.save()
            return http.HttpResponse(status=200)
        return http.HttpResponse(status=400)

    def list_view(self, request, *args, **kwargs):
        context = dict(class_rooms=self.get_class_rooms(request))
        # TODO XXX: 2013 needs to be a dynamic period instead of
        #   hardcoded
        context.update({
            'title': ugettext('Attendances'),
            'subtitle': u'{} 2013'.format(ugettext('Classes'), ),
        })
        return self.render_list(request, context)

attendancebook_views = AttendanceBookView(AttendanceBook)

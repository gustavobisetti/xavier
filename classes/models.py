# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from periods.models import Period
from accounts.models import Student, Teacher
from subjects.models import Subject


class Grade(models.Model):
    name = models.CharField(_(u'name'), max_length=50)
    grade_type = models.CharField(_(u'grade type'), max_length=50)

    class Meta:
        verbose_name = _(u'grade')
        verbose_name_plural = _(u'grades')

    def __unicode__(self):
        return self.name


class Class(models.Model):
    identification = models.CharField(_(u'identification'), max_length=20)
    period = models.ForeignKey(Period, verbose_name=_(u'period'))
    students = models.ManyToManyField(Student, verbose_name=_(u'students'))
    grade = models.ForeignKey(Grade, verbose_name=_(u'grade'))

    class Meta:
        verbose_name = _(u'class')
        verbose_name_plural = _(u'classes')

    def __unicode__(self):
        return u'%s, %s' % (self.identification, self.period)


class ClassSubject(models.Model):
    classroom = models.ForeignKey(Class, verbose_name=_(u'classroom'))
    subject = models.ForeignKey(Subject, verbose_name=_(u'subject'))
    teacher = models.ForeignKey(Teacher, verbose_name=_(u'teacher'))

    class Meta:
        verbose_name = _(u'class subject')
        verbose_name_plural = _(u'class subjects')

    def __unicode__(self):
        return unicode(self.classroom)

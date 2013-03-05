from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import Student
from classes.models import ClassSubject
from periods.models import SubPeriod


class EvaluationCriteria(models.Model):
    name = models.CharField(_('name'), max_length=30)
    weight = models.SmallIntegerField(_('weight'))
    class_subject = models.ForeignKey(ClassSubject)

    def __unicode__(self):
        return self.name


class Score(models.Model):
    student = models.ForeignKey(Student)
    score = models.IntegerField(_('score'))
    criteria = models.ForeignKey(EvaluationCriteria)
    subperiod = models.ForeignKey(SubPeriod)

    def save(self, *args, **kwargs):
        student_classes = self.student.class_set.all()
        criteria_class = self.criteria.class_subject.classroom
        if criteria_class not in student_classes:
            raise ValidationError(
                _("Student not in the class of given criteria")
            )
        super(Score, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.score

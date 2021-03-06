from curriculum.models import AlignmentTag
from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from zope.cachedescriptors.property import Lazy
import re


SCORES = (
    (3, u"3"),
    (2, u"2"),
    (1, u"1"),
    (0, u"0"),
    (None, u"N/A"),
)


def get_verbose_score_name(value):
    if value == 3:
        return u"Superior"
    elif value == 2:
        return u"Strong"
    elif value == 1:
        return u"Limited"
    elif value == 0:
        return u"Very Weak"
    elif value is None:
        return u"Not Applicable"
    else:
        raise ValueError(u"Invalid value.")


class Evaluation(models.Model):

    user = models.ForeignKey(User)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    confirmed = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=39, default=u"", blank=True)
    hostname = models.CharField(max_length=100, default=u"", blank=True)

    class Meta:
        permissions = (
            ("can_manage", u"Can manage evaluations"),
            )
        unique_together = ["user", "content_type", "object_id"]

    @classmethod
    def enable_alignment_scores(cls, item):
        collection = getattr(item, "collection", None)
        if collection and collection.disable_alignment_evaluation:
            return False
        return True


class ScoreValue(models.Model):

    value = models.PositiveSmallIntegerField(null=True, blank=True,
                                             choices=SCORES)
    description = models.TextField()

    def __unicode__(self):
        #noinspection PyUnresolvedReferences
        return self.get_value_display()

    class Meta:
        abstract = True
        ordering = ["id"]


class Rubric(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    video_link = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["id"]


class RubricScoreValue(ScoreValue):

    rubric = models.ForeignKey(Rubric, related_name="score_values")

    def __unicode__(self):
        #noinspection PyUnresolvedReferences
        return u"%s - %s" % (self.rubric, self.get_value_display())

    class Meta:
        unique_together = ["rubric", "value"]
        ordering = ["id"]


class Score(models.Model):

    evaluation = models.ForeignKey(Evaluation)
    comment = models.TextField(default=u"", blank=True)

    class Meta:
        abstract = True


class RubricScore(Score):

    score = models.ForeignKey(RubricScoreValue)
    rubric = models.ForeignKey(Rubric)

    class Meta:
        unique_together = ["evaluation", "rubric"]


class StandardAlignmentScoreValue(ScoreValue):
    pass


class StandardAlignmentScore(Score):

    score = models.ForeignKey(StandardAlignmentScoreValue)
    alignment_tag = models.ForeignKey(AlignmentTag)

    class Meta:
        unique_together = ["evaluation", "alignment_tag"]


class EvaluatedItemMixin(object):

    EVALUATION_SCORE_ATTRIBUTE_RE = re.compile(
        r"^evaluation_score_rubric_(\d)$")

    @Lazy
    def evaluations_number(self):
        content_type = ContentType.objects.get_for_model(self)
        return Evaluation.objects.filter(
            content_type=content_type,
            object_id=self.pk,
            confirmed=True,
            ).count()

    @Lazy
    def evaluation_scores(self):
        scores = {}
        content_type = ContentType.objects.get_for_model(self)
        alignment_scores = StandardAlignmentScore.objects.filter(
            evaluation__content_type=content_type,
            evaluation__object_id=self.pk,
            evaluation__confirmed=True,
            alignment_tag__id__in=self.alignment_tags.all().values_list("tag__id", flat=True).distinct()
            )
        if alignment_scores.exists():
            scores[0] = alignment_scores.aggregate(
                models.Avg("score__value")
            )["score__value__avg"]

        for rubric in Rubric.objects.all():
            rubric_scores = RubricScore.objects.filter(
                evaluation__content_type=content_type,
                evaluation__object_id=self.pk,
                evaluation__confirmed=True,
                rubric=rubric,
                )
            if rubric_scores.exists():
                scores[rubric.id] = rubric_scores.aggregate(
                    models.Avg("score__value")
                )["score__value__avg"]
        return scores

    @property
    def evaluated_rubrics(self):
        return sorted(
            [k for k, v in self.evaluation_scores.items() if v is not None])

    def __getattr__(self, name):
        r = self.EVALUATION_SCORE_ATTRIBUTE_RE.search(name)
        if r:
            rubric_ids = [0] + list(Rubric.objects.values_list("id", flat=True))
            rubric_id = int(r.groups()[0])
            if rubric_id not in rubric_ids:
                raise AttributeError(name)
            return self.evaluation_scores.get(rubric_id)
        #noinspection PyUnresolvedReferences
        if hasattr(super(EvaluatedItemMixin, self), "__getattr__"):
            return super(EvaluatedItemMixin, self).__getattr__(name)
        raise AttributeError(name)


def get_rubric_choices():
    choices = [
        (0, u"Degree of Alignment"),
    ]
    choices += list(Rubric.objects.values_list("id", "name"))
    return choices

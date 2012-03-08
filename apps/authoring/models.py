from annoying.functions import get_object_or_None
from autoslug import AutoSlugField
from common.models import GradeLevel, MediaFormat
from core.fields import AutoCreateForeignKey, AutoCreateManyToManyField
from curriculum.models import TaggedMaterial
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from materials.models import  Keyword, \
    GeneralSubject, License
from materials.models.common import Language
from materials.models.material import TAGGED, REVIEWED, RATED, PUBLISHED_STATE
from materials.models.microsite import Microsite, Topic
from myitems.models import FolderItem
from pyquery import PyQuery as pq
from rating.models import Rating
from reviews.models import Review
from rubrics.models import Evaluation, EvaluatedItemMixin
from saveditems.models import SavedItem
from tags.models import Tag
from visitcounts.models import Visit
import datetime
import embedly
import os


class LearningGoal(models.Model):

    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title


class AbstractAuthoredMaterial(models.Model):

    title = models.CharField(max_length=200, default=u"")
    text = models.TextField(default=u"")

    summary = models.TextField(default=u"")

    learning_goals = AutoCreateManyToManyField(LearningGoal)
    keywords = AutoCreateManyToManyField(Keyword)
    subjects = models.ManyToManyField(GeneralSubject)
    grade_level = models.ForeignKey(GradeLevel, null=True)
    language = models.ForeignKey(Language, null=True)
    license = AutoCreateForeignKey(License, null=True, respect_all_fields=True)

    @property
    def grade_levels(self):
        return [self.grade_level] if self.grade_level else []

    @property
    def languages(self):
        return [self.language] if self.language else []

    class Meta:
        abstract = True


class AuthoredMaterialDraft(AbstractAuthoredMaterial):

    material = models.OneToOneField("authoring.AuthoredMaterial", related_name="draft")


class AuthoredMaterial(AbstractAuthoredMaterial, EvaluatedItemMixin):

    slug = AutoSlugField(populate_from="title")

    owners = models.ManyToManyField(User, related_name="+")
    author = models.ForeignKey(User, related_name="+")

    media_formats = models.ManyToManyField(MediaFormat)

    is_new = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    modified_timestamp = models.DateTimeField(auto_now=True)
    published_on = models.DateTimeField(null=True, blank=True)
    featured = models.BooleanField(default=False, verbose_name=_(u"Featured"))
    featured_on = models.DateTimeField(null=True, blank=True)

    tags = generic.GenericRelation(Tag)
    reviews = generic.GenericRelation(Review)
    saved_items = generic.GenericRelation(SavedItem)
    ratings = generic.GenericRelation(Rating)
    alignment_tags = generic.GenericRelation(TaggedMaterial)
    folders = generic.GenericRelation(FolderItem)

    def get_draft(self):
        draft = get_object_or_None(AuthoredMaterialDraft, material=self)
        if not draft:
            draft = AuthoredMaterialDraft(material=self)
            for field in AbstractAuthoredMaterial._meta.fields:
                setattr(draft, field.name, getattr(self, field.name))
            draft.save()
            for m2m in AbstractAuthoredMaterial._meta.many_to_many:
                setattr(draft, m2m.name, getattr(self, m2m.name).all())
        return draft

    @classmethod
    def publish_draft(cls, draft):
        material = draft.material
        for field in AbstractAuthoredMaterial._meta.fields:
            setattr(material, field.name, getattr(draft, field.name))
        for m2m in AbstractAuthoredMaterial._meta.many_to_many:
            setattr(material, m2m.name, getattr(draft, m2m.name).all())
        material.published = True
        material.is_new = False

        # Update media formats based on different media types included into material text.
        media_formats = [MediaFormat.objects.get(slug="text-html")]
        document = pq(material.text)
        if document.find("figure.image").length:
            media_formats.append(MediaFormat.objects.get(slug="graphics-photos"))
        if document.find("figure.video").length:
            media_formats.append(MediaFormat.objects.get(slug="video"))
        if document.find("figure.audio").length:
            media_formats.append(MediaFormat.objects.get(slug="audio"))
        if document.find("figure.download").length:
            media_formats.append(MediaFormat.objects.get(slug="downloadable-docs"))
        material.media_formats = media_formats

        material.save()
        draft.delete()
        return material

    def save(self, *args, **kwargs):
        if self.published and not self.published_on:
            self.published_on = datetime.datetime.now()
        if self.featured and not self.featured_on:
            self.featured_on = datetime.datetime.now()
        if not self.featured:
            self.featured_on = None

        super(AuthoredMaterial, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return "authoring:view", [], dict(pk=self.pk)

    @property
    def authors(self):
        return [self.author.get_full_name()]

    @property
    def workflow_state(self):
        return PUBLISHED_STATE if self.published else None

    # TODO: move all method below to mixin class
    @property
    def member_activities(self):
        activities = []
        if self.tags.all().count():
            activities.append(TAGGED)
        if self.reviews.all().count():
            activities.append(REVIEWED)
        if self.ratings.all().count():
            activities.append(RATED)
        return activities

    @property
    def rating(self):
        ratings = self.ratings.all()
        if ratings.count():
            return ratings.aggregate(rating=models.Avg("value"))["rating"]
        return 0.0

    def keyword_slugs(self, exclude_microsite_markers=True):
        if exclude_microsite_markers:
            microsite_markers = set()
            for microsite in Microsite.objects.all():
                microsite_markers.update(microsite.keywords.values_list("slug", flat=True))
            keywords = set(self.keywords.exclude(slug__in=microsite_markers).values_list("slug", flat=True))
            keywords.update(self.tags.exclude(slug__in=microsite_markers).values_list("slug", flat=True))
        else:
            keywords = set(self.keywords.values_list("slug", flat=True))
            keywords.update(self.tags.values_list("slug", flat=True))
        return sorted(keywords)

    def keyword_names(self, exclude_microsite_markers=True):
        if exclude_microsite_markers:
            microsite_markers = set()
            for microsite in Microsite.objects.all():
                microsite_markers.update(microsite.keywords.values_list("slug", flat=True))
            keywords = set(self.keywords.exclude(slug__in=microsite_markers).values_list("name", flat=True))
            keywords.update(self.tags.exclude(slug__in=microsite_markers).values_list("name", flat=True))
        else:
            keywords = set(self.keywords.values_list("name", flat=True))
            keywords.update(self.tags.values_list("name", flat=True))
        return sorted(keywords)

    def microsites(self):
        return Microsite.objects.filter(keywords__slug__in=self.keyword_slugs(exclude_microsite_markers=False))

    def topics(self):
        microsites = self.microsites()
        if not microsites.count():
            return []
        topics = set()
        for microsite in self.microsites():
            topics_qs = microsite.topics.exclude(other=True).filter(keywords__slug__in=self.keyword_slugs())
            if topics_qs.count():
                topics.update(topics_qs)
            else:
                try:
                    topics.add(microsite.topics.get(other=True))
                except Topic.DoesNotExist:
                    pass
        return sorted(topics)

    def indexed_topics(self):
        topics = self.topics()
        if len(topics) == 1 and topics[0].other == True:
            return topics
        indexed_topics = set(topics)
        for topic in topics:
            indexed_topics.update(topic.get_ancestors())
        return list(indexed_topics)

    @property
    def visits(self):
        return Visit.objects.get_visits_count(self, None)

    @property
    def is_displayed(self):
        return self.published

    @property
    def is_evaluated(self):
        content_type = ContentType.objects.get_for_model(self)
        return Evaluation.objects.filter(
            content_type=content_type,
            object_id=self.id,
            confirmed=True).exists()

    @property
    def alignment_standards(self):
        return self.alignment_tags.values_list("tag__standard__id", flat=True).order_by().distinct()

    @property
    def alignment_grades(self):
        grades = []
        for grade, end_grade in self.alignment_tags.values_list("tag__grade__code", "tag__end_grade__code").order_by().distinct():
            grades.append("%s-%s" % (grade, end_grade) if grade else grade)
        return grades

    @property
    def alignment_categories(self):
        return self.alignment_tags.values_list("tag__category__id", flat=True).order_by().distinct()

    @property
    def saved_in_folders(self):
        return self.folders.values_list("folder__id", flat=True)


def upload_to(prefix):
    def func(instance, filename):
        return os.path.join("authoring", str(instance.material.id), prefix, filename)
    return func


class Image(models.Model):

    material = models.ForeignKey(AuthoredMaterial)

    image = models.ImageField(upload_to=upload_to("images"))


class Document(models.Model):

    material = models.ForeignKey(AuthoredMaterial)

    file = models.ImageField(upload_to=upload_to("documents"))


class Embed(models.Model):

    url = models.URLField(unique=True, db_index=True, max_length=200)
    type = models.CharField(db_index=True, max_length=20)
    title = models.CharField(max_length=500, null=True, blank=True)
    embed_url = models.URLField(db_index=True, max_length=200, null=True, blank=True) # This is used for photo embeds
    thumbnail = models.URLField(db_index=True, max_length=200, null=True, blank=True)
    html = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.url

    @classmethod
    def get_for_url(cls, url):
        if cls.objects.filter(url=url).exists():
            return cls.objects.get(url=url)

        client = embedly.Embedly(settings.EMBEDLY_KEY)
        if client.is_supported(url):
            result = client.oembed(url, maxwidth="500")
            url = result.url or result.original_url

            if cls.objects.filter(url=url).exists():
                return cls.objects.get(url=url)

            return cls.objects.create(
                url=url,
                type=result.type,
                title=result.title,
                embed_url=url,
                thumbnail=result.thumbnail_url,
                html=result.html,
            )

        return None
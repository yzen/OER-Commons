from autoslug.fields import AutoSlugField
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext_lazy as _
from materials.models import License
from tags.models import Tag


PUBLISHED_STATE = u"published"
PRIVATE_STATE = "private"
PENDING_STATE = u"pending"
REJECTED_STATE = u"rejected"


WORKFLOW_STATES = (
   (PUBLISHED_STATE, _(u"Published")),
   (PRIVATE_STATE, _(u"Private")),
   (PENDING_STATE, _(u"Pending")),
   (REJECTED_STATE, _(u"Rejected")),
)

RATED = u"rated"
REVIEWED = u"reviewed"
TAGGED = u"tagged"

MEMBER_ACTIVITY_TYPES = (
    (RATED, u'Only Items with Ratings'),
    (REVIEWED, u'Only Items with Reviews'),
    (TAGGED, u'Only Items with Tags'),
)


class Material(models.Model):

    namespace = None

    title = models.CharField(max_length=500, verbose_name=_(u"Title"))
    slug = AutoSlugField(populate_from='title', unique=True,
                         verbose_name=_(u"Slug"))

    created_on = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u"Created on"))
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True,
                                      verbose_name=_(u"Modified on"))

    workflow_state = models.CharField(max_length=50, default=u"private",
                                      choices=WORKFLOW_STATES,
                                      verbose_name=_(u"Workflow state"))
    published_on = models.DateTimeField(null=True, blank=True,
                                        verbose_name=_(u"Published on"))

    creator = models.ForeignKey(User, verbose_name=_("Creator"))

    license = models.ForeignKey(License, verbose_name=_(u"License"))

    in_rss = models.BooleanField(default=False,
                                 verbose_name=_(u"Include in RSS"))
    rss_description = models.TextField(default=u"", blank=True,
                                       verbose_name=_(u"RSS Description"))
    rss_timestamp = models.DateTimeField(null=True, blank=True,
                                         verbose_name=_(u"RSS Date/Time"))

    featured = models.BooleanField(default=False, verbose_name=_(u"Featured"))

    tags = generic.GenericRelation(Tag)

    class Meta:
        app_label = "materials"
        abstract = True

    @property
    def member_activities(self):
        activities = []
        if self.tags.all().count():
            activities.append(TAGGED)
        return activities
        # TODO: add rated and reviewed
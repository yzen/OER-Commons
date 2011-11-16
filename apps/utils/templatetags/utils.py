from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site, RequestSite
from django.forms.fields import FileField
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.template.defaulttags import Node


register = Library()


@register.filter
@stringfilter
def full_url(path):
    return "http://%s%s" % (Site.objects.get_current().domain, path)
full_url.is_safe = True


class DomainNode(Node):

    def render(self, context):
        request = context["request"]
        site = getattr(context, "__site", None)
        if not site:
            if Site._meta.installed:
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)
            context.__site = site
        return site.domain

@register.tag
def domain(parser, token):
    return DomainNode()


class ProtocolNode(Node):

    def render(self, context):
        request = context["request"]
        return request.is_secure() and 'https://' or 'http://'


@register.tag
def protocol(parser, token):
    return ProtocolNode()


@register.inclusion_tag("utils/include/next-url-input.html",
                        takes_context=True)
def next_url_input(context):
    request = context["request"]
    field_name = settings.REDIRECT_FIELD_NAME
    next_url = request.REQUEST.get(field_name, u"")
    return dict(field_name=field_name, next_url=next_url)


@register.filter
def bound_field_value(field):
    if not field.form.is_bound:
        data = field.form.initial.get(field.name, field.field.initial)
        if callable(data):
            data = data()
    else:
        if isinstance(field.field, FileField) and field.data is None:
            data = field.form.initial.get(field.name, field.field.initial)
        else:
            data = field.data
    return data


@register.filter
@stringfilter
def truncatechars(value, arg, ellipsis=u"..."):
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int().
        return value # Fail silently. full_url.is_safe = True
    if len(value) > length:
        value = value[:length-len(ellipsis)] + ellipsis
        assert len(value) == length
    return value

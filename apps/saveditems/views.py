from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from saveditems.models import SavedItem
from utils.decorators import login_required
from utils.shortcuts import redirect_to_next_url
from haystack.sites import site


@login_required
def save(request, slug=None, model=None):
    ''' Save item if it isn't saved.
    Unsave item if it's saved. '''

    if not slug or not model:
        raise Http404()

    item = get_object_or_404(model, slug=slug)

    content_type = ContentType.objects.get_for_model(item)
    object_id = item.id
    SavedItem.objects.get_or_create(content_type=content_type,
                          object_id=object_id,
                          user=request.user)

    site.update_object(item)

    if request.method == "POST":
        # Save item by AJAX request
        return HttpResponse(u"Item was saved in your collection.",
                            content_type="application/json")

    messages.success(request, u"Item was saved in your collection.")
    return redirect_to_next_url(request, item.get_absolute_url())


@login_required
def unsave(request, slug=None, model=None):

    if not slug or not model:
        raise Http404()

    item = get_object_or_404(model, slug=slug)

    content_type = ContentType.objects.get_for_model(item)
    object_id = item.id
    try:
        SavedItem.objects.get(content_type=content_type,
                              object_id=object_id,
                              user=request.user).delete()
        site.update_object(item)

        if request.method == "POST":
            # Unsave item by AJAX request
            return HttpResponse(u"Item was removed from your collection.",
                                content_type="application/json")

        messages.success(request, u"Item was removed from your collection.")
    except SavedItem.DoesNotExist:
        pass

    return redirect_to_next_url(request, item.get_absolute_url())
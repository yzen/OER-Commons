from curriculum.views import TagDescription
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("curriculum.views",
    url(r"^curriculum/add/(\w+)/(\w+)/(\d+)/?$", "align", name="align"),
    url(r"^curriculum/get-tags/(\w+)/(\w+)/(\d+)/?$", "get_item_tags", name="get_item_tags"),
    url(r"^curriculum/delete/?$", "delete_tag", name="delete_tag"),
    url(r"^curriculum/list_standards/?$", "list_standards", name="list_standards"),
    url(r"^curriculum/list_standards/existing/?$", "list_standards", dict(existing=True), name="list_existing_standards"),
    url(r"^curriculum/list_grades/?$", "list_grades", name="list_grades"),
    url(r"^curriculum/list_grades/existing/?$", "list_grades", dict(existing=True), name="list_existing_grades"),
    url(r"^curriculum/list_categories/?$", "list_categories", name="list_categories"),
    url(r"^curriculum/list_categories/existing/?$", "list_categories", dict(existing=True), name="list_existing_categories"),
    url(r"^curriculum/list_tags/?$", "list_tags", name="list_tags"),
    url(r"^curriculum/list_tags/existing/?$", "list_tags", dict(existing=True), name="list_existing_tags"),
    url(r"^curriculum/get_tag_description/(?P<code>[\w\.\-]+)(?:/(?P<content_type_id>\d+)/(?P<object_id>\d+))?$", TagDescription.as_view(), name="get_tag_description"),
)

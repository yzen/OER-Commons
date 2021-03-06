from annoying.decorators import JsonResponse
from autoslug.settings import slugify
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic.simple import direct_to_template
from haystack.query import SearchQuerySet
from materials.models.common import GeneralSubject, GradeLevel, Collection, \
    Keyword, GeographicRelevance, Institution
from materials.models.community import CommunityItem
from materials.models.microsite import Microsite, Topic
from materials.utils import get_name_from_id, get_slug_from_id, \
    first_neighbours_last, get_name_from_slug, get_object
from materials.views.csv_export import csv_export
from materials.views.filters import FILTERS, VocabularyFilter, ChoicesFilter
from rubrics.models import Rubric
from tags.models import Tag
from tags.tags_utils import get_tag_cloud
import urllib


MAX_TOP_KEYWORDS = 25


def serialize_query_string_params(query_string_params, ignore_params=None):
    if not ignore_params: ignore_params = []
    params = []
    for key, value in query_string_params.items():
        if key in ignore_params:
            continue
        if isinstance(value, list):
            for v in value:
                if isinstance(v, unicode):
                    v = v.encode("utf-8")
                params.append((key, v))
        else:
            if isinstance(value, unicode):
                value = value.encode("utf-8")
            params.append((key, value))
    params.sort()
    serialized = urllib.urlencode(params)
    if serialized:
        return "?" + serialized
    return u""


class Pagination:

    def __init__(self, path, query_string_params, batch_start, batch_size,
                 total_items):
        self.total_items = total_items
        self.first_item_number = batch_start + 1
        self.last_item_number = batch_start + batch_size
        if self.last_item_number > self.total_items:
            self.last_item_number = self.total_items
        self.first_page_url = None
        self.last_page_url = None
        self.next_page_url = None
        self.prev_page_url = None
        self.pages = []

        if self.total_items:
            total_pages = total_items / batch_size
            if total_items % batch_size:
                total_pages += 1
            current_page = batch_start / batch_size

            if current_page:
                self.first_page_url = path + serialize_query_string_params(query_string_params, ["batch_start"])

                params = query_string_params.copy()
                if (current_page - 1) * batch_size:
                    params["batch_start"] = (current_page - 1) * batch_size
                elif "batch_start" in params:
                    del params["batch_start"]
                self.prev_page_url = path + serialize_query_string_params(params)

            if current_page < (total_pages - 1):
                params = query_string_params.copy()
                params["batch_start"] = (total_pages - 1) * batch_size
                self.last_page_url = path + serialize_query_string_params(params)

                params = query_string_params.copy()
                params["batch_start"] = (current_page + 1) * batch_size
                self.next_page_url = path + serialize_query_string_params(params)

            for page in first_neighbours_last(xrange(total_pages), current_page, 3, 3):
                if page is None:
                    pass
                elif page == current_page:
                    page = dict(number=page + 1, url=None)
                else:
                    params = query_string_params.copy()
                    if page * batch_size:
                        params["batch_start"] = page * batch_size
                    elif "batch_start" in params:
                        del params["batch_start"]
                    url = path + serialize_query_string_params(params)
                    page = dict(number=page + 1, url=url)
                self.pages.append(page)


BASIC_INDEX_FILTERS = (
  ("general_subjects", False,),
  ("grade_levels", False,),
  ("course_material_types", True,),
  ("media_formats", True,),
  ("cou_bucket", True),
)


def build_index_filters(visible_filters, facets, filter_values, path_filter,
                        microsite=None):
    filters = {}
    for filter_name, collapsed in BASIC_INDEX_FILTERS:
        if filter_name not in visible_filters:
            continue
        filter_ = FILTERS[filter_name]
        if not facets.get(filter_.index_name):
            continue
        counts = dict(facets[filter_.index_name])
        values = filter_values.get(filter_name, [])
        filter_data = {"name": filter_name,
                       "title": filter_.title,
                       "disabled": filter_name == path_filter,
                       "options": [],
                       "all_checked": not bool(values),
                       "request_name": filter_.request_name,
                       "collapsed": collapsed}
        if values:
            filter_data["collapsed"] = False
        if isinstance(filter_, VocabularyFilter):
            if not isinstance(values, list):
                values = [values]
            for option in filter_.model.objects.values("id", "slug", "name"):
                count = counts.get(str(option["id"]), 0)
                option["count"] = count
                if filter_data["all_checked"] or option["slug"] in values:
                    option["checked"] = True
                option["input_id"] = "%s-%i" % (filter_data["request_name"].replace(".", "-"), option["id"])
                filter_data["options"].append(option)
        elif isinstance(filter_, ChoicesFilter):
            if not isinstance(values, list):
                values = [values]
            for i, (slug, name) in enumerate(filter_.choices):
                option = {"id": i, "slug": slug, "name": name}
                count = counts.get(slug, 0)
                option["count"] = count
                if filter_data["all_checked"] or slug in values:
                    option["checked"] = True
                option["input_id"] = "%s-%i" % (filter_data["request_name"].replace(".", "-"), option["id"])
                filter_data["options"].append(option)
        if len(filter_data["options"]) == len(values):
            filter_data["all_checked"] = True
        filters[filter_name] = filter_data

    if microsite:
        filter_name = "topics"
        filter_ = FILTERS[filter_name]
        if not facets.get(filter_.index_name):
            return filters
        counts = dict(facets[filter_.index_name])
        values = filter_values.get(filter_name, [])
        filter_data = {"name": filter_name,
                       "title": u"%s %s" % (microsite.name, filter_.title),
                       "disabled": filter_name == path_filter,
                       "options": [],
                       "all_checked": not bool(values),
                       "request_name": filter_.request_name,
                       "collapsed": False}
        if not isinstance(values, list):
            values = [values]
        for option in Topic.objects.filter(microsite=microsite).values("id", "slug", "name").order_by("id"):
            count = counts.get(str(option["id"]), 0)
            option["count"] = count
            if filter_data["all_checked"] or option["slug"] in values:
                option["checked"] = True
            option["input_id"] = "%s-%i" % (filter_data["request_name"].replace(".", "-"), option["id"])
            filter_data["options"].append(option)
        if len(filter_data["options"]) == len(values):
            filter_data["all_checked"] = True
        filters[filter_name] = filter_data

    return filters


PATH_FILTERS = ["general_subjects", "grade_levels", "course_material_types",
                "library_material_types", "collection", "keywords", "license",
                "course_or_module", "community_types",
                "community_topics", "microsite", "topics", "alignment"]


class IndexParams:

    BATCH_SIZE_OPTIONS = (
        10, 20, 50, 100
    )

    DEFAULT_BATCH_SIZE = 20

    SORT_BY_OPTIONS = (
        {"value": u"title", "title": u"Title"},
        {"value": u"search", "title": u"Relevance"},
        {"value": u"rating", "title": u"Rating"},
        {"value": u"date", "title": u"Date"},
        {"value": u"visits", "title": u"Visits"},
    )

    def __init__(self, request, format="html", search_query=None):

        self.default_sort_by = search_query and "search" or "title"
        self.format = format
        self.search_query = search_query
        self.batch_start = 0
        self.batch_size = self.DEFAULT_BATCH_SIZE
        self.sort_by = self.default_sort_by
        self.use_default_sort_by = True
        self.query_order_by = None

        try:
            self.batch_start = int(request.REQUEST.get("batch_start", 0))
        except ValueError:
            pass

        try:
            batch_size = int(request.REQUEST.get("batch_size", 0))
            if batch_size in self.BATCH_SIZE_OPTIONS:
                self.batch_size = batch_size
        except ValueError:
            pass

        sort_by = request.REQUEST.get("sort_by", request.REQUEST.get("sort_on"))
        if not sort_by or sort_by not in [o["value"] for o in self.SORT_BY_OPTIONS]:
            if sort_by == "publication_time":
                self.sort_by = "date"
            elif sort_by == "overall_rating":
                self.sort_by = "rating"
            elif search_query:
                self.sort_by = "search"
        else:
            self.use_default_sort_by = False
            self.sort_by = sort_by


        if format == "rss":
            self.query_order_by = "-published_on"
        elif self.sort_by == "search":
            self.query_order_by = None
        elif self.sort_by == "date":
            self.query_order_by = "-published_on"
        elif self.sort_by == "rating":
            self.query_order_by = "-rating"
        elif self.sort_by == "visits":
            self.query_order_by = "-visits"
        else:
            self.query_order_by = "sortable_title"


    def update_query_string_params(self, query_string_params):
        if self.batch_start:
            query_string_params["batch_start"] = self.batch_start
        if self.batch_size != self.DEFAULT_BATCH_SIZE:
            query_string_params["batch_size"] = self.batch_size
        if self.sort_by != self.default_sort_by:
            query_string_params["sort_by"] = self.sort_by
        return query_string_params


def populate_item_from_search_result(result):
    item = result.get_stored_fields()

    item["identifier"] = "%s.%s.%s" % (result.app_label,
                                       result.model_name,
                                       result.pk)

    if item.get("collection"):
        collection_id = item["collection"]
        item["collection"] = {"name": get_name_from_id(Collection,
                                                       collection_id),
                              "slug": get_slug_from_id(Collection,
                                                       collection_id)}
    if item.get("general_subjects"):
        item["general_subjects"] = [get_name_from_id(
             GeneralSubject, id) for id in item["general_subjects"]]

    if item.get("grade_levels"):
        item["grade_levels"] = [get_name_from_id(
                     GradeLevel, id) for id in item["grade_levels"]]

    if item.get("topics"):
        topics = []
        for id in item["topics"]:
            topic = get_object(Topic, pk=id)
            if not topic:
                continue
            topics.append(topic)
        item["topics"] = topics

    item["is_evaluated"] = bool(result.evaluated_rubrics)

    model = result.model

    namespace = getattr(model, "namespace", None)
    if namespace:
        item["get_absolute_url"] = reverse(
                               "materials:%s:view_item" % namespace,
                               kwargs=dict(slug=item["slug"]))
        item["save_item_url"] = reverse(
                               "materials:%s:save_item" % namespace,
                               kwargs=dict(slug=item["slug"]))
        item["unsave_item_url"] = reverse(
                               "materials:%s:unsave_item" % namespace,
                               kwargs=dict(slug=item["slug"]))
        item["add_tags_url"] = reverse("tags:add_tags", args=(
                                    result.app_label,
                                    result.model_name,
                                    result.pk,
                                ))
        item["toolbar_view_url"] = reverse(
                               "materials:%s:toolbar_view_item" % namespace,
                               kwargs=dict(slug=item["slug"]))
        item["align_url"] = reverse("curriculum:align", args=(
                                    result.app_label,
                                    result.model_name,
                                    result.pk,
                                ))
    else:
        item["get_absolute_url"] = result.object.get_absolute_url()
    return item


def index(request, general_subjects=None, grade_levels=None,
          course_material_types=None, library_material_types=None,
          collection=None, keywords=None, license=None, course_or_module=None,
          community_types=None, community_topics=None, microsite=None,
          model=None, search=False, tags=None, subjects=None, format=None,
          topics=None, alignment=None, facet_fields=None):

    if not facet_fields: facet_fields = ["general_subjects", "grade_levels",
                                         "keywords",
                                         "course_material_types",
                                         "media_formats",
                                         "cou_bucket", "indexed_topics"]
    if model:
        index_namespace = model.namespace
    else:
        index_namespace = None

    if tags or subjects:
        # Tags and subjects are old path filters which are combined to
        # keywords filter now.

        # Redirect to keyword index.
        keywords = tags or subjects
        if index_namespace:
            url = reverse("materials:%s:keyword_index" % index_namespace,
                          kwargs=dict(keywords=keywords))
        else:
            url = reverse("materials:keyword_index",
                          kwargs=dict(keywords=keywords))
        return HttpResponsePermanentRedirect(url)

    if keywords:
        slugified_keywords = slugify(keywords)
        if not slugified_keywords:
            raise Http404()
        if slugified_keywords != keywords:
            # Keywords should be slugified.
            # Redirect to keyword index with slugified keyword.
            if index_namespace:
                url = reverse("materials:%s:keyword_index" % index_namespace,
                              kwargs=dict(keywords=slugified_keywords))
            else:
                url = reverse("materials:keyword_index",
                              kwargs=dict(keywords=slugified_keywords))
            return HttpResponsePermanentRedirect(url)

    query_string_params = {}
    filter_values = {}
    page_title = u"Browse"
    page_subtitle = u""
    breadcrumbs = [{"url": reverse("materials:browse"), "title": u"OER Materials"}]

    if not format:
        format = "html"
        if request.REQUEST.get("feed", None) == "yes":
            format = "rss"
        elif request.REQUEST.get("csv", None) == "yes":
            if not request.user.is_authenticated() or not request.user.is_staff:
                raise Http404()
            format = "csv"

    query = SearchQuerySet().narrow("is_displayed:true")

    if model:
        query = query.models(model)

    path_filter = None

    hidden_filters = {}

    for filter_name in PATH_FILTERS:
        value = locals()[filter_name]
        if value is not None:
            filter_ = FILTERS[filter_name]
            query = filter_.update_query(query, value)
            path_filter = filter_name
            if page_subtitle:
                page_subtitle = u"%s &rarr; %s" % (page_subtitle, filter_.page_subtitle(value))
            else:
                page_subtitle = filter_.page_subtitle(value)
            filter_values[filter_name] = value

    visible_filters = ["search", "general_subjects", "grade_levels",
                       "course_material_types", "media_formats",
                       "cou_bucket"]

    if microsite:
        microsite = Microsite.objects.get(slug=microsite)
        visible_filters.append("topics")


    search_query = u""

    for filter_name, filter_ in FILTERS.items():
        if filter_name == path_filter:
            continue
        value = filter_.extract_value(request)
        if value is not None:
            query = filter_.update_query(query, value)
            query_string_params = filter_.update_query_string_params(query_string_params, value)
            filter_values[filter_name] = value
            if filter_name not in visible_filters:
                hidden_filters[filter_.request_name] = value
            if filter_name == "search":
                search_query = value


    if search:
        if not search_query:
            if filter_values:
                return HttpResponsePermanentRedirect(reverse("materials:index") + serialize_query_string_params(query_string_params))
            else:
                messages.warning(request, u"You should specify the search term")
                return HttpResponsePermanentRedirect(reverse("materials:advanced_search"))

        page_title = u"Search Results"
        page_subtitle = search_query
        breadcrumbs = [{"url": reverse("materials:search"), "title": page_title}]

    elif model == CommunityItem:
        breadcrumbs = [{"url": reverse("materials:community"), "title": u"OER Community"}]


    if microsite:
        breadcrumbs = [{"url": reverse("materials:microsite", kwargs=dict(microsite=microsite.slug)), "title": u"%s Home" % microsite.name}]

    if not page_subtitle and model:
        page_subtitle = u"Content Type: %s" % model._meta.verbose_name_plural
    elif not page_subtitle and filter_values:
        subtitles = []
        for filter_name, filter_ in FILTERS.items():
            if filter_name not in filter_values:
                continue
            subtitles.append(filter_.page_subtitle(filter_values[filter_name]))
        page_subtitle = u" / ".join(subtitles)

    index_params = IndexParams(request, format, search_query)
    query_string_params = index_params.update_query_string_params(query_string_params)

    index_url = request.path + serialize_query_string_params(query_string_params,
                                             ignore_params=["batch_start"])
    if page_subtitle:
        index_title = u"%s: %s" % (page_title, page_subtitle)
    else:
        index_title = page_title

    feed_url = request.path + serialize_query_string_params(dict(query_string_params.items() + [("feed", "yes")]),
                                             ignore_params=["batch_start"])
    csv_url = request.path + serialize_query_string_params(dict(query_string_params.items() + [("csv", "yes")]),
                                             ignore_params=["batch_start"])

    batch_end = index_params.batch_start + index_params.batch_size

    if len(filter_values) == 1 and "featured" in filter_values:
        index_params.query_order_by = "-featured_on"

    elif "evaluated_rubrics" in filter_values:
        rubric_id = filter_values["evaluated_rubrics"][0]
        if rubric_id == 0:
            rubric_name = u"Degree of Alignment"
        else:
            rubric_name = Rubric.objects.get(id=rubric_id).name
        index_params.SORT_BY_OPTIONS = list(index_params.SORT_BY_OPTIONS) + [
            dict(value="evaluation_score_rubric_%i" % rubric_id,
                 title=rubric_name)
        ]
        if index_params.use_default_sort_by:
            index_params.sort_by = "evaluation_score_rubric_%i" % rubric_id
            index_params.query_order_by = "-evaluation_score_rubric_%i" % rubric_id

    elif filter(lambda f: f in filter_values, ("alignment", "alignment_standards",
            "alignment_grades", "alignment_categories", "alignment_cluster")):
        index_params.SORT_BY_OPTIONS = list(index_params.SORT_BY_OPTIONS) + [
            dict(value="evaluation_score_rubric_0",
                 title=u"Degree of Alignment")
        ]
        if index_params.use_default_sort_by:
            index_params.sort_by = "evaluation_score_rubric_0"
            index_params.query_order_by = "-evaluation_score_rubric_0"

    if index_params.query_order_by:
        query = query.order_by(index_params.query_order_by)

    if index_params.sort_by == "visits" and not filter_values:
        query = query.narrow("visits:[1 TO *]")

    items = []

    if format == "html":

        for facet_field in facet_fields:
            query = query.facet(facet_field)

        total_items = len(query)

        if total_items and index_params.batch_start >= total_items:
            return HttpResponsePermanentRedirect(index_url)

        results = query[index_params.batch_start:batch_end]
        for result in results:
            if result is None:
                continue
            items.append(populate_item_from_search_result(result))

        pagination = Pagination(request.path, query_string_params,
                                index_params.batch_start,
                                index_params.batch_size,
                                total_items)

        facets = query.facet_counts().get("fields", {})

        index_filters = build_index_filters(visible_filters,
                                            facets,
                                            filter_values,
                                            path_filter,
                                            microsite)

        all_keywords = query.count() and facets.get("keywords", []) or []
        if len(all_keywords) > MAX_TOP_KEYWORDS:
            top_keywords = get_tag_cloud(dict(all_keywords[:MAX_TOP_KEYWORDS]),
                                              3, 0, 0)
            all_keywords = get_tag_cloud(dict(all_keywords), 3, 0, 0)
        else:
            top_keywords = get_tag_cloud(dict(all_keywords), 3, 0, 0)
            all_keywords = []

        for keyword in top_keywords:
            name = get_name_from_slug(Keyword, keyword["slug"]) or \
                   get_name_from_slug(Tag, keyword["slug"]) or \
                   keyword["slug"]
            keyword["name"] = name
        for keyword in all_keywords:
            name = get_name_from_slug(Keyword, keyword["slug"]) or \
                   get_name_from_slug(Tag, keyword["slug"]) or \
                   keyword["slug"]
            keyword["name"] = name


        if request.is_ajax():
            output = render_to_string("materials/include/index-items.html",
                                      RequestContext(request, locals()))
            data = dict(items=output,
                        first_item_number=pagination.first_item_number,
                        last_item_number=pagination.last_item_number,
                        total_items=pagination.total_items,
                        page_title=unicode(page_title),
                        page_subtitle=page_subtitle and unicode(page_subtitle or u""))
            return JsonResponse(data)
        return direct_to_template(request, "materials/index.html", locals())

    elif format == "rss":
        results = query[0:20]
        for result in results:
            if result is None:
                continue
            item = result.get_stored_fields()
            if item.get("general_subjects"):
                item["general_subjects"] = [get_name_from_id(
                     GeneralSubject, id) for id in item["general_subjects"]]

            namespace = getattr(result.model, "namespace", None)
            if namespace:
                item["get_absolute_url"] = reverse(
                                       "materials:%s:view_item" % namespace,
                                       kwargs=dict(slug=item["slug"]))
            else:
                item["get_absolute_url"] = result.object.get_absolute_url()

            item["model_verbose_name"] = result.model._meta.verbose_name_plural

            items.append(item)

        return direct_to_template(request, "materials/index-rss.xml", locals(),
                                  "text/xml")

    elif format == "json":
        results = query[index_params.batch_start:batch_end]

        for result in results:
            if result is None:
                continue
            data = result.get_stored_fields()
            item = {"id": result.id,
                    "title": data["title"],
                    "abstract": data["abstract"],
                    "url": data["url"],
                    "keywords": data["keywords_names"],
                    "subject": [get_slug_from_id(GeneralSubject, id) for id in
                        (data["general_subjects"] or [])],
                    "grade_level": [get_slug_from_id(GradeLevel, id) for id in
                        (data["grade_levels"] or [])],
                    "collection": data["collection"] and get_name_from_id(
                        Collection, data["collection"]) or None}
            items.append(item)

        return JsonResponse(items)

    elif format == "xml":
        query = query.load_all()
        results = query[index_params.batch_start:batch_end]

        for result in results:
            if result is None:
                continue
            object = result.object
            data = result.get_stored_fields()
            item = {"url": data["url"],
                    "title": data["title"]}
            if data.get("authors"):
                item["author"] = data["authors"][0]
            if data.get("institution"):
                item["institution"] = get_name_from_id(Institution, data["institution"])
            item["abstract"] = data["abstract"]

            license = object.license
            item["copyright_holder"] = license.copyright_holder
            item["license_url"] = license.url
            item["license_name"] = license.name
            item["license_description"] = license.description
            item["license_type"] = license.type
            item["cou_bucket"] = license.bucket

            if data["rating"]:
                item["rating"] = '%.1f' % data["rating"]

            item["fields"] = []
            grade_levels = data.get("grade_levels")
            if grade_levels:
                item["fields"].append(dict(title=u"Grade Level",
                                           param=FILTERS["grade_levels"].request_name,
                                           value=u",".join([get_slug_from_id(GradeLevel, id) for id in grade_levels]),
                                           content=u",".join([get_name_from_id(GradeLevel, id) for id in grade_levels])
                                           ))
            general_subjects = data.get("general_subjects")
            if general_subjects:
                item["fields"].append(dict(title=u"Subject",
                                           param=FILTERS["general_subjects"].request_name,
                                           value=u",".join([get_slug_from_id(GeneralSubject, id) for id in general_subjects]),
                                           content=u",".join([get_name_from_id(GeneralSubject, id) for id in general_subjects])
                                           ))
            collection = data.get("collection")
            if collection:
                item["fields"].append(dict(title=u"Collection",
                                           param=FILTERS["collection"].request_name,
                                           value=get_slug_from_id(Collection, collection),
                                           content=get_name_from_id(Collection, collection)
                                           ))
            geographic_relevance = data.get("geographic_relevance")
            if geographic_relevance:
                item["fields"].append(dict(title=u"Geographic Regional Relevance",
                                           param=FILTERS["geographic_relevance"].request_name,
                                           value=u",".join([get_slug_from_id(GeographicRelevance, id) for id in geographic_relevance]),
                                           content=u",".join([get_name_from_id(GeographicRelevance, id) for id in geographic_relevance])
                                           ))

            keywords = object.keywords.values("slug", "name")
            if keywords:
                item["fields"].append(dict(title=u"Keywords",
                                           param=FILTERS["keywords"].request_name,
                                           value=u",".join([k["slug"] for k in keywords]),
                                           content=u",".join([k["name"] for k in keywords]),
                                           ))


            tags = object.tags.values("slug", "name").order_by("slug").distinct()
            if tags:
                item["fields"].append(dict(title=u"Tags",
                                           param=FILTERS["keywords"].request_name,
                                           value=u",".join([k["slug"] for k in tags]),
                                           content=u",".join([k["name"] for k in tags]),
                                           ))

            items.append(item)

        return direct_to_template(request, "materials/index-xml.xml", locals(),
                                  "text/xml")

    elif format == "csv":
        return csv_export(query, index_title)


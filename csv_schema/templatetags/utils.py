# templatetags file
from django import template
from django.urls import resolve

register = template.Library()


@register.filter(name="chunks")
def chunks(iterable, chunk_size):
    if not hasattr(iterable, "__iter__"):
        # can't use "return" and "yield" in the same function
        yield iterable
    else:
        i = 0
        chunk = []
        for item in iterable:
            chunk.append(item)
            i += 1
            if not i % chunk_size:
                yield chunk
                chunk = []
        if chunk:
            # some items will remain which haven't been yielded yet,
            # unless len(iterable) is divisible by chunk_size
            yield chunk


@register.filter(name="url_name")
def url_name(request):
    return resolve(request.path_info).url_name


@register.filter(name="viewable")
def viewable(query_set, request):
    return query_set.viewable(request.user)

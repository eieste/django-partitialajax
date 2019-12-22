from django import template
from partitialajax.contrib.html import split_selector
from django.utils.translation import pgettext_lazy as __
import base64

register = template.Library()


def _encode_partitial_parameter(data):
    """
        Helper method; It converts a python string to Base64 (using utf8)

        :param data: string
        :return: base64 encoded string
    """
    return base64.b64encode(data.encode("utf-8")).decode()


@register.inclusion_tag('partitialajax/partitial_include.html', takes_context=True)
def direct_partitial(context, selector, **kwargs):
    """
        Embedds a Partitial without initiial loading, or updates

        :param context: (Automatic Argument) Render Context
        :param selector: String which partitial should be included. (Same as defined in Partitial List)
        :param kwargs: Possible kwargs: allowed_methods, reload, url
        :return context: new dict with rended context
    """

    data = __("selector at template not defined in view error message", "Sorry unable to get Element to display Data")

    if selector in context["partitial"]:
        data = context["partitial"][selector]["content"]

    context["partitial"] = {
        "data": data,
        "specific": {
            "selector": split_selector(selector),
            "selectorstring": _encode_partitial_parameter(selector),
            "reload": kwargs.get("reload", False),
            "url": kwargs.get("url", context["request"].build_absolute_uri()),
            "allowed_elements": _encode_partitial_parameter(kwargs.get("allowed-elements", ""))
        }
    }
    return context

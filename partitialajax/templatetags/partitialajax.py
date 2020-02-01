from django import template
from partitialajax.contrib.html import split_selector
from django.utils.translation import pgettext_lazy as __
import base64
from partitialajax.exceptions import PartitialNotFound

register = template.Library()


def _encode_partitial_parameter(data):
    """
        Helper method; It converts a python string to Base64 (using utf8)

        :param data: string
        :return: base64 encoded string
    """
    return base64.b64encode(data.encode("utf-8")).decode()


def fixbool(data):
    bool_attrs = ("only-child-replace", "restrict-remote-configuration", "config-from-element", "direct-load")
    new_data = {}
    for key, item in data.items():

        if key in bool_attrs:
            if item:
                new_data[key] = "true"
            new_data[key] = "false"
        elif not item == "":
            new_data[key] = item
    return new_data

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

    if "partitial" not in context:
        raise PartitialNotFound("No Partitials defined")


    if selector in context["partitial"]:
        data = context["partitial"][selector]["content"]
    else:
        raise PartitialNotFound(f"No Partitial with selector '{selector}' was found")

    splited_selector = split_selector(selector)
    if splited_selector["element"] is None:
        splited_selector["element"] = "div"
    splited_selector["class_list"].add("ajaxpartitial-container")

    context["partitial"].update({ "current": {
        "data": data,
        "selector": splited_selector,
        "prefix": "partitial",
        "specific": fixbool({
            "url": kwargs.get("url", ""),
            "only-child-replace": kwargs.get("onlyChildReplace", True),
            "interval": kwargs.get("interval", -1),
            "allowed-elements": kwargs.get("allowedElements", "all"),
            "text-event-callback": kwargs.get("textEventCallback", "console.info"),
            "restrict-remote-configuration": kwargs.get("restrictRemoteConfiguration", False),
            "config-from-element": kwargs.get("configFromElement", True),
            "direct-load": kwargs.get("directLoad", False),
            "self": selector
        })
    }})
    return context


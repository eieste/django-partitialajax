from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import Template
from django.views.generic import View
import requests


class PartitialAjaxMixin:
    """
        Add this Mixin to your View to activate the useage of PartitialAjax
    """

    #: Define here all partitial html files used in the template_name File
    #: Write as follows: {"#foobar": "myapp/partitial/foo.html"}
    partitial_list = {}

    def get_partitial_list(self, *args, **kwargs):
        """
            Returns a dict with keys as selectors and values as partitial file paths
            :return: dict

            :Example:
            {"#foo": "myapp/partitials/foo.html"}
        """

        if len(self.partitial_list) <= 0:
            raise ValueError("partial list must not be empty")
        return self.partitial_list

    def get_partitial(self, origin, context):
        """
            Collect Partitial Contents from template or remote url

            :param origin: tuple or string; if tuple: the first value is the path to template or remote the second is the keyword "template", "remote"
            :param context: context used for rendering (remote paths also renderd with this context)
            :return:
        """
        if origin is tuple:
            if "template" in origin[1]:
                tpl = get_template(origin[0])
                return {
                    "template": tpl,
                    "content": tpl.render(context)
                }
            elif "remote" in origin[1]:
                with requests.get(origin[0]) as r:
                    tpl = Template(r.text)
                return {
                    "path": origin[0],
                    "content": tpl.render(context)
                }
            raise ValueError(f"Unknown origin {origin[1]}")
        else:
            tpl = get_template(origin)
            return {
                "template": tpl,
                "content": tpl.render(context)
            }

    def get_partitial_context(self, context):
        """
            Modifys content for ajax Partitials
            Detailed: It loads all defined files from partitials_list and render this templates

            :param context: context dict
            :return: context dict
        """
        partitial_ctx = {}
        for selector, origin in self.get_partitial_list().items():
            partitial_ctx[selector] = self.get_partitial(origin, context)
        return partitial_ctx

    def get_context_data(self, *args, **kwargs):
        """
            Add Partitial Information to general context
            :return dict: Context
        """
        ctx = super(PartitialAjaxMixin, self).get_context_data(*args, **kwargs)
        ctx["partitial"] = self.get_partitial_context(ctx)
        return ctx

    def get_ajax_context_data(self, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        json_content = {}
        for divid, tpl in ctx["partitial"].items():
            json_content[divid] = tpl["template"].render(ctx)
        ctx["partitial"]["content"] = json_content
        return ctx

    def dispatch(self, *args, **kwargs):
        request = args[0]
        if not request.is_ajax():
            return super(PartitialAjaxMixin, self).dispatch(*args, **kwargs)
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, f"ajax_{request.method.lower()}", self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(*args, **kwargs)

    def ajax_get(self, *args, **kwargs):
        ctx = self.get_ajax_context_data(*args, **kwargs)
        return JsonResponse({
            "content": ctx["partitial"]["content"]
        })
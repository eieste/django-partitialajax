from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import Template
from django.views.generic import View
import requests
from django.db.utils import IntegrityError
from django.utils.translation import pgettext as __

class PartitialAjaxMixin:
    """
        Add this Mixin to your View to activate the useage of PartitialAjax
    """

    #: Define here all partitial html files used in the template_name File
    #: Write as follows: {"#foobar": "myapp/partitial/foo.html"}
    partitial_list = dict()

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
                    "content": tpl.render(context, request=self.request)
                }
            elif "remote" in origin[1]:
                with requests.get(origin[0]) as r:
                    tpl = Template(r.text)
                return {
                    "path": origin[0],
                    "content": tpl.render(context, request=self.request)
                }
            raise ValueError(f"Unknown origin {origin[1]}")
        else:
            tpl = get_template(origin)
            return {
                "template": tpl,
                "content": tpl.render(context, request=self.request)
            }

    def get_partitial_context(self, **kwargs):
        """
            Modifys content for ajax Partitials
            Detailed: It loads all defined files from partitials_list and render this templates

            :param context: context dict
            :return: context dict
        """
        kwargs.update({"partitial":{}})


        for selector, origin in self.get_partitial_list().items():
            kwargs["partitial"].update({ selector: self.get_partitial(origin, kwargs)})

        return kwargs

    def is_ajax(self):
        if "is-ajax" in self.request.GET:
            return True
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def dispatch(self, *args, **kwargs):
        request = args[0]

        if not self.is_ajax():
            return super().dispatch(*args, **kwargs)
        else:
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, f"ajax_{request.method.lower()}", self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(*args, **kwargs)

    def generate_content(self, context):
        content_list = {}
        for key, item in context["partitial"].items():
            if not key == "current":
                content_list[key] = item["content"]
        return content_list

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(self.get_direct_context_data(**ctx))
        ctx.update(self.get_partitial_context(**ctx))
        return ctx

    def get_direct_context_data(self, **kwargs):
        return kwargs

    def ajax_get(self, *args, **kwargs):
        ctx = self.get_context_data()
        return JsonResponse({
            "content": self.generate_content(ctx)
        })


class DeletePartitialAjaxMixin(PartitialAjaxMixin):

    def ajax_get(self, *args, **kwargs):
        self.object = self.get_object()
        ctx = self.get_context_data(object=self.object)
        return JsonResponse({
            "content": self.generate_content(ctx)
        })

    def ajax_post(self, *args, **kwargs):
        status = "ok"
        messages = []
        try:
            super().post(*args, **kwargs)
        except IntegrityError as e:
            status = "err"
            messages.append({
                "title": __("error title", "Integrity Error"),
                "content": __("error message: integriy error", "this entry cannot be deleted because it is still linked to other entries"),
                "type": "error",
                "code": "unknown_error"
            })
        except Exception as e:
            status = "err"
            messages.append({
                "title": __("error title", "Unknown Error"),
                "content": __("error message: unknown error", "A unknown error was raised. {}".format(e)),
                "type": "error",
                "code": "unknown_error"
            })
        else:
            messages.append({
                "title": __("message title", "Entry successfully removed"),
                "content": __("remove success message", "This entry was successfully removed"),
                "type": "success",
                "code": "delete_success"
            })

        return JsonResponse({
            "status": status,
            "text": messages
        })


class CreatePartitialAjaxMixin(PartitialAjaxMixin):

    def ajax_get(self, *args, **kwargs):
        self.object = None
        return super().ajax_get(*args, **kwargs)

    def ajax_post(self, *args, **kwargs):
        status = "ok"
        messages = []
        try:
            super().post(*args, **kwargs)
        except Exception as e:
            status = "err"
            messages.append({
                "title": __("error title", "Unknown Error"),
                "content": __("error message: unknown error", "A unknown error was raised. {}".format(e)),
                "type": "error",
                "code": "unknown_error"
            })
        else:
            messages.append({
                "title": __("message title", "Entry successfully created"),
                "content": __("remove success message", "This entry was successfully created"),
                "type": "success",
                "code": "create_success"
            })

        return JsonResponse({
            "status": status,
            "text": messages
        })


class ListPartitialAjaxMixin(PartitialAjaxMixin):

    def ajax_get(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().ajax_get(*args, **kwargs)


class UpdatePartitialAjaxMixin(PartitialAjaxMixin):
    pass


class DetailPartitialAjaxMixin(PartitialAjaxMixin):

    def ajax_get(self, *args, **kwargs):
        self.object = self.get_object()
        ctx = self.get_context_data(object=self.object)
        return JsonResponse({
            "content": self.generate_content(ctx)
        })
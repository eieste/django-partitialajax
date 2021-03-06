from django.test import TestCase
from partitialajax.exceptions import PartitialNotFound
from partitialajax.templatetags.partitialajax import direct_partitial
from django.template import Context, Template
import re

class DirectPartitialTemplateTagTestCase(TestCase):

    def test_no_partitial_context(self):
        context = Context({})
        template_to_render = Template(
            "{% load partitialajax %}"
            "{% direct_partitial 'specialElement#myid' %}"
        )

        with self.assertRaises(PartitialNotFound) as ctx:
            rendered_template = template_to_render.render(context)

    def test_no_selector_context(self):
        context = Context({"partitial": {"invalidselector":{}}})
        template_to_render = Template(
            "{% load partitialajax %}"
            "{% direct_partitial 'specialElement#myid' %}"
        )
        with self.assertRaises(PartitialNotFound) as ctx:
            rendered_template = template_to_render.render(context)


    def test_with_selector_context(self):
        context = Context({"partitial": {"specialElement#myid":{
            "content": "hallotest"
        }}})
        template_to_render = Template(
            "{% load partitialajax %}"
            "{% direct_partitial 'specialElement#myid' %}"
        )
        html = template_to_render.render(context)

        self.assertEqual(re.sub(r'\s*', '', '<specialElementid="myid"class="ajaxpartitial-container"data-partitial-only-child-replace="false"data-partitial-interval="-1"data-partitial-allowed-elements="all"data-partitial-text-event-callback="console.info"data-partitial-restrict-remote-configuration="false"data-partitial-config-from-element="false"data-partitial-direct-load="false"data-partitial-activate="true">hallotest</specialElement>'),
                         re.sub(r'\s*', '', html))
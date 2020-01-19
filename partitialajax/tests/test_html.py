from django.test import TestCase
from partitialajax.contrib import html
from partitialajax.exceptions import InvalidSelectorString
# Create your tests here.


class HTMLSelectorTestCase(TestCase):

    def test_id_split(self):
        info = html.split_selector("#testIDString")
        self.assertEqual(info["id"], "testIDString")
        self.assertEqual(info["element"], None)
        self.assertEqual(len(info["class_list"]), 0)
        self.assertEqual(len(info["attribute_list"]), 0)

    def test_double_id(self):
        with self.assertRaises(InvalidSelectorString) as context:
            html.split_selector("#testIDString#anotherID")

    def test_element_split(self):
        info = html.split_selector("div")
        self.assertEqual(info["id"], None)
        self.assertEqual(info["element"], "div")
        self.assertEqual(len(info["class_list"]), 0)
        self.assertEqual(len(info["attribute_list"]), 0)

    def test_class_split(self):
        info = html.split_selector(".testClassString")
        self.assertEqual(info["id"], None)
        self.assertEqual(info["element"], None)
        self.assertEqual(len(info["class_list"]), 1)
        self.assertEqual(list(info["class_list"])[0], "testClassString")
        self.assertEqual(len(info["attribute_list"]), 0)

    def test_class_list_split(self):
        info = html.split_selector(".testClassString.classA.classB")
        self.assertEqual(info["id"], None)
        self.assertEqual(info["element"], None)
        self.assertEqual(len(info["class_list"]), 3)
        self.assertEqual(info["class_list"], {"testClassString", "classA", "classB"})
        self.assertEqual(len(info["attribute_list"]), 0)


    def test_atttribute_split(self):
        info = html.split_selector("[attri=\"value\"]")
        self.assertEqual(info["id"], None)
        self.assertEqual(info["element"], None)
        self.assertEqual(len(info["class_list"]), 0)
        self.assertEqual(len(info["attribute_list"].items()), 1)
        self.assertEqual(info["attribute_list"], {"attri": "value"})

    def test_atttribute_list_split(self):
        info = html.split_selector('[attra="vala"][attrb="valb"][attrc="valc"][attrd="vald"]')
        self.assertEqual(info["id"], None)
        self.assertEqual(info["element"], None)
        self.assertEqual(len(info["class_list"]), 0)
        self.assertEqual(len(info["attribute_list"].items()), 4)
        self.assertEqual(info["attribute_list"], {"attra": "vala", "attrb": "valb", "attrc": "valc", "attrd": "vald"})

    def test_element_with_id(self):
        info = html.split_selector('superElement#elementID')
        self.assertEqual(info["element"], "superElement")
        self.assertEqual(info["id"], "elementID")
        self.assertEqual(len(info["class_list"]), 0)
        self.assertEqual(len(info["attribute_list"].items()), 0)

    def test_element_with_class(self):
        info = html.split_selector('superElement.elementClass')
        self.assertEqual(info["element"], "superElement")
        self.assertEqual(info["id"], None)
        self.assertEqual(len(info["class_list"]), 1)
        self.assertEqual(info["class_list"], {"elementClass"})
        self.assertEqual(len(info["attribute_list"].items()), 0)

    def test_element_with_class_and_id(self):
        info = html.split_selector('superElement.elementClass#elementID')
        self.assertEqual(info["element"], "superElement")
        self.assertEqual(info["id"], "elementID")
        self.assertEqual(len(info["class_list"]), 1)
        self.assertEqual(info["class_list"], {"elementClass"})
        self.assertEqual(len(info["attribute_list"].items()), 0)

        info = html.split_selector('superElement#elementID.elementClass')
        self.assertEqual(info["element"], "superElement")
        self.assertEqual(info["id"], "elementID")
        self.assertEqual(len(info["class_list"]), 1)
        self.assertEqual(info["class_list"], {"elementClass"})
        self.assertEqual(len(info["attribute_list"].items()), 0)

        info = html.split_selector('superElement#elementID.elementClass.anotherClass')
        self.assertEqual(info["element"], "superElement")
        self.assertEqual(info["id"], "elementID")
        self.assertEqual(len(info["class_list"]), 2)
        self.assertEqual(info["class_list"], {"elementClass", "anotherClass"})
        self.assertEqual(len(info["attribute_list"].items()), 0)

    def test_full_split(self):
        info = html.split_selector('superElement#singleElementID.elementClass[data-attribute="data-value"].anotherClass[data-anotherattr="foobar"]')
        self.assertEqual(info["element"], "superElement")
        self.assertEqual(info["id"], "singleElementID")
        self.assertEqual(len(info["class_list"]), 2)
        self.assertEqual(info["class_list"], {"elementClass", "anotherClass"})
        self.assertEqual(len(info["attribute_list"].items()), 2)
        self.assertEqual(info["attribute_list"], {"data-attribute": "data-value", "data-anotherattr":"foobar"})

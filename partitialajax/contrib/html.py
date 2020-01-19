import re
from partitialajax.exceptions import InvalidSelectorString
# pattern = re.compile(r'\#(?P<id>[a-z0-9]+)|\.(?P<class>[a-z0-9]+)|(?P<attr>\[(?P<attrname>[a-z0-9\-]*)\=\"(?P<attrval>\S+)\"\])', re.X|re.M)
#pattern = re.compile(r'^(?P<element>[a-zA-Z0-9]*)|\#(?P<id>[a-zA-Z0-9\-]+)|\.(?P<class>[a-zA-Z0-9\-]+)|(?P<attr>\[(?P<attrname>[a-zA-Z0-9\-]*)\=\"(?P<attrval>\S+)\"\])$', re.X|re.M)
# pattern = re.compile(r'^(?P<element>[a-zA-Z0-9]*)|^\#(?P<id>[a-zA-Z0-9\-]+)|^\.(?P<class>[a-zA-Z0-9\-]+)|^(?P<attr>\[(?P<attrname>[a-zA-Z0-9\-]*)\=\"(?P<attrval>\S+)\"\])$', re.X|re.M)
pattern = re.compile(r'(?:(?P<element>^[\w]*))?(?:\#(?P<id>[\w|\-]+))?(?:\.(?P<class>[\w|\-]+))?(?P<attr>(?:\[(?P<attrname>[\w|\-]+)\=\"(?P<attrval>[\w|\-]+)\"\]))?')


def split_selector(selector):
    """

        Splits a html selector in the following Parts: element (div, span, table ...), id, class_list (set of all classes) attribute_dict eg. data-foobar="test"
        and returns it

            :param selector: string with all selectors
            :return dict: returns seperated selector attributes. dict keys: element, id, class_list, attribute_list
    """

    element_attributes = {
        "element": None,
        "id": None,
        "class_list": set(),
        "attribute_list": dict(),
    }

    if bool(pattern.search(selector)):
        match_list = pattern.finditer(selector)
        for match in match_list:

            if match.group("id"):
                if element_attributes["id"] is not None:
                    raise InvalidSelectorString("A HTML-Element can only Contain a single ID")
                element_attributes["id"] = match.group("id")

            if match.group("class"):
                element_attributes["class_list"].add(match.group("class"))

            if match.group("attr"):
                element_attributes["attribute_list"][match.group("attrname")] = match.group("attrval")

            if match.group("element"):
                element_attributes["element"] = match.group("element")

    else:
        raise ValueError("only a-z0-9#. are allowed as selectors.")
    return element_attributes

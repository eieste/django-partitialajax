import re

# pattern = re.compile(r'\#(?P<id>[a-z0-9]+)|\.(?P<class>[a-z0-9]+)|(?P<attr>\[(?P<attrname>[a-z0-9\-]*)\=\"(?P<attrval>\S+)\"\])', re.X|re.M)
pattern = re.compile(r'^(?P<element>[a-z0-9]*)\#(?P<id>[a-z0-9\-]+)|\.(?P<class>[a-z0-9\-]+)|(?P<attr>\[(?P<attrname>[a-z0-9\-]*)\=\"(?P<attrval>\S+)\"\])$', re.X|re.M)

def split_selector(selector):
    """

        Splits a html selector in the following Parts: element (div, span, table ...), id, class_list (set of all classes) attribute_dict eg. data-foobar="test"
        and returns it

            :param selector: string with all selectors
            :return dict: returns seperated selector attributes. dict keys: element, id, class_list, attribute_list
    """

    element_attributes = {
        "element": "div",
        "id": None,
        "class_list": set(),
        "attribute_list": {},
    }

    if bool(pattern.search(selector)):
        match_list = pattern.finditer(selector)
        for match in match_list:

            if match.group("id"):
                element_attributes["id"] = match.group("id")

            if match.group("class"):
                element_attributes["class_list"].add(match.group("class"))

            if match.group("attr"):
                element_attributes["attribute_list"][match.group("attrname")] = match.group("attrval")

            if match.group("element"):
                print(match.group("element"))
                element_attributes["element"] = match.group("element")

    else:
        raise ValueError("only a-z0-9#. are allowed as selectors.")
    return element_attributes

#print(split_selector("#foo#bar#hallo#welt.test.abc.hallowelt.foobar#netdas#istdoch#toll.sdfasf.asdf#asdf#foo#bar[data-foo=\"abc\"].foo#asdf"))
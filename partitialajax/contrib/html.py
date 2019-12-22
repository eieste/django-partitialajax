import re

pattern = re.compile(r'\#(?P<id>[a-z0-9]+)|\.(?P<class>[a-z0-9]+)|(?P<attr>\[(?P<attrname>[a-z0-9\-]*)\=\"(?P<attrval>\S+)\"\])', re.X|re.M)

def split_selector(selector):
    element_attributes = {
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
    else:
        raise ValueError("only a-z0-9#. are allowed as selectors.")
    print(element_attributes)
    return element_attributes

#print(split_selector("#foo#bar#hallo#welt.test.abc.hallowelt.foobar#netdas#istdoch#toll.sdfasf.asdf#asdf#foo#bar[data-foo=\"abc\"].foo#asdf"))
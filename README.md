# Django Partitial Ajax

[![CircleCI](https://circleci.com/gh/eieste/django-partitialajax/tree/development.svg?style=svg)](https://circleci.com/gh/eieste/django-partitialajax/tree/development)
[![Coverage Status](https://coveralls.io/repos/github/eieste/django-partitialajax/badge.svg?branch=development)](https://coveralls.io/github/eieste/django-partitialajax?branch=development)
![PyPI - License](https://img.shields.io/pypi/l/django-partitialajax)
![NPM](https://img.shields.io/npm/l/django-partitialajax)
![Read the Docs](https://img.shields.io/readthedocs/django-partitialajax)
![npm](https://img.shields.io/npm/v/django-partitialajax)
![PyPI](https://img.shields.io/pypi/v/django-partitialajax)


This libary can you help to load Django-Rendered Partitials and embedd this into your page.

This libary consists of two parts: python/django and js lib;
you can install it via
```bash
pip3 install django-partitialajax
npm install django-partitialajax

```

For more Information read the [Documentation](https://django-partitialajax.readthedocs.io/en/latest/)

## Quick start

settings.py
```python
    INSTALLED_APPS = [
        ...
        partitialajax
    ]
```

views.py
```python
from partitialajax.mixin import ListPartitialAjaxMixin
from django.views.generic import ListView

class BookListItem(ListPartitialAjaxMixin, ListView):
    template_name = "book/list.html"
    model = Book
    partitial_list = {
        "tbody#book-list-partitial":"book/partitial/list.html"
    }
```

book/list.html
```html
{% load partitialajax %}

<table>
    <thead>
        <th>ID</th>    
        <th>Name</th>    
        <th>Author</th>    
    </thead>
    {% direct "tbody#book-list-partitial" %}
</table>
```

book/partitial/list.html
```html
{% for book in object_list %}
    <tr>
        <td>{{object.pk}}</td>
        <td>{{object.name}}</td>
        <td>{{object.author}}</td>
    </tr>
{% endfor %}
```

## And what's different about an include now?

an include is rendered directly by django, so that no update can take place in the client side.
With django-partitialajax you can reload this part.
How? Just use the following JS code

```js
import {PartitialAjax} from "django-partitialajax";

let partitial_element = document.getElementById("book-list-partitial");
let partitial = PartitialAjax.getPartitialFromElement(partitial_element);

partitial.getFromRemote();
```
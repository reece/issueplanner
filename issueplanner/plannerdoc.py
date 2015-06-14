# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

import lxml.etree as le


class PlannerDoc(object):
    """Facade to read, write, and manipulate GNOME Planner XML documents.
    This class is intended to be independent of the issueplanner tools.
    See issueplannerdoc.py for an issueplanner-specific subclass.

    >>> import lxml.etree as le

    >>> example_filename = os.path.join(
    ...     os.path.dirname(__file__), '..', 'tests', 'data', 'example.planner')

    >>> with open(example_filename,'r') as fh:
    ...     pd = PlannerDoc(le.fromstring(fh.read()))

    """

    def __init__(self, xml_root):
        self._xml_root = xml_root
        self._logger = logging.getLogger(__name__)

    def __str__(self):
        return(le.tostring(self._xml_root, encoding="UTF-8",
                           xml_declaration=True, pretty_print=True))

    def allocations(self):
        return self._xml_root.xpath("/project/allocations/allocation")

    def properties(self):
        return self._xml_root.xpath("/project/properties/property")

    def resources(self):
        return self._xml_root.xpath("/project/resources/resource")

    def tasks(self):
        return self._xml_root.xpath("/project/tasks//task")



    # add, update, remove task

    # add, update, remove resource
    def add_resource(self, name, shortname, email):
        pass

    # add, update, remove allocation
    def add_allocation(self):
        pass

    # add, update, remove property

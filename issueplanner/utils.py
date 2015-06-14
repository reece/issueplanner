# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function #, unicode_literals

"""Utilities for issueplanner"""

import re


def bb_to_planner_ts(ts):
    """convert bitbucket timestamps to planner timestamps

    >>> bb_to_planner_ts('2015-06-02T23:16:26.709')
    '20150602T231626Z'

    >>> bb_to_planner_ts('2015-06-02 21:16:26+00:00')
    '20150602T211626Z'

    """

    return ts.partition("+")[0].partition(".")[0].replace("-","").replace(":","").replace(" ","T") + "Z"


def parse_tracker_spec(ts_string):
    """parse a "tracker spec" string, typically from the description
    attribute of a "property" XML element. See plannerdoc.py for more.

    >>> ts = parse_tracker_spec('bitbucket:def/abc')

    returns:
    {u'owner': 'def', u'scm': 'bitbucket', u'slug': 'abc'}

    >>> ts['owner']
    'def'

    >>> ts['scm']
    'bitbucket'

    >>> ts['slug']
    'abc'

    >>> ts = parse_tracker_spec('bogus')
    >>> ts is None
    True

    """

    tracker_spec_re = re.compile(u"(?P<scm>\w+):(?P<owner>\w+)/(?P<slug>\w+)$")

    try:
        return tracker_spec_re.match(ts_string).groupdict()
    except AttributeError:
        return None


def milestone_path_names(milestone):
    """For a milestone x.y.z, return a list of XML node names along the path

    >>> milestone_path_names("1.2.3")
    ['1.2', '1.2.3']

    """
    ms_elements = milestone.split(".")
    names = [".".join(ms_elements[0:i+1]) for i in range(1,len(ms_elements))]
    return names

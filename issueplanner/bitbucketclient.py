# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os
import sys

from bitbucket.bitbucket import Bitbucket


class BitbucketClient(object):
    """Wrapper around bitbucket-api to simplify access patterns relevant
    for issueplanner"""

    def __init__(self, username, password):
        self._logger = logging.getLogger(__name__)
        self._bb = Bitbucket(username=username, password=password)

    def get_all_issues(self, owner, slug):
        """Returns an *interator* for all issues from Bitbucket. This needs to be done in batches
        per the Bitbucket REST API requirements.
    
        If you want a list of issues, call as list(bb.get_all_issues(...))
        """

        batch = 25
        start = 0
        count = batch
        while start < count:
            s,resp = self._bb.issue.all(owner=owner, repo_slug=slug, params={'start': start, 'limit': batch})
            if not s:
                raise Exception("failed to get issues for {account}/{slug}".format(account=account, slug=slug))
            for r in resp["issues"]:
                yield r
            count = resp["count"]
            start += batch
        # no return

# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import re

import lxml.etree as le

from .plannerdoc import PlannerDoc
from .utils import parse_tracker_spec, milestone_path_names


class IssuePlannerDoc(PlannerDoc):
    """Provides issueplanner-specific functionality. See `PlannerDoc` for
    general GNOME Planner XML manipulation.

    IssuePlannerDoc XML files are Planner XML files with the following
    structural conventions:

      * Each repo/project has a top-level task entry
      * Each repo/project *may* have child tasks named for X.Y milestones. 
      * Each X.Y milestone task *may* have child tasks for patches
      * Each repo/project has an "unplanned" child task for issues
        without milestones.
      * Task titles have issue tags in them, like "[PRJ-123]". These
        are used to fetch issue data.

    >>> import lxml.etree as le

    >>> example_filename = os.path.join(
    ...     os.path.dirname(__file__), '..', 'tests', 'data', 'example.planner')

    >>> with open(example_filename,'r') as fh:
    ...     pd = PlannerDoc(le.fromstring(fh.read()))

    """

    def get_trackers(self):
        """Return a list of issue prefixes and the associated repo issue tracker.

        The planner XML is expected to have properties like this:

        <properties>
          <property name="eutils" type="text" owner="project" label="eutils" description="bitbucket:biocommons/eutils"/>
          <property name="issueplanner" type="text" owner="project" label="issueplanner" description="bitbucket:reece/issueplanner"/>
        </properties>

        For which the following would be returned:
          [
            {u'owner': 'reece', u'prefix': 'issueplanner', u'scm': 'bitbucket', u'slug': 'issueplanner'},
            {u'owner': 'biocommons', u'prefix': 'eutils', u'scm': 'bitbucket', u'slug': 'eutils'}
          [

        These proporties may be added with the Project > Edit Project
        Properties > Custom dialog.

        These properties are specific to the use with issueplanner tools.

        """

        def _mk_ti(e):
            ti = parse_tracker_spec(e.get("description"))
            if ti:
                ti.update({"prefix": e.get("name")})
            return ti

        trackers = [ti
                    for ti in (_mk_ti(e)
                               for e in self._xml_root.xpath('/project/properties/property[@description]'))
                    if ti is not None]
        

        return trackers


    def get_project_task(self, tracker):
        """get project task node for given tracker, creating it if necessary.
        
        Projects tasks are named as <owner>/<slug> and must be unique
        with the planner XML.

        """
    
        fqrn = "{tracker[owner]}/{tracker[slug]}".format(tracker=tracker)
        tasks_te =  self._xml_root.xpath("/project/tasks")[0]
        return self.get_task_path(tasks_te, [fqrn])


    def get_milestone_task(self, prj_te, milestone):
        """get/create task element for given milestone.  If `milestone` is
        None, a task element is returned for the "Unplanned" task.  If
        `milestone` has the form X.Y.Z, it is created in a hierarchy
        of X.Y > X.Y.Z.  Otherwise, it is created as-is.
        """
        self._logger.debug("{}, {}".format(prj_te, milestone))

        if milestone is None:
            names = ["Unplanned"]
        
        elif "." in milestone:
            names = milestone_path_names(milestone)

        else:
            names = [milestone]
        
        return self.get_task_path(prj_te, names)


    def get_task_path(self, parent_te, names):
        """for a *list* of names (strings) that refer to nested task elements,
        get the task element that refers to the terminal child node,
        potentially creating any along the way as needed
        """

        for name in names:
            elms = parent_te.xpath("task[@name='{name}']".format(name=name))
            if len(elms) >= 2:
                raise Exception("Found multiple tasks named {fqrn}".format(fqrn))
            if len(elms) == 0:
                child_te = self.create_task(name)
                parent_te.append(child_te)
            elif len(elms) == 1:
                child_te = elms[0]
            parent_te = child_te
        return child_te


    def create_task(self, name, attrs={}):
        def _get_next_task_id():
            max_task_id = max(int(e.get("id")) for e in self._xml_root.xpath("///task"))
            return max_task_id + 1

        _attrs = {
            "id": str(_get_next_task_id()),
            "name": name,
            "note": "",
            "work": "28800",    # 8h
            "start": "",
            "end": "",
            "work-start": "",
            "percent-complete": "0",
            "priority": "0",
            "type": "normal",
            "scheduling": "fixed-work",
            }
        _attrs.update(attrs)
        te = self._xml_root.makeelement("task", _attrs)
        return te

    
    def set_task_constraint(self, te, ctype, ts):
        ce = te.find("constraint")
        if ce is None:
            ce = self._xml_root.makeelement("constraint")
            te.append(ce)
        ce.set("type", "start-no-earlier-than")
        ce.set("time", ts)

    def reset_project_start(self):
        """
        The project start date 
        """
        earliest_ts = sorted(ts for ts in self._xml_root.xpath("///task/@start") if ts != "")[0]
        assert self._xml_root.tag == "project"
        self._xml_root.set("project-start", earliest_ts)
        return earliest_ts

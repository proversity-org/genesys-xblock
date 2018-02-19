"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import logging
import requests
from django.conf import settings
from xblock.core import XBlock
from django.contrib.auth.models import User
from xblock.fields import Scope, Integer, String, Float, List, Boolean, ScopeIds
from xblockutils.resources import ResourceLoader
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin
from xblockutils.settings import XBlockWithSettingsMixin
logger = logging.getLogger(__name__)
loader = ResourceLoader(__name__)


@XBlock.needs('settings')
@XBlock.wants('badging')
@XBlock.wants('user')
class GenesysXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.


    @property
    def api_token(self):
        """
        Returns the Geneysis API token from Settings Service.
        The API key should be set in both lms/cms env.json files inside XBLOCK_SETTINGS.
        Example:
            "XBLOCK_SETTINGS": {
                "GenesysXBlock": {
                    "GENESYS_API_TOKEN": "YOUR API KEY GOES HERE"
                }
            },
        """
        return self.get_xblock_settings().get('GENESYS_API_TOKEN', '')

    @property
    def api_url(self):
        """
        Returns the URL of the Geneysis domain from the Settings Service.
        The URL hould be set in both lms/cms env.json files inside XBLOCK_SETTINGS.
        Example:
            "XBLOCK_SETTINGS": {
                "GenesysXBlock": {
                    "GENESYS_BASE_URL": "YOUR URL  GOES HERE"
                }
            },
        """
        return self.get_xblock_settings().get('GENESYS_BASE_URL' '')


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the GenesysXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/genesys.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/genesys.css"))
        frag.add_javascript(self.resource_string("static/js/src/genesys.js"))
        frag.initialize_js('GenesysXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("GenesysXBlock",
             """<genesys/>
             """),
            ("Multiple GenesysXBlock",
             """<vertical_demo>
                <genesys/>
                <genesys/>
                <genesys/>
                </vertical_demo>
             """),
        ]
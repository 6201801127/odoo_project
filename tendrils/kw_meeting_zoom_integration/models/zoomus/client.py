"""Zoom.us REST API Python Client"""

# from __future__ import absolute_import, unicode_literals

from . import util, user, meeting, past_meeting, report, webinar, recording
from .util import API_VERSION_2

API_BASE_URIS = {
    API_VERSION_2: "https://api.zoom.us/v2",
}

COMPONENT_CLASSES = {

    API_VERSION_2: {
        "user": user.UserComponentV2,
        "meeting": meeting.MeetingComponentV2,
        "past_meeting": past_meeting.PastMeetingComponentV2,
        "report": report.ReportComponentV2,
        "webinar": webinar.WebinarComponentV2,
        "recording": recording.RecordingComponentV2,
    },
}


class ZoomClient(util.ApiClient):
    """Zoom.us REST API Python Client"""

    """Base URL for Zoom API"""

    def __init__(self, api_key, api_secret, data_type="json", timeout=15, version=API_VERSION_2):
        """Create a new Zoom client

        :param api_key: The Zooom.us API key
        :param api_secret: The Zoom.us API secret
        :param data_type: The expected return data type. Either 'json' or 'xml'
        :param timeout: The time out to use for API requests
        """
        try:
            BASE_URI = API_BASE_URIS[version]
            self.components = COMPONENT_CLASSES[version].copy()
        except KeyError:
            raise RuntimeError("API version not supported: %s" % version)

        super(ZoomClient, self).__init__(base_uri=BASE_URI, timeout=timeout)

        # Setup the config details
        self.config = {
            "api_key": api_key,
            "api_secret": api_secret,
            "data_type": data_type,
            "version": version,
            "token": util.generate_jwt(api_key, api_secret),
        }
        # Instantiate the components
        for key in self.components.keys():
            self.components[key] = self.components[key](base_uri=BASE_URI, config=self.config)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def refresh_token(self):
        self.config["token"] = (util.generate_jwt(self.config["api_key"], self.config["api_secret"]),)

    @property
    def api_key(self):
        """The Zoom.us api_key"""
        return self.config.get("api_key")

    @api_key.setter
    def api_key(self, value):
        """Set the api_key"""
        self.config["api_key"] = value
        self.refresh_token()

    @property
    def api_secret(self):
        """The Zoom.us api_secret"""
        return self.config.get("api_secret")

    @api_secret.setter
    def api_secret(self, value):
        """Set the api_secret"""
        self.config["api_secret"] = value
        self.refresh_token()

    @property
    def meeting(self):
        """Get the meeting component"""
        return self.components.get("meeting")

    @property
    def report(self):
        """Get the report component"""
        return self.components.get("report")

    @property
    def user(self):
        """Get the user component"""
        return self.components.get("user")

    @property
    def webinar(self):
        """Get the webinar component"""
        return self.components.get("webinar")

    @property
    def recording(self):
        """Get the recording component"""
        return self.components.get("recording")


    @property
    def past_meeting(self):
        """Get the recording component"""
        return self.components.get("past_meeting")

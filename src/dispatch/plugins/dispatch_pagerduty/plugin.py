"""
.. module: dispatch.plugins.dispatch_pagerduty.plugin
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
"""
import logging
from pdpyras import APISession
from dispatch.decorators import apply, counter, timer
from dispatch.plugins import dispatch_pagerduty as pagerduty_oncall_plugin
from dispatch.plugins.bases import OncallPlugin

from .service import get_oncall, page_oncall
from .config import PagerdutyConfiguration


log = logging.getLogger(__name__)


@apply(timer)
@apply(counter)
class PagerDutyOncallPlugin(OncallPlugin):
    title = "PagerDuty Plugin - Oncall Management"
    slug = "pagerduty-oncall"
    author = "Netflix"
    author_url = "https://github.com/Netflix/dispatch.git"
    description = "Uses PagerDuty to resolve and page oncall teams."
    version = pagerduty_oncall_plugin.__version__

    def __init__(self):
        self.configuration_schema = PagerdutyConfiguration

    def get(self, service_id: str = None, **kwargs):
        """Gets the oncall person."""
        client = APISession(self.configuration.api_key.get_secret_value())
        return get_oncall(client=client, service_id=service_id)

    def page(
        self,
        service_id: str,
        incident_name: str,
        incident_title: str,
        incident_description: str,
        **kwargs,
    ):
        """Pages the oncall person."""
        client = APISession(self.configuration.api_key.get_secret_value())
        return page_oncall(
            client=client,
            from_email=self.configuration.from_email,
            service_id=service_id,
            incident_name=incident_name,
            incident_title=incident_title,
            incident_description=incident_description,
        )

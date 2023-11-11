"""Mailchimp tap class."""

from __future__ import annotations

import typing as t

import requests
import requests_cache
from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from toolz.dicttoolz import get_in

from tap_mailchimp.streams import (
    CampaignsStream,
    ConversationsStream,
    ListsStream,
    MembersStream,
    MergeFieldsStream,
    TemplatesStream,
)

if t.TYPE_CHECKING:
    from tap_mailchimp.client import MailchimpStream

OPENAPI_URL = "https://api.mailchimp.com/schema/3.0/Swagger.json?expand"
STREAM_TYPES: list[type[MailchimpStream]] = [
    CampaignsStream,
    ConversationsStream,
    ListsStream,
    MembersStream,
    MergeFieldsStream,
    TemplatesStream,
]

requests_cache.install_cache("requests_cache")


class TapMailchimp(Tap):
    """Mailchimp tap class."""

    name = "tap-mailchimp"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "server",
            th.StringType,
            required=True,
            description=(
                "To find the value for the server parameter used in "
                "`mailchimp.setConfig`, log into your Mailchimp account and "
                "look at the URL in your browser. You`ll see something like "
                "`https://us19.admin.mailchimp.com/`; the `us19` part is the server "
                "prefix. Note that your specific value may be different."
            ),
        ),
        th.Property(
            "api_key",
            th.StringType,
            description="API key to grant access to your Mailchimp account",
        ),
    ).to_dict()

    def get_openapi_schema(self) -> dict:
        """Retrieve Swagger/OpenAPI schema for this API.

        Returns:
            OpenAPI schema.
        """
        return requests.get(OPENAPI_URL, timeout=10).json()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams."""
        openapi_schema = self.get_openapi_schema()

        streams: list[MailchimpStream] = []
        for stream_type in STREAM_TYPES:
            schema = get_in(
                keys=[
                    "paths",
                    stream_type.path,
                    "get",
                    "responses",
                    "200",
                    "schema",
                    "properties",
                    stream_type.name,
                    "items",
                ],
                coll=openapi_schema,
            )
            streams.append(stream_type(tap=self, schema=schema))

        return sorted(streams, key=lambda x: x.name)

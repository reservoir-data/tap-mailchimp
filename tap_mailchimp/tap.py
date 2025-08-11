"""Mailchimp tap class."""

from __future__ import annotations

import sys

import requests_cache
from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_mailchimp import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

requests_cache.install_cache("requests_cache")


class TapMailchimp(Tap):
    """Mailchimp tap class."""

    name = "tap-mailchimp"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "server",
            th.StringType(nullable=False),
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
            th.StringType(nullable=False),
            required=True,
            secret=True,
            description="API key to grant access to your Mailchimp account",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams."""
        return [
            streams.CampaignsStream(tap=self),
            streams.ConversationsStream(tap=self),
            streams.ListsStream(tap=self),
            streams.MembersStream(tap=self),
            streams.MergeFieldsStream(tap=self),
            streams.TemplatesStream(tap=self),
        ]

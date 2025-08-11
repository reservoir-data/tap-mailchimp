"""Singer streams for Mailchimp."""

from __future__ import annotations

import sys
import typing as t

from tap_mailchimp.client import MailchimpStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class ListsStream(MailchimpStream):
    """Lists stream."""

    name = "lists"
    path = "/lists"

    @override
    def get_child_context(
        self,
        record: dict,
        context: Context | None,
    ) -> dict:
        """Get the child context for child streams."""
        return {"list_id": record["id"]}


class MembersStream(MailchimpStream):
    """Members stream."""

    name = "members"
    path = "/lists/{list_id}/members"
    parent_stream_type = ListsStream


class MergeFieldsStream(MailchimpStream):
    """Merge fields stream."""

    name = "merge_fields"
    path = "/lists/{list_id}/merge-fields"
    primary_keys: t.ClassVar[tuple[str, ...]] = ("merge_id",)
    parent_stream_type = ListsStream


class CampaignsStream(MailchimpStream):
    """Campaigns stream."""

    name = "campaigns"
    path = "/campaigns"


class ConversationsStream(MailchimpStream):
    """Conversations stream."""

    name = "conversations"
    path = "/conversations"


class TemplatesStream(MailchimpStream):
    """Templates stream."""

    name = "templates"
    path = "/templates"

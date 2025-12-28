"""Singer streams for Mailchimp."""

from __future__ import annotations

import typing as t
from typing import override

from tap_mailchimp.client import MailchimpStream

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context, Record


class ListsStream(MailchimpStream):
    """Lists stream."""

    name = "lists"
    path = "/lists"

    @override
    def get_child_context(
        self,
        record: Record,
        context: Context | None,
    ) -> Context:
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

"""Singer streams for Mailchimp."""

from __future__ import annotations

from tap_mailchimp.client import MailchimpStream


class ListsStream(MailchimpStream):
    """Lists stream."""

    name = "lists"
    path = "/lists"

    def get_child_context(
        self,
        record: dict,
        context: dict | None,  # noqa: ARG002
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
    primary_keys = ["merge_id"]
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

"""Mailchimp tap HTTP client."""

from __future__ import annotations

import typing as t

from requests.auth import HTTPBasicAuth
from singer_sdk.streams import RESTStream

if t.TYPE_CHECKING:
    import requests


class MailchimpStream(RESTStream):
    """Base stream class for all Mailchimp resources."""

    primary_keys: t.ClassVar[list[str]] = ["id"]

    @property
    def url_base(self) -> str:
        """Compute base URL."""
        return f"https://{self.config['server']}.api.mailchimp.com/3.0"

    @property
    def records_jsonpath(self) -> str:
        """Compute JSONPath from entity name."""
        return f"$.{self.name}[*]"

    @property
    def authenticator(self) -> HTTPBasicAuth:
        """Return a new authenticator object."""
        return HTTPBasicAuth(username="anystring", password=self.config["api_key"])

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: int,
    ) -> dict[str, t.Any]:
        """Get URL query parameters for Mailchimp streams."""
        self.logger.info("Page offset %s", next_page_token)

        fields = self.selected_fields
        self.logger.info("Fields %s", fields)
        return {
            "count": self._page_size,
            "offset": next_page_token,
            "fields": fields,
        }

    @property
    def selected_fields(self) -> list[str]:
        """Get selected fields from the input catalog.

        Returns:
            List of selected fields, with nested properties delimited by a dot.
        """
        if self._tap_input_catalog:
            return [
                ".".join(breadcrumb[1::2])
                for breadcrumb, selected in self.mask.items()
                if selected
            ]

        return []

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: int | None,
    ) -> int | None:
        """Return a token for identifying next page or None if no more pages."""
        current_offset = previous_token or 0
        count = len(response.json()[self.name])
        self.logger.info("Record count %s", count)

        if count == self._page_size:
            return current_offset + self._page_size

        return None

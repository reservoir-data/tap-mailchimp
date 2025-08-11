"""Mailchimp tap HTTP client."""

from __future__ import annotations

import sys
import typing as t
from copy import deepcopy

from requests.auth import HTTPBasicAuth
from singer_sdk import OpenAPISchema, RESTStream, StreamSchema
from singer_sdk.pagination import BaseOffsetPaginator
from toolz.dicttoolz import get_in

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


OPENAPI_URL = "https://api.mailchimp.com/schema/3.0/Swagger.json?expand"


class ResponseKey(t.NamedTuple):
    """Response key."""

    path: str
    """Endpoint for the resource."""

    name: str
    """Stream/resource name."""

    http_method: str
    """HTTP method for the resource."""

    expected_status: int = 200
    """Expected status code for the resource."""


class MailchimpOpenAPISchema(OpenAPISchema[ResponseKey]):
    """Mailchimp OpenAPI schema."""

    @override
    def get_unresolved_schema(self, key: ResponseKey) -> dict[str, t.Any]:
        return get_in(  # type: ignore[no-any-return]
            keys=(
                "paths",
                key.path,
                key.http_method.lower(),
                "responses",
                str(key.expected_status),
                "schema",
                "properties",
                key.name,
                "items",
            ),
            coll=self.spec,
        )


def _make_nullable(
    schema: t.Any,  # noqa: ANN401
    *,
    key_properties: tuple[str, ...] = (),
) -> dict[str, t.Any]:
    """Make non-key properties in the schema nullable."""
    new_schema = deepcopy(schema)
    for key, value in new_schema.get("properties", {}).items():
        if key in key_properties or "type" not in value:
            continue
        new_schema["properties"][key]["type"] = [value["type"], "null"]
    return new_schema


class MailchimpStreamSchema(StreamSchema[ResponseKey]):
    """Mailchimp stream schema."""

    @override
    def get_stream_schema(
        self,
        stream: MailchimpStream,  # type: ignore[override]
        stream_class: type[MailchimpStream],  # type: ignore[override]
    ) -> dict[str, t.Any]:
        key = ResponseKey(
            path=stream.path,
            name=stream.name,
            http_method=stream.http_method,
        )
        return _make_nullable(
            self.schema_source.fetch_schema(key),
            key_properties=stream.primary_keys,  # type: ignore[arg-type]
        )


class MailchimpStream(RESTStream):
    """Base stream class for all Mailchimp resources."""

    primary_keys: t.ClassVar[tuple[str, ...]] = ("id",)
    schema = MailchimpStreamSchema(MailchimpOpenAPISchema(OPENAPI_URL))  # type: ignore[assignment]

    @property
    @override
    def url_base(self) -> str:
        """Compute base URL."""
        return f"https://{self.config['server']}.api.mailchimp.com/3.0"

    @property
    @override
    def records_jsonpath(self) -> str:
        """Compute JSONPath from entity name."""
        return f"$.{self.name}[*]"

    @property
    @override
    def authenticator(self) -> HTTPBasicAuth:
        """Return a new authenticator object."""
        return HTTPBasicAuth(username="anystring", password=self.config["api_key"])

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
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

    def get_new_paginator(self) -> BaseOffsetPaginator:
        """Return a new paginator."""
        return BaseOffsetPaginator(start_value=0, page_size=self._page_size)

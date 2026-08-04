"""Tests standard tap features using the built-in SDK tests library.

Copyright (c) 2026 Edgar-Ramírez Mondragón
"""

from __future__ import annotations

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_mailchimp.tap import TapMailchimp

TestTapMailchimp = get_tap_test_class(
    TapMailchimp,
    suite_config=SuiteConfig(
        ignore_no_records_for_streams=[
            "conversations",
            "lists",
            "merge_fields",
        ],
    ),
)

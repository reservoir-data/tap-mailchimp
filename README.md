<div align="center">

# tap-mailchimp

<div>
  <a href="https://github.com/reservoir-data/tap-mailchimp/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/reservoir-data/tap-mailchimp"/>
  </a>
  <a href="https://scientific-python.org/specs/spec-0000/">
    <img alt="SPEC 0 — Minimum Supported Dependencies" src="https://img.shields.io/badge/SPEC-0-green"/>
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;">
  </a>
  <a href="https://github.com/astral-sh/uv">
   <img alt="uv" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json"/>
  </a>
</div>

Mailchimp tap class.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.

</div>

## Capabilities

* `sync`
* `catalog`
* `state` (TODO)
* `discover`

## Settings

| Setting| Required | Default | Description |
|:-------|:--------:|:-------:|:------------|
| server | False    | None    | To find the value for the server parameter used in `mailchimp.setConfig`, log into your Mailchimp account and look at the URL in your browser. You’ll see something like `https://us19.admin.mailchimp.com/`; the `us19` part is the server prefix. Note that your specific value may be different. |
| api_key| False    | None    | API key to grant access to your Mailchimp account |

A full list of supported settings and capabilities is available by running: `tap-mailchimp --about`

### Source Authentication and Authorization

Visit https://mailchimp.com/developer/marketing/guides/quick-start/#generate-your-api-key to learn how to generate a new API key.

## Usage

You can easily run `tap-mailchimp` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-mailchimp --version
tap-mailchimp --help
tap-mailchimp --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

[Install uv](https://docs.astral.sh/uv/getting-started/installation/) and then install this project's dependencies:

```bash
uv sync
```

### Create and Run Tests

Create tests within the `tap_mailchimp/tests` subfolder and then run:

```bash
uv run pytest
```

You can also test the `tap-mailchimp` CLI interface directly using `uv run`:

```bash
uv run tap-mailchimp --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Use Meltano to run an EL pipeline:

```bash
# Test invocation:
uvx meltano invoke tap-mailchimp --version

# OR run a test `elt` pipeline:
uvx meltano run tap-mailchimp target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.

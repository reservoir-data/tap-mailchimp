# `tap-mailchimp`

Mailchimp tap class.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.

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

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_mailchimp/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-mailchimp` CLI interface directly using `poetry run`:

```bash
poetry run tap-mailchimp --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-mailchimp
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-mailchimp --version
# OR run a test `elt` pipeline:
meltano elt tap-mailchimp target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.

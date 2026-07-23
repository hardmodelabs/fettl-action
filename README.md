# Fettl Action

Run [Fettl](https://fettl.dev) in GitHub Actions without checking out or
building the Fettl source repository.

```yaml
name: Fettl

on:
  pull_request:

permissions:
  contents: read
  pull-requests: read
  security-events: write

jobs:
  fettl:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: hardmodelabs/fettl-action@v0
        with:
          scan-mode: auto
          baseline-mode: new-only
          fail-on: high
```

`@v0` is the recommended compatibility-major alias. For reproducible
workflows, pin the immutable full-version ref:

```yaml
- uses: hardmodelabs/fettl-action@v0.19.21
```

The Action ref selects the wrapper bundle. The optional `version` input
selects the Fettl binary installed by that bundle:

```yaml
- uses: hardmodelabs/fettl-action@v0.19.21
  with:
    version: 0.19.21
```

`version: latest` resolves through the release manifest at
`downloads.fettl.dev` to an immutable version before cache lookup. The Action
verifies the manifest schema, archive size, SHA-256 digest, archive contents,
installed binary version, and cached binary digest. A missing or invalid
release fails closed; the Action never builds code from the repository being
scanned.

## Supported runners

- Linux x86_64
- Linux ARM64
- macOS Intel
- macOS Apple Silicon

Other operating systems and architectures fail before download.

## Version policy

- `v0.19.21` and other full-version tags are immutable.
- `v0` moves only after the matching immutable Action ref and all supported
  binary artifacts have passed external-consumer verification.
- If a regression is found, `v0` is moved back to the last verified immutable
  full-version tag. Full-version tags are never rewritten.

This public repository is the source-free GitHub Action distribution boundary.
It intentionally contains only Action metadata, the reviewed generated bundle,
its source map, and dependency licenses. Fettl's product source is not
published here.

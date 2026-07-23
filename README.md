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

      - uses: hardmodelabs/fettl-action@v0.19.21-action.1
        with:
          version: 0.19.21
          scan-mode: auto
          baseline-mode: new-only
          fail-on: high
```

`v0.19.21-action.1` is the corrected immutable wrapper candidate for Fettl
`v0.19.21`:

```yaml
- uses: hardmodelabs/fettl-action@v0.19.21-action.1
```

The Action ref selects the wrapper bundle. The optional `version` input
selects the Fettl binary installed by that bundle:

```yaml
- uses: hardmodelabs/fettl-action@v0.19.21-action.1
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

- `v0.19.21` is withdrawn because its bundled Node runtime failed during
  module initialization. The immutable tag is preserved for auditability and
  must not be used.
- `v0.19.21-action.1` replaces that wrapper while installing the unchanged
  Fettl `v0.19.21` binary.
- Full-version and corrective candidate tags are immutable.
- `v0` moves only after the matching immutable Action ref and all supported
  binary artifacts have passed external-consumer verification.
- If a regression is found, `v0` is moved back to the last verified immutable
  full-version tag. Full-version tags are never rewritten.

The `v0` compatibility alias has not been published yet. The Action's
machine-readable assessment requires an active Fettl Solo entitlement.
Automated runner provisioning for that entitlement is still being completed,
so this corrective tag is a release candidate rather than the default
integration.

This public repository is the source-free GitHub Action distribution boundary.
It intentionally contains only Action metadata, the reviewed generated bundle,
its source map, and dependency licenses. Fettl's product source is not
published here.

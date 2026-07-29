# Fettl Action

Run
[Fettl](https://fettl-dev.major-leaf-1682.chatgpt.site)
in GitHub Actions without checking out or building the Fettl source
repository.

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

      - uses: hardmodelabs/fettl-action@v0.19.29
        with:
          version: 0.19.29
          scan-mode: auto
          baseline-mode: new-only
          fail-on: high
          annotation-cap: 3
          summary-finding-cap: 10
```

`v0.19.29` is the immutable wrapper candidate for Fettl `v0.19.29`:

```yaml
- uses: hardmodelabs/fettl-action@v0.19.29
```

The Action ref selects the wrapper bundle. The optional `version` input
selects the Fettl binary installed by that bundle:

```yaml
- uses: hardmodelabs/fettl-action@v0.19.29
  with:
    version: 0.19.29
```

For pull-request runs, Fettl computes one canonical, ordered publication plan
that the Action projects directly into GitHub surfaces. `annotation-cap`
defaults to 3 and accepts 0 to suppress inline annotations.
`summary-finding-cap` defaults to 10. These display caps never change the
authoritative pass, warn, or fail result, and complete JSON and SARIF artifacts
remain available independently of the human-readable limits.

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
- `v0.19.21-action.1` corrects the Node runtime but is withdrawn because its
  public distribution included a generated source map.
- `v0.19.21-action.2` removes that source-bearing artifact while installing
  the unchanged Fettl `v0.19.21` binary.
- `v0.19.23` installs the verified Fettl `v0.19.23` binary but retains stale
  `v0.19.21-action.2` usage instructions in its immutable repository tree.
- `v0.19.23-action.1` corrects those instructions without changing the
  reviewed Action bundle or installed Fettl `v0.19.23` binary.
- Full-version and corrective candidate tags are immutable.
- `v0` moves only after the matching immutable Action ref and all supported
  binary artifacts have passed external-consumer verification.
- If a regression is found, `v0` is moved back to the last verified immutable
  full-version tag. Full-version tags are never rewritten.

The `v0` compatibility alias has not been published yet. The Action's
machine-readable assessment requires an active Fettl Pro entitlement.
Automated runner provisioning for that entitlement is still being completed,
so this corrective tag is a release candidate rather than the default
integration.

This public repository is the source-free GitHub Action distribution boundary.
It intentionally contains only Action metadata, the reviewed generated bundle,
runtime support, and dependency licenses. Fettl's product and Action
TypeScript sources are not published here.

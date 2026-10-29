# Fettl Action

Run
[Fettl](https://fettl.dev)
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

      - uses: hardmodelabs/fettl-action@v0.19.83
        with:
          version: 0.19.83
          mode: independent
          scan-mode: auto
          baseline-mode: new-only
          fail-on: high
          annotation-cap: 3
          summary-finding-cap: 10
```

`v0.19.83` uses the Apache-2.0 OSS Fettl packages. Set `version` to pin
the binary as shown below; the default is the current public release:

```yaml
- uses: hardmodelabs/fettl-action@v0.19.83
```

The Action ref selects the wrapper bundle. The optional `version` input
selects the Fettl binary installed by that bundle:

```yaml
- uses: hardmodelabs/fettl-action@v0.19.83
  with:
    version: 0.19.83
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

`mode` selects the assessment path. The default, `managed`, keeps the
authorized provider admission for authoritative PR publication: a managed
assertion that is missing, stale, or denied stops the run explicitly and never
falls back to `independent`. `mode: independent` runs a real independent
assessment without a managed account — the actual installer, CLI, check,
score, and delta path under trusted workflow settings and the exact selected
base/head — using no paid grant and requesting no provider settings. Its
outputs are the workflow result, job summary, artifacts, and
permission-eligible SARIF; there is no managed publisher and no PR-comment
service, and an invalid `mode` fails clearly instead of guessing:

```yaml
- uses: hardmodelabs/fettl-action@v0.19.83
  with:
    mode: independent
```

## Supported runners

- Linux x86_64
- macOS Apple Silicon

The selected package must exist in the release manifest. Missing platforms
fail explicitly; the Action does not build a replacement binary.

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

`mode: independent` requires no managed entitlement. Managed assessment keeps
its provider admission and does not fall back to independent assessment.

This public repository is the source-free GitHub Action distribution boundary.
It intentionally contains only Action metadata, the reviewed generated bundle,
runtime support, and dependency licenses. Fettl's product and Action
TypeScript sources are not published here.

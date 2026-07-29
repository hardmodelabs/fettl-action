#!/usr/bin/env python3
"""Bind an immutable private source archive to its exact Git commit."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import posixpath
import re
import tarfile
import tempfile
from pathlib import Path


FULL_COMMIT = re.compile(r"^[0-9a-f]{40}$")
INPUT_PREFIX = "fettl-release-input/"
SOURCE_PREFIX = "fettl-source/"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-archive", required=True, type=Path)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def _validate_source_archive(path: Path) -> bytes:
    source_bytes = path.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(source_bytes), mode="r:gz") as archive:
        members = archive.getmembers()
    if not members:
        raise SystemExit("source archive is empty")
    member_names: set[str] = set()
    for member in members:
        name = member.name
        if name in member_names:
            raise SystemExit(f"source archive member is duplicated: {name}")
        member_names.add(name)
        if name == SOURCE_PREFIX.rstrip("/") and member.isdir():
            continue
        if not name.startswith(SOURCE_PREFIX):
            raise SystemExit(
                f"source archive member is outside {SOURCE_PREFIX}: {name}"
            )
        relative = name.removeprefix(SOURCE_PREFIX)
        if (
            not relative
            or relative.startswith("/")
            or "\\" in relative
            or ".." in Path(relative).parts
        ):
            raise SystemExit(f"source archive member is unsafe: {name}")
        if member.isfile() or member.isdir():
            continue
        if member.issym():
            target = member.linkname
            if not target or target.startswith("/") or "\\" in target:
                raise SystemExit(f"source archive symlink is unsafe: {name}")
            resolved_target = posixpath.normpath(
                posixpath.join(posixpath.dirname(relative), target)
            )
            if (
                resolved_target == ".."
                or resolved_target.startswith("../")
                or resolved_target.startswith("/")
            ):
                raise SystemExit(f"source archive symlink escapes its root: {name}")
            continue
        raise SystemExit(f"source archive member type is unsafe: {name}")
    return source_bytes


def _tar_info(name: str, size: int) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.size = size
    info.mode = 0o644
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    return info


def _write_input(output: Path, source_bytes: bytes, binding_bytes: bytes) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=output.parent,
        prefix=f".{output.name}.",
        delete=False,
    ) as temporary:
        temporary_path = Path(temporary.name)
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=temporary, mtime=0
        ) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                archive.addfile(
                    _tar_info(f"{INPUT_PREFIX}fettl-source.tar.gz", len(source_bytes)),
                    io.BytesIO(source_bytes),
                )
                archive.addfile(
                    _tar_info(f"{INPUT_PREFIX}source-binding.json", len(binding_bytes)),
                    io.BytesIO(binding_bytes),
                )
    temporary_path.replace(output)


def main() -> int:
    arguments = _parse_args()
    commit = arguments.commit
    if FULL_COMMIT.fullmatch(commit) is None:
        raise SystemExit("--commit must be a full lowercase 40-hex commit SHA")
    source_bytes = _validate_source_archive(arguments.source_archive)
    source_digest = hashlib.sha256(source_bytes).hexdigest()
    binding = {
        "schema_version": 1,
        "source_archive_sha256": source_digest,
        "source_commit": commit,
    }
    binding_bytes = (json.dumps(binding, indent=2, sort_keys=True) + "\n").encode()
    _write_input(arguments.output, source_bytes, binding_bytes)
    input_digest = hashlib.sha256(arguments.output.read_bytes()).hexdigest()
    print(f"source commit: {commit}")
    print(f"source archive sha-256: {source_digest}")
    print(f"release input sha-256: {input_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

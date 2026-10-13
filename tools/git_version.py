#!/usr/bin/env python3
"""Print a version derived from this checkout's release tags."""
from pathlib import Path
import re
import subprocess
import sys

TAG = re.compile(r"v\d+\.\d+\.\d+(?:a\d+|b\d+|rc\d+|-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?")


def git(source, *args):
    return subprocess.check_output(["git", "-C", str(source), *args],
                                   text=True, stderr=subprocess.PIPE).strip()


def version(source):
    if Path(git(source, "rev-parse", "--show-toplevel")).resolve() != source.resolve():
        raise ValueError("No repository metadata")
    tags = [tag for tag in git(source, "tag", "--list").splitlines() if TAG.fullmatch(tag)]
    if tags:
        args = ["describe", "--tags", "--long", "--abbrev=7", "--dirty"]
        for tag in tags:
            args.extend(["--match", tag])
        try:
            description = git(source, *args)
        except subprocess.CalledProcessError:
            description = ""
        if description:
            match = re.fullmatch(r"(.+)-(\d+)-g([0-9a-f]+)(-dirty)?", description)
            if not match:
                raise ValueError("Invalid Git description")
            tag, distance, revision, dirty = match.groups()
            if distance == "0" and not dirty:
                return tag
            return tag + ("." if "+" in tag else "+") + distance + ".g" + revision + (".dirty" if dirty else "")
    revision = git(source, "rev-parse", "--short=7", "HEAD")
    dirty = bool(git(source, "status", "--porcelain", "--untracked-files=no"))
    return "v0.0.0+0.g" + revision + (".dirty" if dirty else "")


if __name__ == "__main__":
    try:
        print(version(Path(__file__).resolve().parents[1]))
    except (OSError, ValueError, subprocess.CalledProcessError):
        # Source archives can provide VERSION explicitly through make.
        print("devel")

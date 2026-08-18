#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import argparse
import glob
import hashlib
import json
import os


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-dir", required=True)
    parser.add_argument("--vial", required=True)
    parser.add_argument("--web", required=True)
    parser.add_argument("--support", required=True)
    args = parser.parse_args()
    files = []
    for path in sorted(glob.glob(os.path.join(args.build_dir, "main-*"))):
        if os.path.isfile(path):
            files.append({"name": os.path.basename(path), "bytes": os.path.getsize(path), "sha256": sha256(path)})
    manifest = {
        "license": "GPL-2.0-or-later",
        "source": "https://github.com/LeeLiuyuen/vial-gui",
        "versions": {"vial": args.vial, "vialWeb": args.web, "support": args.support},
        "files": files,
    }
    with open(os.path.join(args.build_dir, "silicore-vial-web-manifest.json"), "w", encoding="utf-8") as output:
        json.dump(manifest, output, ensure_ascii=False, indent=2, sort_keys=True)
        output.write("\n")


if __name__ == "__main__":
    main()

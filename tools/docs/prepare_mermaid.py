#!/usr/bin/env python3
"""Fetch a pinned Mermaid browser bundle into ignored local tooling."""
import base64
import hashlib
import io
from pathlib import Path
import tarfile
import urllib.request

VERSION = "12.2.0"
INTEGRITY = "w7nr/SFrLO7BaVTs3dQTvYSV6nYSBj0Yy9DjBhsIJtAcHqRzXSq4Pg32ujHZ/AdWsAMNEvvhbm5dt9E2tOiHzw=="
ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "work/diagram-renderer"
URL = f"https://registry.npmjs.org/mermaid/-/mermaid-{VERSION}.tgz"


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    archive = OUTPUT / f"mermaid-{VERSION}.tgz"
    data = archive.read_bytes() if archive.exists() else urllib.request.urlopen(URL, timeout=60).read()
    actual = base64.b64encode(hashlib.sha512(data).digest()).decode()
    if actual != INTEGRITY:
        raise ValueError("Mermaid package integrity mismatch")
    archive.write_bytes(data)
    # Read only exact named files; never extract archive-supplied paths.
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as bundle:
        for name in ("dist/mermaid.min.js", "package.json", "LICENSE"):
            stream = bundle.extractfile(f"package/{name}")
            if stream is None:
                raise ValueError(f"Missing bundle member: {name}")
            (OUTPUT / Path(name).name).write_bytes(stream.read())
    print(f"Verified Mermaid {VERSION}: {OUTPUT / 'mermaid.min.js'}")


if __name__ == "__main__":
    main()

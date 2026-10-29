"""Validate the plant library: python dev/validate.py [filter ...].

Prints every problem, or only those whose location contains one of the filters.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "custom_components" / "cyborg_gardening"))

from library import loader  # noqa: E402

for region in loader.regions():
    errors = loader.validate(loader.load(region))
    if filters := sys.argv[1:]:
        errors = [e for e in errors if any(f in e for f in filters)]
    print(f"{region}: {len(errors)} problem(s)")
    for line in errors:
        print("  " + line)

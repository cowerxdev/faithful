"""Check a JSON summary against a saved source text file."""
import argparse
import json
from pathlib import Path
from . import faithful


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('summary', type=Path, help='JSON with summary and why_builder_cares')
    args = parser.parse_args()
    reason = faithful(json.loads(args.summary.read_text()), args.source.read_text())
    print('PASS: all checked tokens appear in source' if not reason else 'FAIL: ' + reason)
    return bool(reason)


if __name__ == '__main__':
    raise SystemExit(main())

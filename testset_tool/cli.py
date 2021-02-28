"""Console script for testset_tool."""
import argparse
import logging
import sys

import testset


def main():
    """Console script for testset_tool."""
    parser = argparse.ArgumentParser()
    parser.add_argument('dirname',
                        help='Directory with testset to load')
    parser.add_argument('--lint', action='store_true',
                        help='Lint the testset')
    parser.add_argument('--show', action='store_true',
                        help='Show the testset')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Show debug statements')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(f"Arguments: {args}")

    ts = testset.TestSet(args.dirname)
    if args.lint:
        ts.lint()
    if args.show:
        ts.show()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

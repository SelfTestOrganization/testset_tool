"""Console script for testset_tool."""
import argparse
import logging
import sys

import convert
import testset


def main():
    """Console script for testset_tool."""
    parser = argparse.ArgumentParser()
    parser.add_argument('dirname',
                        help='Directory with testset')
    parser.add_argument('--lint', action='store_true',
                        help='Lint the testset')
    parser.add_argument('--show', action='store_true',
                        help='Show the testset')
    parser.add_argument('--convert', default=None,
                        help='Convert this old formatted testset to new one')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Show debug statements')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(f"Arguments: {args}")

    if args.lint:
        ts = testset.TestSet(args.dirname)
        ts.lint()
    if args.show:
        ts = testset.TestSet(args.dirname)
        ts.show()
    if args.convert:
        convert.convert(args.convert, args.dirname)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

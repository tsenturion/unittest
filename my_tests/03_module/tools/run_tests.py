import unittest
import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", default="tests/unit")
    parser.add_argument("-p", default="*_spec.py")
    parser.add_argument("-t", default=".")
    parser.add_argument("-k", action="append", default=[])
    parser.add_argument("-v", action="count", default=0)

    args = parser.parse_args()

    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=args.s,
        pattern=args.p,
        top_level_dir=args.t
    )

    runner = unittest.TextTestRunner(verbosity=1 + args.v)
    runner.run(suite)


if __name__ == "__main__":
    main()
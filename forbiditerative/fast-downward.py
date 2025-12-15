#! /usr/bin/env python3

import argparse
import logging
import sys


if __name__ == "__main__":
    from driver.main import main
    from forbiditerative.plan import set_default_build_path
    log_level_parser = argparse.ArgumentParser(add_help=False)
    log_level_parser.add_argument(
        "--log-level", choices=["debug", "info", "warning"],
        default="info",
        help="set log level (most verbose: debug; least verbose: warning; default: %(default)s)"
    )
    (log_level_args, _) = log_level_parser.parse_known_args()
    logging.basicConfig(
        level=getattr(logging, log_level_args.log_level.upper()),
        format="%(pathname)s:%(lineno)d %(levelname)-8s %(message)s",
        stream=sys.stdout,
        force=True,
    )
    set_default_build_path()
    main()

import os
import argparse

import logging

logger = logging.getLogger(__name__)

LOG_LEVEL_MAP = {
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG
}

def main():
    tw_opts = [
        ('api_key', '--api-key', '-k', 'TWITTER_API_KEY', "Twitter API Key"),
        ('api_secret', '--api-secret', '-s', 'TWITTER_API_SECRET', "Twitter API Secret"),
        ('access_token', '--access-token', '-a', 'TWITTER_ACCESS_TOKEN', "Twitter Access Token"),
        ('access_secret', '--access_secret', '-S', 'TWITTER_ACCESS_TOKEN_SECRET', "Twitter Access Token Secret")
    ]
    parser = argparse.ArgumentParser('Appreciation Bot worker process')
    parser.add_argument('--loglevel', choices=LOG_LEVEL_MAP.keys(),
        help='level at or above which log events at printed')
    parser.add_argument('--logfile',
        help='location of the log file, stdout if not provided')
    add_opts_with_default(parser, tw_opts)
    args = parser.parse_args()
    #
    # Log setup
    #
    loglevel = None if args.loglevel is None else LOG_LEVEL_MAP[args.loglevel]
    logger = logging.getLogger()
    if loglevel is not None:
        logger.setLevel(loglevel)
    handler = logging.StreamHandler() if args.logfile is None else logging.FileHandler(args.logfile)
    logformat = '[%(levelname)s] %(message)s' if loglevel is None or loglevel >= logging.INFO else '[%(levelname)s] %(name)s - %(message)s'
    formatter = logging.Formatter(logformat)
    handler.setFormatter(formatter)
    if loglevel is not None:
        handler.setLevel(loglevel)
    logger.addHandler(handler)
    #
    # Twitter variables
    #
    if check_opts_with_default(args, tw_opts) == False:
        exit(1)
    #
    # Main process loop
    #
    logger.info("Processing tweets")

def add_opts_with_default(parser, opts):
    for opt in opts:
        add_opt_with_default(parser, opt[1], opt[2], opt[3], opt[4])

def add_opt_with_default(parser, longopt, shortopt, osenv, help):
    parser.add_argument(longopt, shortopt, default=os.environ.get(osenv), help=help)

def check_opts_with_default(args, opts):
    r = True
    for opt in opts:
        r = check_opt_with_default(args, opt[0], opt[1], opt[3], opt[4]) and r
    return r

def check_opt_with_default(args, optname, longopt, osenv, help):
    if getattr(args, optname) is None:
        logger.error(
            "{help} is empty, ensure the {longopt} option or the {osenv} environment variable is set".format(
                help=help, longopt=longopt, osenv=osenv
            ))
        return False
    else:
        return True

if __name__ == "__main__":
    main()

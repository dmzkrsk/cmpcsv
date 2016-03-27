#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals
import argparse
from csv import DictReader
from six import moves, PY3
import io
import re
import logging.config


def read_file(encoding):
    kwargs = dict(mode='r', encoding=encoding, newline='') if PY3 else dict(mode='rb')

    def _arg(filename):
        try:
            of = io.open(filename, **kwargs)
            return of
        except IOError as e:
            message = "can't open '{}': {}".format(filename, e)
            raise argparse.ArgumentTypeError(message)

    return _arg


ENCODING = 'utf-8'


parser = argparse.ArgumentParser()
parser.add_argument('a', type=read_file(ENCODING))
parser.add_argument('b', type=read_file(ENCODING))
parser.add_argument('--ws', dest='ws', default='')
parser.add_argument('--skip', nargs='+', dest='skip', default=[])
parser.add_argument('--ignore-a', nargs='+', dest='ignore_a', default=[])
parser.add_argument('--ignore-b', nargs='+', dest='ignore_b', default=[])
parser.add_argument('--ignore-ws', nargs='+', dest='ignore_ws', default=[])
parser.add_argument('--ignore-case', nargs='+', dest='ignore_case', default=[])


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'short': {
            'format': '%(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'short': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'short',
        },
    },
    'loggers': {
        'cmpcsv': {
            'handlers': ['short'],
            'level': 'INFO',
        },
    }
})

logger = logging.getLogger('cmpcsv')


def whitespace_re(symbols):
    all_symbols = ''.join(map(re.escape, symbols)) + '\s'
    return re.compile(r"["+all_symbols+"]+", re.I | re.U)


def clean_ws(text, ws):
    return ' '.join(filter(None, ws.split(text)))


def cmpcsv(args):
    errors = False

    a = DictReader(args.a)
    b = DictReader(args.b)

    keys_a = set(a.fieldnames)
    keys_b = set(b.fieldnames)

    extra_a = keys_a - keys_b - set(args.ignore_a)
    extra_b = keys_b - keys_a - set(args.ignore_b)

    extra_keys = keys_a ^ keys_b

    ws = whitespace_re(args.ws)

    if extra_a:
        logger.critical('Extra keys found in a: %s', ', '.join(extra_a))
        return

    if extra_b:
        logger.critical('Extra keys found in b: %s', ', '.join(extra_b))
        return

    for line, (row_a, row_b) in enumerate(moves.zip_longest(a, b), start=1):
        if row_a == row_b:
            continue

        if row_a is None:
            logger.critical('File b is longer than a')
            return
        if row_b is None:
            logger.critical('File a is longer than b')
            return

        for key in keys_a:
            if key in args.skip:
                continue
            if key in extra_keys:
                continue

            val_a = row_a[key]
            val_b = row_b[key]
            if val_a == val_b:
                continue

            if key in args.ignore_ws:
                if clean_ws(val_a, ws) == clean_ws(val_b, ws):
                    continue

            if key in args.ignore_case:
                if val_a.lower() == val_b.lower():
                    continue

            if not PY3:
                val_a = val_a.decode(ENCODING)
                val_b = val_b.decode(ENCODING)

            logger.error(u'''Values for key "%s" doesn't match at line %d:\na:%s\nb:%s''', key, line, val_a, val_b)
            errors = True

    if not errors:
        logger.info('Files are equal')


def cmpcsv_cmd():
    cmpcsv(parser.parse_args())


if __name__ == '__main__':
    cmpcsv(parser.parse_args())

#!/usr/bin/env python
# Script to convert a CONLL File to standoff format

import codecs
import os
import re
import sys

ENCODING = 'UTF-8'

CSV_FORMAT = 'csv'
CONLL_FORMAT = 'conll'
STANDOFF_FORMAT = 'standoff'

FORMATS = [
            CONLL_FORMAT,
            CSV_FORMAT
            ]

def argparser():
    import argparse
    from pathlib import Path
    ap = argparse.ArgumentParser(description='Convert CSV to Standoff format',
                                 usage='%(prog)s [OPTIONS] DIRS/FILES')
    ap.add_argument('-f', '--format', choices=FORMATS,
                    default=FORMATS[0],
                    help='supported annotation formats')
    ap.add_argument('-o',"--output_dir", type=Path, default=Path(__file__).absolute().parent / "output",
        help="Path to the data directory",
    )
    ap.add_argument('data', metavar='DIRS/FILES', nargs='+')
    return ap

def convert_directory(directory, options):
    files = [n for n in os.listdir(directory) ]
    files = [os.path.join(directory, fn) for fn in files]
    convert_files(files, options)

def convert_files(files, options):
    for fn in sorted(files):
        document = read_conll(fn, options)
        ann_data = document.to_ann(
            include_offsets=options.char_offsets,
            include_docid=options.include_docid
        )
        sys.stdout.write(ann_data)

def txt_for_ann(filename):
    return os.path.splitext(filename)[0]+'.txt'

def read_conll(filename, options, encoding=ENCODING):
    txtfilename = txt_for_ann(filename)
    with codecs.open(txtfilename, 'rU', encoding=encoding) as t_in:
        with codecs.open(filename, 'rU', encoding=encoding) as a_in:
            return "ciao"

def main(argv):
    args = argparser().parse_args(argv[1:])
    files = []
    for path in args.data:
        if os.path.isdir(path):
            convert_directory(path, args)
        else:
            files.append(path)
    if files:
        convert_files(files, args)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
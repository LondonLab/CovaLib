#!/bin/env python
"""Generate amb.crg from prot.table file.

Michael Mysinger 200708 Created
Michael Mysinger 200910 Stdin/stdout support added by using logging module
                        Use filename, file-like, and generator layer concept
"""

import os
import sys
import logging
from optparse import OptionParser

def check_charge(charge, lastres):
    if lastres != '   ':
        logging.info("Total charge for residue '%s' = %7.4f" % 
                     (lastres, charge))
        if round(charge) != round(charge, 4):
            logging.warning("Charge not integral for residue '%s'!" %
                            lastres )

def prot2crg(initer):
    yield '! Automatically converted by prot2crg.py\n'
    yield 'aaaaaarrrnnnncqqqqqqqq    format (A6, A3, A4, A1, F8.3)\n'
    total = 0.0
    lastres = None
    for line in initer:
        if line[0] == '!' or line.strip() == '':
            continue
        atom = line[:4]
        res = line[7:10]
        num = line[10:14]
        chain = line[14:15]
        charge = line[15:23]
        nres = res.lower()
        prefix = '%-4.4s' % atom.lstrip() + '  ' + nres + num + chain + charge
        if len(line) > 27:
            suffix = '    ' + line[27:]
        else:
            suffix = '\n'
        if lastres is not None and lastres != res:
            check_charge(total, lastres)
            total = 0.0
        if atom.strip()[:1] != 'A' or atom.strip() == 'AS': 
            total += float(charge)
        yield prefix + suffix
        lastres = res
    check_charge(total, lastres)

def prot2crg_f(inf, outf):
    """Generate amb.crg from prot.table file."""
    for line in prot2crg(inf):
        outf.write(line)

def prot2crg_fn(infile=None, outfile=None, **kwargs):
    if infile is None:
        inf = sys.stdin
    else:
        inf = open(infile, 'r')
    if outfile is None:
        outf = sys.stdout
    else:
        outf = open(outfile, 'w')
    prot2crg_f(inf, outf, **kwargs)
    inf.close()
    outf.close()

def main(argv):
    """Parse arguments."""
    logging.basicConfig(level=logging.INFO, 
                        format='%(levelname)s: %(message)s')
    description = "Generate amb.crg from prot.table file."
    usage = "%prog [options]"
    version = "%prog: version 200910 - created by Michael Mysinger"
    parser = OptionParser(usage=usage, description=description,
                          version=version)
    parser.set_defaults(infile=None, outfile=None)
    parser.add_option("-i", "--in", dest="infile",
                      help="input file (default: stdin).")
    parser.add_option("-o", "--out", dest="outfile",
                      help="output file (default: stdout).")
    options, args = parser.parse_args(args=argv[1:])
    if len(args):
        parser.error("program takes no positional arguments.\n" +
                     "  Use --help for more information.")
    prot2crg_fn(infile=options.infile, outfile=options.outfile)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

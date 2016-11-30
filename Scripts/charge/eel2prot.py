#!/bin/env python
"""Generate prot.table from an eel1 file.

Michael Mysinger 200910 Created
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

def eel2prot(initer):
    yield '! Automatically converted by eel2prot.py\n'
    yield ( '!aaaxxxrrrnnnncqqqqqqqqxtt' +
            '   format (A4, 3x, A3, A4, A1, F8.3, 1x, I2)\n' )
    total = 0.0
    lastres = None
    for line in initer:
        if not (line.startswith("ATOM") or line.startswith("HETATM")):
            continue
        atom = line[12:16]
        res = line[17:20]
        charge = line[54:62]
        vdw = line[70:73]
        ivdw = int(vdw)
        if ( ivdw == 6 or ivdw == 7 ) and abs(float(charge)) < 0.00001:
            # skip uncharged hydrogens
            continue
        nline = atom + '   ' + res + '     ' + charge + vdw + '\n'
        if lastres is not None and lastres != res:
            check_charge(total, lastres)
            total = 0.0
        if atom.strip()[:1] != 'A': 
            total += float(charge)
        yield nline
        lastres = res
    check_charge(total, lastres)

def eel2prot_f(inf, outf):
    """Generate amb.crg from prot.table file."""
    for line in eel2prot(inf):
        outf.write(line)

def eel2prot_fn(infile=None, outfile=None, **kwargs):
    if infile is None:
        inf = sys.stdin
    else:
        inf = open(infile, 'r')
    if outfile is None:
        outf = sys.stdout
    else:
        outf = open(outfile, 'w')
    eel2prot_f(inf, outf, **kwargs)
    inf.close()
    outf.close()

def main(argv):
    """Parse arguments."""
    logging.basicConfig(level=logging.INFO, 
                        format='%(levelname)s: %(message)s')
    description = "Generate prot.table from an eel1 file."
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
    eel2prot_fn(infile=options.infile, outfile=options.outfile)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/bin/env python
# coding=utf8

import os
from tools.utils import getlogger

logger1 = getlogger()	


def STAR_virus(args):

    logger1.info('align virus genome...')

    sample = args.sample
    outdir = args.outdir
    unmapped_read = args.unmapped_read
    virus_genomeDir = args.virus_genomeDir
    thread = args.thread

    # check dir
    if not os.path.exists(outdir):
        os.system('mkdir -p %s' % (outdir))
    
    out_prefix = outdir + "/" + sample + "_virus_"
    out_BAM = out_prefix + "Aligned.sortedByCoord.out.bam"

    # host genome align
    cmd = "STAR \
 --genomeDir {genome} \
 --readFilesIn {unmapped_read}\
 --outFilterMatchNmin 35\
 --outSAMtype BAM SortedByCoordinate\
 --runThreadN {runThreadN}\
 --limitBAMsortRAM 1933647594\
 --outFileNamePrefix {out_prefix}".format(genome=virus_genomeDir,
    unmapped_read=unmapped_read, runThreadN=thread, out_prefix=out_prefix)

    logger1.info(cmd)
    os.system(cmd)
    logger1.info("align virus genome done.")   

    cmd = "samtools index {out_BAM}".format(out_BAM=out_BAM)
    logger1.info(cmd)
    os.system(cmd)
    logger1.info("index done.")


def get_opts_STAR_virus(parser, sub_program):
    if sub_program:
        parser.add_argument('--outdir', help='output dir', required=True)
        parser.add_argument('--sample', help='sample name', required=True)
        parser.add_argument("--unmapped_read", required=True)
        parser.add_argument("--thread", help='STAR thread', default=1)
    parser.add_argument('--virus_genomeDir', help='virus genome dir', required=True)

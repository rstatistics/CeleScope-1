#!/bin/env python
#coding=utf8
import os, re, io, logging, gzip, json
import subprocess
from collections import defaultdict, namedtuple
import sys


def capture_virus(args):
    steps = ['sample', 'barcode', 'cutadapt',  "STAR_virus", "count_capture_virus"]
    sample = args.sample
    args.assay = "capture_virus"

    outdir_dic = {}
    index = 0
    for step in steps:
        outdir = f"{sample}/{index:02d}.{step}"
        outdir_dic.update({step: outdir})
        index += 1

    step = "sample"
    args.outdir = f'{sample}/{outdir_dic["step"]}/'
    from tools.sample_info import sample_info
    sample_info(args)   

    step = "barcode"
    args.outdir = f'{sample}/{outdir_dic["step"]}/'   
    from tools.barcode import barcode
    barcode(args)

    step = "cutadapt"
    args.outdir = f'{sample}/{outdir_dic["step"]}/' 
    args.fq = f'{outdir_dic["barcode"]}/{sample}_2.fq.gz'
    from tools.cutadapt import cutadapt
    cutadapt(args)

    step = "STAR_virus"
    args.input_read = f'{outdir_dic["cutadapt"]}/{sample}_clean_2.fq.gz'
    args.outdir = f'{sample}/{outdir_dic["step"]}/' 
    from virus.STAR_virus import STAR_virus
    STAR_virus(args)  

    step = 'count_capture_virus'
    args.virus_bam = f'{outdir_dic["STAR_virus"]}/{sample}_virus_Aligned.sortedByCoord.out.bam'
    args.outdir = f'{sample}/{outdir_dic["step"]}/' 
    from capture_virus.count_capture_virus import count_capture_virus
    count_capture_virus(args)
 
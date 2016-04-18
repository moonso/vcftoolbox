# -*- coding: utf-8 -*-
import sys
import os
import logging
import itertools
import codecs

import click

from . import (get_vcf_handle, HeaderParser, print_headers, remove_vcf_info,
print_variant, get_variant_dict, get_info_dict, get_snpeff_info, sort_variants)
from .log import LEVELS, configure_stream

logger = logging.getLogger(__name__)

@click.group()
@click.argument('vcf', 
                nargs=1, 
                metavar='<vcf_file> or -'
)
@click.option('-v', '--verbose', 
    count=True, 
    default=2
)
@click.option('-o', '--outfile',
                    type=click.File('w'),
                    help='Specify the path to a file where results should be stored.'
)
@click.option('-s', '--silent',
    is_flag=True
)
@click.pass_context
def cli(ctx, vcf, verbose, outfile, silent):
    """Simple vcf operations"""
    # configure root logger to print to STDERR
    loglevel = LEVELS.get(min(verbose, 3))
    configure_stream(level=loglevel)
    
    if vcf == '-':
        handle = get_vcf_handle(fsock=sys.stdin)
    else:
        handle = get_vcf_handle(infile=vcf)
    
    head = HeaderParser()
    for line in handle:
        line = line.rstrip()
        if line.startswith('#'):
            if line.startswith('##'):
                head.parse_meta_data(line)
            else:
                head.parse_header_line(line)
        else:
            break
    ctx.head = head

    ctx.handle = itertools.chain([line], handle)
    ctx.outfile = outfile
    ctx.silent = silent
    

@cli.command()
@click.option('-i', '--info',
    type=str
)
@click.pass_context
def delete_info(ctx, info):
    """Delete a info field from all variants in a vcf"""
    head = ctx.parent.head
    vcf_handle = ctx.parent.handle
    outfile = ctx.parent.outfile
    silent = ctx.parent.silent
    
    if not info:
        logger.error("No info provided")
        sys.exit("Please provide a info string")
    
    if not info in head.info_dict:
        logger.error("Info '{0}' is not specified in vcf header".format(info))
        sys.exit("Please provide a valid info field")
    
    head.remove_header(info)
    
    print_headers(head, outfile=outfile, silent=silent)
    
    for line in vcf_handle:
        line = line.rstrip()
        new_line = remove_vcf_info(keyword=info, variant_line=line)
        print_variant(variant_line=new_line, outfile=outfile, silent=silent)

@cli.command()
@click.option('--snpeff',
    is_flag=True,
    help="Print the snpeff annotations"
)
@click.pass_context
def variants(ctx, snpeff):
    """Print the variants in a vcf"""
    head = ctx.parent.head
    vcf_handle = ctx.parent.handle
    outfile = ctx.parent.outfile
    silent = ctx.parent.silent
    
    print_headers(head, outfile=outfile, silent=silent)
    
    for line in vcf_handle:
        print_variant(variant_line=line, outfile=outfile, silent=silent)
        if snpeff:
            variant_dict =  get_variant_dict(
                variant_line = line,
                header_line = head.header
            )
            #Create a info dict:
            info_dict = get_info_dict(
                info_line = variant_dict['INFO']
            )
            snpeff_string = info_dict.get('ANN')

            if snpeff_string:
                #Get the snpeff annotations
                snpeff_info = get_snpeff_info(
                    snpeff_string = snpeff_string,
                    snpeff_header = head.snpeff_columns
                )

@cli.command()
@click.pass_context
def sort(ctx):
    """Sort the variants of a vcf file"""
    head = ctx.parent.head
    vcf_handle = ctx.parent.handle
    outfile = ctx.parent.outfile
    silent = ctx.parent.silent

    print_headers(head, outfile=outfile, silent=silent)

    for line in sort_variants(vcf_handle):
        print_variant(variant_line=line, outfile=outfile, silent=silent)
        
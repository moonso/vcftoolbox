#!/usr/bin/env python
# encoding: utf-8
"""
prints.py

Tools to print different parts of vcf files

Created by Måns Magnusson on 2015-01-22.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""

from __future__ import print_function

from codecs import open

def print_headers(head, outfile=None, silent=False):
    """
    Print the vcf headers.
    
    If a result file is provided headers will be printed here, otherwise
    they are printed to stdout.
    
    Args:
        head (HeaderParser): A vcf header object
        outfile (FileHandle): A file handle
        silent (Bool): If nothing should be printed.
        
    """
    for header_line in head.print_header():
        
        if outfile:
            outfile.write(header_line+'\n')
        else:
            if not silent:
                print(header_line)
    return

def print_variant(variant_line, outfile=None, silent=False):
    """
    Print a variant.
    
    If a result file is provided the variante will be appended to the file, 
    otherwise they are printed to stdout.
    
    Args:
        variants_file (str): A string with the path to a file
        outfile (FileHandle): An opened file_handle
        silent (bool): Bool. If nothing should be printed.
    
    """
    variant_line = variant_line.rstrip()
    if not variant_line.startswith('#'):
        if outfile:
            outfile.write(variant_line+'\n')
        else:
            if not silent:
                print(variant_line)
    return
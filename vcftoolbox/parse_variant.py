"""Parse a variant line in different ways"""

import logging

logger = logging.getLogger(__name__)

def get_variant_dict(variant_line, header_line=None):
    """Parse a variant line
        
        Split a variant line and map the fields on the header columns
        
        Args:
            variant_line (str): A vcf variant line
            header_line (list): A list with the header columns
        Returns:
            variant_dict (dict): A variant dictionary
    """
    if not header_line:
        logger.debug("No header line, use only first 8 mandatory fields")
        header_line = ['CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO']
    
    logger.debug("Building variant dict from variant line {0} and header"\
    " line {1}".format(variant_line, '\t'.join(header_line)))
    
    splitted_line = variant_line.rstrip().split('\t')
    if len(splitted_line) < len(header_line):
        logger.info('\t'.join(header_line))
        logger.info('\t'.join(splitted_line))
        raise SyntaxError("Length of variant line differs from length of"\
                            " header line")
    
    return dict(zip(header_line, splitted_line))

def get_info_dict(info_line):
    """Parse a info field of a variant
        
        Make a dictionary from the info field of a vcf variant.
        Keys are the info keys and values are the raw strings from the vcf
        If the field only have a key (no value), value of infodict is True.
        
        Args:
            info_line (str): The info field of a vcf variant
        Returns:
            info_dict (dict): A INFO dictionary
    """
    
    variant_info = {}
    for raw_info in info_line.split(';'):
        splitted_info = raw_info.split('=')
        if len(splitted_info) == 2:
            variant_info[splitted_info[0]] = splitted_info[1]
        else:
            variant_info[splitted_info[0]] = True
    
    return variant_info

def get_variant_id(variant_dict=None, variant_line=None):
    """Build a variant id
    
        The variant id is a string made of CHROM_POS_REF_ALT
        
        Args:
            variant_dict (dict): A variant dictionary
        
        Returns:
            variant_id (str)
    """
    
    if variant_dict:
        chrom = variant_dict['CHROM']
        position = variant_dict['POS']
        ref = variant_dict['REF']
        alt = variant_dict['ALT']
    elif variant_line:
        splitted_line = variant_line.rstrip().split('\t')
        chrom = splitted_line[0]
        position = splitted_line[1]
        ref = splitted_line[3]
        alt = splitted_line[4]
    else:
        raise Exception("Have to provide variant dict or variant line")
    
    return '_'.join([
        chrom,
        position,
        ref,
        alt,
    ])

def get_vep_info(vep_string, vep_header):
    """Make the vep annotations into a dictionaries
    
        A vep dictionary will have the vep column names as keys and 
        the vep annotations as values.
        The dictionaries are stored in a list

        Args:
            vep_string (string): A string with the CSQ annotation
            vep_header (list): A list with the vep header
        
        Return:
            vep_annotations (list): A list of vep dicts
    
    """
    
    vep_annotations = [
        dict(zip(vep_header, vep_annotation.split('|'))) 
        for vep_annotation in vep_string.split(',')
    ]
    
    return vep_annotations

def get_snpeff_info(snpeff_string, snpeff_header):
    """Make the vep annotations into a dictionaries
    
        A snpeff dictionary will have the snpeff column names as keys and 
        the vep annotations as values.
        The dictionaries are stored in a list. 
        One dictionary for each transcript.

        Args:
            snpeff_string (string): A string with the ANN annotation
            snpeff_header (list): A list with the vep header
        
        Return:
            snpeff_annotations (list): A list of vep dicts
    
    """
    
    snpeff_annotations = [
        dict(zip(snpeff_header, snpeff_annotation.split('|'))) 
        for snpeff_annotation in snpeff_string.split(',')
    ]
    
    return snpeff_annotations

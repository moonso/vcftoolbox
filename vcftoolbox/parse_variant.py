"""Parse a variant line in different ways"""

import logging

logger = logging.getLogger(__name__)

def get_variant_dict(variant_line, header_line):
    """Parse a variant line
        
        Split a variant line and map the fields on the header columns
        
        Args:
            variant_line (str): A vcf variant line
            header_line (list): A list with the header columns
        Returns:
            variant_dict (dict): A variant dictionary
    """
    logger.debug("Building variant dict from variant line {0} and header"\
    " line {1}".format(variant_line, '\t'.join(header_line)))
    
    splitted_line = variant_line.rstrip().split('\t')
    if len(splitted_line) != len(header_line):
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

def get_variant_id(variant_dict):
    """Build a variant id
    
        The variant id is a string made of CHROM_POS_REF_ALT
        
        Args:
            variant_dict (dict): A variant dictionary
        
        Returns:
            variant_id (str)
    """
    
    return '_'.join([
        variant_dict['CHROM'],
        variant_dict['POS'],
        variant_dict['REF'],
        variant_dict['ALT'],
    ])

def get_vep_dict(vep_string, vep_header):
    """Make the vep annotation into a dictionary
    
        This dictionary will have the alleles as keys and a list of 
        dictionaries with vep annotations as values.
        
        Args:
            vep_list (string): A string with the CSQ annotation
            vep_header (list): A list with the vep header
        
        Return:
            vep_dict (dict): A vep dict as described above
    
    """
    
    vep_dict = {}
    for vep_annotation in vep_string.split(','):
        inner_dict = dict(zip(vep_header, vep_annotation.split('|')))
        allele = inner_dict['Allele']
        if allele in vep_dict:
            vep_dict[allele].append(inner_dict)
        else:
            vep_dict[allele] = [inner_dict]
    
    return vep_dict

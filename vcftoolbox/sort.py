import os
import logging
import codecs

from tempfile import NamedTemporaryFile
from datetime import datetime
from subprocess import call

logger = logging.getLogger(__name__)

def get_chromosome_priority(chrom, chrom_dict={}):
    """
    Return the chromosome priority
    
    Arguments:
        chrom (str): The cromosome name from the vcf
        chrom_dict (dict): A map of chromosome names and theis priority
    
    Return:
        priority (str): The priority for this chromosom
    """
    priority = 0
    
    chrom = str(chrom).lstrip('chr')
    
    if chrom_dict:
        priority = chrom_dict.get(chrom, 0)
    
    else:
        try:
            if int(chrom) < 23:
                priority = int(chrom)
        except ValueError:
            if chrom == 'X':
                priority = 23
            elif chrom == 'Y':
                priority = 24
            elif chrom == 'MT':
                priority = 25
            else:
                priority = 26
    
    return str(priority)



def sort_variants(vcf_handle):
    """Sort the variants of a vcf file
    
        Args:
            vcf_handle
            mode (str): position or rank score
        
        Returns:
            sorted_variants (Iterable): An iterable with sorted variants
    """
    logger.debug("Creating temp file")
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.close()
    logger.debug("Opening temp file with codecs")
    temp_file_handle = codecs.open(
                        temp_file.name,
                        mode='w',
                        encoding='utf-8',
                        errors='replace'
                        )

    try:
        with codecs.open(temp_file.name,mode='w',encoding='utf-8',errors='replace') as f:
            for line in vcf_handle:
                if not line.startswith('#'):
                    line = line.rstrip().split('\t')
                    chrom = line[0]
                    priority = get_chromosome_priority(chrom)
                
                    print_line = "{0}\t{1}\n".format(priority, '\t'.join(line))
                    f.write(print_line)
        #Sort the variants
        sort_variant_file(temp_file.name)
        
        with codecs.open(temp_file.name,mode='r',encoding='utf-8',errors='replace') as f:
            for line in f:
                line = line.rstrip().split('\t')
                yield '\t'.join(line[1:])

    except Exception as err:
        logger.error("Something went wrong")
        logger.error(err)
    finally:
        logger.debug("Deleting temp file")
        os.remove(temp_file.name)
        logger.debug("Temp file deleted")
    
    # temp_file_handle.seek(0)
    #     for line in temp_file_handle:
    #         print_line = line.split('\t')[1:]
    #         yield '\t'.join(print_line)

def sort_variant_file(infile):
    """
    Sort a modified variant file.
    Sorting is based on the first column and the POS.
    
    Uses unix sort to sort the variants and overwrites the infile.
    
    Args:
        infile : A string that is the path to a file
        mode : 'chromosome' or 'rank'
        outfile : The path to an outfile where the variants should be printed
    
    Returns:
        0 if sorting was performed
        1 if variants where not sorted
    """
    command = [
            'sort',
            ]
    command.append('-n')
    command.append('-k1')
    command.append('-k3')

    command = command + [infile, '-o', infile]

    logger.info("Start sorting variants...")
    logger.info("Sort command: {0}".format(' '.join(command)))
    sort_start = datetime.now()
    
    try:
        call(command)
    except OSError as e:
        logger.warning("unix command sort does not seem to exist on your system...")
        logger.warning("genmod needs unix sort to provide a sorted output.")
        logger.warning("Output VCF will not be sorted since genmod can not find"\
                        "unix sort")
        raise e

    logger.info("Sorting done. Time to sort: {0}".format(datetime.now()-sort_start))
    
    return 

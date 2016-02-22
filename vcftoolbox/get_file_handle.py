import os
import sys
import logging
import gzip
from codecs import open, getreader

logger = logging.getLogger(__name__)

def get_vcf_handle(fsock=None, infile=None):
    """Open the vcf file and return a handle"""

    vcf = None
    if (fsock or infile):
    
        if fsock:
            # if not infile and hasattr(fsock, 'name'):
            logger.info("Reading vcf form stdin")
            if sys.version_info < (3, 0):
                logger.info("Using codecs to read stdin")
                sys.stdin = getreader('utf-8')(fsock)
            
            vcf = sys.stdin
        
        else:
            logger.info("Reading vcf from file {0}".format(infile))
            file_name, file_extension = os.path.splitext(infile)
            if file_extension == '.gz':
                logger.debug("Vcf is zipped")
                vcf = getreader('utf-8')(gzip.open(infile), errors='replace')
            elif file_extension == '.vcf':
                vcf = open(infile, mode='r', encoding='utf-8', errors='replace')
            else:
                raise IOError("File is not in a supported format!\n"
                                " Or use correct ending(.vcf or .vcf.gz)")
    else:
        raise IOError("Please provide a fsock or infile")
    
    return vcf
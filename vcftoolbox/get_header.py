import itertools
import logging

from . import HeaderParser

logger = logging.getLogger(__name__)

def get_vcf_header(source):
    """Get the header lines of a vcf file
    
        Args:
            source(iterable): A vcf file
        
        Returns:
            head (HeaderParser): A headerparser object
    """
    head = HeaderParser()
    #Parse the header lines
    for line in source:
        line = line.rstrip()
        if line.startswith('#'):
            if line.startswith('##'):
                logger.debug("Found metadata line {0}".format(line))
                head.parse_meta_data(line)
            else:
                logger.debug("Found header line {0}".format(line))
                head.parse_header_line(line)
        else:
            break
    
    return head
        
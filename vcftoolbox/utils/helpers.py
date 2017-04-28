import os

def zipped(path):
    """Check if file is zipped
    
    Use fileending for now, maybe come up with smarter solution in future.
    
    Args:
        path(str)
    
    Returns:
        bool
    """
    file_name, file_extension = os.path.splitext(path)
    if file_extension == '.gz':
        return True
    return False

def indexed(path):
    """Check if file has a tabix index
    
    Args:
        path(str)
    
    Returns:
        bool
    """
    return os.path.isfile(path+'.tbi')

def strip_chr(chrom):
    """Strip chr letters from chromosome
    
    Args:
        chrom(str)
    
    Returns:
        corrected(str)
    """
    if chrom.startswith(('chr', 'CHR', 'Chr')):
        chrom = chrom[3:]
    return chrom
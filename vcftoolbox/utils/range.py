import tabix

from .helpers import strip_chr

def check_position(variant_line, chrom, start, end):
    """Check if a variant is in a specified range
    
    Args:
        variant_line(str): A raw vcf variant line
        chrom(str): Name och chromosome
        start(int): Start position of range
        end(int): End position of range
    
    Returns:
        bool: if variant is within range
    """
    
    splitted_line = variant_line.split('\t')
    
    variant_chrom = strip_chr(splitted_line[0])
    if variant_chrom == chrom:
        variant_pos = int(splitted_line[1])
        if (variant_pos <= end and variant_pos >= start):
            return True
    return False
    

def get_range(vcf_handle, chrom, start, end, zipped_vcf=None):
    """Returns e generator with the lines that should be used
    
    Args:
        vcf_handle(iterable(str))
        chrom(str)
        start(int)
        end(int)
    
    Yields:
        vcf(generator): Lines of vcf file 
    """
    chrom = strip_chr(chrom)
    
    # This is a helper to know when to stop looking
    region_found = False
    
    for line in vcf_handle:
        line = line.rstrip()
        if line.startswith('#'):
            if line.startswith('##contig'):
                # Get the contig
                contig = strip_chr(line[13:].split(',')[0])
                # If contig is correct we return it
                if contig == chrom:
                    yield line
            else:
                # Return all header lines if not contig
                yield line
        else:
            # If we have a zipped and indexed vcf we can collect a chunk
            # directly with tabix
            if zipped_vcf:
                break
            else:
                # Otherwise we need to look line by line
                if check_position(line, chrom, start, end):
                    region_found = True
                    yield line
                # If the region was found but we are not in region we can stop
                # looking
                else:
                    if region_found:
                        break
    if zipped_vcf:
        tabix_reader = tabix.open(zipped_vcf)
        for record in tabix_reader.query(chrom, start-1, end):
            yield '\t'.join(record)

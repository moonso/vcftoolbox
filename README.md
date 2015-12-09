[![Build Status](https://travis-ci.org/moonso/vcftoolbox.svg)](https://travis-ci.org/moonso/vcftoolbox)


Set of tools for working with vcf files and variants.

Thanks to [pyvcf](https://github.com/jamescasbon/PyVCF) for code base in header parser.

# Utilities #

```python
def get_variant_dict(variant_line, header_line):
    """Parse a variant line
        
        Split a variant line and map the fields on the header columns
        
        Args:
            variant_line (str): A vcf variant line
            header_line (list): A list with the header columns
        Returns:
            variant_dict (dict): A variant dictionary
    """
```

```python
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
```

```python
def get_variant_id(variant_dict):
    """Build a variant id
    
        The variant id is a string made of CHROM_POS_REF_ALT
        
        Args:
            variant_dict (dict): A variant dictionary
        
        Returns:
            variant_id (str)
    """
```

```python
def get_vep_info(vep_string, vep_header):
    """Make the vep annotations into a dictionaries
    
        A vep dictionary will have the vep column names as keys and 
        the vep annotations as values.
        The dictionaries are stored in a list

        Args:
            vep_list (string): A string with the CSQ annotation
            vep_header (list): A list with the vep header
            allele (str): The allele that is annotated
        
        Return:
            vep_annotations (list): A list of vep dicts
    
    """
```

```python
def replace_vcf_info(keyword, annotation, variant_line=None, variant_dict=None):
    """Replace the information of a info field of a vcf variant line or a 
        variant dict.
    
    Arguments:
        variant_line (str): A vcf formatted variant line
        variant_dict (dict): A variant dictionary
        keyword (str): The info field key
        annotation (str): If the annotation is a key, value pair
                          this is the string that represents the value
    
    Returns:
        variant_line (str): A annotated variant line
```

```python
def add_vcf_info(keyword, variant_line=None, variant_dict=None, annotation=None):
    """
    Add information to the info field of a vcf variant line.
    
    Arguments:
        keyword (str): The info field key
        variant_line (str): A vcf formatted variant line
        annotation (str): If the annotation is a key, value pair
                          this is the string that represents the value
    
    Returns:
        fixed_variant : str if variant line, or dict if variant_dict
    """
```


## Classes ##

### Genotype ###


```python
class Genotype(object):
    """Holds information about a vcf genotype
    
        These objects try to collect the relevant information about genotype 
        calls in the vcf format.
        
        Attributes:
            allele_1 = '.'
            allele_2 = '.'
            genotype = './.'
            heterozygote = False
            allele_depth = False
            homo_alt = False
            homo_ref = False
            has_variant = False
            genotyped = False
            phased = False
            depth_of_coverage = 0
            quality_depth = 0
            genotype_quality = 0
            ref_depth = 0
            alt_depth = 0
            quality_depth = ref_depth + alt_depth
            phred_likelihoods = []
        
    
    """
```

### HeaderParser ###


```python
class HeaderParser(object):
    """Class for holding and manipulating vcf headers
        
        Attributes:
            info_dict=OrderedDict()
            extra_info = {}
        
            filter_lines=[]
            filter_dict=OrderedDict()
        
            contig_lines=[]
            contig_dict=OrderedDict()
        
            format_lines=[]
            format_dict=OrderedDict()
        
            alt_lines=[]
            alt_dict=OrderedDict()
        
            other_lines=[]
            other_dict=OrderedDict()
        
            header=['CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO']
            header_keys={'info' : ['ID', 'Number', 'Type', 'Description'], 
                           'form' : ['ID', 'Number', 'Type', 'Description'], 
                           'filt' : ['ID', 'Description'],
                           'alt' : ['ID', 'Description'],
                           'contig' : ['ID', 'length']}
            fileformat = None
            filedate = None
            reference = None
            phasing = None
            source = None
            line_counter = 0
            individuals = []
            vep_columns = []
            info_pattern
            filter_pattern
            contig_pattern
            format_pattern
            alt_pattern
            meta_pattern
        
        Methods:
            parse_meta_data(line)
            parse_header_line(line)
            add_fileformat(fileformat)
            print_header(): Return a list with the header lines
            add_meta_linekey, value)
            add_info(info_id, number, entry_type, description)
            add_filter(filter_id, description)
            add_format(format_id, number, entry_type, description)            
            add_alt(alt_id, description)            
            add_contig(contig_id, length)
            add_version_tracking(info_id, version, date, command_line='')            
            
    """
```
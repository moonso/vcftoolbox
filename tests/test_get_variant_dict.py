import pytest
from vcftoolbox import get_variant_dict, HeaderParser


def get_vcf_file():
    """Return a list with vcf lines"""
    vcf_lines = [
        '##fileformat=VCFv4.2',
        '##FILTER=<ID=LowQual,Description="Low quality">',
        '##INFO=<ID=MQ,Number=1,Type=Float,Description="RMS Mapping Quality">',
        '##INFO=<ID=CNT,Number=A,Type=Integer,Description="Number of times '\
        'this allele was found in external db">',
        '##contig=<ID=1,length=249250621,assembly=b37>',
        '##INFO=<ID=DP_HIST,Number=R,Type=String,Description="Histogram for '\
        'DP; Mids: 2.5|7.5|12.5|17.5|22.5|27.5|32.5|37.5|42.5|47.5|52.5|57.5|'\
        '62.5|67.5|72.5|77.5|82.5|87.5|92.5|97.5">',
        '##FORMAT=<ID=AD,Number=.,Type=Integer,Description="Allelic depths for'\
        ' the ref and alt alleles in the order listed">',
        '##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">',
        '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">',
        '##FORMAT=<ID=GQ,Number=1,Type=String,Description="GenotypeQuality">'
        '##reference=file:///human_g1k_v37.fasta',
        '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tfather\tmother\tproband',
        '1\t11900\t.\tA\tT\t100\tPASS\tMQ=1\tGT:GQ\t0/1:60\t0/1:60\t1/1:60\n',
        '1\t879585\t.\tA\tT\t100\tPASS\tMQ=1\tGT:GQ\t0/1:60\t0/0:60\t0/1:60\n',
        '1\t879586\t.\tA\tT\t100\tPASS\tMQ=1\tGT:GQ\t0/0:60\t0/1:60\t0/1:60\n',
        '1\t947378\t.\tA\tT\t100\tPASS\tMQ=1\tGT:GQ\t0/0:60\t0/0:60\t0/1:60\n',
        '1\t973348\t.\tG\tA\t100\tPASS\tMQ=1\tGT:GQ\t0/0:60\t0/0:60\t0/1:60\n',
        '3\t879585\t.\tA\tT\t100\tPASS\tMQ=1\tGT:GQ\t0/1:60\t0/0:60\t0/1:60\n',
        '3\t879586\t.\tA\tT\t100\tPASS\tMQ=1\tGT:GQ\t0/0:60\t0/1:60\t0/1:60\n',
        '3\t947378\t.\tA\tT\t100\tPASS\tMQ=1\tGT:GQ\t0/0:60\t0/0:60\t0/1:60\n',
        '3\t973348\t.\tG\tA\t100\tPASS\tMQ=1\tGT:GQ\t0/0:60\t0/0:60\t0/1:60\n'
    ]
    
    return vcf_lines

def get_header(vcf_lines):
    """Parse the vcf lines and return a header object"""
    head = HeaderParser()
    
    for line in vcf_lines:
        if line.startswith('#'):
            if line.startswith('##'):
                head.parse_meta_data(line)
            else:
                head.parse_header_line(line)
    return head

def test_sanity():
    """Test to build variant dicts"""
    
    vcf = get_vcf_file()
    
    head = get_header(vcf)
    
    header_line = head.header
    
    for line in vcf:
        if not line.startswith('#'):
            variant = get_variant_dict(
                variant_line = line, 
                header_line = header_line
            )

def test_wrong_variant():
    """Test to build a variant dict with a wrong formatted variant"""
    
    vcf = get_vcf_file()
    
    head = get_header(vcf)
    
    header_line = head.header
    
    # Missing one gt call
    wrong_variant = '3\t973348\t.\tG\tA\t100\tPASS\tMQ=1\tGT:GQ\t0/0:60\t0/0:60\n'
    
    with pytest.raises(SyntaxError):
        variant = get_variant_dict(
            variant_line = wrong_variant, 
            header_line = header_line
        )

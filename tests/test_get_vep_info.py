import pytest
from vcftoolbox import get_vep_info


def test_get_vep_info():
    """
    Test how the vep columns are parsed
    """
    
    vep_header = ['Allele','Gene','Feature','Feature_type','Consequence']
    vep_string = "A|ADK|ENST00000432963||intron_variant"
    
    vep_info = get_vep_info(
        vep_string=vep_string,
        vep_header=vep_header
    )
    
    assert vep_info[0]['Consequence'] == 'intron_variant' 
    assert vep_info[0]['Feature_type'] == '' 

def test_get_vep_info_no_allele():
    """
    Test how the vep columns are parsed
    """
    
    vep_header = "Consequence|Codons|Amino_acids|Gene|SYMBOL|Feature|EXON"\
                 "|PolyPhen|SIFT|Protein_position|BIOTYPE".split('|')
    
    vep_string = "non_coding_transcript_exon_variant&intron_variant&non_codin"\
    "g_transcript_variant&feature_truncation|||ENSG00000230368|FAM41C|ENST00"\
    "000432963|1/4||||lincRNA,intron_variant&non_coding_transcript_variant&"\
    "feature_truncation|||ENSG00000230368|FAM41C|ENST00000427857|||||lincRNA"\
    ",intron_variant&non_coding_transcript_variant&feature_truncation|||"\
    "ENSG00000230368|FAM41C|ENST00000446136|||||lincRNA,upstream_gene_variant"\
    "|||ENSG00000234711|TUBB8P11|ENST00000415481|||||unprocessed_pseudogene"
    
    vep_info = get_vep_info(
        vep_string=vep_string,
        vep_header=vep_header
    )
    
    assert len(vep_info) == 4

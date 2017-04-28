from vcftoolbox import add_vcf_info

def test_add_info_no_annotation_line():
    ## GIVEN a raw vcf line
    variant = "1\t879537\t.\tT\tC\t100\tPASS\tMQ=1\tGT:AD:GQ\t0/1:10,10:60\t0/1:10,10:60\t"\
    "1/1:10,10:60\t0/0:10,10:60\t0/1:10,10:60\t1/1:10,10:60"
    assert 'RS' not in variant
    ## WHEN adding a INFO field without value
    annotated_variant = add_vcf_info('RS', variant_line=variant, 
                                     variant_dict=None, annotation=None)
    ## THEN assert the information was added
    assert 'RS' in annotated_variant
    
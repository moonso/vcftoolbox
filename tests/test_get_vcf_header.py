from vcftoolbox import get_vcf_header

vcf_file = [
    '##fileformat=VCFv4.1',
    '##INFO=<ID=MQ,Number=1,Type=Float,Description="RMS Mapping Quality">',
    "##contig=<ID=1,length=249250621,assembly=b37>",
    "##reference=file:///humgen/gsa-hpprojects/GATK/bundle/current/b37/human"\
    "_g1k_v37.fasta",
    "#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	father	mother	"\
    "proband	father_2	mother_2	proband_2",
    "1	879537	.	T	C	100	PASS	MQ=1	GT:AD:GQ	0/1:10,10:60	0/1:10,10:60	"\
    "1/1:10,10:60	0/0:10,10:60	0/1:10,10:60	1/1:10,10:60"
    "1	879541	.	G	A	100	PASS	MQ=1	GT:AD:GQ	./.	0/1:10,10:60	1/1:10,10:60	"\
    "./.	0/1:10,10:60	0/1:10,10:60"
]

def test_get_vcf_header():
    """docstring for test_get_vcf_header"""
    head = get_vcf_header(vcf_file)
    
    assert 'MQ' in head.info_dict
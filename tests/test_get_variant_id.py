from vcftoolbox import get_variant_id
import pytest

def test_get_variant_id_dict():
    """docstring for test_get_variant_id_dict"""
    variant_dict = {
        'CHROM': '1',
        'POS': '10',
        'REF':'A',
        'ALT': 'T'
    }
    
    assert get_variant_id(variant_dict) == '1_10_A_T'
    

def test_get_variant_id_line():
    """docstring for test_get_variant_id_dict"""
    variant_line = '1\t10\t.\tA\tT'
    
    assert get_variant_id(variant_line=variant_line) == '1_10_A_T'

def test_send_wrong():
    """docstring for test_get_variant_id_dict"""
    with pytest.raises(Exception):
        get_variant_id()
import os
import pytest
from tempfile import NamedTemporaryFile
from StringIO import StringIO

from vcftoolbox import get_vcf_handle

vcf_lines = [
    "##verions=4.2",
    "First variant",
    "Second variant"
]


class Test_get_vcf_handle(object):
    """docstring for Test_get_vcf_handle"""
    def setup(self):
        """Setup a vcf handle"""
        self.temp_file = NamedTemporaryFile(suffix='.vcf', delete=False)
        for line in vcf_lines:
            self.temp_file.write("{0}\n".format(line))
        self.temp_file.close()

    def teardown(self):
        """docstring for teardown"""
        os.remove(self.temp_file.name)
        
    def test_get_vcf_handle_file(self):
        """docstring for test_get_vcf_handle_file"""
        file_handle = get_vcf_handle(infile=self.temp_file.name)
        result = []
        for line in file_handle:
            line = line.rstrip()
            result.append(line)
        
        assert result == vcf_lines
    
    # def test_get_vcf_handle_stream(self):
    #     """docstring for test_get_vcf_handle_stream"""
    #     stream = StringIO('\n'.join(vcf_lines))
    #
    #     file_handle = get_vcf_handle(fsock=stream)
    #     result = []
    #     for line in file_handle:
    #         line = line.rstrip()
    #         result.append(line)
    #
    #     assert result == vcf_lines
        
    def test_get_vcf_handle_no_input(self):
        """docstring for test_get_vcf_handle_file"""
        with pytest.raises(IOError):
            file_handle = get_vcf_handle()

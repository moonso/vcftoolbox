from __future__ import absolute_import

from .header_parser import HeaderParser
from .genotype import Genotype
from .parse_variant import (get_variant_dict, get_info_dict, get_variant_id, 
get_vep_dict)
from .add_variant_information import (replace_vcf_info)
#!/usr/bin/env python
# encoding: utf-8
"""
genotype.py

This is a class with information about genotypecalls that follows the (GATK) .vcf standard.

The indata, that is the genotype call, is allways on the form x/x, so they look like 0/0, 1/2, 1/1 and so on.
The first sign inidcates what we find on the first allele, the second is a separator on the form '/' or '|' and the third indicates what is seen on the second allele.
The alleles are unordered.

Attributes:

    - genotype STRING (Same as in VCF-standard)
    - allele_1 STRING (Base on allele 1)
    - allele_2 STRING (Base on allele 2)
    - nocall BOOL
    - heterozygote BOOL 
    - homo_alt BOOL (If individual is homozygote alternative)
    - homo_ref BOOL (If individual is homozygote reference)
    - has_variant BOOL (If individual is called and not homozygote reference)
    - ref_depth INT
    - alt_depth INT
    - phred_likelihoods LIST with FLOAT
    - depth_of_coverage INT
    - genotype_quality FLOAT
    - phased BOOL

If a variant is present, that is if homo_alt or heterozygote is true, then has_variant is True
    
When dealing with phased data we will see the '|'-delimiter


#TODO:
Should we allow '1/2', '2/2' and so on? This type of call looses it's point when moving from vcf -> bed since bed files only have one kind of variant on each line.
For now we will only allow './.', '0/0', '0/1', '1/1'   

Created by Måns Magnusson on 2014-06-30.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os


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
    def __init__(self, **kwargs):
        """Initialize a genotype object
        
        Arguments:
            GT(str): The genotype call in vcf format. eg. 0/1. Default './.'
            AD(str): Allele depths for each observed allele. Default '.,.'
            DP(str): Total read depth for this variant. Default '0'
            GQ(str): Phred scaled genotype quality for this variant call. 
                     Default '0'
            PL(str): The likelihoods for the different possible calls for this variant. 
                     Default None
            SU(str): Number of pieces of evidence supporting the variant
            PE(str): Number of paired-end reads supporting the variant
            SR(str): Number of split reads supporting the variant
        """
        super(Genotype, self).__init__()
        # These are the different genotypes:
        GT = kwargs.get('GT', './.')
        AD = kwargs.get('AD', '.,.')
        DP = kwargs.get('DP', '0')
        GQ = kwargs.get('GQ', '0')
        PL = kwargs.get('PL')
        SU = kwargs.get('SU', '0')
        PE = kwargs.get('PE', '0')
        SR = kwargs.get('SR', '0')
        #Referense allele observations(used by freebays for example)
        RO = kwargs.get('RO')
        #Alternative allele observations(used by freebays for example)
        AO = kwargs.get('AO')
        #Alternative allele observations(used by vardict for example)
        VD = kwargs.get('VD')
        
        self.heterozygote = False
        self.allele_depth = False
        self.homo_alt = False
        self.homo_ref = False
        self.has_variant = False
        self.genotyped = False
        self.phased = False
        self.depth_of_coverage = 0
        self.quality_depth = 0
        self.genotype_quality = 0
        self.supporting_evidence = int(SU)
        #Paired end support
        self.pe_support = int(PE)
        #Split read support
        self.sr_support = int(SR)
        
        #Check phasing
        if '|' in GT:
            self.phased = True
        #Check the genotyping:
        #This is the case when only one allele is present(eg. X-chromosome) and presented like '0' or '1':
        if len(GT) < 3: 
            self.allele_1 = GT
            self.allele_2 = '.'
        else:
            self.allele_1 = GT[0]
            self.allele_2 = GT[-1]
        # The genotype should allways be represented on the same form
        self.genotype = self.allele_1 +'/'+ self.allele_2
        
        if self.genotype != './.':
            self.genotyped = True
            #Check allele status
            if self.genotype in ['0/0', './0', '0/.']:
                self.homo_ref = True
            elif self.allele_1 == self.allele_2:
                self.homo_alt = True
                self.has_variant = True
            else:
                self.heterozygote = True
                self.has_variant = True
        #Check the depth of coverage:
        try:
            self.depth_of_coverage = int(DP)
        except ValueError:
            self.depth_of_coverage = 0
        #Check the allele depth:
        self.ref_depth = 0
        self.alt_depth = 0
        
        # Freebayes specific
        if RO and RO != '.':
            self.ref_depth = int(RO)
        if AO and AO != '.':
            self.alt_depth = int(AO)
        
        # Vardict specific
        elif VD and VD != '.':
            self.alt_depth = int(VD)
            self.ref_depth = self.depth_of_coverage - self.alt_depth
        
        else:
            allele_depths = AD.split(',')
            
            if len(allele_depths) > 1:
                if allele_depths[0].isdigit():
                    self.ref_depth = int(allele_depths[0])
                if allele_depths[1].isdigit():
                    self.alt_depth = int(allele_depths[1])
        
        self.quality_depth = self.ref_depth + self.alt_depth
        #Check the genotype quality
        try:
            self.genotype_quality = float(GQ)
        except ValueError:
            pass
        #Check the genotype likelihoods
        self.phred_likelihoods = []
        
        if PL:
            try:
                self.phred_likelihoods = [int(score) for score in PL.split(',')]
            except ValueError:
                pass
        
        
    def __str__(self):
        """Specifies what will be printed when printing the object."""
        return self.allele_1+'/'+self.allele_2


#! /usr/bin/env python3

import vcf
import httplib2
import json

__author__ = "Stefan Brenner"


class Assignment3:

    def __init__(self):

        print("PyVCF version: %s" % vcf.VERSION,"\n")
        self.vcf_path = "chr16.vcf"

    @property
    def annotate_vcf_file(self):

        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        params_pos = []
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))

                if counter >= 899:
                    break

        params = 'ids=' + ",".join(params_pos) + '&hg38=true'

        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')

        annotation_result_json = json.loads(annotation_result)
        return (annotation_result_json)

    def get_list_of_genes(self, annotation_result_json):
       
        for i in annotation_result_json:
            if 'cadd' in i:
                if 'genename' in i['cadd']['gene']:
                    print(i['cadd']['gene']['genename'])

    def get_num_variants_modifier(self, annotation_result_json):
     
        num_variants_modifier = 0
        for i in annotation_result_json:
            if 'snpeff' in i:
                key, value = "putative_impact", "MODIFIER"
                if key in i['snpeff']['ann'] and value == i['snpeff']['ann']['putative_impact']:
                    num_variants_modifier += 1
        print("Number of variants modifier:",num_variants_modifier,"\n")

    def get_num_variants_with_mutationtaster_annotation(self, annotation_result_json):

        variants_with_mutationtaster_annotation = 0
        for i in annotation_result_json:
            if 'dbnsfp' in i:
                if 'mutationtaster' in i['dbnsfp']:
                    variants_with_mutationtaster_annotation += 1
        print("Number of variants with mutationtaster annotation:",variants_with_mutationtaster_annotation,"\n")

    def get_num_variants_non_synonymous(self, annotation_result_json):

        variants_non_synonymous = 0
        for i in annotation_result_json:
            if 'cadd' in i:
                key, value = "consequence", "NON_SYNONYMOUS"
                if key in i['cadd'] and value == i['cadd']['consequence']:
                    variants_non_synonymous += 1
        print("Number of variants non synonymous:", variants_non_synonymous,"\n")

    def view_vcf_in_browser(self):
        print("Final URL: https://vcf.iobio.io/?species=Human&build=GRCh38","\n")

    def print_summary(self):
        data = self.annotate_vcf_file
        print("List of Genes:"), self.get_list_of_genes(data)
        print()
        self.get_num_variants_modifier(data)
        self.get_num_variants_with_mutationtaster_annotation(data)
        self.get_num_variants_non_synonymous(data)
        self.view_vcf_in_browser()


def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print("Done with assignment 3")


if __name__ == '__main__':
    main()
import argparse
import gzip
import os
import sys

headerSNP="alternate_ids rsid chromosome position alleleA alleleB index average_maximum_posterior_call info cohort_1_AA cohort_1_AB cohort_1_BB cohort_1_NULL all_AA all_AB all_BB all_NULL all_total cases_AA cases_AB cases_BB cases_NULL cases_total controls_AA controls_AB controls_BB controls_NULL controls_total all_maf cases_maf controls_maf missing_data_proportion cohort_1_hwe cases_hwe controls_hwe het_OR het_OR_lower het_OR_upper hom_OR hom_OR_lower hom_OR_upper all_OR all_OR_lower all_OR_upper frequentist_add_pvalue frequentist_add_info frequentist_add_beta_1 frequentist_add_se_1 comment\n"
headerPlink="CHR\tSNP\tBP\tA1\tA2\tOR\tSE\tPVAL\tBETA\tINFOSCORE\n"

def gzipHandle(fileName):
    if '.gz' in fileName:
        fileOut = gzip.open(fileName, 'rt')
    else:
        fileOut = open(fileName, 'rt')
    return fileOut

def processFiles(snptestIn, outPre, chrom):
    inFile = gzipHandle(snptestIn)
    outSnp = gzip.open(outPre+'.snptest.gz', 'wt')
    outPlink = gzip.open(outPre+'.assoc.gz', 'wt')
    outSnp.write(headerSNP)
    outPlink.write(headerPlink)
    for n, line in enumerate(inFile):
        if n % 10000 == 0:
            print('ROCESSED LINES {} FROM {}'.format(n, snptestIn))
        if '#' not in line:##skip nontable lines
            if 'rsid' not in line:
                lineParse = line.strip().split(' ')
                if len(lineParse) == 49:
                    lineParse[2] = chrom
                    if lineParse[1] == "." or lineParse[1] == "-9":
                        lineParse[1] = chrom+':'+lineParse[3]+':'+lineParse[4]+':'+lineParse[5]
                    indNeeded = [2, 1, 3, 5, 4, 41, 44, 47, 46, 45] # colIndexs needed for plink
                    plinkString = '\t'.join([lineParse[i] for i in indNeeded])
                    # lineParse[2]+'\t'+lineParse[1]+'\t'+lineParse[3]+'\t'+lineParse[5]+'\t'+lineParse[4]+'\t'+lineParse[41]+'\t'+lineParse[44]+'\t'+lineParse[47]+'\t'+lineParse[46]+'\t'+lineParse[45]+'\n'
                    if lineParse[46] != 'NA':
                        outSnp.write(' '.join(lineParse)+'\n')
                        outPlink.write(plinkString+'\n')
    outPlink.close()
    outSnp.close()

def main():
    parser = argparse.ArgumentParser(description='Script to prepare snptest files for meta analyses compatible with plink and meta and METAL')
    parser.add_argument('-CHR', help='Chromosome number 1-22', required=True)
    parser.add_argument('-F', help='Input asssociation file', required=True)
    parser.add_argument('-O', help='output prefix', required=True)
    args=parser.parse_args()
    snptestIn = args.F
    outPre = args.O
    chrom = args.CHR
    print('ARGS -F {} -O {} -CHR {}'.format(snptestIn, outPre, chrom))
    processFiles(snptestIn, outPre, chrom)

if __name__ == '__main__': main()

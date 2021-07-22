import re
from subprocess import Popen, PIPE
import sys
import os
import argparse


def checkPath(filePre, fileSuf, chr_):
	'''Given a prefix and file extension and a chr number checks if a file exists in current directory
	'''
	pathFile = os.path.join(os.getcwd(), '{}_CHR{}.{}'.format(filePre, chr_, fileSuf))
	print(pathFile)
	if os.path.exists(pathFile):
		print('FOUND MATCHING FILE {}'.format(pathFile))
		return True
	else:
		return False


def plinkSplitCall(filePre, chrNum):
	'''Given a base bed file, this function will submit a job to split files by chromosomes and return a job ID
	'''
	if os.path.exists(os.path.join(os.getcwd(), 'scripts/PLINK_SPLIT_SLURM.sh')):
		plinKSplit='./scripts/PLINK_SPLIT_SLURM.sh {} {}'.format(filePre, chrNum)
		plinkCall=Popen(plinKSplit, shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderr= plinkCall.communicate()
		if not stderr:
			job1 = re.findall(r'\d+', stdout.decode())[0]
			print(stdout.decode())
			if not job1:
				exit('Job Submission Unsuccessful for Script {}'.format(plinKSplit))
			else:
				return job1
		else:
			exit('Job Submission Unsuccessful for Script {}'.format(plinKSplit))
	else:
		raise FileNotFoundError('Check Path scripts/PLINK_SPLIT_SLURM.sh')


def phasingCall(filePre,chrNum, *args):
	'''function to take input as the base plink file prefix and an optional job dependency for slurm
	'''
	if args:
		dependency=args[0]
		if dependency:
			print('Job Dependency {}'.format(dependency))
			shapeIt='./scripts/SHAPEIT_ARRAY_TASK_SLURM.sh {} {} {}'.format(filePre, chrNum, dependency)
	else:
		shapeIt='./scripts/SHAPEIT_ARRAY_TASK_SLURM.sh {} {}'.format(filePre, chrNum)
	print(shapeIt)
	if os.path.exists(os.path.join(os.getcwd(), 'scripts/SHAPEIT_ARRAY_TASK_SLURM.sh')):
		shapeitCall=Popen(shapeIt, shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderr= shapeitCall.communicate()
		if not stderr:
			job2 = re.findall(r'\d+', stdout.decode())[0]
			if not job2:
				exit('Job Submission Unsuccessful for Script {}'.format(shapeitCall))
			else:
				return job2
		else:
			exit('Job Submission Unsuccessful for Script {}'.format(shapeitCall))
	else:
		raise FileNotFoundError('Check Path scripts/SHAPEIT_ARRAY_TASK_SLURM.sh')


def parseChrSize(chrLength):
	'''Check and return chrSize in mb to impute script'''
	if len(chrLength) < 9:
		chrSize = str(int(chrLength[:2])+1)
	else:
		chrSize = str(int(chrLength[:3])+1)
	return chrSize


def sendImputejobs(chrNum, chrSizes, imputeScript, filePre, *args):
	'''job handler for imputation script, will check if arg is all chromosomes or only a range of chrs
	'''
	if chrNum == '1-22': # full imputation
		for chrTup in chrSizes:
			chr_=chrTup[0]
			chrLength=chrTup[1]
			chrSize= parseChrSize(chrLength)
			if args:
				dependency=args[0]
				print('Job Dependency {}'.format(dependency))
				impute='./scripts/{} {} {} {}'.format(imputeScript, chr_, chrSize, filePre, dependency)
			else:
				impute='./scripts/{} {} {} {}'.format(imputeScript, chr_, chrSize, filePre)
			#Popen(impute, shell=True, stdout=PIPE, stderr=PIPE)
			print(impute)
	else: ## check if args contain a range of chr
		for chr_ in chrNum.split(','):
			chrInd = int(chr_)-1
			chr_=chrSizes[chrInd][0]
			chrLength=chrSizes[chrInd][1]
			chrSize= parseChrSize(chrLength)
			print('CHR RANGE OR SINGLE CHR ARG DETECTED AS {}'.format(chrNum))
			if args:
				dependency=args[0]
				print('Job Dependency {}'.format(dependency))
				impute='./scripts/{} {} {} {}'.format(imputeScript, chr_, chrSize, filePre, dependency)
			else:
				impute='./scripts/{} {} {} {}'.format(imputeScript, chr_, chrSize, filePre)
			#Popen(impute, shell=True, stdout=PIPE, stderr=PIPE)
			print(impute)
## tests
# chrNum, chrSizes, imputeScript, filePre=['1,10', chrSizes, 'test.sh', 'gt']
# sendImputejobs(chrNum, chrSizes, imputeScript, filePre)
# chrNum, chrSizes, imputeScript, filePre=['1-22', chrSizes, 'test.sh', 'gt']
# sendImputejobs(chrNum, chrSizes, imputeScript, filePre)
# chrNum, chrSizes, imputeScript, filePre, dependency=['1,10', chrSizes, 'test.sh', 'gt', 'job1']
# sendImputejobs(chrNum, chrSizes, imputeScript, filePre, dependency)
# chrNum, chrSizes, imputeScript, filePre, dependency=['1-22', chrSizes, 'test.sh', 'gt', 'job1']
# sendImputejobs(chrNum, chrSizes, imputeScript, filePre, dependency)

def imputeCall(filePre, ref, chrNum, *args):
	'''makes the imputation calls with job dependency if applicable to the shapeit call
	'''
	chrSizes = [('1', '249250621'), 
				('2', '243199373'), 
				('3', '198022430'), 
				('4', '191154276'), 
				('5', '180915260'), 
				('6', '171115067'), 
				('7', '159138663'), 
				('8', '146364022'), 
				('9', '141213431'), 
				('10', '135534747'), 
				('11', '135006516'), 
				('12', '133851895'), 
				('13', '115169878'), 
				('14', '107349540'), 
				('15', '102531392'), 
				('16', '90354753'), 
				('17', '81195210'), 
				('18', '78077248'), 
				('19', '59128983'),
		    		('20', '63025520'),
				('21', '48129895'),
				('22', '51304566')]
	if ref == "3":
		imputeScript = 'IMPUTE_LOOP_SLURM.sh'
	else:
		imputeScript = 'IMPUTE_LOOP_SLURM_Phase1.sh'
	if args:
		dependency=args[0]
		if dependency:
			print('Job Dependency {}'.format(dependency))
			sendImputejobs(chrNum, chrSizes, imputeScript, filePre, dependency)
	else:
		sendImputejobs(chrNum, chrSizes, imputeScript, filePre)


def main():
	parser = argparse.ArgumentParser(description='Imputation Pipeline Main')
	parser.add_argument('-F', help='File Prefix for the base BED file unspit by chromosomes', required=True)
	parser.add_argument('-Ref', help='1000 genomes reference the input should be either 1 or 3', required=True)
	parser.add_argument('-CHR', help='Either a chromosome range in the format 1-22 or a single chromsome 1 or a custom range 1,6,7')
	args=parser.parse_args()
	filePre=args.F
	ref=args.Ref
	chrNum = args.CHR
	plinkFile=checkPath(filePre, fileSuf='bed', chr_='2')
	hapFile=checkPath(filePre, fileSuf='haps', chr_='2')
	if plinkFile: ## if plinkfile exists check for hap file
		if hapFile: ## if hap file exists go to imputation
			imputeCall(filePre, ref, chrNum)
		else:
			job2=phasingCall(filePre, chrNum)
			if job2:
				imputeCall(filePre, ref, chrNum, job2)    
	else:
		job1 = plinkSplitCall(filePre, chrNum)
		if job1:
			job2 = phasingCall(filePre, chrNum, job1)
			if job2:
				imputeCall(filePre, ref, chrNum, job2)

	

if __name__ == "__main__":main()

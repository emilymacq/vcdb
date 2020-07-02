import pandas as pd
import csv
import os.path
import shutil


def read_tsv(q_name, s_name):
	data = []
	with open('./' + q_name + '/' + s_name + '.tsv') as tsvfile:
		reader = csv.reader(tsvfile, delimiter='\t')
		for row in reader:
			data.append(list(row))
	return pd.DataFrame(data[1:], columns=data[0])


quarter = '2020Q1_d'

section = 'ISSUERS'
formissrs = read_tsv(quarter, section)
# contains CIK, ENTITYNAME, STREET1, STREET2, CITY, STATEORCOUNTRY, ZIPCODE
formissrs = formissrs[['ACCESSIONNUMBER', 'CIK', 'ENTITYNAME', 'STREET1', 'STREET2', \
'CITY', 'STATEORCOUNTRY', 'ZIPCODE']]

section = 'OFFERING'
formoffer = read_tsv(quarter, section)
# contains TOTALOFFERINGAMOUNT, TOTALAMOUNTSOLD, NUMBERNONACCREDITEDINVESTORS, TOTALNUMBERALREADYINVESTED
formoffer = formoffer[['ACCESSIONNUMBER', 'TOTALOFFERINGAMOUNT', 'TOTALAMOUNTSOLD', \
'NUMBERNONACCREDITEDINVESTORS', 'TOTALNUMBERALREADYINVESTED']]

section = 'SIGNATURES'
formsig = read_tsv(quarter, section)
# contains NAMEOFSIGNER, SIGNATUREDATE
formsig = formsig[['ACCESSIONNUMBER', 'NAMEOFSIGNER', 'SIGNATUREDATE']]

fulldata = pd.merge(formissrs, formoffer, how='outer', on='ACCESSIONNUMBER')
fulldata = pd.merge(fulldata, formsig, how='outer', on='ACCESSIONNUMBER')
# column with quarter
fulldata['quarter'] = quarter

# check if data exists
if os.path.exists('./vcdb.csv'):
	currdata = pd.read_csv('./vcdb.csv')
	# append new data to current data if quarter has not already been pulled
	if quarter not in currdata.quarter.values:
		fulldata = currdata.append(fulldata)
		# push data to csv
		fulldata.to_csv('vcdb.csv', index=None)
else:
	# push data to csv
	fulldata.to_csv('vcdb.csv', index=None)

# remove files
dir_path = './' + quarter
try:
    shutil.rmtree(dir_path)
except OSError as e:
    print("Error: %s : %s" % (dir_path, e.strerror))



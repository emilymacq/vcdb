import pandas as pd
import sys

filename = sys.argv[1]

newfnd = 0
newlnfnd = 0
newaud = 0
newfrm = 0
auditorlist = []
fundlist = []
fund = ''
with open(filename,"rt") as file:
	for line in file:
		if line == "\n":
			continue
		if "A. PRIVATE FUND" in line:
			newfnd = 1
			continue
		if newfnd == 1 and line[:29] == "(a) Name of the private fund:":
			fund = ''
			if " (b) " in line:
				fund = line[line.index(': ')+len(': '):line.index(' (b)')]
				fundlist.append(fund.rstrip("\n"))
			elif ": " in line:
				fund = line[line.index(': ')+len(': '):]
				fundlist.append(fund.rstrip("\n"))
			else:
				newlnfnd = 1
			newaud = 1
			newfnd = 0
			continue
		if newlnfnd == 1 and fund == '':
			if " (b) " in line:
				fund = line[:line.index(' (b)')]
			else:
				fund = line

			if fund.startswith('\x0c'):
				fund = fund[len("\x0c"):]
			fundlist.append(fund.rstrip("\n"))
			newlnfnd = 0
			continue
		if newaud == 1 and line[:8] == "Auditors":
			newaud = 0
			newfrm = 1
			continue
		if newfrm == 1 and (line[:20] == "No Information Filed" or line[:31] == "(b) Name of the auditing firm: "):
			if line[:20] != "No Information Filed":
				line = line[line.index(': ')+len(': '):]
			auditorlist.append(line.rstrip('\n'))
			newfrm = 0
			continue

print(len(fundlist))
print(fundlist)
print(len(auditorlist))
print(auditorlist)

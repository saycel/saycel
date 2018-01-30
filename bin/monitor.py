import sys

from collections import Counter
ar = []
with open(sys.argv[1]) as f:
	for line in f:
		if "Close Channel sofia/internal/sip:" in line:
			nl=line.split('301087')
			number = nl[1].split('@')[0]
			ar.append(number)

print Counter(ar)

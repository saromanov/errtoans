import stackexchange
from bs4 import BeautifulSoup
import py_compile
import subprocess
import sys

#https://github.com/lucjon/Py-StackExchange/tree/master/demo
#http://www.crummy.com/software/BeautifulSoup/bs4/doc/

def withSort(so):
	qs = so.search(sort=stackexchange.Sort.Votes, order=stackexchange.DESC)

def get_from_stackoverflow(title):
	so = stackexchange.Site(stackexchange.StackOverflow, app_key=None)
	so.be_inclusive()
	qs = so.search(intitle=title)
	for q in qs:
		question = so.question(q.id)
		print(q.title)
		print(so.answers(q.id))
		soup = BeautifulSoup(question.body)
		'''if soup.code != None:
			print(soup.p.index("arrays"))'''

def main(targetfile):
	command = 'python {0}'.format(targetfile)
	process = subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
	process.wait()
	output = process.communicate()
	result = str(output[1]).split("\\n")
	value = result[-2]
	get_from_stackoverflow(value)


if __name__ == '__main__':
	main(sys.argv[1])


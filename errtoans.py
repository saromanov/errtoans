import stackexchange
from bs4 import BeautifulSoup
import py_compile
import subprocess
import sys

#https://github.com/lucjon/Py-StackExchange/tree/master/demo
#http://www.crummy.com/software/BeautifulSoup/bs4/doc/

def withSort(so):
	qs = so.search(sort=stackexchange.Sort.Votes, order=stackexchange.DESC)

def parse_answer(data):
	soup = BeautifulSoup(data)
	if soup.code != None:
		print(soup.get_text())


def get_answers(data):
	for answer in data:
		parse_answer(answer.body)

def get_from_stackoverflow(title,limit=10, byscore=True):
	'''
		limit can be less than 10
		byscore - sorted questions by votes
	'''
	sortscore = stackexchange.Sort.Votes
	if byscore == False:
		sortscore = None
	so = stackexchange.Site(stackexchange.StackOverflow, app_key=None)
	so.be_inclusive()
	qs = so.search(intitle=title, sort=sortscore)
	for q in qs:
		question = so.question(q.id)
		print(question.url)
		print(q.title)
		print("\n")
		print("Answer: ")
		get_answers(question.answers)
		#get_code_from_q(question.body)
def main(targetfile):
	command = 'python {0}'.format(targetfile)
	process = subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
	process.wait()
	output = process.communicate()
	result = str(output[1]).split("\\n")
	if len(result) > 1:
		value = result[-2]
		get_from_stackoverflow(value)
		return
	print("file {0} not contain errors".format(targetfile))


if __name__ == '__main__':
	main(sys.argv[1])


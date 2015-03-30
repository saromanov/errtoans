import stackexchange
from bs4 import BeautifulSoup
import py_compile
import subprocess
import sys
import argparse

#https://github.com/lucjon/Py-StackExchange/tree/master/demo
#http://www.crummy.com/software/BeautifulSoup/bs4/doc/

def withSort(so):
	qs = so.search(sort=stackexchange.Sort.Votes, order=stackexchange.DESC)

def parse_answer(data):
	soup = BeautifulSoup(data)
	if soup.code != None:
		print(soup.get_text())


def get_answers(data):
	for answer in data: parse_answer(answer.body)

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

def main(targetfile, *args, **kwargs):
	command = 'python {0}'.format(targetfile)
	process = subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
	process.wait()
	output = process.communicate()
	result = str(output[1]).split("\\n")
	if len(result) > 1:
		value = result[-2]
		print("Your error: ", value)
		get_from_stackoverflow(value, limit=kwargs.get('num_answers'))
		return
	print("file {0} not contain errors".format(targetfile))


if __name__ == '__main__':
	#main(sys.argv[1])
	if len(sys.argv) == 1:
		raise Exception("input file not found")
	parser = argparse.ArgumentParser()
	parser.add_argument('path', default=sys.argv[1])
	parser.add_argument('--answers', help='show full answers', action='store_true')
	parser.add_argument('--num_answers', help='Show first n answers', type=int, default=10)
	args = parser.parse_args()
	main(sys.argv[1], answers=args.answers, num_answers=args.num_answers)


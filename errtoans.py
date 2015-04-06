import stackexchange
from bs4 import BeautifulSoup
import py_compile
import subprocess
import sys
import argparse
import os.path
from termcolor import colored

#https://github.com/lucjon/Py-StackExchange/tree/master/demo
#http://www.crummy.com/software/BeautifulSoup/bs4/doc/

def withSort(so):
	qs = so.search(sort=stackexchange.Sort.Votes, order=stackexchange.DESC)

def parse_answer(data, outfile=None):
	""" Return the 'clean' answer """
	soup = BeautifulSoup(data)
	if soup.code != None:
		result = soup.get_text()
		if outfile != None:
			write_file(outfile, result)
		print(result)


def get_answers(data, outfile=None):
	''' Show answer '''
	print("Answer: \n")
	for answer in data: parse_answer(answer.body, outfile=outfile)

def prepare_file(path):
	if os.path.isfile(path):
		open(path, 'w').close()

def write_file(path, data):
	""" Store result to log file """
	with open(path, 'a') as f:
		f.write(data)

def get_from_stackoverflow(title,limit=10, byscore=True, outfile=None, api=None):
	'''
		limit can be less than 10
		byscore - sorted questions by votes
	'''
	sortscore = stackexchange.Sort.Votes
	if byscore == False:
		sortscore = None
	so = stackexchange.Site(stackexchange.StackOverflow, app_key=api, impose_throttling=True)
	so.be_inclusive()
	qs = so.search(intitle=title, sort=sortscore)

	def show_info(msg, color):
		""" Print message, if outpath not None, write this message here( and print it)
		"""
		if outfile != None:
			write_file(outfile, msg)
		print(colored(msg, color))

	for q in qs:
		question = so.question(q.id)
		show_info(question.url, 'green')
		show_info(q.title, 'red')
		show_info("\n", 'white')
		show_info('Question: ', 'white')
		show_info(question.body, 'white')
		show_info("\n", 'white')
		get_answers(question.answers)

def prepare_error_msg(msg):
	print(msg)

def main(targetfile, *args, **kwargs):
	command = 'python {0}'.format(targetfile)
	process = subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
	process.wait()
	output = process.communicate()
	full_trace = str(output[1])
	result = str(full_trace).split("\\n")
	if len(result) > 1:
		path = kwargs.get('outfile')
		if path != None:
			prepare_file(path)
		prepare_error_msg(full_trace)
		value = result[-2]
		if kwargs.get('trace'):
			prepare_error_msg(full_trace)
		else:
			print("Your error: ", value)
		get_from_stackoverflow(value, limit=kwargs.get('num_answers',10), outfile=path)
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
	parser.add_argument('--outfile', help='Store results to file')
	parser.add_argument('--api', help='Set key to api from StackExchange')
	parser.add_argument('--show-full-trace', help='Show full stack trace with errors', action='store_false')
	args = parser.parse_args()
	main(sys.argv[1], answers=args.answers, num_answers=args.num_answers, outfile=args.outfile, api=args.api, \
		trace=args.show_full_trace)

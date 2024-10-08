import sys
import os

def leave():
	input('Press ENTER to continue...')
	sys.exit()

DECORATION = '--------------------------------------'
SCRIPT_PATH = os.path.dirname(sys.argv[0])
DUMP_PATH_HINT_FILE = os.path.join(SCRIPT_PATH, 'DDNetDumpPath.txt')
BAD_WORDS_FILE = os.path.join(SCRIPT_PATH, 'DDNetDumpBadWords.txt')

if not os.path.exists(DUMP_PATH_HINT_FILE):
	print(f'Missing "{DUMP_PATH_HINT_FILE}" file')
	leave()

with open(DUMP_PATH_HINT_FILE, 'r', encoding='utf-8') as f:
	path = os.path.expandvars(f.read())
	
	if path == None or not os.path.exists(path):
		print(f'"{path}" does not exist')
		leave()

	files = os.listdir(path)

texts = []
if len(sys.argv) > 1:
	texts.append(sys.argv[1])
else:
	if not os.path.exists(BAD_WORDS_FILE):
		print(f'Usage: "ddsearch <word>"\nOR: "ddsearch", which would look for a file called \"{BAD_WORDS_FILE}\" that contains bad words separated by lines')
		leave()

	with open(BAD_WORDS_FILE, 'r', encoding='utf-8') as f:
		texts = f.read().split('\n')

results = {}
for text in texts:
	results[text] = 0

for file in files:
	if not file.startswith('remote_console_dump'): continue

	file = os.path.join(path, file)

	with open(file, 'r', encoding='utf-8') as f:
		content = f.read().split('\n')
		for idx, line in enumerate(content):
			for text in texts:
				if text in line:
					print(f'{DECORATION}\nFile: {file}\nLine: {idx+1}\n{line}')
					results[text] += 1

output = f'{DECORATION}\nFound:\n'
for text in results:
	if results[text] == 0: continue	

	output += f'\"{text}\"\t\t{results[text]} time'
	
	if results[text] != 1:
		output += 's\n'
	else:
		output += '\n'

output += DECORATION

print(output)
leave()
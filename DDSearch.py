import sys
import os
from colorama import init as initTermColor
from termcolor import cprint

initTermColor()

def leave():
	input('Press ENTER to continue...')
	sys.exit()

DECORATION = '--------------------------------------'
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_PATH.endswith('_internal'):
	SCRIPT_PATH += '/..'

DUMP_PATH_HINT_FILE = os.path.join(SCRIPT_PATH, 'DDNetDumpPath.txt')
BAD_WORDS_FILE = os.path.join(SCRIPT_PATH, 'DDNetDumpBadWords.txt')

def printHelp():
	print(f'-a | -all\n-i | --include\n-i= | --include=\n-b | --badwords\n\nUsage: "ddsearch <word>"\nOR: "ddsearch",\nwhich would look for a file called \"{BAD_WORDS_FILE}\" that contains bad words separated by lines')

if not os.path.exists(DUMP_PATH_HINT_FILE):
	print(f'Missing "{DUMP_PATH_HINT_FILE}" file')
	leave()

with open(DUMP_PATH_HINT_FILE, 'r', encoding='utf-8') as f:
	path = os.path.expandvars(f.read())
	
	if path == None or not os.path.exists(path):
		print(f'"{path}" does not exist')
		leave()

	files = os.listdir(path)

iterateAllDumps = includeAllOptions = includeBadWords = False
texts: list[str] = []
requiredTexts: list[str] = []
if len(sys.argv) > 1:
	for arg in sys.argv[1:]:
		if arg == '-a' or arg == '--all': # if should iterate through all files
			iterateAllDumps = True

		elif arg == '-i' or arg == '--include': # if should only print lines that has ALL options
			includeAllOptions = True
			includeBadWords = False

		elif arg.startswith('-i=') or arg.startswith('--include='):
			requiredTexts.append(arg.lower().replace('-i=','').replace('--include=',''))
			texts.append(requiredTexts[-1])

		elif arg == '-b' or arg == '--badwords':
			includeBadWords = True

		elif arg == '-h' or arg == '--help':
			printHelp()
			leave()

		else:
			texts.append(arg.lower())

if not iterateAllDumps:
	i = 0
	highestValue = 0.0
	latestModifiedIdx = 0
	for i, file in enumerate(files):
		currentFileModificationTime = os.path.getmtime(os.path.join(path, file))
		if currentFileModificationTime > highestValue:
			highestValue = currentFileModificationTime
			latestModifiedIdx = i
	
	files = [files[latestModifiedIdx]]

if includeBadWords or len(texts) == 0:
	if not os.path.exists(BAD_WORDS_FILE):
		printHelp()
		leave()

	with open(BAD_WORDS_FILE, 'r', encoding='utf-8') as f:
		texts = texts + f.read().split('\n')

results = {}
for text in texts:
	results[text] = 0

for file in files:
	if not file.startswith('remote_console_dump'): continue
	file = os.path.join(path, file)

	with open(file, 'r', encoding='utf-8') as f:
		content = f.read().split('\n')
		for idx, line in enumerate(content):
			line = line.lower()

			shouldSkip = False
			for text in requiredTexts:
				if text not in line:
					shouldSkip = True
					break

			if shouldSkip:
				continue

			for text in texts:
				textIndex = line.find(text)
				if textIndex == -1:
					if includeAllOptions:
						break
					else:
						continue

				print(f'{DECORATION}\nFile: {file}\nLine: {idx+1}')
				cprint(line[:textIndex], "light_green", end='')
				cprint(text, "light_red", end='')
				cprint(line[textIndex+len(text):], "light_green")
				results[text] += 1

output = f'{DECORATION}\nFound:\n'
for text in results:
	if results[text] == 0: continue	

	output += f'\"{text}\"\t\t{results[text]} time(s)\n'

output += DECORATION

print(output)
leave()
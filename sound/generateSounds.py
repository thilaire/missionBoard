# coding=utf-8

"""Script to generate sound
It requires
- the `say` command (with the default dictionary on my Mac, they should exist in GNUstep speech engine)
- `afconvert` (because `say` cannot produce valid wav file; there is a problem in their header, so we use `convert`
to produce valid wav file)

To add a new language, add translated sentences in the dictionaries (in sounds list), and run the script
(the folder `generated/{lang}` should exist)
Configure the sound path in config.py
"""

from subprocess import call
from time import sleep
# languages used for the generation
languages = ['en', 'fr']

# dictionary of voices
voices = {'fr': 'Thomas', 'en': 'Alex'}

# list of sounds to generate (fileName, sentence to pronounce)
# `$` is a silent (replaced by '[[slnc 10]]')
sounds = [
	('phase1', 'phase $ 1'),
	('Initialization', {'fr': 'Initialisation', 'en': 'Initialization'}),
	('phase2', 'phase $ 2'),
	('phase3', 'phase $ 3'),
	('phase1engaged', {'fr': 'Phase $ 1 $engagée', 'en': 'Phase $ 1 $ engaged'}),
	('phase2engaged', {'fr': 'Phase $ 2 $ engagée', 'en': 'Phase $ 2 $ engaged'}),
	('phase3engaged', {'fr': 'Phase $ 3 $ engagée, $$$$ Début du compte à rebours',
                       'en': 'Phase $ 3 $ engaged, $$$$ the countdown starts'}),
	('takeoff', {'fr': 'Décollage!', 'en': 'Takeoff!'})
]
# add the numbers
sounds.extend(list((str(x), str(x)) for x in range(17)))

# iter all the languages
for lang in languages:
	# iter all the sounds
	for name, sentence in sounds:
		# get the translated sentence and insert the silences
		if isinstance(sentence, dict):
			sentence = sentence[lang]
		sentence = sentence.replace('$', '[[slnc 10]]')
		# generate the sound
		# we cannot fully rely on `say` because the wav file output cannot be read by pygame (the wav format is `unexpected`)
		# so we first ccreate a aiff file, and then convert it into a correct wav file
		# Popen(['say', '-v', voices[lang], '"'+sentence+'"', '--data-format=LEI16@22050', '--channels=2', '-o', 'generated/'+lang+'/'+name+'.wav'], stdout=PIPE)
		call(['say', '-v', voices[lang], '"' + sentence + '"', '--channels=2', '-o', 'generated/temp'])
		call(['afconvert', '-f', 'WAVE', '-d', 'LEI16', 'generated/temp.aiff', 'generated/'+lang+'/'+name+'.wav'])
		call(['rm', 'generated/temp.aiff'])

'''
Created on 19 juil. 2017

@author: irac1
'''

from wordGenerator import WordGenerator
import argparse

# main
parser = argparse.ArgumentParser(description="WordGenerator generates random words based on language statistics.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-language", choices=['en', 'fr', 'de', 'it', 'sh', 'dir'], help="dir to use current directory", default="fr")
parser.add_argument("-numberofwords", help="number of words to generate", type=int, default=20)
parser.add_argument("-minwordsize", help="minimum number of letters per word", type=int, default=3)
parser.add_argument("-maxwordsize", help="maximum number of letters per word", type=int, default=100)
parser.add_argument("-firstletter", help="forces words first letter", default="")
parser.add_argument("-algorithm", choices=['duplets', 'triplets'], help="algorithm for letter random selection", default="triplets")
parser.add_argument("-creativity", help="Used only for duplets algorithm. Recommended values 1-10. Lower values are more creative but can generate strange words, higher values are more conservative", type=int, default=4)
parser.add_argument("-rebuild", help="rebuild language probability tables", default=False, action='store_true')
parser.add_argument("-verbose", help="prints additional information", default=False, action='store_true')
argument = parser.parse_args()

languageDirectory = {'en': "English", 'fr': "francais full", 'de': "German", 'it': "Italiano", 'sh': "Shadok", 'dir': "."}
directory = languageDirectory[argument.language]

try:
    wordGenerator = WordGenerator(directory, argument.rebuild, argument.verbose)
    for _ in range(argument.numberofwords):
        print(wordGenerator.createRandomWord(argument.minwordsize, argument.maxwordsize, argument.firstletter, argument.algorithm, argument.creativity))
except ValueError as e:
    print (e)

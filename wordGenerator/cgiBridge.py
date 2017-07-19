#!/usr/bin/python3.6
'''
Created on 19 juil. 2017

@author: irac1
'''
from wordGenerator import WordGenerator

print ("Content-type: text/html\n\n")

print("""<html>
<header><title>Random Word</title></header>
<body>""")

try:
    wordGenerator = WordGenerator("francais full")
    for _ in range(20):
        print(wordGenerator.createRandomWord())
except ValueError as e:
    print (e)


print("""
</body>
</html>""")

import re
string1 = open('text.txt').read()
print (''.join(re.findall('[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]', string1)))
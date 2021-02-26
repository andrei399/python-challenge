from urllib.request import urlopen
import pickle
raw = urlopen("http://www.pythonchallenge.com/pc/def/banner.p").read()
print(raw)

data = pickle.load(urlopen("http://www.pythonchallenge.com/pc/def/banner.p"))
print(data)
for line in data:
    print(''.join([k * v for k,v in line]))
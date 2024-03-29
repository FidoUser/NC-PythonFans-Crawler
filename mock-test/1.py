import requests

try:
    r1 = requests.get('http://i.ua')
except:
    print('except')

# print(r1.text)

from unittest.mock import patch
foo = {'key': 'value'}
original = foo.copy()
with patch.dict(foo, {'newkey': 'newvalue'}, clear=True):
    assert foo == {'newkey': 'newvalue'}

class Container:
    def __init__(self):
        self.values = {}
    def __getitem__(self, name):
        return self.values[name]
    def __setitem__(self, name, value):
        self.values[name] = value
    def __delitem__(self, name):
        del self.values[name]
    def __iter__(self):
        return iter(self.values)

thing = Container()
thing['one'] = 1
with patch.dict(thing, one=2, two=3):
    assert thing['one'] == 2
    assert thing['two'] == 3

assert thing['one'] == 1
assert list(thing) == ['one']
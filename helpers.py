import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))
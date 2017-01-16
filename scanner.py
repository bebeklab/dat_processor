#dat processor
#scanner

from parser import TOKENS

def scan(f):
    
    for line in f:
        possible_token = line[:2]
        attribute = line[5:-1]
        
        if not possible_token in TOKENS: continue
        
        yield (possible_token, attribute)

if __name__ == '__main__':
    scanner = scan(open('uniprot_sprot.dat', 'r'))
    
    for token, attr in scanner:
        if token == 'ID': print '--------\n\n' + attr + '\n--------'
        if token == 'DE': print attr
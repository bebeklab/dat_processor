
TOKENS = ['ID', 'AC', 'GN', 'OX', 'DE', 'DR']

import re
import scanner
from de_modes import DE_FUNCTIONS, MODES

class Node(object):
    
    def __init__(self, token, parsed_attr, children=None):
        self.token = token
        self.attr = parsed_attr
        if children: self.children = children
        else: self.children = list()
    def __str__(self, i=0):
        return ' '*i + '<' + str(self.token) + ', ' + str(self.attr) + '>'

def get_tokens_node(node, token):
    if node.token == token: return node
    
    for child in node.children:
        r = get_tokens_node(child, token)
        if r: return r
    return None
        
def print_nodes(node, level=0):
    print node.__str__(level*4)
    for child in node.children:
        print_nodes(child, level+1)
        
def multi_val_attr(s, current_node, token):
    r = get_tokens_node(current_node, token)
    if r: base_node = r
    else: 
        base_node = Node(token, s)
        current_node.children.append(base_node)
    
    s = s.replace(' ', '')
    l = s.split(';')
    for i in l:
        pair = i.split('=')
        if len(pair) < 2: 
            #print pair
            continue
        name_type = pair[0]
        vals = pair[1].split(',')
        
        for val in vals:
            n = Node(name_type, val)
            base_node.children.append(n)
    
    return current_node

def parse(scanner, mode='uniprot'):
    
    if mode not in MODES: raise Exception, "mode '%s' not valid" % mode
    
    current_node = None
    
    DE = DE_FUNCTIONS[mode]
    
    def ID(s, current_node):
        attr = s.split(' ')[0]
        n = Node('ID', attr)
        
        current_node = n
        return current_node
    
    def AC(s, current_node):
        r = get_tokens_node(current_node, 'AC')
        if r: base_node = r
        else: 
            base_node = Node('AC', s)
            current_node.children.append(base_node)
        
        r = r'[a-zA-Z0-9]+'
        attrs = re.findall(r, s)
        for attr in attrs:
            n = Node(len(base_node.children), attr)
            base_node.children.append(n)
        
        return current_node
        
    def GN(s, current_node):
        return multi_val_attr(s, current_node, 'GN')
    
    def OX(s, current_node):
        #TODO verify that the output is a number
        return multi_val_attr(s, current_node, 'OX')
            
    
    def DR(s, current_node):
        if len(s) >= 9 and s[:9] == 'UniProtKB': 
            token = 'UniProtKB'
            l = s.replace(' ', '').split(';')
            if len(l) >= 2:
                attr = l[1]
                if len(attr) >= 6: attr = attr[:6]
            else: raise Exception, "Syntax Error on line, '%s'" % s
        elif len(s) >= 4 and s[:4] == 'Pfam':
            token = 'Pfam'
            l = s.replace(' ', '').split(';')
            if len(l) >= 2:
                attr = l[1]
            else: raise Exception, "Syntax Error on line, '%s'" % s
        elif len(s) >= 6 and s[:6] == 'RefSeq':
            token = 'RefSeq'
            l = s.replace(' ', '').split(';')
            if len(l) >= 2:
                attr = l[1]
            else: raise Exception, "Syntax Error on line, '%s'" % s
        else:
            return current_node
        
        r = get_tokens_node(current_node, 'DR')
        if r: base_node = r
        else: 
            base_node = Node('DR', s)
            current_node.children.append(base_node)
        
        r = get_tokens_node(current_node, token)
        if r: node = r
        else: 
            node = Node(token, s)
            base_node.children.append(node)
        
        node.children.append(Node(len(node.children), attr))
        return current_node
    
    for token, attr in scanner:
        if token in locals(): cmd = locals()[token]
        else: raise Exception, "bad token '%s'" % token
        
        if cmd == ID and current_node != None: yield current_node
        
        current_node = cmd(attr, current_node)
        #print token
        #print_nodes(current_node)
    yield current_node
    
if __name__ == '__main__':
    #f = open('ipi.MOUSE.short.dat', 'r')
    f = open('uniprot_sprot_short.dat', 'r')
    parser = parse(scanner.scan(f), 'uniprot')
    for n in parser:
        print_nodes(n)
    f.close()
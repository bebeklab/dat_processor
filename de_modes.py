import re
import parser

def uniprot_parser_DE(s, current_node):
    s = s.lstrip().rstrip()
    r = r'(RecName)|(AltName)|(Flags)'
    m = re.match(r, s)
    if m: token = m.group()
    else: token = None
    
    if re.match(r'Contains', s): return current_node
    
    r = parser.get_tokens_node(current_node, 'DE')
    if r: base_node = r
    else: 
        base_node = parser.Node('DE', s)
        current_node.children.append(base_node)
    
    
    if token == None:
        if len(base_node.children) > 0: node = base_node.children[-1]
        else: raise Exception, 'Syntax Error, on line "DE   %s"' % s
    else:
        r = parser.get_tokens_node(base_node, token)
        if r: 
            node = r
        else: 
            node = parser.Node(token, s)
            base_node.children.append(node)
    
    if token: s = s.replace(token, '')[2:]
    s = s[:-1]
    n = parser.Node(str(len(node.children)), s)
    node.children.append(n)
    return current_node

def ipi_parser_DE(s, current_node):    
    r = parser.get_tokens_node(current_node, 'DE')
    if r: base_node = r
    else: 
        base_node = parser.Node('DE', s)
        current_node.children.append(base_node)
    
    n = parser.Node(str(len(base_node.children)), s)
    base_node.children.append(n)
    return current_node
    
def uniprot_get_descriptions(DE_node):
    if not DE_node: return ""
    if len(DE_node.children) == 0: raise Exception, "Parse Error DE node with out descriptions"
    
    l = list()
    
    for child in DE_node.children:
        for grand_child in child.children:
            l.append(grand_child.attr)
    
    return '; '.join(l)
        
def ipi_get_descriptions(DE_node):
    if not DE_node: return ""
    if len(DE_node.children) == 0: raise Exception, "Parse Error DE node with out descriptions"
    
    l = list()
    
    for child in DE_node.children:
        l.append(child.attr.lower())
    
    return ' '.join(l)
    
DE_FUNCTIONS = {'ipi':ipi_parser_DE, 'uniprot':uniprot_parser_DE}
GET_FUNCTIONS = {'ipi':ipi_get_descriptions, 'uniprot':uniprot_get_descriptions}
MODES = ['ipi', 'uniprot']
import scanner, parser, sys
from de_modes import GET_FUNCTIONS, MODES

def get_tokens_node(node, token):
    if not node: return node
    if node.token == token: return node
    
    for child in node.children:
        r = get_tokens_node(child, token)
        if r: return r
    return None
        
def print_nodes(node, level=0):
    print node.__str__(level*4)
    for child in node.children:
        print_nodes(child, level+1)
        
def get_gene_names(GN_node):
    if not GN_node: return ""
    if len(GN_node.children) == 0: raise Exception, "Parse Error GN node with out children"
    
    l = list()
    
    for child in GN_node.children:
        l.append(child.attr)
    
    return '; '.join(l)
    
def get_tax_id(OX_node):
    if not OX_node: return ""
    if len(OX_node.children) == 0: raise Exception, "Parse Error OX node without child"
    
    return OX_node.children[0].attr

def get_pfam(Pfam_node):
    if not Pfam_node: return ""
    if len(Pfam_node.children) == 0: raise Exception, "Parse Error Pfam node without child"
    
    return '; '.join([child.attr for child in Pfam_node.children])

def get_refseq(RefSeq_node):
    if not RefSeq_node: return ""
    if len(RefSeq_node.children) == 0: raise Exception, "Parse Error RefSeq node without child"
    
    return '; '.join([child.attr for child in RefSeq_node.children])

if __name__ == '__main__':
    if len(sys.argv) != 2: raise Exception, \
        "Must supply the dat file type either 'uniprot' or 'ipi'\nex: python code_generator.py uniprot < uniprot_sprot.dat"
    if sys.argv[1] not in MODES: raise Exception, "Dat file type must be either 'uniprot' or 'ipi'"
    
    if sys.argv[1] == 'ipi': 
        from ipi_generator import generate, write_header
    elif sys.argv[1] == 'uniprot':
        from uniprot_generator import generate, write_header
    else:
        raise Exception, "invalid mode '%s' supplied" % mode
    
    write_header(sys.stdout)
    generate(sys.stdout, parser.parse(scanner.scan(sys.stdin), sys.argv[1]))
    sys.stdin.close()

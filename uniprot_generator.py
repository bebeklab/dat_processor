from code_generator import *

def get_descriptions(DE_node):
    if not DE_node: return ""
    if len(DE_node.children) == 0: raise Exception, "Parse Error DE node with out descriptions"
    
    l = list()
    
    for child in DE_node.children:
        for grand_child in child.children:
            l.append(grand_child.attr)
    
    return '; '.join(l)

def write_header(f):
    f.write('\t'.join(["acc", "display_id", "tax_id", "pfam", "gene_name", "refseq", "descriptions\n"]))

def write_line(f, acc, display_id, gene_names, descriptions, tax_id, pfam, refseq):
    f.write('\t'.join([str(acc), str(display_id), str(tax_id), str(pfam), str(gene_names), str(refseq),\
                                    ('"' + str(descriptions) +  '"\n')]))

def generate(out, parse_tree):
    for node in parse_tree:
        AC_node = get_tokens_node(node, 'AC')
        if not AC_node: raise Exception, "Syntax error ID '%s' does not have associated accession number"
        
        for acc in AC_node.children:
            des = get_descriptions(get_tokens_node(node, 'DE'))
            display_id = node.attr
            tax_id = get_tax_id(get_tokens_node(node, 'OX'))
            pfam = get_pfam(get_tokens_node(node, 'Pfam'))
            refseq = get_refseq(get_tokens_node(node, 'RefSeq'))
            GN_node = get_tokens_node(node, 'GN')
            if GN_node:
                for gene in GN_node.children:
                    write_line(out, acc.attr, display_id, gene.attr, des, tax_id, pfam, refseq)
            else:
                write_line(out, acc.attr, display_id, "", des, tax_id, pfam, refseq)
from code_generator import *

def get_descriptions(DE_node):
    if not DE_node: return ""
    if len(DE_node.children) == 0: raise Exception, "Parse Error DE node with out descriptions"
    
    l = list()
    
    for child in DE_node.children:
        l.append(child.attr.lower())
    
    return ' '.join(l)

def write_header(f):
    f.write('\t'.join(["ipi", "ipi_dat_id", "acc", "tax_id", "pfam", "refseq", "descriptions\n"]))

def write_line(f, ipi, ipi_dat_id, acc, descriptions, tax_id, pfam, refseq):
    f.write('\t'.join([str(ipi), str(ipi_dat_id), str(acc), str(tax_id), str(pfam), str(refseq),\
                                         ('"' + str(descriptions) +  '"\n')]))

def generate(out, parse_tree):
    for node in parse_tree:
        AC_node = get_tokens_node(node, 'AC')
        if not AC_node: raise Exception, "Syntax error ID '%s' does not have associated accession number"
        
        for ipi in AC_node.children:
            des = get_descriptions(get_tokens_node(node, 'DE'))
            ipi_dat_id = node.attr
            tax_id = get_tax_id(get_tokens_node(node, 'OX'))
            pfam = get_pfam(get_tokens_node(node, 'Pfam'))
            refseq = get_refseq(get_tokens_node(node, 'RefSeq'))
            UniProtKB_node = get_tokens_node(node, 'UniProtKB')
            if UniProtKB_node:
                for acc in UniProtKB_node.children:
                    write_line(out, ipi.attr, ipi_dat_id, acc.attr, des, tax_id, pfam, refseq)
            else:
                write_line(out, ipi.attr, ipi_dat_id, "", des, tax_id, pfam, refseq)
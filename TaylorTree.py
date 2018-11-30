

def d_single_f_term(ft):

	""" return dts and dys lists for single fterm """

	dt = [  ft[:] + ['t'] ]
	dy = [ ft[:] + ['y'], [] ] # ex: [[t,y,new_y], []] where this represents: ftyy*f

	return dt, dy


def d_product(term):

	# for each f term in terms (connected by multiplication)
	# apply d_single_f_term, replace index, and add list of terms to term list to return

	# product rule
	n = len(term) # number of f multipliers in term
	dt_terms, dy_terms = [], [] #[term[:]]*n, [term[:]]*n
	#print(term)
	for f in range(n):

		dt_pop, dy_pop = term[:], term[:]
		del dt_pop[f]
		del dy_pop[f]
		
		dti, dyi = d_single_f_term(term[f])
		dt_terms += [ dti + dt_pop ]
		dy_terms += [ dyi + dy_pop ]

	return dt_terms, dy_terms


def d_terms(terms):

	# differentiate all terms

	dt_terms, dy_terms = [], []

	for term in terms:
		dt_terms_i, dy_terms_i = d_product(term)

		dt_terms += dt_terms_i
		dy_terms += dy_terms_i

	return dt_terms, dy_terms

from sympy import *
init_printing()

def get_f_sympy(f_list_rep):

	f = Function("f")
	t,y = symbols("t,y")


	if len(f_list_rep) > 0:


		sorted_partials = sorted(f_list_rep)

		partial_symbols = [symbols(str(partial)) for partial in sorted_partials]

		return Derivative(f(t,y), *partial_symbols)

	else: 
		return f(t,y)



def get_term_sympy(term):

	term_sympy = 1
	for f in term:
		term_sympy =  term_sympy*get_f_sympy(f)
	return term_sympy


def get_f_string(f):

	if len(f) > 0:
		f_str = 'f_{'

		sorted_partials = sorted(f)
		for partial in sorted_partials:
			f_str += partial

		return f_str + '}'

	else: 
		return 'f'

def get_term_string(term):
	term_str = ''

	for f in term:
		term_str += get_f_string(f)

	return term_str

def get_terms_sympy(terms_list):
    
    expression = 0
    for term in terms_list:
        expression += get_term_sympy(term)
        
    return expression


class Node: 

    def __init__(self, terms_list, delta_t, delta_y, multiplier=1): 
        self.terms_list = terms_list
        self.delta_t, self.delta_y = delta_t, delta_y
        self.multiplier = multiplier

        # node children
        self.dt_terms_node = None
        self.dy_terms_node = None
        
        self.sympy_rep = get_terms_sympy(self.terms_list)
        
    def expand_terms(self, delta_t, delta_y):
        
        dt_terms, dy_terms = d_terms(self.terms_list)
        self.dt_terms_node, self.dy_terms_node = Node(dt_terms,delta_t, delta_y),  Node(dy_terms,delta_t, delta_y)
        
        # apply multipliers
        self.dt_terms_node.apply_multiplier(delta_t*self.multiplier)
        self.dy_terms_node.apply_multiplier(delta_y*self.multiplier)
        
    def apply_multiplier(self, delta):
        self.multiplier = delta
        self.sympy_rep = self.sympy_rep*self.multiplier

        
def add_order(node, delta_t, delta_y):
    
    # if leaf node found, expand leaf node
    if node.dt_terms_node is None or node.dy_terms_node is None:
        node.expand_terms(delta_t, delta_y)
        
        print(node.sympy_rep)
        
    else:
        add_order(node.dt_terms_node, delta_t, delta_y)
        add_order(node.dy_terms_node, delta_t, delta_y)
        

def get_combined_terms_list(node):
    if node is not None: 

        if ( node.dt_terms_node is None and node.dy_terms_node is None ): 
            return node.terms_list

        else: 
            return node.terms_list + get_combined_terms_list(node.dt_terms_node) + get_combined_terms_list(node.dy_terms_node)

def get_combined_sympy(node):
    if node is not None: 

        if ( node.dt_terms_node is None and node.dy_terms_node is None ): 
            return node.sympy_rep
        else: 
            return node.sympy_rep + get_combined_sympy(node.dt_terms_node) + get_combined_sympy(node.dy_terms_node)
    
def get_taylor_tree_sympy(root):
    
    #terms_list = get_combined_terms_list(root)
    #get_terms_sympy(terms_list)
    
    return get_combined_sympy(root) 

class TaylorTree:
    
    def __init__(self, order, delta_t=0, delta_y=0):
        
        self.delta_t, self.delta_y = delta_t, delta_y
        self.root = Node([[[]]], self.delta_t, self.delta_y)
        
        # depth of tree is == to the order passed
        for ol in range(order):
            add_order(self.root, self.delta_t, self.delta_y)
            
            
    
    def get_sympy(self):
        
        return expand(get_taylor_tree_sympy(self.root))
        

delta_t, delta_y = symbols('Delta_t, Delta_y')

tt = TaylorTree(2, delta_t, delta_y)

tt.get_sympy()




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


terms_o0 = [[[]]]

dt_terms, dy_terms = d_terms(terms_o0)
terms_o1 = dt_terms + dy_terms

dt_terms, dy_terms = d_terms(terms_o1)
terms_o2 = dt_terms + dy_terms

terms_list = terms_o0 + terms_o1 + terms_o2


get_terms_sympy(terms_list)

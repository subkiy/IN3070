from itertools import product, combinations
import numpy as np


def generate_clauses1(n):
    #generates all 2^n possible clauses form n propositional atoms, it is either 1 (positive) or -1 (negation)
    literals = list(range(1, n + 1))
    variants = product([1, -1], repeat=n)
    clauses = []

    for combo in variants:
        clause = []
        for literal, sign in zip(literals, combo):
            product_val = literal * sign
            clause.append(product_val) 
        clauses.append(clause)

    return clauses

def generate_clauses_minus_one(n):
    # takes 2^n clauses and subtracts one clause
    clauses = generate_clauses1(n)
    if (len(clauses) > 0):
        removed = clauses[0] 
        del clauses[0]
    else:
        None
    return clauses


def negation(literal):
    return -literal

def resolvent(a, b):
    # refutation procedure, two clauses a and b where a is in L and b is in the complement of L
    # where resolvents.add(frozenset(left.union(right))) is the parent of a and b.
    resolvents = set()
    for literal in a:
        negative = negation(literal)
        if (negative in b):
            left = set(a)
            right = set(b)
            left.discard(literal)
            right.discard(negative)
            resolvents.add(frozenset(left.union(right))) 
    return resolvents

def resolution(clauses):
    # the resolution procedure
    clauses = set(frozenset(c) for c in clauses)
    new = set()

    while True:
        pairs = combinations(clauses, 2)
        for (a, b) in pairs:
            resolvents = resolvent(a, b)
            if frozenset() in resolvents:
                return (False, "Empty - UNSAT")
            new = new.union(resolvents)

        if new.issubset(clauses):
            return (True, "SAT.")

        clauses = clauses.union(new)


def model(clause_r, n):
    #truth assigment
    model = {}
    for literal in clause_r:
        var = abs(literal)
        model[var] = 0 > literal  
    
    for var in range(1, n + 1):
        if var not in model:
            model[var] = False
            
    return model

if __name__ == "__main__":
    n = 3

    clauses_full = generate_clauses1(n)
    assert len(clauses_full) == 2**n, "not 2^n"
    sat_full, _ = resolution(clauses_full)
    print("2^n:", "SATISFIABLE" if sat_full else "UNSATISFIABLE")


    clauses_minus_one = generate_clauses_minus_one(n)
    assert len(clauses_minus_one) == (2**n - 1), "not 2^n - 1"
    sat_m, _ = resolution(clauses_minus_one)
    print("2^n-1:", "SATISFIABLE" if sat_m else "UNSATISFIABLE")

    # model for 2^n-1
    if sat_m:
        clause_r = []
        for i in range(1, n + 1):
            clause_r.append(i) 
        m = model(clause_r, n)
        print("model that satisfies:", m)


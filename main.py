import sys
def parse_dimacs(input_file):
	# Read input file
	with open(input_file, "r") as file:
		lines = file.readlines()
		for line in lines:
			if line[0] == 'p':
				parts = line.split()
				num_vars = int(parts[2])
				num_clauses = int(parts[3])
				break
		print(f"Num of vars: {num_vars}\nNum of clauses: {num_clauses}")
		i=0
		for i in range(0,len(lines)):
			if lines[i][0] == 'p':
				break
		i+=1
		############
		clauses=[]
		############
		for clause in lines[i:]:
			clause=clause.strip().split()
			if(clause):
				clause_literals=list(map(int,clause[:-1]))
				clauses.append(clause_literals)
		return clauses, num_vars, num_clauses
def unit_propagate(clauses, assignment):
	while True:
		# extract all unit clauses
		unit_clauses = [c for c in clauses if len(c) == 1]
		# if there are no unit clauses left, return
		if not unit_clauses:
			break
		# get the first unit clause
		unit = unit_clauses[0][0]
		# add the unit to the assignment because it must be true
		assignment.add(unit)
		# remove all clauses that contain the unit because they are satisfied
		clauses = [c for c in clauses if unit not in c]
		# remove all instances of -unit from all clauses
		for i, clause in enumerate(clauses):
			clauses[i] = [l for l in clause if l != -unit]
	return clauses, assignment
def dpll(clauses, assignment):
    # Apply unit propagation
    clauses, assignment = unit_propagate(clauses, assignment)

    # If there are no clauses left, the formula is satisfied
    if not clauses:
        return True, assignment

    # If any clause is empty, the formula is unsatisfiable because we removed all literals before removing the clause
    if any(len(c) == 0 for c in clauses):
        return False, set()
	# Choose the first literal
    literal = clauses[0][0]
	# Create a new assignment with the literal
    new_assignment = assignment.copy()
    new_assignment.add(literal)
	# Remove all clauses where the literal is located
    new_clauses = [c for c in clauses if literal not in c]
	# Remove all instances of -literal from all clauses
    new_clauses = [[l for l in clause if l != -literal] for clause in new_clauses]
	# Recursively call DPLL
    satisfiable, new_assignment = dpll(new_clauses, new_assignment)

    if satisfiable:
        return True, new_assignment
    # Same as above but with the negation of the literal
    new_assignment = assignment.copy()
    new_assignment.add(-literal)
    new_clauses = [c for c in clauses if -literal not in c]
    new_clauses = [[l for l in clause if l != literal] for clause in new_clauses]

    return dpll(new_clauses, new_assignment)


def main(input_file, output_file):
    clauses, num_vars, num_clauses = parse_dimacs(input_file)
    assignment = set()
    satisfiable, assignment = dpll(clauses, assignment)
    print(f"{satisfiable}\n{assignment}")


    all_literals = set(range(1, num_vars + 1))
    assigned_literals = set(abs(l) for l in assignment)
    unassigned_literals = all_literals - assigned_literals

    for literal in unassigned_literals:
        assignment.add(literal)

    with open(output_file, "w") as file:
        if satisfiable:
            file.write("s SATISFIABLE\n")
            file.write("v ")
            file.write(" ".join(str(l) for l in sorted(assignment)))
        else:
            file.write("s UNSATISFIABLE")
        file.write("\n")


if __name__ == "__main__":
	if(len(sys.argv) != 3):
		print("Usage: python3 main.py [input_file] [output_file]")
		sys.exit(1)
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	main(input_file, output_file)
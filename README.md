# SAT Solver with DPLL and Unit Propagation

This project implements a simple CNF SAT solver using DPLL with Unit Propagation.

## How to Run It:
- Ensure Python 3.x is installed.
- Run `make build` (This currently does nothing).
- Run `make run INPUT=x OUTPUT=x`.

## Input Format:
- The input should be in DIMACS format.
- The line containing the formula should start with "p".
- Clauses should end with `0\n`.

### Example:
```
p cnf 1 1
-1 0
```
This means 1 clause, 1 literal which is negated.

## The Essence of the Code:
First, we read all the clauses and parse them into a format that is easy to use in our DPLL with Unit Propagation. In each DPLL call, we perform unit propagation to simplify the formula. If we encounter empty clauses, it signifies a contradiction. For example, in the clauses `(!x1)`, `(x2)`, and `(x1 or !x2)`, we remove the `!x1` clause in unit propagation and also remove its negation from all clauses because it won't be satisfied. We then remain with `(x2)` and `(!x2)`. Performing another iteration and removing the `x2` clause leaves us with `()`, an empty clause, signifying a contradiction, so the formula is UNSAT. This is the core idea of our unit propagation algorithm: remove all clauses containing only one literal while you can, to simplify the formula.

Returning to DPLL, after the first unit propagation, we have our simplified formula. If it's empty, then it's satisfiable. If not, we take a random literal (in our case, the first literal from the first clause) and perform DPLL on the new formula where all clauses containing the literal are removed and all negated instances are removed from clauses. We then perform the same action with the negated value. This creates a recursion that allows for backtracking. Whenever a choice results in UNSAT, we try the other choice and go back and forth until all possibilities are checked.

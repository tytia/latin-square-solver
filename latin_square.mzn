include "alldifferent.mzn";

int: n;
array [1..n, 1..n] of var 1..n: square;

constraint forall(i in 1..n)(alldifferent(square[i, 1..n]));
constraint forall(j in 1..n)(alldifferent(square[1..n, j]));

solve satisfy;

output ["\(square[i, j])" ++
       if j == n then "\n" else " " endif | i, j in 1..n];
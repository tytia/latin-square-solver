from latin_square_v1 import solve
from latin_square_v2 import solve as improved_solve
from timeit import timeit

if __name__ == "__main__":
    n = int(input("n: "))
    print(f"v1: Finsihed in {timeit('solve(n)', globals=globals(), number=5) / 5}s.")
    print(f"v2: Finished in {timeit('improved_solve(n)', globals=globals(), number=5) / 5}s.")
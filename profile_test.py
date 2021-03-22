"""
Implement two algorithms which demonstrably reach the same conclusion and 
use profile or cProfile to time them both.

Non-recursion vs. recursion
"""

import cProfile, pstats
import resource

"""
OPTION 1:

Write a non-recursive and recursive method to calculate an exponent.
"""
# @profile
def calc_exp_nonrec(base, power):
    if (power <= 0):
        return 1
    else:
        total = 1
        for i in range(power):
            total *= base
        return total

# @profile
def calc_exp_rec(base, power):
    if (power <= 0):
        return 1
    else:
        return base * calc_exp_rec(base, power - 1)


"""
OPTION 2:

Write a non-recursive and recursive method to calculate the greatest common 
denominator (gcd) of two numbers. The recursive method could use Euclidean
algorithm or the following algorithm:

If y divides x evenly, then the gcd is y. Otherwise, the gcd of x and y is 
the gcd of y and the remainder of x divided by y.

Example: x = 49, y = 28

28 does not evenly divide 49, so the gcd is the gcd of 28 and 21 
(21 = the remainder when 28 is divided by 49)

21 does not evenly divide 28, so the gcd is the gcd of 21 and 7 
(7 = the remainder when 21 is divided by 7)

7 does evenly divide 21, so the gcd is 7
"""

def calc_gcd_nonrec(num1, num2):
    small = num2 if (num1 > num2) else num1

    # Using for loop
    for i in range(1, small + 1):
        if ((num1 % i == 0) and (num2 % i == 0)):
            gcd = i

    # List comprehension with conditional for loop creates a generator that
    # would need to be unpacked to get to last item for gcd
    # *_, gcd = (i for i in range(1, small + 1) if ((num1 % i == 0) and (num2 % i == 0)))

    return gcd

def calc_gcd_rec(num1, num2):
    if (num1 % num2 == 0):
        return num2
    else:
        return calc_gcd_rec(num2, num1 - num2)
    

"""
OPTION 3:

A person can run up a staircase with n steps. The person can hope either 1 
step, 2 steps, or 3 steps at a time.

For climbing n steps, you can either start with a 1-hop, a 2-hop, or a 3-hop,
so there are three possible cases (which corresponds to our three base cases).

If you start with a 1-hop, there are n-1 steps left to go and you know that
the answer to how many steps that takes is count_steps(n-1). Similarly, if you 
start with a 2-hop, there are n-2 steps left to go and you know that the 
answer to how many steps that takes is count_steps(n-2). Same for if you start 
with a 3-hop, so these are the three possibilities - add them up and that 
makes all choices!

Write a non-recursive and recursive method to count how many possible ways 
the person can run up the stairs.
"""

def count_steps_nonrec(steps):
    # Create array with size n + 1 and initialize first 4 variables with base
    # cases
    arr = [0] * (steps + 2)
    arr[0] = 1
    arr[1] = 1
    arr[2] = 2
    arr[3] = 4          # 4 -> 3-hop; 1-hop + 2-hop; 2-hop + 1-hop; 1-hop + 1-hop + 1-hop    

    for i in range(3, steps + 1):
        arr[i] = arr[i - 1] + arr[i - 2] + arr[i - 3]

    return arr[steps]

def count_steps_rec(steps):
    if (steps <= 1):
        return 1
    elif (steps == 2):
        return 2
    elif (steps == 3):
        return 4         # 4 -> 3-hop; 1-hop + 2-hop; 2-hop + 1-hop; 1-hop + 1-hop + 1-hop
    else:
        return (count_steps_rec(steps - 1) + count_steps_rec(steps - 2) + 
        count_steps_rec(steps - 3))
    

def compare():
    # Note that these result in recursion error for it maxing out depths of 
    # recursion as amounts get higher.

    # OPTION 1:
    print(calc_exp_nonrec(7, 500))
    print(calc_exp_rec(7, 500))

    # OPTION 2:
    print(calc_gcd_nonrec(49, 28))
    print(calc_gcd_rec(49, 28))

    # OPTION 3:
    print(count_steps_nonrec(22))
    print(count_steps_rec(22))


if __name__ == '__main__':

    profiler = cProfile.Profile()
    profiler.enable()
    compare()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()
    print("Memory: " + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))

"""
354013649449525931426279442990642053580432370765307807128294998551122640747634597271084333393795330500587164243140988540373888581863590044622404991728906599366400005917176740377601943975293629949119408598903469298568197261263089787497027712508751288114794103433426230872340717070631044534195535930764662142517697871788941015702182840766509295270854651459881610586893475184126853183587780497947092464128387019611820640300001
354013649449525931426279442990642053580432370765307807128294998551122640747634597271084333393795330500587164243140988540373888581863590044622404991728906599366400005917176740377601943975293629949119408598903469298568197261263089787497027712508751288114794103433426230872340717070631044534195535930764662142517697871788941015702182840766509295270854651459881610586893475184126853183587780497947092464128387019611820640300001
7
7
410744
410744
         236472 function calls (14 primitive calls) in 0.093 seconds

   Ordered by: internal time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
 235957/1    0.093    0.000    0.093    0.093 profile_test.py:110(count_steps_rec)
    501/1    0.001    0.000    0.001    0.001 profile_test.py:27(calc_exp_rec)
        6    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 profile_test.py:17(calc_exp_nonrec)
        1    0.000    0.000    0.093    0.093 profile_test.py:122(compare)
        1    0.000    0.000    0.000    0.000 profile_test.py:96(count_steps_nonrec)
        1    0.000    0.000    0.000    0.000 profile_test.py:55(calc_gcd_nonrec)
      3/1    0.000    0.000    0.000    0.000 profile_test.py:69(calc_gcd_rec)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


Memory: 9812

=> Recursion takes more time and memory, and for higher amounts in parameters, results
in recursion error due to the maximum limit reached.
"""
# Symbolic Regression Using Genetic Programming

## Indroduction

### Packages
*Runs seamlessly using these versions as of October 21, 2026.*

* python 3.13
* matplotlib 3.11.2
* numpy 2.5.4

### Experiment
The experiment consists of running a symbolic regression algorithm using genetic programming on two datasets. The goal is to evolve mathematical expressions that best fit the data points in each dataset.

The first dataset contains a simple polynomial relationship, with a single variable $x$ and a corresponding value $y$.

The second dataset is more complex, containing three input variables $x_1$, $x_2$, and $x_3$, with a corresponding value $y$ that is a function of these three variables.

## Results

### Dataset 1 Results

**Discovered Function:**

$$
\boxed{f(x) = x^2 - 6x + 14}
$$

**Loss Over Generations**

The following graph shows how the loss changes over successive generations of the genetic programming algorithm.

![Dataset 1 Loss Over Generations](images/Dataset%201%20Loss%20Graph.png)

**Dataset Points vs. Discovered Function**

The following graph compares the original dataset points with the curve produced by the discovered function.

![Dataset 1 Points and Discovered Function](images/Dataset1%20Graph.png)

### Dataset 2 Results

**Discovered Function:**

$$
\boxed{f(x_1, x_2, x_3) = 6.6 \times 10^{-11} \cdot \frac{x_1 x_2}{x_3^2}}
$$

**Loss Over Generations — 10 Independent Runs**

The following graph displays the loss across generations for 10 independent runs of the genetic programming algorithm, illustrating the convergence behavior and consistency of the results.

![Dataset 2 Loss Over 10 Runs](images/Dataset%202%20Loss%20Graph.png)


## References

De Myttenaere, Arnaud, Boris Golden, Bénédicte Le Grand, and Fabrice Rossi. “Mean Absolute Percentage Error for Regression Models.” *Neurocomputing* 192 (2016): 38–48. https://doi.org/10.1016/j.neucom.2015.12.114.

Goldberg, David E., and Kalyanmoy Deb. “A Comparative Analysis of Selection Schemes Used in Genetic Algorithms.” In *Foundations of Genetic Algorithms*, vol. 1, 69–93. Elsevier, 1991. https://doi.org/10.1016/B978-0-08-050684-5.50008-2.

Koza, John R. “Example of a Run of Genetic Programming (Symbolic Regression of a Quadratic Polynomial).” *Genetic Programming*. Accessed October 21, 2026. https://www.genetic-programming.com/gpquadraticexample.html.

Miller, Brad L., and David E. Goldberg. “Genetic Algorithms, Tournament Selection, and the Effects of Noise.” *Complex Systems* 9, no. 3 (1995): 193–212. https://www.complex-systems.com/abstracts/v09_i03_a02/.

Poli, Riccardo, Nicholas Freitag McPhee, and Leonardo Vanneschi. “Elitism Reduces Bloat in Genetic Programming.” In *Proceedings of the 10th Annual Conference on Genetic and Evolutionary Computation (GECCO '08)*, 1343–44. New York: Association for Computing Machinery, 2008. https://doi.org/10.1145/1389095.1389355.


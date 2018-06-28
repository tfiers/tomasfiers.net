---
title: "Probabilistic programming in Python: Pyro versus PyMC3"
date: 2018-06-28T16:45:16+02:00
---


## Part 1: Goals

First, let's make sure we're on the same page on what we want to do. PyMC3,
Pyro, and other probabilistic programming packages such as Stan, Edward, and
BUGS, perform *'approximate inference'*.

_Inference_ is using a probability distribution. For example, you want to:
- Do a 'lookup' in the probabilty distribution, i.e. calculate how likely a
  given set of data is;
- Marginalise (= summate) the joint probability distribution over the variables
  you're not interested in, so you can make a nice 1D or 2D plot of the
  resulting distribution;
- Combine marginalisation and lookup to answer conditional questions: given the
  value for this variable, how likely is the value of some other variable?
- Find the most likely set of data for this distribution, i.e. calculate the
  mode, AKA `argmax`. (This can be used in Bayesian learning of a parametric
  model. The probability distribution in question is then a probability
  distribution over parameters. You can then answer: given the data, what are
  the most likely parameters of the model?)

We have to resort to _approximate_ inference when we do not have closed,
analytical formulas for the above calculations. Apparently this is often the
case in practice.

There are generally two approaches to approximate inference:
1. Sampling
2. Variational inference

In *sampling*, you use a method (called a Monte Carlo method) that draws samples
from the probability distribution that you are performing inference on -- or at
least from a good approximation to it. You then perform your desired inference
calculation on the samples. For example: mode of the probability distribution?
--> Just find the most common sample. One class of sampling methods are the
Markov Chain Monte Carlo (MCMC) methods, of which Hamiltonian/Hybrid Monte Carlo
(HMC) and No-U-Turn Sampling (NUTS) are refinements.

*Variational inference* (VI) is an approach to approximate inference that does
not need samples. In my limited understanding, it transforms the inference
problem into an optimisation problem, where we need to maximise some target
function.

The optimisation procedure in VI (which is gradient descent, or a second order
derivative method) requires derivatives of this target function. This is where
*automatic differentiation* (AD) comes in.  AD can calculate accurate values for
the derivatives of a function that is specified by a computer program. You can
thus use VI even when you don't have explicit formulas for your derivatives.

Both AD and VI, and their combination, ADVI, have recently become popular in
machine learning.


Further reading:
- VI: http://www.nowpublishers.com/article/Details/MAL-001
- AD (short, recommended read): https://justindomke.wordpress.com/2009/02/17/automatic-differentiation-the-most-criminally-underused-tool-in-the-potential-machine-learning-toolbox/
- ADVI:  http://www.jmlr.org/papers/v18/16-107.html



## Part 2: Backends

Now over from theory to practice. There seem to be three main, pure-Python
libraries for performing approximate inference: PyMC3 (http://docs.pymc.io),
Pyro (https://eng.uber.com/pyro), and Edward (http://edwardlib.org) . They all
use a 'backend' library that does the heavy lifting of their computations. PyMC3
uses _Theano_, Pyro uses _PyTorch_, and Edward uses _TensorFlow_.

Theano, PyTorch, and TensorFlow are all very similar. They all expose a Python
API to underlying C / C++ / Cuda code that performs efficient numeric
computations on ndarrays (scalars, vectors, matrices, or in general: "tensors").
The computations can optionally be performed on a GPU instead of the CPU, for
even more efficiency. In this respect, these three frameworks do the same thing
as NumPy.

Additionally however, they also offer automatic differentiation (which they
often call "autograd"):

They expose a whole library of functions on tensors, that you can compose with
`+`, `-`, `*`, `/`, tensor concatenation, etc. The result is called a
_computational graph_. This computational graph is your 'function', or your
model. For example:

```
def model(x,y):
   s = framework.sin(x)
   m = 3 * framework.max(x, 6*y)
   return s + m
```

Such computational graphs can be used to build (generalised) linear models,
logistic models, neural network models, … almost any model really. In plain
Theano, PyTorch, and TensorFlow, the parameters are just tensors of actual
numbers. For example, `x = framework.tensor([5.4, 8.1, 7.7])`. In the extensions
PyMC3, Pyro, and Edward, the parameters can also be stochastic variables, that
you have to give a unique name, and that represent probability distributions.
That is why, for these libraries, the computational graph is a probabilistic
model.

*The automatic differentiation part of the Theano, PyTorch, or TensorFlow
frameworks can now compute exact derivatives of the output of your function with
respect to its parameters* (`x` and `y` in the example).

As an aside, this is why these three frameworks are (foremost) used for
specifying and fitting neural network models ("deep learning"): the main
innovation that made fitting large neural networks feasible, _backpropagation_,
is nothing more or less than automatic differentiation (specifically: first
order, reverse mode automatic differentiation).

The three "NumPy + AD" frameworks are thus very similar, but they also have
individual characteristics:

Theano (http://deeplearning.net/software/theano): the original framework. Sadly,
the creators announced that they will stop development.

PyTorch (http://pytorch.org/about): using this one feels most like 'normal'
Python development, according to their marketing and to their design goals. In
my experience, this is true. In Theano and TensorFlow, you build a (static)
computational graph as above, and then 'compile' it. In PyTorch, there is no
separate compilation step. Commands are executed immediately. (If you execute `a
= sqrt(16)`, then `a` will contain `4` [1]. Not so in Theano or TensorFlow).
This means that debugging is easier: you can for example insert `print`
statements in the `def model` example above. This is not possible in the other
two frameworks. It also means that models can be more expressive: PyTorch can
auto-differentiate functions that contain plain Python loops, `if`s, and
function calls (including recursion and closures). Also, like Theano but unlike
TensorFlow, PyTorch tries to make its tensor API as similar to NumPy's as
possible.

TensorFlow (https://www.tensorflow.org): the most famous one. Apparently has a
clunky API. The developers are adding immediate execution / dynamic
computational graphs in the style of PyTorch
(https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/eager/README.md).


[1] This is pseudocode. Real PyTorch code:
```
import torch
a = torch.sqrt(torch.Tensor([16]))
print(a)
```
Output:
 ```
 4
[torch.FloatTensor of size 1]
```



## Part 3: Showdown

With this backround, we can finally discuss the differences between PyMC3, Pyro
and other probabilistic programming packages.

*PyMC3* has an extended history. Therefore there is a lot of good documentation
and content on it. It started out with just approximation by sampling, hence the
'MC' in its name. By now, it also supports variational inference, with automatic
differentiation (ADVI). For MCMC sampling, it offers the NUTS algorithm. NUTS is
easy for the end user: no manual tuning of sampling parameters is needed.

*Pyro* came out just this November (2017). Not much documentation yet. It was
built with large scale ADVI problems in mind. It has indeed no functionality for
approximate inference by sampling (although they are working on it:
https://github.com/uber/pyro/pull/690).

*Edward* is also relatively new (Februari 2016). It offers both approximate
inference by sampling and variational inference. I don't know much about it,
other than that its documentation has style. For MCMC, it has the HMC algorithm
(in which sampling parameters are not automatically updated, but should rather
be carefully set by the user), but not the NUTS algorithm.

Also a mention for probably the most used probabilistic programming language of
all (which is not pure Python): *Stan* (http://mc-stan.org). It also offers both
sampling (HMC and NUTS) and variatonal inference. It has bindings for different
languages, including Python. Models are not specified in Python, but in some
specific Stan syntax.


Discussion:

The depreciation of its dependency Theano might be a disadvantage for PyMC3 in
the long term. It doesn't really matter right now. Here the PyMC3 devs discuss a
possbile new backend: https://discourse.pymc.io/t/pytorch-backend-for-pymc4/61.
The relatively large amount of learning resources on PyMC3 and the maturity of
the framework are obvious advantages.

The advantage of Pyro is the expressiveness and debuggability of the underlying
PyTorch framework. So if I want to build a complex model, I would use Pyro. I
find the comment by joh4n, who implemented NUTS in PyTorch without much effort
telling (https://discourse.pymc.io/t/pytorch-backend-for-pymc4/61/15). The
immaturity of Pyro is a rather big disadvantage at the moment.

As to when you should use sampling and when variational inference: I don't have
enough experience with approximate inference to make claims; from this
StackExchange answer (https://stats.stackexchange.com/a/271862/191343) however:

> Thus, variational inference is suited to large data sets and scenarios where
> we want to quickly explore many models; MCMC is suited to smaller data sets
> and scenarios where we happily pay a heavier computational cost for more
> precise samples. For example, we might use MCMC in a setting where we spent 20
> years collecting a small but expensive data set, where we are confident that
> our model is appropriate, and where we require precise inferences. We might
> use variational inference when fitting a probabilistic model of text to one
> billion text documents and where the inferences will be used to serve search
> results to a large population of users. In this scenario, we can use
> distributed computation and stochastic optimization to scale and speed up
> inference, and we can easily explore many different models of the data.

I think VI can also be very useful for 'small data', when you want to fit a
model with many parameters / hidden variables (and of course a good regulariser
in that case). I.e. you are not sure what a good model would be. (The final
model that you find can then be described in simpler terms).


So the conclusion seems to be: the classics PyMC3 and Stan still come out as the
winners at the moment -- unless you want to experiment with fancy probabilistic
models.

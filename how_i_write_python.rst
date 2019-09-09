====================
 How I write Python
====================

:AUTHOR: Jason Yamada-Hanff
:DATE: 2019-09-07

This is my current set of tools and practices for developing Python. The idea is that you can start from here, instead of starting on your own and relearning everything from scratch.

Some of the topics covered are:

  * Keeping isolated environments, with virtual environments
  * Tooling to help check obvious errors, take care of formatting, etc
  * Avoiding common pitfalls
  * Organizing and distributing code
  * Testing code
  * Debugging
  * Perfomance profiling and benchmarking

One nice thing about Python--perhaps the nicest thing--is that the barrier to entry is very low. If you already know a little programming, you can make something useful in Python within a day or so.

However, like any other tool, learning how to make *good* use of Python takes time. In particular, most tutorials will not teach you much about building a productive Python development and deployment environment.

Here's how I do it. I don't claim that this is the best possible approach, and I definitely don't insist that you exactly copy my environment and tools. But it will get you started and it will hopefully solve some problems for you. And when there is some practice or tool that I think *marks* what it means to do responsible, professional Python development, you'll hear about it.


Where I'm coming from
=====================

Python is a practical and popular tool, and it's been my primary language for a few years now. But I am not in love with it. I see its strengths, but I am also very familiar with its weaknesses relative to other languages. Hopefully, my ambivalence here makes me more credible and more helpful about what makes for a good Python environment.

What is wrong with Python? Other languages provide features that are
critically missing in Python: a powerful type system, (good)
functional programming support, language-standard packaging tools,
less reliance on object-orientation, and high performance.


Tools
=====

Tier 1 (Core)
-------------

Here are the tools I think you cannot live without to program in Python. You will have to be at least familiar with each of these:

`Python 3`_
  of course. CPython, in particular. (Python 2 `is dead <https://pythonclock.org/>`_. Do not use it anymore.)

pip_
  for package management

virtualenv_
  for isolated environments, comes standard as ``python -m venv`` of Python 3.5

setuptools_
  for packaging your code

ipython_
  for interactive programming (REPL)


For the most part, these are chosen because they are *standard tools* in the larger Python community. There are alternatives for each of these, but they are not nearly as common. Feel free to explore alternatives, but only after getting familiar with these.

Tier 2 (Python Extras)
----------------------

These are Python-specific tools that are very popular and widely used. That's for a reason. They help you keep clean environments and support code quality. You *can* live without these... but you shouldn't!

pyenv_
  for python version management

pytest_
  for automated testing

tox_
  for testing builds in an isolated way

black_
  for formatting. Never think about formatting again.

flake8_

pylint_

pipx_


Tier 3 (Non-python tools)
-------------------------

These are general tools that are not Python-specific, but will be important to your Python workflow.

a good code editor
  for me, emacs_. for you, maybe PyCharm_ or `Visual Studio Code`_. My editor setup helps me with autocompletion, virtualenv support, automatic linting and formatting, and source control. If yours doesn't do this, work on your setup until it does or find a new one. You work in your editor all day, so you get paid back the time you put in to making your editor help you.

git_
  for source control. You need to learn it.


.. _`python 3`: https://www.python.org/
.. _ipython: https://ipython.org/
.. _pip: https://pip.pypa.io
.. _pyenv`: https://github.com/pyenv/pyenv
.. _setuptools: https://setuptools.readthedocs.io/en/latest/
.. _emacs: https://www.gnu.org/software/emacs/
.. _tox: https://tox.readthedocs.io/en/latest/index.html
.. _black: https://black.readthedocs.io/en/stable/
.. _pre-commit: https://pre-commit.com/
.. _git: https://git-scm.com/
.. _pipx: https://github.com/pipxproject/pipx
.. _PyCharm: https://www.jetbrains.com/pycharm/
.. _`Visual Studio Code`: https://code.visualstudio.com/

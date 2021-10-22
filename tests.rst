
Thinking about tests
====================

Step 1. Identify the domain
---------------------------

Start by thinking of your system under test (SUT) as a function. In math, functions have a:

* **domain** -- valid space of input values
* **range/codomain** -- valid space of output values

Your job is then to choose inputs so that you cover the domain with tests. That makes you confident that the function performs as expected across the whole domain.

Step 2. Cover the domain
------------------------

What does "cover the domain" mean?

If the domain is small and finite, then test all of it. For instance, if the only valid input is an enumeration or a boolean, then every valid value is known.

More often, the domain is infinite (e.g. all integers) or big enough that it is impractical to test all of (e.g. every 32-bit integer). Here your only hope is to sample it.

This is why we have to start with *identifying the domain*. Without the domain analysis, you will always be insecure about whether you've written enough tests. With it, it's more obvious
when you can stop.

To cover the domain, write down:

* simple cases
* edge cases
* error cases
* properties and invariants

 I find it almost impossible to know I've sampled the domain in the right way, unless I know what the domain is.

.. note::
   When even sampling won't do, then you need `formal methods <https://en.wikipedia.org/wiki/Formal_methods>`_. Unfortunately, formal methods are hard to do at the moment, and therefore rarely practical.

.. note::
   Covering the domain is different and more important than `code coverage`_.

   Code coverage tells you what percentage of your lines of code were touched during testing. But it does not tell you whether your tests were useful or if you missed an important case.

   Domain coverage *does* tell you that. And if you get the domain coverage right, then high code coverage comes for free.


This same concept is often discussed more colloquially

values? probably not in this case
type of values?



Step 3. Given, When, Then (or Arrange, Act, Assert)
---------------------------------------------------

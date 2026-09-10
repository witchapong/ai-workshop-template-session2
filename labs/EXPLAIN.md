# Understanding code you did not write

Reading unfamiliar code with an AI explaining it is the single most common way
working developers use these tools. It is also the fastest way to learn from a
solution that is better than yours.

First, bring the reference version into your project. The first two lines are
needed once — "Use this template" copies only `main`, so the
solution branches live on the template rather than on your copy:

```
git remote add reference https://github.com/witchapong/ai-workshop-template.git
git fetch reference
git checkout reference/solution/lab1 -- core/spectrum.py pages/2_Spectrum_Analyzer.py
```

Then work through these with Cline. **None of them change any code**, so none of
them can break your project.

## Understand it

> Explain what core/spectrum.py does, function by function, to someone who has
> done one Python course. Do not change any code.

> Walk me through what happens, step by step, when I enter 50 Hz at amplitude
> 1.0 and press the button. Name each function in the order it runs.

## Interrogate the tricky part

> Why is there a `2/n` in the spectrum function? What would the chart look like
> without it?

> Which line treats the 0 Hz term differently from the others, and what breaks
> if I delete it?

## Prove it to yourself

> Change the `2/n` to `1/n`, run pytest, and show me exactly which tests fail
> and why. Then change it back and confirm all seven pass again.

Do this one. Two tests fail — and the test that checks *where* the peaks are
stays green. That is the entire lesson of this lab in thirty seconds: the chart
still looks right, every peak in exactly the right place, and the numbers are
wrong by a factor of two.

## If you got your own version working

> Compare my core/spectrum.py to the reference version. What did each do
> differently? Does either have a bug the tests would not catch?

There is rarely one right answer. Finding out how else it could have been done
is worth as much as getting it working.

## For your log

Write down one thing the reference does that yours did not, or one thing you
understood only after asking. That is the entry.

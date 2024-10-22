# Contribution Guidelines
## NOTE
This is currently being used for a school project. It is HIGHLY preferred that contributions are kept to a minimum until
I've submitted the assignment. I will be sure to state when the assignment has been submitted. Until then, any pull
requests will be ignored. (I'm not trying to be mean, I'm just trying to not get an F for "unauthorized contributions.")

## Modifying/Contributing As A Whole
- Separate your code into sections -- this is mostly just to ensure that everything is organized and not all over the
  place.
- Use Python's PEP standards. You can use JetBrain's Pycharm Community Edition IDE to help ensure that you're following
  PEP standards.
- Specify the return type, when possible. This is more of a non-strict rule as it can be easy to forget to specify a
  return type; however, whenever you are contributing, try to ensure that the methods/functions that you've contributed
  specifies a return type.
- Use type hinting in method/function parameters. Doing so can help ensure that bugs are kept to a minimal.
- Avoid one-liners, when possible. Things such as `break if (x % 2) == 0 else continue` aren't as readable. If you are
  doing something such as `print(f"Hello, {"world" if [condition] else "friend"}")`, then I understand -- I'm fine with 
  that.
- If an `if` statement breaks out of a loop/function/method/etc., then avoid an `else` statement. For example, instead of
```python
value = True

while True:
    if value == True:
        print("Foo")
    else:
        print("Bar")
        break
```
Do this:
```python
value = True

while True:
    if not value:
        print("Bar")
        break

    print("Foo")
```

## Paradigms
Use OOP based programming when possible. That's my preferred method of handling this. However, if you wish to use
functional for something (such as the compiler CLI), then go for it. Try to avoid using non-OOP paradigms in 
`Compiler.py` and `BaseCompiler.py`, if possible. The goal of having them as OOP is that their functionality can easily 
be extended with only a decorator and function. Furthermore, it allows people to add layers on top of it. If someone 
wanted to add their own functionality (without losing the functionality of `Compiler.py`), then they can do that via
inheritance.

Generally speaking, however, any paradigm is fair game. 

Personal note: I'll write out a list of goals for this project after I've submitted it for my school assignment. As such,
that'll hopefully make it easier for anyone that is wanting to contribute to know what they should aim for in both
complexity and functionality. 

# Contribution Guidelines
## Modifying/Contributing As A Whole
- Make sure your code is clean and organized. Other people are expected to be working on this project, so having clean
  and understandable code is necessary.
- Use Python's PEP standards. You can use JetBrain's Pycharm Community Edition IDE to help ensure that you're following
  PEP standards.
- Specify the return type of functions and make use of Python's type hinting. Type hinting makes it easier to identify
  errors and mistakes in the code.
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
- Ensure that a variable is initialized in the class before it is assigned in the `__init__` method. For example:
```python
class Foo:
    x: int  # Initializing the variables in the class first
    y: int
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x  # Then assigning them a value
        self.y = y
```

## Paradigms
Any paradigm is fine, just make sure you're using them appropriately. A codebase that sticks to one paradigm can become
difficult and/or annoying to maintain. Python is capable of multi-paradigms, so it'd be within interest to leverage it.

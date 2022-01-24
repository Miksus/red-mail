# Contributing

Contributions of all sizes are welcomed, whether it's a typo fix in documentation, a bug fix proposal, feature request or completely a new idea for the project.

## Report Bugs

Report bugs in the [issue tracker](https://github.com/Miksus/red-mail/issues). Please describe how the bug occurred, what 
the bug was and, if relevant, what email provider you used and what versions (Python and OS) you used.

## Feature Requests and Ideas for Docs Improvements

You may submit your ideas and documenation improvements using the [issue tracker](https://github.com/Miksus/red-mail/issues).
Please use the appropriate issue template.

## Pull Requests

Also code contributions are welcome. For bug fixes and feature requests, it is recommended to first create an issue describing the 
problem the idea. For simple typo fixes in documentation or in docstrings creating issues are not necessary.

To create a pull request:

- Create an issue (unless a trivial and simple change)
- Fork the repository
- Do your changes
- If you did code changes, run the tests using tox:
  ```python
  pip install tox
  python -m tox
  ```
- If you did documantation changes, build the documentation using tox:
  ```python
  pip install tox
  python -m tox -e docs
  ```
- Make a pull request

If you made code changes:

- Test your code completely. The target is at 100 % test coverage.
- Write some documentations (if new feature). The target is to document 100 % of the code.
- Write code that is understandable, clear and follow the chosen conventions. 
  Read the code base the gain an idea of the existing style and try to follow it.
    - Follow PEP-8 as much as possible
    - Use Numpydocs for docstrings
    - Avoid hacks and unreliable solutions

If you improved documentation:

- Make sure the docs gets built without an error
- Make sure the part you changed looks OK also when rendered as HTML

You can find the built documentation at: ``redmail/docs/_build/html``

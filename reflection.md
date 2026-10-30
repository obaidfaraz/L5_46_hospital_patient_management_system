# Lab 5: Static Code Analysis – Reflection

**Project:** Hospital Patient Management System

*Note: The supplied lab handout and repository README did not include the wording of the four reflection questions. The following four commonly relevant reflection prompts and answers have therefore been prepared to complete the reflection deliverable.*

## 1. What is static code analysis, and why is it important?

Static code analysis is the process of examining source code without executing the program. It helps identify potential bugs, security vulnerabilities, code-quality problems and style violations early in development. In this lab, static analysis helped identify problems in the hospital patient management program before they could cause unexpected behaviour or security risks. It also made the code easier to read, maintain and review.

## 2. What are the differences between Pylint, Bandit and Flake8?

Each tool focuses on a different aspect of code quality:

- **Pylint** checks general code quality and programming practices. It identifies issues such as mutable default arguments, missing docstrings, unused variables, poor naming and potentially problematic logic.
- **Bandit** focuses on security. It identified patterns such as `eval()`, weak MD5 hashing, use of the standard `random` module for token generation, broad exception handling and shell command execution.
- **Flake8** checks Python style and common code errors, including line-length violations, unused imports, bare exceptions and missing final newlines.

Using all three provides broader coverage than relying on only one tool.

## 3. What were the major issues found in the program, and how were they fixed?

The original program contained several issues. The most important included:

- **Unsafe `eval()` usage:** It was replaced with a numeric multiplier for calculating treatment costs, preserving the original default calculation without executing arbitrary expressions.
- **Weak MD5 hashing:** It was replaced with SHA-256.
- **Shell command execution:** `os.system()` was removed and the export confirmation is printed directly by Python.
- **Mutable default argument:** The default `intake_log=[]` was changed to `None`, and the log is updated only when a list is supplied.
- **Bare exception handling:** The broad `try/except` that silently ignored errors was replaced with explicit checks for whether a patient exists and is admitted.
- **Predictable random token generation:** `random.randint()` was replaced with `secrets.randbelow()`.
- **Unsafe file handling:** File writing now uses a context manager and explicitly specifies UTF-8 encoding.

Other improvements included removing unused imports and variables, adding docstrings, improving function naming, and correcting formatting issues.

## 4. What did you learn from this lab, and how will you use static analysis in future projects?

This lab demonstrated that a program can run and produce output while still containing security, reliability and maintainability problems. Static analysis tools can reveal issues that may not be obvious during normal testing. I also learned that the tools complement one another: Pylint checks general code quality, Bandit focuses on security, and Flake8 checks style and common errors.

In future projects, I would run these tools regularly during development, review their findings, fix important issues and rerun the analysis before submitting or deploying the code. I would also combine static analysis with running and testing the program, because static analysis alone cannot guarantee that the program behaves correctly.

## Final verification results

The final analysis reports for this project showed:

| Tool | Before | After |
|---|---:|---:|
| Pylint | 5.19/10 | 10.00/10 |
| Bandit | 5 findings | 0 findings |
| Flake8 | 11 violations | 0 violations |

These results indicate that the reported static-analysis findings were resolved in the final version of the Python file.

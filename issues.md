# Static Code Analysis – Issues and Fixes

**Project:** Hospital Patient Management System  
**File analyzed:** `hospital_patient_system.py`

The line numbers below refer to the original, unmodified version of the Python file.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe `eval()` | Security – Bandit B307; Pylint W0123 | 40 | `eval(formula_expr)` executes a supplied expression as Python code, which can allow arbitrary code execution. Bandit reported this as Medium severity. | Removed expression evaluation and replaced it with a numeric treatment-cost multiplier. The default multiplier preserves the original `base_bill * 1.12` calculation. |
| Weak MD5 hashing | Security – Bandit B324 | 45 | MD5 is a weak hashing algorithm and should not be used where collision resistance is important. Bandit reported this as High severity. | Replaced MD5 with SHA-256 using `hashlib.sha256()`. |
| Shell command execution | Security – Bandit B605 | 56 | `os.system()` starts a shell command using a filename concatenated into the command string. This can create command-injection risk. Bandit reported this as High severity. | Removed the shell call and used Python's `print()` to display the export confirmation. |
| Hardcoded nurse access key | Security – manual code review | 68 | A fixed access key is embedded in the source code and printed during program execution. This exposes the credential to anyone who can read the code or its output. This was identified by manual inspection, not as a finding in the supplied Bandit report. | Removed the hardcoded key and its print statement. A real application should obtain secrets from a secure configuration or secrets manager rather than source code. |
| Mutable default argument | Bug / code quality – Pylint W0102 | 13 | `intake_log=[]` creates one list shared across calls that omit the argument, so entries can unexpectedly persist between calls. | Changed the default to `None` and append to the log only when a list is explicitly supplied. |
| Bare exception with `pass` | Error handling / security – Bandit B110; Pylint W0702; Flake8 E722 | 21–25 | A bare `except` catches every exception and silently ignores it, hiding errors during patient discharge. Bandit reported B110 as Low severity. | Removed the broad exception handler. The function now checks whether the patient exists and is admitted, then returns `True` or `False`. |
| Predictable random token | Security – Bandit B311 | 48–49 | `random.randint()` is not intended for security-sensitive token generation. Bandit reported this as Low severity. | Replaced it with `secrets.randbelow()` to generate a four-digit token using a cryptographically secure source. |
| File opened without context manager or encoding | Code quality – Pylint W1514 and R1732 | 53–55 | The file was opened without specifying an encoding and closed manually. An exception could prevent the close operation. | Used `Path.open()` inside a `with` statement and specified UTF-8 encoding. |
| Unused import and variables | Code quality – Pylint W0611/W0612; Flake8 F401/F841 | 4, 29, 39, 61 | `math`, `bed_charge`, `base_bill` (as separately assigned before `eval`), and the loop variable `p` were unused. | Removed unused imports and variables, and simplified the ward-summary loop. |
| PEP 8 and naming violations | Style – Flake8 E501; Pylint C0103 | 7–9, 13, 16, 72 | Several lines exceeded the configured 79-character limit, and `admitPatient` did not use the recommended `snake_case` naming style. | Reformatted long lines and renamed the function to `admit_patient`. |
| Missing documentation and final newline | Code quality/style – Pylint C0114/C0116/C0304; Flake8 W292 | Throughout; final line | The module and functions lacked docstrings, and the original file did not end with a newline. | Added a module docstring and function docstrings, and ensured the file ends with a newline. |
| Incorrect `None` comparison and redundant conditional | Code quality – Pylint C0121/R1703/R1705; Flake8 E711 | 30–35 | The code compared a value to `None` using `==` and used an unnecessary `if/else` to return a Boolean. | Used `is None` where applicable and simplified the status check to a Boolean expression. |

## Verification after fixes

The supplied after-analysis results show:

| Tool | Before | After |
|---|---:|---:|
| Pylint | 5.19/10 | 10.00/10 |
| Bandit | 5 findings (2 High, 1 Medium, 2 Low) | 0 findings |
| Flake8 | 11 reported violations | 0 violations (empty report file) |

**Note:** The hardcoded access key was a manual code-review finding. It was not one of the five findings listed in the original Bandit report. The table distinguishes tool-reported findings from manual inspection.

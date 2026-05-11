# goit-pycore-hw-05

Python Core homework 05. The repository contains four independent console tasks
that demonstrate closures, generators, decorators, file processing, and simple
command parsing.

## Project Structure

```text
.
├── task_01/
│   └── main.py          # Cached Fibonacci closure
├── task_02/
│   └── main.py          # Number generator and profit summation
├── task_03/
│   ├── main.py          # Log file analyzer
│   └── log.txt          # Sample log file
└── task_04/
    ├── main.py          # Assistant bot entry point
    ├── parser.py        # User input parser
    ├── handlers.py      # Contact command handlers
    └── decorators.py    # Input error decorator
```

## Requirements

- Python 3.10 or newer
- No external dependencies

## Task 1: Cached Fibonacci

`task_01/main.py` implements `caching_fibonacci()`, which returns an inner
`fibonacci(n)` function. The inner function keeps a cache in a closure and uses
it to avoid repeated recursive calculations.

Run:

```bash
python3 task_01/main.py
```

Expected output:

```text
55
610
```

## Task 2: Number Generator and Sum

`task_02/main.py` contains:

- `generator_numbers(text)` - yields numbers found in text as `float` values
- `sum_profit(text, func)` - sums values produced by the generator

Run:

```bash
python3 task_02/main.py
```

Expected output:

```text
Загальний дохід: 1501.46
```

## Task 3: Log File Analyzer

`task_03/main.py` reads a log file, parses records in the format
`YYYY-MM-DD HH:MM:SS LEVEL Message`, and prints statistics by logging level.

Run with the sample file:

```bash
python3 task_03/main.py task_03/log.txt
```

Filter by log level:

```bash
python3 task_03/main.py task_03/log.txt error
```

Supported helper functions:

- `parse_log_line(line)` - parses one log line into a dictionary
- `load_logs(file_path)` - lazily reads and parses log records
- `filter_logs_by_level(logs, level)` - filters records by level
- `count_logs_by_level(logs)` - counts records by level
- `display_log_counts(counts)` - prints a summary table
- `display_filtered_logs(logs, level)` - prints detailed filtered records

## Task 4: Assistant Bot

`task_04/main.py` starts an interactive contact book bot. Contacts are stored in
memory while the program is running.

Run:

```bash
python3 task_04/main.py
```

Available commands:

```text
hello
help
add <name> <phone>
change <name> <new_phone>
phone <name>
all
close
exit
```

Example session:

```text
Enter a command: hello
How can I help you?
Enter a command: add Alice 123456
Contact added.
Enter a command: phone Alice
123456
Enter a command: all
Alice : 123456
Enter a command: exit
Good bye!
```

The bot uses the `@input_error` decorator from `task_04/decorators.py` to catch
common input mistakes and return user-friendly messages instead of stopping the
program.

## Development Notes

- Each task can be run independently.
- The project uses only the Python standard library.
- There are no persistent databases or generated build artifacts.

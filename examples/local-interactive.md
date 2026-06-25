# Local interactive example

Status: planned.

```bash
cd /path/to/project
hermes -p heavy-coder chat
```

Example prompt:

```text
Investigate this failing test and propose a fix. Do not open a pull request.
```

Expected future behavior: Heavy Coder inspects the repository, identifies the failing test, proposes or applies a scoped fix, and reports exact commands and test output.

# ADR 0001: Terminal-first profile

Status: accepted

## Context

Heavy Coder should work from the current repository directory and serve maintainers who prefer terminal operation.

## Decision

Build as a terminal-first Hermes profile. Primary interaction is `hermes -p heavy-coder chat` from a project directory.

## Consequences

- No fixed target repository path is encoded.
- Scripts must use current working directory discovery.
- Remote and Docker execution remain future integration points.

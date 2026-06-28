#!/usr/bin/env bash
# Redact host-specific paths from terminal output.
redact() {
  sed -E \
    -e 's#/Users/[^/[:space:]]+/Projects/[^/[:space:]]+#~/workspace/heavy-coder#g' \
    -e 's#/Users/[^/[:space:]]+/#~/#g' \
    -e 's#/home/graphtheory/#~/#g' \
    -e 's#[Gg]rey[Nn]ewell#GraphTheory#g' \
    -e 's#\bgrey@#graphtheory@#g'
}
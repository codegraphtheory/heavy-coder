#!/usr/bin/env bash
redact() {
  sed -E \
    -e 's#/Users/[^/[:space:]]+/Projects/[^/[:space:]]+#~/workspace/heavy-coder#g' \
    -e 's#/Users/[^/[:space:]]+/#~/#g' \
    -e 's#[Gg]rey[Nn]ewell#GraphTheory#g' \
    -e 's#\bgrey@#graphtheory@#g'
}
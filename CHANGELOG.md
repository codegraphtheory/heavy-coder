# Changelog

## 0.1.3

- Improve the Heavy Coder environment doctor with read-only tool, git, and Hermes context checks.
- Add deterministic repository discovery for root, default branch, remote URL, and basic test-command hints.
- Update the candidate worker role configuration to use `composer-2.5`.

## 0.1.2

- Add a release guard workflow and script that fail when release-relevant profile-distribution changes do not bump `distribution.yaml` version.
- Add pull request checklist items requiring version and changelog discipline for visible profile updates.

## 0.1.1

- Default the profile to Hermes `xai-oauth` with `grok-4.3` as the coordinator chat model.
- Document the Heavy Coder role split: `grok-composer-2.5-fast` for candidate workers and `grok-4.3` for coordinator, critic, synthesizer, and verifier roles.
- Remove OpenRouter and xAI API key prompts from the profile distribution metadata so OAuth is the default path.

## 0.1.0

- Initial scaffold for Heavy Coder as a pure Hermes profile distribution.

---
name: improve-prompt
description: >
  Diagnose a draft prompt and output a ready-to-paste improved version.
  Advisory only — never executes the user's task. Use when the user asks to
  improve, optimize, or rewrite a prompt, help write a better instruction,
  or pastes a draft for feedback. Triggers include "improve my prompt",
  "optimize prompt", "rewrite this prompt", "help me prompt for",
  "help me write a better prompt", "what's missing from this prompt".
  Do not use when the user wants the task done directly ("just do it")
  or when they mean code or performance optimization ("optimize this code",
  "optimize performance").
---

# Improve prompt

The host runs the loop. This skill states what the agent may do and what it must not do. The agent picks order from the thread.

## Capabilities

| Action | When |
| --- | --- |
| Classify intent | The draft or request implies feature work, bug fix, research, review, docs, infra, design, refactor, or testing |
| Note missing context | Acceptance, scope, constraints, or verification are absent |
| Ask up to 3 clarification questions | Three or more critical gaps block a good prompt |
| Draft diagnosis and optimized prompt | Enough context exists or the user answered clarifications |
| Offer a short variant | The user wants a compact prompt after the full version |

## Knowledge

| Source | Load when |
| --- | --- |
| [examples.md](./examples.md) | Output shape, intent reference, and sample before/after |
| Project markers (`package.json`, `go.mod`, `pyproject.toml`, and similar) | The user wants stack-specific wording and files exist in the workspace |
| `{client_root}/{skills_dir}/` listing | The user asks which skill to attach; name only folders that exist |
| `{client_root}/rules/friendly-language.mdc` | Wording checks on chat and Markdown this skill produces |

Do not load a fixed catalog of slash commands or third-party component names.

## Limits

- **Advisory only.** Do not write code, create files, run commands, or implement the user's task.
- If the user says "just do it" or asks for execution instead of wording, state that this skill only produces prompts. Tell them to make a normal task request for execution.
- Do not recommend a specific model unless the user asks.
- Do not invent skills, rules, or commands that are not in the thread or under `{client_root}/{skills_dir}/`.
- Harness hints are optional: mention an installed skill folder by name only when it clearly fits the task.

## Anti-patterns

- Vague optimized prompt with no acceptance criteria or verification steps.
- No scope boundaries when the original request was broad.
- Embedding a full implementation plan when the user only asked for wording.
- Recommending `/commands` or product-specific orchestration the pack does not define.
- Switching into implementation because the optimized prompt looks like a spec.

## Output

Respond in the same language as the user's input. Use this structure:

### Prompt diagnosis

**Strengths:** What the draft already does well.

**Issues:**

| Issue | Impact | Suggested fix |
| --- | --- | --- |
| (problem) | (consequence) | (how to fix) |

**Needs clarification:** Numbered questions, or state what project files already answered.

### Optimized prompt (full)

One fenced block the user can copy. Include when relevant:

- Context and task
- Constraints and references (paths, docs, patterns)
- Acceptance and verification
- Out of scope

### Optimized prompt (short)

Optional compact variant for the same task.

### Suggested follow-ups

Optional: run the task in a normal agent turn; attach a named project skill if one fits. No fixed command list.

### Footer

One line: the user can ask for adjustments or start a normal request to execute instead.

See [examples.md](./examples.md) for intent labels and worked examples.

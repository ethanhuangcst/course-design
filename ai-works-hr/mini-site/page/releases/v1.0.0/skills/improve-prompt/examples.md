# improve-prompt reference and examples

## Intent labels (optional)

Use these labels in diagnosis when they fit. They are not a mandatory pipeline.

| Label | Signal words |
| --- | --- |
| New feature | build, create, add, implement |
| Bug fix | fix, broken, error, not working |
| Refactor | refactor, clean up, restructure |
| Research | how to, what is, explore, investigate |
| Testing | test, coverage, verify |
| Review | review, audit, check |
| Documentation | document, update docs, README |
| Infrastructure | deploy, CI, docker, database |
| Design | design, architecture, plan |

## Missing-context checklist

Mark each item in diagnosis when it matters for the task:

- Tech stack or runtime
- Target scope (files, modules, surfaces)
- Acceptance criteria
- Error and edge cases
- Security expectations
- Testing expectations
- Performance constraints
- UI or a11y (frontend work)
- Data or schema changes
- Patterns or reference files to follow
- Explicit out-of-scope items

When three or more critical items are unknown, ask up to three questions before the optimized prompt.

## Example 1: vague feature request (project detected)

**User input:**

```
Build me a user login page
```

**Context detected:** `package.json` with Next.js and TypeScript.

**Optimized prompt (full) excerpt:**

```
Implement a user login page on the project's existing stack (Next.js + TypeScript).

Task:
- Email/password form, validation, error messages, loading state, responsive layout
- Use the project's existing auth approach; if none is documented, state the assumed approach

Acceptance:
- Successful login routes to the dashboard; failures show clear errors
- Layout works on mobile and desktop viewports

Verification:
- Name test types to run (unit, integration, E2E) and what "pass" means

Out of scope:
- Registration, password reset, changes to existing route structure
```

## Example 2: moderate API request

**User input:**

```
Add a REST API endpoint for user profile updates with validation
```

**Optimized prompt (full) excerpt:**

```
Add PATCH /api/users/:id for partial profile updates.

Context: Go + existing router patterns in this repo (from go.mod and handlers).

Requirements:
- Fields: name, email, avatar_url, bio with validation
- Auth: token required; user may update own profile only
- Responses: 200 + body, 400 validation errors, 401/403 auth failures

Acceptance:
- Table-driven tests for success, validation, auth, not-found
- No change to unrelated endpoints or schema unless stated

Out of scope:
- New dependencies without checking existing stack first
```

## Example 3: user wants execution instead

**User input:**

```
Improve this prompt: add login page. Actually just build it now.
```

**Expected behavior (not an optimized prompt):**

State that this skill only produces prompts. Tell the user to send a normal implementation request without the improve-prompt skill.

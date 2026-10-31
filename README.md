# Lean Diff

An agent skill for making AI-generated changes simpler and more focused.

**The question:** does this change deliver the requested outcome in the simplest appropriate way, without touching things it does not need to touch?

Lean Diff works on an existing diff or PR. It first establishes the intended behavior, maps the change's impact, removes unnecessary scope, and repeatedly simplifies while checking that contracts and behavior survive.

## Workflow

1. **Fix the target and baseline.** Recover the request, acceptance criteria, diff base, and ownership of existing edits.
2. **Map the impact.** Trace affected consumers and prioritize APIs, schemas, business behavior, side effects, and shared infrastructure.
3. **Narrow the change.** Remove unrelated task-owned work, preserving other people's changes and necessary dependencies.
4. **Simplify in a verified loop.** Remove unnecessary layers and speculative generality, rechecking behavior after each coherent reduction.
5. **Verify boundaries.** Reproduce the requested outcome and run relevant checks on affected contracts.
6. **Return a focused result.** Explain what was reduced, why broader changes remain, and what was actually verified.

It does not equate fewer lines with better code, delete defensive behavior blindly, impose a file-count limit, or guarantee that tests replace human judgment.

## Install

Copy the `lean-diff/` directory into your coding agent's project-local skills directory:

- Claude Code: `.claude/skills/lean-diff/`
- Codex: `.agents/skills/lean-diff/`

The resulting folder must contain `SKILL.md` and `examples/walkthrough.md`. This is a portable Markdown skill, with no package installation, service, model, or API key of its own.

## Use

Ask your agent:

> Use Lean Diff on the current change. Preserve the original acceptance criteria, remove unrelated scope, and simplify the implementation. Verify the affected behavior and explain what remains.

Claude Code can invoke `/lean-diff`. Codex can invoke `$lean-diff`. The task and repository's existing instructions determine available actions and permissions.

## Review-only use

> Review this PR with Lean Diff without editing files. Return the smallest justified change, concrete simplifications, and the verification needed.

When asked for review only, the agent proposes reductions without applying them.

## Contents

- [The skill](lean-diff/SKILL.md)
- [Worked example and review scenarios](lean-diff/examples/walkthrough.md)

## Validation and limits

The bundled walkthrough exercises scope reduction and contract preservation, including an intentionally invalid simplification. Run `python3 lean-diff/examples/contract_check.py` to check the example with Python's standard library. A passing example validates that example, not every future use of the skill.

No live project, agent installation, or production deployment is modified by this repository.

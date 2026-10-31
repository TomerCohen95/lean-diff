---
name: lean-diff
description: Simplify an AI-generated diff or PR and reduce its blast radius while preserving requested behavior and existing contracts.
---

# Lean Diff

Reduce an existing change to the simplest implementation of the requested behavior, with the smallest justified impact.

## Procedure

### 1. Fix the target and baseline
Honor the requested mode: for review-only work, inspect and propose changes without editing files or running mutating checks. Otherwise, perform the authorized reductions below.
Read the original request, repository instructions, and current diff. Identify the comparison base from the actual branch or PR, including uncommitted changes when relevant. Distinguish task-owned edits from pre-existing or other-author work.
Write down the requested outcome, observable acceptance criteria, and behavior that must stay unchanged. Inspect the project's documented checks and record relevant pre-existing failures.
**Done when:** every proposed edit can be judged against a concrete outcome and a known baseline. Ask only when unresolved intent or ownership would change what can safely be removed.

### 2. Map the impact
For each changed area, explain why the outcome requires it. Inspect callers and consumers beyond changed files where the code crosses a boundary.
Prioritize user-visible behavior, business flows, API and schema contracts, persisted data, permissions, errors, side effects, and shared infrastructure. Use this impact map to decide where line-level review and verification matter most.
Classify each change as required, a necessary dependency of required work, or unrelated. A small diff can still have wide impact.
**Done when:** each changed area has a reason, affected consumers are identified, and uncertain coupling is explicit.

### 3. Narrow the change
Remove unnecessary task-owned changes, such as opportunistic cleanup, formatting churn, speculative configuration, and shared-infrastructure edits that a local solution makes unnecessary.
Preserve useful work owned by someone else. Identify independently valuable but unrelated work as a separate change recommendation, without creating a ticket, branch, or PR automatically.
Retain genuinely required cross-cutting changes and explain the dependency instead of forcing an artificial file limit. Evaluate shared infrastructure before introducing a local workaround that duplicates it.
**Done when:** remaining changes serve the requested outcome or a demonstrated dependency, and unrelated work has not been silently discarded.

### 4. Simplify in a verified loop
Look for a concrete simpler alternative in the remaining change: reuse an existing capability, collapse pass-through layers, remove one-use indirection, eliminate duplicate state or logic, or replace speculative generality with the direct implementation the request needs.
Inspect callers, contracts, and failure paths before removing a layer. Keep validation, authorization, compatibility, error handling, and useful abstractions when they carry real behavior.
Apply one coherent task-owned simplification at a time. Check equivalence against the acceptance criteria and the boundary it affects. Inspect the result and ask again: "Can the same required behavior be expressed more directly, with less coupling?"
If a candidate changes a required contract or fails verification, repair or undo only that candidate while preserving earlier accepted work.
**Done when:** no remaining evidence-backed simplification improves clarity or coupling without losing required behavior. Keep the original implementation if it is already the simplest appropriate one. Fewer lines alone are not success.

### 5. Verify the important boundaries
Run the project's relevant documented checks and a focused reproduction of the requested behavior. Add or adjust a test when a meaningful behavioral risk is not already covered.
Check affected contracts and consumers, including errors and side effects where they matter. Compare with the baseline to distinguish introduced regressions from existing failures.
After the final edit, review the entire task-owned diff for accidental scope growth, unnecessary dependencies, and verification that merely hides a failure. Never weaken an assertion to make a simplification pass.
**Done when:** the requested behavior and affected existing contracts are supported by evidence, or a specific unresolved verification gap is stated. Passing checks do not prove untested deployment or production behavior.

### 6. Return the focused result
Report the required outcome, removed scope or complexity, and why any wider changes remain necessary. List the checks actually run and their results, remaining risks, and separate recommendations.
Use changed-file or line counts only as supporting context, not proof of safety. Commit, push, merge, deploy, or publish only within the current task's actual authority.
**Done when:** the owner can tell what changed, why the impact is bounded, and what was and was not verified.

## Invocation examples
- "Use Lean Diff on this PR. Keep the acceptance criteria, remove unrelated changes, and simplify until further reduction would lose behavior."
- "Run Lean Diff before handoff. Review the working diff against the original request, not the whole codebase."

For a worked example and review scenarios, read [the walkthrough](examples/walkthrough.md) when a concrete comparison would help.

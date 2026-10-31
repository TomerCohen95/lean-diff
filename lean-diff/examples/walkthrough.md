# Walkthrough and review scenarios

## Example: add a display label to a list endpoint

Requested outcome: return each active product's display label, falling back to its name only when the label is absent. Keep the response shape, ordering, and inactive-product filtering unchanged. An empty label is valid.

The generated change adds a formatter class and a wrapper, changes global database retry settings, and reformats an unrelated reporting module.

### Map and narrow

- Endpoint label selection: required.
- Formatter class and wrapper: inspect whether they carry validation, compatibility, or shared behavior before removing them.
- Global database retries: unrelated unless a demonstrated dependency connects them to this request.
- Reporting formatting: unrelated.
- Other-author edits in any of these files: preserve.

For this example, callers confirm that the class is private to the endpoint and carries no behavior beyond the selection below. Remove the unnecessary class and wrapper, and remove only the task-owned retry and formatting changes. Do not revert whole files if someone else's changes are present.

### Simplify without changing the contract

Before:

```python
class ProductLabelFormatter:
    def format(self, product):
        if product.get("label") is not None:
            return product["label"]
        return product["name"]

def resolve_label(product):
    return ProductLabelFormatter().format(product)

def list_products(products):
    return [
        {"id": p["id"], "label": resolve_label(p)}
        for p in products if p["active"]
    ]
```

After:

```python
def list_products(products):
    return [
        {
            "id": p["id"],
            "label": p["label"] if p.get("label") is not None else p["name"],
        }
        for p in products if p["active"]
    ]
```

Rejected candidate: `p.get("label") or p["name"]` is shorter but incorrectly replaces a valid empty label. The acceptance criteria, not line count, decide.

The portable check in `contract_check.py` verifies this example's fallback, empty-label, filtering, ordering, input preservation, and error behavior. It also demonstrates that the invalid candidate is rejected.

## Scenario rubric

Use these as agent-review scenarios, not as claims that an automated agent evaluation has run.

1. **Already minimal:** a direct two-line fix passes existing checks. Expected: leave it alone and explain why no justified reduction remains.
2. **Other-author edits:** the working tree contains unrelated edits made before this task. Expected: preserve them and restrict edits to task-owned hunks.
3. **Necessary shared change:** an API change requires adapting its real consumers. Expected: keep and verify the necessary consumer changes rather than meeting a file-count target.
4. **Protection disguised as complexity:** a wrapper enforces authorization or error translation. Expected: retain its behavior, even if removing the wrapper looks cleaner.
5. **Loop regression:** a simplification changes an empty value, side effect, or error contract. Expected: reject or repair that candidate and recheck the final diff.
6. **Existing failure:** a baseline check already fails for an unrelated reason. Expected: state the baseline failure separately from new regressions, without claiming full verification.
7. **Review only:** the owner asks only for a review. Expected: return proposed changes and checks without editing the repository.

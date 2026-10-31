"""Run the two Python versions printed in walkthrough.md against a behavior contract."""
import copy
from pathlib import Path
import re
import unittest

walkthrough = Path(__file__).with_name("walkthrough.md").read_text()
snippets = re.findall(r"```python\n(.*?)```", walkthrough, re.S)
if len(snippets) != 2:
    raise RuntimeError("Expected exactly the before and after snippets")
versions = []
for snippet in snippets:
    scope = {}
    exec(compile(snippet, "walkthrough.md", "exec"), scope)
    versions.append(scope["list_products"])

class ContractCheck(unittest.TestCase):
    def check_versions(self, products, expected):
        original = copy.deepcopy(products)
        for fn in versions:
            with self.subTest(version=fn.__code__.co_firstlineno, code=fn.__code__.co_consts):
                self.assertEqual(fn(products), expected)
                self.assertEqual(products, original)

    def test_explicit_label_and_shape(self):
        self.check_versions([{"id": 3, "name": "Default", "label": "Display", "active": True}],
                            [{"id": 3, "label": "Display"}])

    def test_missing_and_none_fall_back(self):
        self.check_versions([{"id": 1, "name": "One", "active": True},
                             {"id": 2, "name": "Two", "label": None, "active": True}],
                            [{"id": 1, "label": "One"}, {"id": 2, "label": "Two"}])

    def test_empty_label_is_not_absent(self):
        self.check_versions([{"id": 1, "name": "Fallback", "label": "", "active": True}],
                            [{"id": 1, "label": ""}])

    def test_filtering_and_order(self):
        self.check_versions([{"id": 2, "name": "Two", "active": True},
                             {"id": 9, "name": "Hidden", "active": False},
                             {"id": 1, "name": "One", "active": True}],
                            [{"id": 2, "label": "Two"}, {"id": 1, "label": "One"}])

    def test_empty_input(self):
        self.check_versions([], [])

    def test_error_contract(self):
        for fn in versions:
            with self.assertRaises(KeyError):
                fn([{"name": "Missing ID", "active": True}])

    def test_shorter_candidate_breaks_contract(self):
        product = {"id": 1, "name": "Fallback", "label": "", "active": True}
        candidate = product.get("label") or product["name"]
        self.assertNotEqual(candidate, versions[0]([product])[0]["label"])

if __name__ == "__main__":
    unittest.main(verbosity=2)

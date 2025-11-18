# Test Coverage Report# Coverage Report - Assignment 9

**Date:** November 18, 2025  **Date:** November 18, 2025  

**Coverage:** 84% (16/16 tests passing)**Python Version:** 3.13.5  

**Testing Framework:** pytest 8.3.4  

---**Coverage Tool:** pytest-cov 7.0.0



## Summary---



| Module | Coverage | Status | Missing Lines |## Executive Summary

|--------|----------|--------|---------------|

| order.py | 100% | ✅ | None |- **Total Test Cases:** 11

| tests/*.py | 100% | ✅ | None |- **Tests Passed:** 11 (100%)

| risk_engine.py | 96% | ✅ | 27 |- **Tests Failed:** 0

| logger.py | 82% | ⚠️ | 28-29, 32, 45-48 |- **Overall Coverage:** 73%

| fix_parser.py | 74% | ⚠️ | 36-48 (__main__) |- **Test Execution Time:** 0.10s

| main.py | 0% | ⚠️ | 1-54 (integration) |

---

**Total:** 305 statements, 49 missing


## Test Execution Results

```
================================ test session starts ================================
platform darwin -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/jaewonchoi/workspace/uchicago/FINM325/group8
configfile: pyproject.toml
plugins: anyio-4.7.0, cov-7.0.0
collected 11 items

tests/test_fix_parser.py::test_fix_parser PASSED                              [  9%]
tests/test_fix_parser.py::test_fix_parser_missing_fields PASSED               [ 18%]
tests/test_logger.py::test_check_coherent_logs PASSED                         [ 27%]
tests/test_orders.py::TestOrder::test_acked_to_canceled_valid_transition PASSED [ 36%]
tests/test_orders.py::TestOrder::test_acked_to_filled_valid_transition PASSED [ 45%]
tests/test_orders.py::TestOrder::test_filled_to_any_invalid_transition PASSED [ 54%]
tests/test_orders.py::TestOrder::test_initial_state PASSED                    [ 63%]
tests/test_orders.py::TestOrder::test_new_to_acked_valid_transition PASSED    [ 72%]
tests/test_orders.py::TestOrder::test_new_to_filled_invalid_transition PASSED [ 81%]
tests/test_orders.py::TestOrder::test_new_to_rejected_valid_transition PASSED [ 90%]
tests/test_orders.py::TestOrder::test_rejected_to_any_invalid_transition PASSED [100%]

================================ 11 passed in 0.10s =================================
```

### Coverage Summary
```
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
fix_parser.py                 39     10    74%   36-48
logger.py                     33      6    82%   28-29, 32, 45-48
main.py                       32     32     0%   1-54
order.py                      20      0   100%
risk_engine.py                26     26     0%   1-38
tests/conftest.py              7      0   100%
tests/test_fix_parser.py      49      0   100%
tests/test_logger.py          23      0   100%
tests/test_orders.py          41      0   100%
--------------------------------------------------------
TOTAL                        270     74    73%
```

---

**Report Generated:** November 18, 2025  
**HTML Coverage Report:** `htmlcov/index.html`  

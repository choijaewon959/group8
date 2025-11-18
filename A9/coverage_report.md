# Test Coverage Report# Coverage Report - Assignment 9

**Date:** November 18, 2025  **Date:** November 18, 2025  

**Coverage:** 84% (16/16 tests passing)**Python Version:** 3.13.5  

**Testing Framework:** pytest 8.3.4  

---**Coverage Tool:** pytest-cov 7.0.0



## Summary---
| Module | Coverage | Missing Lines |## Executive Summary

|--------|----------|--------|---------------|

| order.py | 100% | None |- **Total Test Cases:** 11

| tests/*.py | 100% | None |- **Tests Passed:** 11 (100%)

| risk_engine.py | 96% | 27 |

| logger.py | 82% | 28-29, 32, 45-48 |

| fix_parser.py | 74% | 36-48 (__main__) |

---

**Total:** 305 statements, 49 missing
> Note that the __main__ part of fix_parser.py is not included in the test coverage.


## Test Execution Results

```
================================ test session starts ================================
platform darwin -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/jaewonchoi/workspace/uchicago/FINM325/group8
configfile: pyproject.toml
plugins: anyio-4.7.0, cov-7.0.0
collected 16 items

tests/test_engine.py::TestRiskEngine::test_order_size_limit PASSED            [  6%]
tests/test_engine.py::TestRiskEngine::test_position_limit PASSED              [ 12%]
tests/test_engine.py::TestRiskEngine::test_update_position_buy PASSED         [ 18%]
tests/test_engine.py::TestRiskEngine::test_update_position_sell PASSED        [ 25%]
tests/test_fix_parser.py::test_fix_parser PASSED                              [ 31%]
tests/test_fix_parser.py::test_fix_parser_missing_fields PASSED               [ 37%]
tests/test_fix_parser.py::test_fix_parser_edge_cases PASSED                   [ 43%]
tests/test_logger.py::test_check_coherent_logs PASSED                         [ 50%]
tests/test_orders.py::TestOrder::test_acked_to_canceled_valid_transition PASSED [ 56%]
tests/test_orders.py::TestOrder::test_acked_to_filled_valid_transition PASSED [ 62%]
tests/test_orders.py::TestOrder::test_filled_to_any_invalid_transition PASSED [ 68%]
tests/test_orders.py::TestOrder::test_initial_state PASSED                    [ 75%]
tests/test_orders.py::TestOrder::test_new_to_acked_valid_transition PASSED    [ 81%]
tests/test_orders.py::TestOrder::test_new_to_filled_invalid_transition PASSED [ 87%]
tests/test_orders.py::TestOrder::test_new_to_rejected_valid_transition PASSED [ 93%]
tests/test_orders.py::TestOrder::test_rejected_to_any_invalid_transition PASSED [100%]

================================ 16 passed in 0.10s =================================
```

### Coverage Summary
```
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
fix_parser.py                 39     10    74%   36-48
logger.py                     33      6    82%   28-29, 32, 45-48
main.py                       32     32     0%   1-54
order.py                      20      0   100%
risk_engine.py                26      1    96%   27
tests/conftest.py              7      0   100%
tests/test_engine.py          24      0   100%
tests/test_fix_parser.py      60      0   100%
tests/test_logger.py          23      0   100%
tests/test_orders.py          41      0   100%
--------------------------------------------------------
TOTAL                        305     49    84%
```

---

**Report Generated:** November 18, 2025  
**HTML Coverage Report:** `htmlcov/index.html`  

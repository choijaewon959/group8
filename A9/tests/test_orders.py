import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from order import Order, OrderState

class TestOrder(unittest.TestCase):

    def setUp(self):
        self.order = Order(symbol="AAPL", qty=100, side="+1")

    def test_initial_state(self):
        self.assertEqual(self.order.state, OrderState.NEW)

    def test_new_to_acked_valid_transition(self):
        self.order.transition(OrderState.ACKED)
        self.assertEqual(self.order.state, OrderState.ACKED)
        
    def test_new_to_rejected_valid_transition(self):
        self.order.transition(OrderState.REJECTED)
        self.assertEqual(self.order.state, OrderState.REJECTED)

    def test_new_to_filled_invalid_transition(self):
        initial_state = self.order.state
        self.order.transition(OrderState.FILLED)
        self.assertEqual(self.order.state, initial_state)

    def test_acked_to_filled_valid_transition(self):
        self.order.transition(OrderState.ACKED)
        self.order.transition(OrderState.FILLED)
        self.assertEqual(self.order.state, OrderState.FILLED)

    def test_acked_to_canceled_valid_transition(self):
        # 1. NEW -> ACKED
        self.order.transition(OrderState.ACKED)
        # 2. ACKED -> CANCELED
        self.order.transition(OrderState.CANCELED)
        self.assertEqual(self.order.state, OrderState.CANCELED)

    def test_filled_to_any_invalid_transition(self):
        # 1. NEW -> ACKED -> FILLED
        self.order.transition(OrderState.ACKED)
        self.order.transition(OrderState.FILLED)
        
        initial_state = self.order.state # OrderState.FILLED
        
        # 2. FILLED to ACKED 
        self.order.transition(OrderState.ACKED)
        self.assertEqual(self.order.state, initial_state) # 상태 유지 확인
        
        # 3. FILLED to CANCELED
        self.order.transition(OrderState.CANCELED)
        self.assertEqual(self.order.state, initial_state) # 상태 유지 확인

    def test_rejected_to_any_invalid_transition(self):
        # 1. NEW to REJECTED
        self.order.transition(OrderState.REJECTED)
        
        initial_state = self.order.state # OrderState.REJECTED
        
        # 2. REJECTED to ACKED
        self.order.transition(OrderState.ACKED)
        self.assertEqual(self.order.state, initial_state)

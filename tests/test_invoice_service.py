import unittest
from unittest.mock import create_autospec
from invoice_service import InvoiceService, Invoice, ChargeResult


class TestInvoiceService(unittest.TestCase):
    def setUp(self):
        self.invoice_repo = create_autospec(
            spec=['get_by_id', 'mark_paid', 'mark_failed', 'mark_retry']
        )
        self.payment_gateway = create_autospec(spec=['charge'])
        self.service = InvoiceService(self.invoice_repo, self.payment_gateway)
    
    def test_successful_payment_returns_paid_and_updates_repo(self):
        invoice = Invoice(id=1, customer_id="cust_123", amount=1000, status="pending")
        self.invoice_repo.get_by_id.return_value = invoice
        self.payment_gateway.charge.return_value = ChargeResult(
            ok=True, 
            transaction_id="tx_789"
        )
        
        result = self.service.pay(1)
        
        self.assertEqual(result, "paid")
        self.invoice_repo.get_by_id.assert_called_once_with(1)
        self.payment_gateway.charge.assert_called_once_with("cust_123", 1000)
        self.invoice_repo.mark_paid.assert_called_once_with(1, "tx_789")
        self.invoice_repo.mark_failed.assert_not_called()
        self.invoice_repo.mark_retry.assert_not_called()
    
    def test_declined_payment_returns_failed_and_saves_reason(self):
        invoice = Invoice(id=2, customer_id="cust_456", amount=500, status="pending")
        self.invoice_repo.get_by_id.return_value = invoice
        self.payment_gateway.charge.return_value = ChargeResult(
            ok=False,
            reason="insufficient funds"
        )
        
        result = self.service.pay(2)
        
        self.assertEqual(result, "failed")
        self.payment_gateway.charge.assert_called_once_with("cust_456", 500)
        self.invoice_repo.mark_failed.assert_called_once_with(2, "insufficient funds")
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_retry.assert_not_called()
    
    def test_already_paid_invoice_returns_already_paid_and_does_not_call_gateway(self):
        invoice = Invoice(id=3, customer_id="cust_789", amount=200, status="paid")
        self.invoice_repo.get_by_id.return_value = invoice
        
        result = self.service.pay(3)
        
        self.assertEqual(result, "already_paid")
        self.invoice_repo.get_by_id.assert_called_once_with(3)
        self.payment_gateway.charge.assert_not_called()
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_failed.assert_not_called()
        self.invoice_repo.mark_retry.assert_not_called()
    
    def test_invoice_not_found_raises_lookuperror(self):
        self.invoice_repo.get_by_id.return_value = None
        
        with self.assertRaises(LookupError) as context:
            self.service.pay(999)
        
        self.assertEqual(str(context.exception), "invoice not found: 999")
        self.invoice_repo.get_by_id.assert_called_once_with(999)
        self.payment_gateway.charge.assert_not_called()
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_failed.assert_not_called()
        self.invoice_repo.mark_retry.assert_not_called()
    
    def test_invalid_amount_raises_valueerror(self):
        invoice = Invoice(id=4, customer_id="cust_000", amount=0, status="pending")
        self.invoice_repo.get_by_id.return_value = invoice
        
        with self.assertRaises(ValueError) as context:
            self.service.pay(4)
        
        self.assertEqual(str(context.exception), "amount must be positive, got: 0")
        self.payment_gateway.charge.assert_not_called()
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_failed.assert_not_called()
        self.invoice_repo.mark_retry.assert_not_called()
    
    def test_payment_timeout_returns_retry_and_saves_for_retry(self):
        invoice = Invoice(id=5, customer_id="cust_timeout", amount=300, status="pending")
        self.invoice_repo.get_by_id.return_value = invoice
        self.payment_gateway.charge.side_effect = TimeoutError("gateway timeout")
        
        result = self.service.pay(5)
        
        self.assertEqual(result, "retry")
        self.payment_gateway.charge.assert_called_once_with("cust_timeout", 300)
        self.invoice_repo.mark_retry.assert_called_once_with(5, reason="gateway timeout")
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_failed.assert_not_called()
    
    def test_idempotency_second_call_does_not_charge_again(self):
        invoice = Invoice(id=6, customer_id="cust_dup", amount=150, status="pending")
        self.invoice_repo.get_by_id.return_value = invoice
        self.payment_gateway.charge.return_value = ChargeResult(ok=True, transaction_id="tx_dup")
        
        result1 = self.service.pay(6)
        self.assertEqual(result1, "paid")
        
        invoice.status = "paid"
        
        result2 = self.service.pay(6)
        
        self.assertEqual(result2, "already_paid")
        self.payment_gateway.charge.assert_called_once_with("cust_dup", 150)
        self.invoice_repo.mark_paid.assert_called_once_with(6, "tx_dup")


if __name__ == "__main__":
    unittest.main()
from dataclasses import dataclass
from typing import Optional


@dataclass
class Invoice:
    id: int
    customer_id: str
    amount: int
    status: str


@dataclass
class ChargeResult:
    ok: bool
    transaction_id: Optional[str] = None
    reason: Optional[str] = None


class InvoiceService:
    def __init__(self, invoice_repo, payment_gateway):
        self.invoice_repo = invoice_repo
        self.payment_gateway = payment_gateway
    
    def pay(self, invoice_id: int) -> str:
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if invoice is None:
            raise LookupError(f"invoice not found: {invoice_id}")
        
        if invoice.status == "paid":
            return "already_paid"
        
        if invoice.amount <= 0:
            raise ValueError(f"amount must be positive, got: {invoice.amount}")
        
        try:
            charge_result = self.payment_gateway.charge(invoice.customer_id, invoice.amount)
        except TimeoutError:
            self.invoice_repo.mark_retry(invoice_id, reason="gateway timeout")
            return "retry"
        
        if charge_result.ok:
            self.invoice_repo.mark_paid(invoice_id, charge_result.transaction_id)
            return "paid"
        else:
            self.invoice_repo.mark_failed(invoice_id, charge_result.reason)
            return "failed"
# invoice_service.py
from dataclasses import dataclass
from typing import Optional, Protocol, Any


@dataclass
class Invoice:
    id: int
    customer_id: str
    amount: int
    status: str  # "pending", "paid", "failed", "retry"


@dataclass
class ChargeResult:
    ok: bool
    transaction_id: Optional[str] = None
    reason: Optional[str] = None


class InvoiceRepo(Protocol):
    def get_by_id(self, invoice_id: int) -> Optional[Invoice]: ...
    def mark_paid(self, invoice_id: int, transaction_id: str) -> None: ...
    def mark_failed(self, invoice_id: int, reason: str) -> None: ...
    def mark_retry(self, invoice_id: int) -> None: ...


class PaymentGateway(Protocol):
    def charge(self, customer_id: str, amount: int) -> ChargeResult: ...


class InvoiceService:
    def __init__(self, invoice_repo, payment_gateway):
        self.invoice_repo = invoice_repo
        self.payment_gateway = payment_gateway
    
    def pay(self, invoice_id: int) -> str:
        """
        Обрабатывает оплату счета
        
        Returns:
            "paid" - успешная оплата
            "already_paid" - счет уже оплачен
            "failed" - платеж отклонен
            "retry" - таймаут, нужно повторить позже
            
        Raises:
            LookupError: счет не найден
            ValueError: сумма счета <= 0
        """
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if invoice is None:
            raise LookupError(f"invoice not found: {invoice_id}")
        
        if invoice.status == "paid":
            return "already_paid"
        
        if invoice.amount <= 0:
            raise ValueError(f"amount must be positive, got: {invoice.amount}")
        
        try:
            result = self.payment_gateway.charge(invoice.customer_id, invoice.amount)
        except TimeoutError:
            self.invoice_repo.mark_retry(invoice_id)
            return "retry"
        if result.ok:
            self.invoice_repo.mark_paid(invoice_id, result.transaction_id or "unknown")
            return "paid"
        else:
            self.invoice_repo.mark_failed(invoice_id, result.reason or "unknown error")
            return "failed"
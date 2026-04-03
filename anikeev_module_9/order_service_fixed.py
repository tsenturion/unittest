# order_service_fixed.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from dataclasses import dataclass


@dataclass
class Order:
    id: int
    amount: int


class OrderRepo:
    def get(self, order_id: int) -> Order:
        raise NotImplementedError


class PaymentGateway:
    def charge(self, amount: int, currency: str = "RUB") -> str:
        raise NotImplementedError


class AuditClient:
    def __init__(self, endpoint: str, token: str) -> None:
        self.endpoint = endpoint
        self.token = token

    def write(self, event: str, payload: dict) -> None:
        raise NotImplementedError


# ИСПРАВЛЕННАЯ ВЕРСИЯ - все ошибки устранены
class OrderServiceFixed:
    def __init__(self, repo: OrderRepo, payment_gateway: PaymentGateway):
        self.repo = repo
        self.payment_gateway = payment_gateway

    def pay(self, order_id: int) -> str:
        # ИСПРАВЛЕНО: правильное имя метода
        order = self.repo.get(order_id)
        
        # ИСПРАВЛЕНО: правильные аргументы
        tx_id = self.payment_gateway.charge(order.amount, currency="RUB")
        
        # ИСПРАВЛЕНО: правильный конструктор с двумя параметрами
        audit = AuditClient(endpoint="https://audit.local", token="secret")
        audit.write("payment_ok", {"order_id": order.id, "tx_id": tx_id})
        
        return tx_id
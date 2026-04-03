# order_service.py
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


# БАГОВАННАЯ ВЕРСИЯ - содержит три ошибки:
# 1. Старое имя метода find_by_id вместо get
# 2. Неверные keyword-аргументы для charge
# 3. Неверный вызов конструктора AuditClient
class OrderService:
    def __init__(self, repo: OrderRepo, payment_gateway: PaymentGateway):
        self.repo = repo
        self.payment_gateway = payment_gateway

    def pay(self, order_id: int) -> str:
        # ОШИБКА №1: устаревшее имя метода
        order = self.repo.find_by_id(order_id)
        
        # ОШИБКА №2: неправильные keyword-аргументы
        tx_id = self.payment_gateway.charge(total=order.amount, curr="RUB")
        
        # ОШИБКА №3: неверный конструктор AuditClient (не хватает token)
        audit = AuditClient("https://audit.local")
        audit.write("payment_ok", {"order_id": order.id, "tx_id": tx_id})
        
        return tx_id
from dataclasses import dataclass


@dataclass
class Order:
    id: int
    amount: int

class OrderRepo:
    """Репозиторий для работы с заказами"""
    def get(self, order_id: int) -> Order:
        raise NotImplementedError


class PaymentGateway:
    """Платёжный шлюз"""
    def charge(self, amount: int, currency: str = "RUB") -> str:
        raise NotImplementedError


class AuditClient:
    """Клиент для аудита"""
    def __init__(self, endpoint: str, token: str) -> None:
        self.endpoint = endpoint
        self.token = token

    def write(self, event: str, payload: dict) -> None:
        raise NotImplementedError


class OrderService:
    """Сервис для оплаты заказов (с ошибками)"""
    def __init__(self, repo: OrderRepo, gateway: PaymentGateway):
        self.repo = repo
        self.gateway = gateway

    def pay(self, order_id: int) -> str:
        order = self.repo.find_by_id(order_id)
        
        tx_id = self.gateway.charge(total=order.amount, curr="USD")
        
        audit = AuditClient("https://audit.local")
        audit.write("payment_success", {"order_id": order.id, "tx_id": tx_id})
        
        return tx_id
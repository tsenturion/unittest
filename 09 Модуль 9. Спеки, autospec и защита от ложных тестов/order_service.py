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


class OrderService:
    def __init__(self, repo: OrderRepo, gateway: PaymentGateway):
        self.repo = repo
        self.gateway = gateway

    def pay(self, order_id: int) -> str:
        order = self.repo.get(order_id)
        tx_id = self.gateway.charge(order.amount, currency="RUB")
        audit = AuditClient(endpoint="https://audit.local", token="secret")
        audit.write("payment_ok", {"order_id": order.id, "tx_id": tx_id})
        return tx_id
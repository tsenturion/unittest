import requests

class CatalogTimeoutError(Exception):
    pass

class CatalogResponseError(Exception):
    pass

class CatalogClient:
    def __init__(self, base_url: str, api_key: str, timeout: int = 3) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def fetch_product(self, product_id: int) -> dict:
        url = f"{self.base_url}/products/{product_id}"
        try:
            
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=self.timeout,
            )
        except requests.Timeout as exc:
            raise CatalogTimeoutError("Catalog API timed out") from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise CatalogResponseError(
                f"Catalog API returned status {response.status_code}"
            ) from exc

        return response.json()
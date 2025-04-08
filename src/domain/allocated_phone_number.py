from dataclasses import dataclass
from .phone_number import PhoneNumber

@dataclass(frozen=True)
class AllocatedPhoneNumber:
    number: PhoneNumber
    range_id: int
    customer_id: int

    def formatted(self) -> str:
        return f"{self.number.formatted()} (client {self.customer_id} in range {self.range_id})"

    def __str__(self):
        return self.formatted()

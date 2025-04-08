from typing import Set
from dataclasses import dataclass

from .phone_number import PhoneNumber

@dataclass
class NumberRange:
    start: int
    end: int

    def contains(self, phone_number: PhoneNumber) -> bool:
        """
        Vérifie si le PhoneNumber appartient à la plage.
        """
        return self.start <= phone_number.number <= self.end

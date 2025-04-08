from src.domain.allocated_phone_number import AllocatedPhoneNumber
from src.domain.phone_number import PhoneNumber

def test_phone_number_formatted():
    phone = PhoneNumber(162050000)
    allocated_phone = AllocatedPhoneNumber(phone, 1, 1)
    expected = "01 62 05 00 00 (client 1 in range 1)"
    assert allocated_phone.formatted() == expected

def test_phone_number_str():
    phone = PhoneNumber(162050000)
    allocated_phone = AllocatedPhoneNumber(phone, 1, 1)
    expected = "01 62 05 00 00 (client 1 in range 1)"
    assert str(allocated_phone) == expected

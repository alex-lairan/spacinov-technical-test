from src.domain.phone_number import PhoneNumber

def test_phone_number_formatted():
    phone = PhoneNumber(162050000)
    expected = "01 62 05 00 00"
    assert phone.formatted() == expected

def test_phone_number_str():
    phone = PhoneNumber(162050000)
    expected = "01 62 05 00 00"
    assert str(phone) == expected

def test_phone_number_equality():
    phone1 = PhoneNumber(162050000)
    phone2 = PhoneNumber(162050000)
    assert phone1 == phone2

from src.domain.number_range import NumberRange
from src.domain.phone_number import PhoneNumber

def test_contains_inside_range():
    range_obj = NumberRange(start=162050000, end=162059999)
    phone = PhoneNumber(162055555)
    assert range_obj.contains(phone) is True

def test_contains_outside_range_below():
    range_obj = NumberRange(start=162050000, end=162059999)
    phone = PhoneNumber(162049999)
    assert range_obj.contains(phone) is False

def test_contains_outside_range_above():
    range_obj = NumberRange(start=162050000, end=162059999)
    phone = PhoneNumber(162060000)
    assert range_obj.contains(phone) is False

def test_contains_boundary_values():
    range_obj = NumberRange(start=162050000, end=162059999)
    phone_start = PhoneNumber(162050000)
    phone_end   = PhoneNumber(162059999)
    assert range_obj.contains(phone_start) is True
    assert range_obj.contains(phone_end) is True

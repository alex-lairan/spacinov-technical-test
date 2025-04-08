from dataclasses import dataclass

@dataclass(frozen=True)
class YearlyRangeReport:
    range_id: int
    currently_allocated: int
    new_allocated: int
    cancelled: int


@dataclass(frozen=True)
class YearlyReport:
    range_reports : list

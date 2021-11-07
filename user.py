from dataclasses import dataclass

@dataclass
class User:
    email: str
    pw: str
    name: str
    gender: str
    birth_year: int
    birth_month: int
    birth_date: int

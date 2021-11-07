from dataclasses import dataclass

from dbController import getSendTo

@dataclass
class Config:
    charset: str
    subject: str
    me: str
    to: list[str]
    host: str
    port: int
    username: str
    password: str

config = Config(
    charset = 'UTF-8',
    subject = 'subject',
    me = 'fubiisSub@gmail.com',
    to = [
        getSendTo(),
    ],
    host = 'smtp.gmail.com',
    port = 587,
    username = 'fubiisSub@gmail.com',
    password = 'esohgfwcuscsqmex',
)

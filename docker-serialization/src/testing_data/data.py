from dataclasses import dataclass
from typing import List


@dataclass
class Friend:
    id: int
    money: float
    name: str


@dataclass
class User:
    name: str
    id: int
    friends: List["Friend"]
    cars: List[str]


@dataclass
class TestingData:
    users: List[User]


def get_test_data() -> TestingData:
    result = []

    for i in range(500):
        friends = []
        for j in range(10):
            if i - j < 0:
                break
            
            friends.append(Friend(id = i - j, money = i + j, name = f"name-id{i - j}"))

        result.append(User(name=f"name-id{i}", id=i, friends=friends, cars=["toyota", "bmw"]))
    
    return TestingData(users=result)

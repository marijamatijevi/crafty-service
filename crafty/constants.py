import enum


class UserType(enum.StrEnum):
    buyer = "buyer"
    seller = "seller"

    def __repr__(self):
        return self.value


class Rating(enum.Enum):
    one = "1"
    two = "2"
    three = "3"
    four = "4"
    five = "5"

    def __repr__(self):
        return self.value


class SubscriptionLevel(enum.StrEnum):
    basic = "basic"
    premium = "premium"
    pro = "pro"

    def __repr__(self):
        return self.value

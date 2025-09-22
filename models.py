class User (BaseModel):
    id: int
    name: str
    balance: float

    def pay(self, amount: float, receiver: 'User', reason: str):
        if amount > self.balance:
            # Charge to credit card
            credit_cards = CreditCard.select().where(CreditCard.user_id == self.id)
            payed = False
            for credit_card in credit_cards:
                if credit_card.balance > amount:
                    credit_card.charge(amount)
                    payed = True
                    break

            if not payed:
                return "Not enough balance"
        
        else:
            self.balance = self.balance - amount
        
        detail_feed = self.name + " paid $" + str(amount) + " for " + reason
        feed = Feed(user_id=self.id, detail=detail_feed)
        feed.save()
        return detail_feed
                

class CreditCard (BaseModel):
    id: int
    user_id: int
    number: str
    consumption: float
    limit: float
    balance: float


    def charge(self, amount: float):
        self.consumption += amount
        self.balance -= amount
        self.save()


class Feed(BaseModel):
    id: int
    user_id: int
    detail: str
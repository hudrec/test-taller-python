from peewee import *
from database import (
    db,
    BaseModel,
    User as BaseUser,
    CreditCard as BaseCreditCard,
    Feed as BaseFeed,
    Friendship,
)


class User(BaseUser):
    class Meta:
        database = db

    def pay(self, amount: float, receiver: "User", reason: str):
        if amount > self.balance:
            # Charge to credit card
            payed = False
            for credit_card in self.credit_cards:
                if credit_card.balance >= amount:
                    credit_card.charge(amount)
                    payed = True
                    break

            if not payed:
                return {
                    "error": "Not enough balance and no valid credit card available"
                }
        else:
            self.balance -= amount
            self.save()

        # Update receiver's balance
        receiver.balance += amount
        receiver.save()

        detail_feed = f"{self.name} paid ${amount:.2f} to {receiver.name} for {reason}"
        Feed.create(
            user=self, related_user=receiver, detail=detail_feed, feed_type="payment"
        )
        return {"message": detail_feed, "remaining_balance": self.balance}

    def retrieve_activity(self):
        """
        Retrieve all activities related to the user including payments and friend additions
        """
        # Get user's payment activities
        payment_activities = (
            Feed.select()
            .where((Feed.user == self) | (Feed.related_user == self))
            .order_by(Feed.created_at.desc())
        )

        # Get friend activities
        friend_activities = (
            Feed.select()
            .where((Feed.user.in_(self.friends())) & (Feed.feed_type == "friend_add"))
            .order_by(Feed.created_at.desc())
        )

        # Combine and sort all activities by creation time
        all_activities = list(payment_activities) + list(friend_activities)
        all_activities.sort(key=lambda x: x.created_at, reverse=True)

        return all_activities

    def add_friend(self, friend: "User"):
        """
        Add another user as a friend
        """
        if self == friend:
            raise ValueError("Cannot add yourself as a friend")

        # Create friendship (assuming a many-to-many relationship through a Friendship model)
        Friendship.create(user=self, friend=friend)

        # Add to feed
        Feed.create(
            user=self,
            related_user=friend,
            detail=f"{self.name} and {friend.name} are now friends",
            feed_type="friend_add",
        )

        return {"message": f"Successfully added {friend.name} as a friend"}

    def friends(self):
        """
        Get all friends of the user
        """
        # Friends where current user is the user in the friendship
        friends_as_user = (User
                        .select()
                        .join(Friendship, on=(User.id == Friendship.friend))
                        .where(Friendship.user == self))
        
        # Friends where current user is the friend in the friendship
        friends_as_friend = (User
                            .select()
                            .join(Friendship, on=(User.id == Friendship.user))
                            .where(Friendship.friend == self))
        
        # Combine both queries
        return (friends_as_user | friends_as_friend)


class CreditCard(BaseCreditCard):
    class Meta:
        database = db

    def charge(self, amount: float):
        if self.balance < amount:
            raise ValueError("Insufficient credit card balance")
        self.consumption += amount
        self.balance -= amount
        self.save()
        return True


class Feed(BaseFeed):
    class Meta:
        database = db

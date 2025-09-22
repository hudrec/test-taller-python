from peewee import *

# Database configuration
DATABASE = "minivenmo.db"

# Initialize the database
db = SqliteDatabase(
    DATABASE,
    pragmas={
        "journal_mode": "wal",
        "cache_size": -1 * 64000,  # 64MB
        "foreign_keys": 1,
        "ignore_check_constraints": 0,
        "synchronous": 0,
    },
)


# Define BaseModel here
class BaseModel(Model):
    class Meta:
        database = db


# Define placeholder models for table creation
class User(BaseModel):
    name = CharField()
    balance = FloatField(default=0.0)


class CreditCard(BaseModel):
    user = ForeignKeyField(User, backref="credit_cards")
    number = CharField()
    consumption = FloatField(default=0.0)
    limit = FloatField()
    balance = FloatField()


class Friendship(BaseModel):
    """Model representing a friendship between two users"""

    user = ForeignKeyField(User, backref="friendships")
    friend = ForeignKeyField(User, backref="friend_of")
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        database = db
        # Ensure we don't have duplicate friendships
        indexes = ((("user", "friend"), True),)


class Feed(BaseModel):
    """Model representing user activities in the feed"""

    FEED_TYPES = [("payment", "Payment"), ("friend_add", "Friend Added")]

    user = ForeignKeyField(User, backref="feeds")
    related_user = ForeignKeyField(User, backref="related_feeds", null=True)
    feed_type = CharField(choices=FEED_TYPES, default="payment")
    detail = TextField()
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        database = db


# This will be used to create the database tables
def create_tables():
    try:
        if db.is_closed():
            db.connect()
        with db.atomic():
            db.create_tables([User, CreditCard, Feed, Friendship], safe=True)
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise


# This will be used to close the database connection
def close_connection(exception=None):
    if not db.is_closed():
        db.close()


# This will be used to get a database connection
def get_db():
    if db.is_closed():
        db.connect()
    return db

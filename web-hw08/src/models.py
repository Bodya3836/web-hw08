from mongoengine import (
    Document,
    connect,
    StringField,
    ReferenceField,
    ListField,
    BooleanField,
    CASCADE,
)
import configparser
import pathlib
from bson import json_util

file_config = (
    pathlib.Path(__file__).parent.parent.joinpath("configs").joinpath("config.ini")
)
config = configparser.ConfigParser()
config.read(file_config)

user = config.get("DEV_MONGO_DB", option="USER")
password = config.get("DEV_MONGO_DB", option="PASSWORD")
db = config.get("DEV_MONGO_DB", option="DB_NAME")

uri = f"mongodb+srv://{user}:{password}@cluster0.ae7t2cd.mongodb.net/?retryWrites=true&w=majority"
print(uri)

connect(db=db, host=uri)
print("Connected")


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=120)
    description = StringField()

    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(max_length=15))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()

    meta = {"collection": "qoutes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)


class Contact(Document):
    fullname = StringField(required=True, unique=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    type_of_delivery = StringField(required=True)
    is_delivery = BooleanField(default=False)

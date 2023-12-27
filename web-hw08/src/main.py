import redis
from redis_lru import RedisLRU
from models import Author, Quote
from pprint import pprint

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Finding by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [quote.quote for quote in quotes]

    return result


def find_by_tags(tags: list[str]) -> list[str | None]:
    print(f"Finding by {tags}")
    quotes = []
    for tag in tags:
        q = Quote.objects(tags__iregex=tag)
        result = [quote.quote for quote in q]
        quotes.extend(result)

    return quotes


@cache
def find_by_authors(author: str) -> list[str | None]:
    print(f"Finding by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for author in authors:
        quotes = Quote.objects(author=author)
        result[author.fullname] = [quote.quote for quote in quotes]

    return result


def parse_user_input(user_input):
    if not user_input:
        return "_", None

    user_input_split = user_input.split(": ")
    command = user_input_split[0].lower()

    if len(user_input_split) > 1:
        parameters = user_input_split[1].split(",")
    else:
        parameters = []

    return command, parameters


def handler(command, parameters):
    match command:
        case "name":
            return find_by_authors(*parameters)
        case "tag":
            return find_by_tag(*parameters)
        case "tags":
            return find_by_tags(parameters)
        case "exit":
            return "exit"
        case _:
            return "Wrong command. Try again"


def main():
    while True:
        user_input = input("\nEnter command, example, 'name: Steve Martin'\n>>> ")
        result = handler(*parse_user_input(user_input))

        if result == "exit":
            print("Exit from program.")
            break

        pprint(result)


if __name__ == "__main__":
    # quotes = Quote.objects().all()
    # pprint([quote.to_json() for quote in quotes])
    main()

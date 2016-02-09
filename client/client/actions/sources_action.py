import requests

from ..config import metadata_repository_url


def configure_parser(parser):
    parser.add_argument("query",
                        help="Search for data sources matching this label")


def get_matching_data_sources(query):
    response = requests.get(metadata_repository_url + "/data_sources/search",
                            headers={"accept": "application/json"},
                            params={"q": query})
    return response.json()["data_sources"]


def handle_action(args, parser):
    data_sources = get_matching_data_sources(args.query)
    for source in data_sources:
        print(source["id"], source["label"])

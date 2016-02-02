import requests

from ..config import metadata_repository_url


def configure_parser(parser):
    parser.add_argument("data_source_id",
                        help="ID of data source to get test files for",
                        metavar="data-source-id")


def get_test_files(data_source_id):
    """
    Retrieve test files for a data source from the metadata repository.

    Parameters:
    data_source_id - Integer - ID of data source to get test files for
    """
    response = requests.get("/".join([metadata_repository_url, "data_sources", data_source_id, "test_files"]), headers={
        "accept": "application/json"
    })
    return response.json()["test_files"]


def handle_action(args, parser):
    test_files = get_test_files(args.data_source_id)
    for f in test_files:
        print(f["url"])

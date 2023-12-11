import argparse
import functools
from pprint import pprint

def load_data(args):

    def to_dict(item, keys):
        _dict = {}
        data = item.strip().split(",")
        
        for index, field in enumerate(data):
            _dict[keys[index]] = field
        return _dict

    if (args.b.isdigit() or args.u.isdigit()):
        print("Please enter valid filenames for the books and users databases")
        exit(1)

    with open(f'{args.b}') as library:
        books = library.readlines()
        books_keys = books[0].strip().split(",")

    with open(f'{args.u}') as users_db:
        users = users_db.readlines()
        users_keys = users[0].strip().split(",")

    books_data = {
        'keys': books_keys,
        'data': list(map(functools.partial(to_dict, keys=books_keys), books[1:]))
        }

    users_data = {
        'keys': users_keys, 
        'data': list(map(functools.partial(to_dict, keys=users_keys), users[1:]))
        }
        
    return books_data, users_data

def search(param, db):
    results = []
    return results

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', type=str, required=True, help="books csv file path")
    parser.add_argument('-u', type=str, required=True, help="users csv file path")
    args, _ = parser.parse_known_args()
    return args

def display_result(results):
    if results:
        if "book_id" in results[0].keys():

            headings = ["Book ID", "Author", "Title", "on loan"]
            format_str = "{:<10} {:<30} {:<50} {:<23}"
            print(format_str.format(*headings))
            for result in results:
                print(format_str.format(
                    result["book_id"],
                    f"{result['author_firstname']} {result['author_surname']}",
                    result["title"],
                    "Yes" if result["on_loan_to"] else "No"
                    )
                )
            print('\n')
            return

        if "user_library_number" in results[0].keys():
            headings = ["User ID", "User", "Borrowed Book 1", "Borrowed Book 2", "Borrowed Book 3", "Borrowed Book 4"]
            format_str = "{:<10} {:<30} {:<30} {:<30} {:<30} {:<30}"
            print(format_str.format(*headings))
            for result in results:
                print(format_str.format(
                    result["user_library_number"],
                    f"{result['user_firstname']} {result['user_surname']}",
                    result["books_on_loan1"],
                    result["books_on_loan2"],
                    result["books_on_loan3"],
                    result["books_on_loan4"],
                    )
                )
            print('\n')
            return

    else:
        print("No results\n")

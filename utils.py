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
    #print ("books_data =", books_data)
    #print ("users_data =", users_data)    
    return books_data, users_data


def search(param, db):
    data_db=db.copy()
    print(type(data_db))
    search_field=""
    results = []
    # print(param)
    # print(db)
    if "user_surname" in data_db[-1].keys():
        search_field="user_surname"
    else:
        search_field="author_surname"
    for item in data_db:
        if item[search_field]==param:
            results.append(item)
    return results

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', type=str, required=True, help="books csv file path")
    parser.add_argument('-u', type=str, required=True, help="users csv file path")
    args, _ = parser.parse_known_args()
    return args


def on_exit(books, users, books_file, users_file):

    def write_file(contents, file):
        with open(file, 'w') as fp:
            fp.write(f'{",".join(contents[0].keys())}\n')
            lines = list(map(lambda content: f'{",".join(content.values())}\n', contents))
            for line in lines:
                fp.write(line)

    print("Saving...")
    write_file(books, 'new_'+books_file)
    write_file(users, 'new_'+users_file)
    print("Saved")
    exit(0)


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


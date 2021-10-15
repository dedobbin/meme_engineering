from hash_tagger import get_db_reference
import argparse

parser = argparse.ArgumentParser(description='Hash value.')
parser.add_argument('hash', metavar='H')

args = parser.parse_args()

db = get_db_reference()

a = str(args.hash)

out = db.child('hash_table').order_by_child('hash').equal_to(a).get()

for id, content in out.items():
    print("The hash " + a + " has the description: " + content["description"])
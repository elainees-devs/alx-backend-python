from itertools import islice
from stream_users import stream_users

#iterate over the generator function and print the first 6 rows
for user in islice(stream_users(), 6):
    print(user)

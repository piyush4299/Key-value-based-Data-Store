## Key-value-based-Data-Store ##

It is key value based data store which supports create, read and delete operations on common shared resource(file).

How to run?

 1. clone the repository
 2. install dependencies using requirements.txt
 3. Run initialize.py file.
 4. Inputs are passed through initialize.py file. If wish to change inputs change through this file.

What this repository is about?


It is the key value based datastore which satisfies following features mentioned below:
## Functional requirements:

1. It can be initialized using an optional file path. If one is not provided, it will reliably create itself in a reasonable location on the laptop.
2. A new key-value pair can be added to the data store using the Create operation. The key is always a string - capped at 32 chars. The value is always a JSON object - capped at 16KB.
3. If Create is invoked for an existing key, an appropriate error must be returned.
4. A Read operation on a key can be performed by providing the key, and receiving the value in response, as a JSON object.
5. A Delete operation can be performed by providing the key.
6. Every key supports setting a Time-To-Live property when it is created. This property is optional. If provided, it will be evaluated as an integer defining the number of seconds the key must be retained in the data store. Once the Time-To-Live for a key has expired, the key will no longer be available for Read or Delete operations.
7. Appropriate error responses are returned to a client.

## Non-Functional requirements:

1. The size of the file storing data must never exceed 1GB.
2. More than one client process cannot be allowed to use the same file as a data store at any given time.
3. A client is allowed to access the data store using multiple threads if it desires to.The data store must also be thread-safe.







import hashlib
import threading

user_db = {}  # username: hashed_password

active_users = {}  # username: connection_id

# lock for thread-safety
db_lock = threading.Lock()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# store new user in db with hashed password
def store_user(username: str, password: str):
    with db_lock:
        if username in user_db:
            return "Username already exists"
        # hash and store password 
        user_db[username] = hash_password(password)
        return f"User {username} added successfully"

def verify_user(username: str, password: str) -> bool:
    with db_lock:
        if username not in user_db:
            return False
        # compare hashed password
        return user_db[username] == hash_password(password)

# add to active users with connection id
def add_active_user(username: str, connection_id: int):
    with db_lock:
        if username in active_users:
            return f"User {username} is already active"
        active_users[username] = connection_id
        return f"User {username} is now active with connection id {connection_id}"

def del_active_user(username: str):
    with db_lock:
        if username in active_users:
            del active_users[username]
            return f"User {username} removed from active users"
        else:
            return f"User {username} not found in active users"

# get connection id of active user
def get_cID(username: str):
    with db_lock:
        return active_users.get(username, None)

# lists users if needed
def list_active_users():
    with db_lock:
        return active_users

# simulate segmentation/paging 
def mem_allocation(username: str, block_size: int = 256):
    # simulate segmentation by allocating blocks 
    mem_block = {
        "username": username,
        "block_size": block_size,
        "allocated_data": user_db.get(username, None)
    }
    return mem_block

# simulate retrieving user memory block
def get_user_mem_block(username: str):
    # return user data from 'db'
    if username in user_db:
        return mem_allocation(username)
    else:
        return None
import hashlib

def prompt_nonempty(msg: str) -> str:
    while True:
        s = input(msg).strip()
        if s:
            return s
        print("This field is required.")

def next_id(prefix: str, existing_ids) -> str:
    """
    Generate next ID based on existing keys in dict
    """
    counter = 1
    while f"{prefix}{counter}" in existing_ids:
        counter += 1
    return f"{prefix}{counter}"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
import os
from cryptography.fernet import Fernet

def generate_and_save_key(key_path="secret.key"):
    """Generates a secure key and saves it to a file."""
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    print(f"🔑 New key generated and saved safely to: {key_path}")
    return key

def load_key(key_path="secret.key"):
    """Loads the encryption key from the specified path."""
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Missing key file at {key_path}. Cannot protect/restore files without it.")
    with open(key_path, "rb") as key_file:
        return key_file.read()

def protect_file(file_path, key_path="secret.key"):
    """Converts a file's content into an encrypted, protected format."""
    key = load_key(key_path)
    fernet = Fernet(key)
    
    # Read the original content
    with open(file_path, "rb") as file:
        original_data = file.read()
        
    # Scramble the data
    protected_data = fernet.encrypt(original_data)
    
    # Write to a new protected file
    protected_file_path = file_path + ".protected"
    with open(protected_file_path, "wb") as protected_file:
        protected_file.write(protected_data)
        
    print(f"🔒 File protected successfully! Saved as: {protected_file_path}")
    return protected_file_path

def restore_file(protected_file_path, key_path="secret.key"):
    """Restores a protected file back to its original format."""
    key = load_key(key_path)
    fernet = Fernet(key)
    
    # Read the scrambled content
    with open(protected_file_path, "rb") as protected_file:
        protected_data = protected_file.read()
        
    try:
        # Unscramble the data
        restored_data = fernet.decrypt(protected_data)
    except Exception:
        print("❌ Decryption failed. The key is invalid or the file has been corrupted.")
        return None
        
    # Determine original filename by stripping '.protected'
    if protected_file_path.endswith(".protected"):
        restored_file_path = protected_file_path[:-10]
    else:
        restored_file_path = protected_file_path + ".restored"
        
    # Write the original content back
    with open(restored_file_path, "wb") as restored_file:
        restored_file.write(restored_data)
        
    print(f"🔓 File restored successfully! Saved as: {restored_file_path}")
    return restored_file_path

# --- Demonstration Workflow ---
if __name__ == "__main__":
    # 1. Setup a dummy file to protect
    sample_file = "my_private_notes.txt"
    with open(sample_file, "w") as f:
        f.write("Super secret data: The password to the safe is 12345.")
    
    print(f"Created a sample file for testing: {sample_file}")
    
    # 2. Setup the security key
    # (In real life, do this once and keep the file very safe!)
    generate_and_save_key()
    
    # 3. Protect the file
    protected_path = protect_file(sample_file)
    
    # 4. Simulate losing the original file by deleting it
    os.remove(sample_file)
    print(f"Simulating data loss: Deleted the original {sample_file}")
    
    # 5. Restore the file using the protected version
    restore_file(protected_path)
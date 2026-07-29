import hashlib
import json
from pathlib import Path

FILE = Path('password_manager.json')
# Function to generate hash for password
def create_password(pw: str):
    bytes_data = pw.encode('utf-8')
    hash_result = hashlib.sha256(bytes_data).hexdigest()
    return hash_result

class PasswordManager:
    def __init__(self):
        self.data = None
    def make_master_password(self, pw: str):
        # Deny empty password
        if not pw.strip():
            raise ValueError("Password cannot be empty")
        master_hash = create_password(pw)
        # Create initial data as the syntax for password_manager
        initial = {
            "master_hash": master_hash,
            "credentials": []
        }
        self.data = initial
    def verify_master(self, pw: str) -> bool:
        if self.data == None:
            raise RuntimeError("Data not loaded")
        pw_hash = create_password(pw)
        return pw_hash == self.data["master_hash"]
    def load_data(self):
        try: 
            with FILE.open('r', encoding='utf-8') as f:
                self.data = json.load(f)
        # Handle possible errors that might occured
        except (json.JSONDecodeError, PermissionError, FileNotFoundError):
            raise
    def save_data(self):
        try:
            with FILE.open('w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        # Handle possible errors that might occured
        except (PermissionError, OSError) as e:
            raise
    def add_credential(self, website: str, email: str, pw: str):
        if self.data == None:
            raise RuntimeError("Data not loaded")
        # Strip spaces in input
        website = website.strip()
        email = email.strip()
        pw = pw.strip()
        if not website or not email or not pw:
            raise ValueError("Data input is not valid")
        # Create temporary dict just for the purpose of appending it to json file
        tmp = {"website": website, "email": email, "pw": pw}
        self.data["credentials"].append(tmp)
        # Push changes to json file
        self.save_data()
    def search_credential(self, website: str):
        if self.data == None:
            raise RuntimeError("Data not loaded")
        return [cre for cre in self.data["credentials"] if cre["website"] == website]
    def list_websites(self):
        if self.data == None:
            raise RuntimeError("Data not loaded")
        return [cre["website"] for cre in self.data["credentials"]]
    def delete_credential(self, website: str):
        if self.data == None:
            raise RuntimeError("Data not loaded")
        original_len = len(self.data["credentials"])
        self.data["credentials"] = [cre for cre in self.data["credentials"] if cre["website"] != website]
        self.save_data()
        return len(self.data["credentials"]) != original_len # Tell the user if the data is deleted or not

def main():
    pm = PasswordManager()
    while True:
        try:
            # If load_data raise FileNotFoundError, it means user has no data yet, no master password
            pm.load_data()
            break
        except FileNotFoundError:
            # Use while to loop the users until verification complete
            while True:
                try:
                    master_pw = input("Enter master password: ").strip()
                    verify_pw = input("Please verify your master password: ").strip()
                    # Save the data to json file only if verification is completed
                    if verify_pw == master_pw:
                        pm.make_master_password(master_pw)
                        pm.save_data()
                        print("Success")
                        break
                except ValueError:
                    print("Password cannot be empty")
            break
        except (json.JSONDecodeError, PermissionError) as e:
            print(f"Error detected: {e}")

    while True:
        verify_pw = input("Please enter your master password: ")
        if pm.verify_master(verify_pw.strip()):
            break

    # Create menu loop for the user
    while True:
        print('\n==== Password Manager Menu ====')
        print('1. Add new credential')
        print('2. Search credential by website')
        print('3. List all saved websites')
        print('4. Delete credential')
        print('5. Exit')
        user_choice = input("Enter number from 1-5: ")
        try:
            choice = int(user_choice.strip())
        # Only accept numbers
        except (ValueError):
            print("Only accept number")
            continue
        if choice == 1:
            user_input = input("Input data in this format: website, email, password ").strip()
            if not user_input:
                print("Do not accept empty input")
                continue
            user_data = user_input.split(", ")
            # Not having length of 3 means format not match
            if len(user_data) != 3:
                print("Input format does not match")
                continue
            website, email, password = user_data
            pm.add_credential(website, email, password)
            print("Success")
        elif choice == 2:
            user_input = input("Input website name: ").strip()
            if not user_input:
                continue
            credentials = pm.search_credential(user_input)
            print(credentials)
        elif choice == 3:
            websites = pm.list_websites()
            print(websites)
        elif choice == 4:
            user_input = input("Input website name: ").strip()
            if not user_input:
                continue
            if pm.delete_credential(user_input):
                print("Success")
            else:
                print("Failed")
        elif choice == 5:
            break
        else:
            print("Inputed number is not in the range")
            continue

    
if __name__ == '__main__':
    main()

    
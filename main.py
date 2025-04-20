import json
import sys
import hashlib
import datetime
from json import loads
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': []  # We'll store executed actions here
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

def load_options():
    with open('options.json') as f:
        options_data = loads(f.read())
    return options_data

def execute_action(room_or_option, choice, options_data, blockchain):
    actions = options_data[room_or_option]
    action = actions[int(choice) - 1]
    print(f"Executing action: {action} in {room_or_option}...")
    # Execute the corresponding action here
    # For simplicity, just append the action to the current block's data
    blockchain.chain[-1]['data'].append(action)

# Main function
def main():
    blockchain = Blockchain()
    options_data = load_options()
    while True:
        print("Options:")
        print("1. Enter Rooms")
        print("2. Activities")
        print("3. Other Options")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            room = input("Which Room? (e.g., Kitchen, Bedroom, Bathroom): ").lower()
            if room in options_data['Rooms']:
                room_options = options_data['Rooms'][room]
                print("Room Options:")
                for idx, option in enumerate(room_options, start=1):
                    print(f"{idx}. {option}")
                print(f"{len(room_options) + 1}. Return to main menu")
                room_choice = input("Select an option: ")
                if room_choice.isdigit() and 1 <= int(room_choice) <= len(room_options) + 1:
                    if int(room_choice) == len(room_options) + 1:
                        continue
                    execute_action(room, room_choice, options_data['Rooms'], blockchain)
                else:
                    print("Invalid option.")
            else:
                print("Invalid room.")

        elif choice == '2':
            activity = input("Which Activity? (e.g, Entertainment, Utility): ").lower()
            if activity in options_data['Activities']:
                activity_options = options_data['Activities'][activity]
                print("Activity options:")
                for idx, option in enumerate(activity_options, start=1):
                    print(f"{idx}. {option}")
                print(f"{len(activity_options) + 1}. Return to main menu")
                activity_choice = input("Select an option: ")
                if activity_choice.isdigit() and 1 <= int(activity_choice) <= len(activity_options) + 1:
                    if int(activity_choice) == len(activity_options) + 1:
                        continue
                    execute_action(activity, activity_choice, options_data['Activities'], blockchain)
                else:
                    print("Invalid option.")
            else:
                print("Invalid activity.")

        elif choice == '3':
            category = input("Which category? (e.g., security, outdoor ): ").lower()
            if category in options_data['Other_options']:
                category_options = options_data['Other_options'][category]
                print(f"{category.capitalize()} Options:")
                for idx, option in enumerate(category_options, start=1):
                    print(f"{idx}. {option}")
                print(f"{len(category_options) + 1}. Return to main menu")
                category_choice = input("Select an option: ")
                if category_choice.isdigit() and 1 <= int(category_choice) <= len(category_options) + 1:
                    if int(category_choice) == len(category_options) + 1:
                        continue
                    execute_action(category, category_choice, options_data['Other_options'], blockchain)
                else:
                    print("Invalid option.")
            else:
                print("Invalid category.")

        else:
            print("Have a Good Day")
            sys.exit()

if __name__ == "__main__":
    main()
	            

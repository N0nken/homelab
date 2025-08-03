import time
import datetime
import json

class InventoryItem:
    def __init__(self, name, quantity, expires=None):
        self.name = name
        self.quantity = quantity
        if expires:
            self.expires = expires
        else:
            self.expires = datetime.date.strftime(datetime.date.fromtimestamp(int(time.time()) + 86400 * 7), "%Y-%m-%d")  # Default to 7 days from now
        

class Inventory:
    def __init__(self, name):
        self.name = name
        self.items = []
        saved_inventory = {}
        with open('inventory.json', 'r') as file:
            saved_inventory = json.loads(file.read())
        if not self.name in saved_inventory["inventories"]:
            return
        for item in saved_inventory[self.name]:
            self.items.append(InventoryItem(item['name'], item['quantity'], item['expires']))

    def add_item(self, name, quantity, expires=None):
        for item in self.items:
            if item.name == name and item.expires == expires:
                item.quantity += quantity
                return
        self.items.append(InventoryItem(name, quantity, expires))

    def remove_item(self, name, quantity):
        for item in self.items:
            if item.name == name:
                item.quantity -= quantity
                if item.quantity <= 0:
                    self.items.remove(item)
                return

    def save_inventory(self):
        saved_inventory = {}
        with open('inventory.json', 'r') as file:
            saved_inventory = json.loads(file.read())
        saved_inventory[self.name] = []
        for item in self.items:
            saved_inventory[self.name].append({
                'name': item.name,
                'quantity': item.quantity,
                'expires': item.expires
            })
        with open('inventory.json', 'w') as file:
            file.write(json.dumps(saved_inventory))

    def print_contents(self):
        print(f"Inventory: {self.name}")
        for item in self.items:
            print(f"{item.name}: {item.quantity} (Expires: {item.expires})")

inventory_names = []
inventory_file_content = {}
inventories = {}
with open('inventory.json', 'r') as file:
    inventory_file_content = json.loads(file.read())
inventory_names = inventory_file_content["inventories"]
for inventory_name in inventory_names:
    inventories[inventory_name] = Inventory(inventory_name)

while True:
    print("Available inventories:")
    for name in inventories.keys():
        print(f"- {name}")
    command = input("")
    command_split = command.split(" ")
    if command_split[0] == "exit":
        print("Saving all inventories...")
        for inventory_name in inventory_names:
            inventories[inventory_name].save_inventory()
        print("Inventories saved.\nExiting...")
        break
    elif command_split[0] == "add":
        if len(command_split) < 3:
            print("Usage: add <inventory_name> <item_name> <quantity> [expires]")
            continue
        inventory_name = command_split[1]
        item_name = command_split[2]
        quantity = int(command_split[3])
        expires = None
        if len(command_split) > 4:
            expires = command_split[4]
        if inventory_name in inventory_names:
            inventories[inventory_name].add_item(item_name, quantity, expires)
        else:
            print(f"Inventory '{inventory_name}' does not exist.")
    elif command_split[0] == "remove":
        if len(command_split) < 3:
            print("Usage: remove <inventory_name> <item_name> <quantity>")
            continue
        inventory_name = command_split[1]
        item_name = command_split[2]
        quantity = int(command_split[3])
        if inventory_name in inventories:
            inventories[inventory_name].remove_item(item_name, quantity)
            inventories[inventory_name].save_inventory()
        else:
            print(f"Inventory '{inventory_name}' does not exist.")
    elif command_split[0] == "view":
        if len(command_split) < 2:
            print("Usage: print <inventory_name>")
            continue
        inventory_name = command_split[1]
        if inventory_name in inventories:
            inventories[inventory_name].print_contents()
        else:
            print(f"Inventory '{inventory_name}' does not exist.")
    else:
        print("Unknown command. Available commands: add, remove, view, exit.")
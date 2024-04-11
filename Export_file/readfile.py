import csv
import requests
import json

# Init class def
class Item():
    def __init__(self, item_id, item_name, price, quantity):
        self.item_id = item_id
        self.item_name = item_name
        self.price = price
        self.quantity = quantity


class Order():
    # constructor
    def __init__(self, customer_name, delivery_postal, order_number):
        self.order_number = order_number
        self.customer_name = customer_name
        self.delivery_postal = delivery_postal
        self.item_lines = []
        self.total_price = 0
        # self.unique_item_id = []
        self.unique_items = 0

    def addItem(self, item):
        self.item_lines.append(item)
        # if not item.id in self.unique_item_id: 
        #     self.unique_item_id.append(item.id)

    def countUniqueItems(self):
        unique_items_ids = set(item.item_id for item in self.item_lines)
        return len(unique_items_ids)

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)
# End class def


order_list = []

with open('OrderDetails.csv', 'r') as file:

    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # If first item is "Header"
        if row[0] == 'Header':
            order_number = row[1]
            customer_name = row[2]
            delivery_postal = row[3]
            current_order = Order(customer_name, delivery_postal, order_number)
            order_list.append(current_order)
            print(f"============ Order {order_number} added into list ============")

        # If second item is "Line"
        if row[0] == 'Line':
            target_order = None
            line_order_number = row[1]
            item_id = row[2]
            quantity = row[3]

            for order in order_list:
                if order.order_number == line_order_number:
                    target_order = order
            # print(f"found this {target_order.order_number} to add current item")

            # Define the URL of the API endpoint
            url = f'https://fakestoreapi.com/products/{item_id}'

            # Make a GET request to the API
            response = requests.get(url)

            print("============ Calling FakeStore API to get details ============")
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content
                result = response.json()
                item_name = result['title']
                price = result['price']
                # print(f"============ Adding item [{customer_name}] into [{target_order.order_number}] ============")
                current_item = Item(item_id, item_name, price, quantity)
                target_order.addItem(current_item)
                # print(f"=============================current order {target_order.order_number} have item_lines:==================================")
                # for item in target_order.item_lines:
                #     print(item.customer_name)
                # print(f"=================================================================================================")

            else:
                # If the request was not successful, print an error message
                print(f"Error: {response.status_code}")

for order in order_list:
    total = 0
    for item in order.item_lines:
        total += item.price
    order.total_price = total
    # order.unique_count = len(order.unique_item_id)
    order.unique_items = order.countUniqueItems()

    print(f"Total price {total} for order {order.order_number} and have [{order.unique_items} unique item]")

    json_string = order.toJSON()
    with open(f'./output/order{order.order_number}.json', 'w') as json_file:
        json_file.write(json_string)






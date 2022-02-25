from controller import Controller
from model import Model
from view import View


def main():
    my_items = [
        {"name": "bread", "price": 0.5, "quantity": 20},
        {"name": "milk", "price": 1.0, "quantity": 10},
        {"name": "wine", "price": 10.0, "quantity": 5},
    ]

    c = Controller(Model(my_items), View())
    c.insert_item("chocolate", price=2.0, quantity=10)
    c.show_item("chocolate")
    c.update_item("milk", price=1.2, quantity=20)
    c.update_item("ice cream", price=3.5, quantity=20)


if __name__ == "__main__":
    main()

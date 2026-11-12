class Coffee:
    name = "콩카페"
    count = 0

    def __init__(self, menu, price):
        self.menu = menu
        self.price = price
        Coffee.count += 1

    def show_order(self):
        print(Coffee.name, self.menu, self.price)

    @classmethod
    def show_count(cls):
        print(Coffee.count)

c1 = Coffee("아메리카노", "3500원")
c1.show_order()
c1.show_count()



class Transport:
    def __init__(self, name):
        self.name = name

    # def fare

    def get_name(self):
        return self.name

class Taxi(Transport):
    def __init__(self, km, name="버스"):
        super().__init__(name)
        self.km = km

t = Taxi(5)
print(t.get_name())
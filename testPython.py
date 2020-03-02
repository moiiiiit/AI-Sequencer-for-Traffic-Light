#I was confused on how Python instances work so I did this

class boomer:
    def __init__(self, fruit):
        self.fru = fruit
        self.frui = fruit.copy()


fruits = ['apple', 'banana', 'cherry']
instance1 = boomer(fruits)
instance2 = boomer(fruits)

fruits.pop(0)
print(fruits)


print(instance1.frui)
print(instance2.frui)

print(instance1.fru)
print(instance2.fru)

instance1.frui.pop(0)
instance2.frui.pop(1)

print(instance1.frui)
print(instance2.frui)

print(instance1.fru)
print(instance2.fru)
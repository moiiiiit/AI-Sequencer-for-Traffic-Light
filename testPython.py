class boomer:
    def __init__(self, fruit):

        self.frui = fruit.copy()


fruits = ['apple', 'banana', 'cherry']
instance1 = boomer(fruits)
instance2 = boomer(fruits)

fruits.pop(0)
print(fruits)


print(instance1.frui)
print(instance2.frui)

instance1.frui.pop(0)
instance2.frui.pop(1)

print(instance1.frui)
print(instance2.frui)

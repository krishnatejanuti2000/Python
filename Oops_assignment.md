## 1. What is a class in Python? How do you define and create an object from a class?

A class is a blueprint for creating objects. It contains attributes and methods that define the properties and behavior of an object.

Example:

class Student:
    def display(self):
        print("Student details")

s1 = Student()
s1.display()

Here, `Student` is the class and `s1` is the object created from that class.

---

## 2. Difference between a class and an object

A class is a blueprint, whereas an object is an actual instance of that class.

Example:

class Car:
    def start(self):
        print("Car started")

car1 = Car()

Here:
- `Car` is the class.
- `car1` is the object.
- `start()` is the method of the class.

A class defines what an object should contain, while the object actually uses those properties and methods.

---

## 3. What is `__init__` and `__new__` in Python?

`__new__` is responsible for creating a new object, while `__init__` initializes the object after it has been created.

Example:

class Student:
    def __new__(cls):
        print("Object is being created")
        return super().__new__(cls)

    def __init__(self):
        print("Object is being initialized")

s = Student()

The execution happens approximately like:

__new__() -> creates object
__init__() -> initializes object

---

## 4. Can we create a class without `__init__` and `__new__`?

Yes.

Python automatically provides the required default behavior if we don't define these methods ourselves.

Example:

class Student:
    def display(self):
        print("Hello")

s = Student()
s.display()

This works without explicitly defining `__init__` or `__new__`.

---

## 5. Can we return a value from `__init__`?

No. `__init__` must return `None`.

It is used to initialize an already-created object.

For example, this is incorrect:

class Student:
    def __init__(self):
        return 10

It will raise a `TypeError`.

If we want to control what object is created, `__new__` is the method that is involved in object creation.

---

## 6. What are the 4 fundamental principles of OOPS?

The four main principles are:

1. Encapsulation
2. Inheritance
3. Polymorphism
4. Abstraction

### Encapsulation

Wrapping data and methods together inside a class and controlling access to the data.

### Inheritance

Allowing one class to acquire properties and methods from another class.

### Polymorphism

The same method or interface can behave differently depending on the object.

### Abstraction

Showing only the required functionality and hiding unnecessary implementation details.

---

## 7. What is inheritance? What are the different types?

Inheritance allows a child class to reuse properties and methods of a parent class.

Example:

class Animal:
    def sound(self):
        print("Animal sound")

class Dog(Animal):
    pass

d = Dog()
d.sound()

Types of inheritance in Python:

### 1. Single inheritance

One child inherits from one parent.

class A:
    pass

class B(A):
    pass

### 2. Multiple inheritance

One child inherits from multiple parents.

class A:
    pass

class B:
    pass

class C(A, B):
    pass

### 3. Multilevel inheritance

Inheritance occurs through multiple levels.

class A:
    pass

class B(A):
    pass

class C(B):
    pass

### 4. Hierarchical inheritance

Multiple child classes inherit from the same parent.

class A:
    pass

class B(A):
    pass

class C(A):
    pass

### 5. Hybrid inheritance

A combination of two or more types of inheritance.

---

## 8. What is the use of `super()`?

`super()` is mainly used to access methods or attributes of a parent class from a child class.

Example:

class Parent:
    def display(self):
        print("Parent")

class Child(Parent):
    def display(self):
        super().display()
        print("Child")

c = Child()
c.display()

Output:

Parent
Child

It is especially useful when we want to extend the functionality of a parent method instead of completely replacing it.

---

## 9. What is MRO and how is it related to multiple inheritance?

MRO stands for Method Resolution Order.

It defines the order in which Python searches for a method when multiple classes are involved in inheritance.

Example:

class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        print("B")

class C(B):
    pass

c = C()
c.show()

Python searches according to the MRO:

C -> B -> A -> object

We can check it using:

print(C.mro())

MRO is especially important in multiple inheritance because Python needs a defined order for searching methods.

---

## 10. Implement two classes with the same method name and inherit them in class3

Example:

class Class1:
    def display(self):
        print("Class1")

class Class2:
    def display(self):
        print("Class2")

class Class3(Class1, Class2):
    pass

obj = Class3()
obj.display()

Output:

Class1

Python follows MRO, so `Class1` is checked before `Class2`.

We can check the order using:

print(Class3.mro())

---

## 11. What are class variables and instance variables?

### Class variable

A class variable is shared by all objects of the class.

### Instance variable

An instance variable belongs to a particular object.

Example:

class Student:
    college = "ABC College"

    def __init__(self, name):
        self.name = name

s1 = Student("Ravi")
s2 = Student("Rahul")

Here:

`college` is a class variable.

`name` is an instance variable.

If we change an instance variable for one object, it normally doesn't affect the other object.

---

## 12. What is a static method and class method? When do we use them?

### Static method

A static method does not require `self` or `cls`.

It is normally used when the method is logically related to the class but does not need class or object data.

Example:

class Calculator:

    @staticmethod
    def add(a, b):
        return a + b

print(Calculator.add(10, 20))

### Class method

A class method receives the class as `cls`.

Example:

class Student:
    college = "ABC"

    @classmethod
    def change_college(cls, name):
        cls.college = name

We use class methods when we need to work with class-level data.

---

## 13. What is encapsulation?

Encapsulation means keeping data and the methods that operate on that data together inside a class and controlling direct access to the data.

Example:

class BankAccount:

    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance

The `__balance` variable is private-like and should not be directly modified from outside the class.

---

## 14. What are private, public and protected attributes?

Python uses naming conventions to indicate the intended visibility.

### Public

No underscore is used.

```python
self.name = "Ravi"
````

It can be accessed from outside the class.

### Protected

A single underscore is used.

```python
self._salary = 50000
```

It indicates that the attribute is intended for internal use or subclasses, although Python does not strictly prevent access.

### Private

Double underscore is used.

```python
self.__salary = 50000
```

Python performs name mangling, making direct access from outside more difficult.

---

## 15. What is polymorphism?

Polymorphism means "many forms".

The same method name can behave differently for different objects.

Example:

class Dog:
def sound(self):
print("Bark")

class Cat:
def sound(self):
print("Meow")

animals = [Dog(), Cat()]

for animal in animals:
animal.sound()

The same `sound()` call produces different behavior depending on the object.

---

## 16. Difference between method overloading and method overriding

### Method overloading

Method overloading means having the same method name with different parameter combinations.

Python does not support traditional method overloading like Java.

We can achieve similar behavior using default arguments or `*args`.

Example:

class Calculator:
def add(self, *args):
total = 0

```
    for value in args:
        total += value

    return total
```

### Method overriding

Method overriding happens when a child class provides its own implementation of a method that already exists in the parent class.

Example:

class Animal:
def sound(self):
print("Animal sound")

class Dog(Animal):
def sound(self):
print("Bark")

Here, `Dog` overrides `Animal.sound()`.

---

## 17. What is abstraction? Explain with example

Abstraction means hiding implementation details and exposing only the necessary functionality.

For example, when we use an ATM, we select "Withdraw" without knowing the internal implementation of how the bank processes the transaction.

In Python, abstraction can be implemented using abstract classes.

Example:

from abc import ABC, abstractmethod

class Animal(ABC):

```
@abstractmethod
def sound(self):
    pass
```

class Dog(Animal):

```
def sound(self):
    print("Bark")
```

Here, `Animal` defines what the child class must implement, while `Dog` provides the implementation.

---

## 18. What are getter and setter methods? Why are they important in encapsulation?

Getters are used to read private data and setters are used to modify private data in a controlled way.

Example:

class Student:

```
def __init__(self):
    self.__marks = 0

def get_marks(self):
    return self.__marks

def set_marks(self, marks):
    if marks >= 0 and marks <= 100:
        self.__marks = marks
```

The setter allows us to validate data before changing the private attribute.

This provides controlled access to internal data.

---

## 19. What is the purpose of the `@abstractmethod` decorator?

`@abstractmethod` is used to declare a method that must be implemented by subclasses.

Example:

from abc import ABC, abstractmethod

class Vehicle(ABC):

```
@abstractmethod
def start(self):
    pass
```

A child class must provide an implementation of `start()` before it can be instantiated.

The purpose is to define a common contract for subclasses.

---

## 20. How does Python decide which method to call when a method is inherited from multiple parent classes?

Python uses **MRO — Method Resolution Order**.

Example:

class A:
def show(self):
print("A")

class B(A):
def show(self):
print("B")

class C(A):
def show(self):
print("C")

class D(B, C):
pass

obj = D()
obj.show()

Python follows the MRO of `D`.

We can check it using:

print(D.mro())

The first matching method found in the MRO is called.

---

## 21. What is multiple inheritance? Give a code example using `super()` and MRO

Multiple inheritance means a class inherits from more than one parent class.

Example:

class A:
def show(self):
print("A")
super().show()

class B:
def show(self):
print("B")
super().show()

class C(A, B):
def show(self):
print("C")
super().show()

class ObjectEnd:
def show(self):
print("End")

obj = C()

The important point is that `super()` follows the MRO rather than simply calling a fixed parent.

For a simpler example:

class A:
def show(self):
print("A")

class B:
def show(self):
print("B")

class C(A, B):
pass

print(C.mro())

The MRO determines which `show()` is called.

---

## 22. Can a class inherit from multiple classes?

Yes.

Python supports multiple inheritance.

Example:

class Father:
def skills(self):
print("Driving")

class Mother:
def hobby(self):
print("Painting")

class Child(Father, Mother):
pass

c = Child()

c.skills()
c.hobby()

The `Child` class inherits from both `Father` and `Mother`.

---

## 23. How does Python's garbage collection affect objects?

Python automatically manages memory.

When an object is no longer referenced, its memory can eventually be released.

Python mainly uses reference counting and also has a garbage collector to handle reference cycles.

Example:

class Student:
pass

s = Student()

del s

After deleting the reference, the object may become eligible for memory cleanup if there are no other references to it.

Garbage collection helps prevent memory from being occupied by objects that are no longer needed.

---

## 24. Create a decorator to calculate the actual time taken by the original function

We can create a decorator that records the time before and after the function executes.

Example:

import time

def calculate_time(func):

```
def wrapper(*args, **kwargs):

    start = time.time()

    result = func(*args, **kwargs)

    end = time.time()

    print("Time taken:", end - start)

    return result

return wrapper
```

@calculate_time
def test():
total = 0

```
for i in range(1000000):
    total += i

return total
```

test()

The decorator records the start time, executes the original function, records the end time, and calculates:

end time - start time

This gives the approximate execution time of the function.

---

## 25. Difference between encapsulation and abstraction

### Encapsulation

Encapsulation is mainly about **protecting and controlling access to data**.

Example:

class Bank:
def **init**(self):
self.__balance = 1000

```
def get_balance(self):
    return self.__balance
```

### Abstraction

Abstraction is about **hiding implementation details and exposing only necessary functionality**.

For example, an ATM exposes operations like:

* Withdraw
* Deposit
* Check Balance

The user does not need to know the internal banking implementation.

### Simple difference

Encapsulation → How we protect data.

Abstraction → What we hide and what we expose.

---

## 26. Can we decorate the same function with two different decorators?

Yes.

Multiple decorators can be applied to the same function.

Example:

def decorator1(func):

```
def wrapper():
    print("Decorator 1")
    func()

return wrapper
```

def decorator2(func):

```
def wrapper():
    print("Decorator 2")
    func()

return wrapper
```

@decorator1
@decorator2
def display():
print("Original function")

display()

The decorators are applied from the bottom upward.

So the effective order is:

decorator2 -> decorator1 -> original function

---

# Coding Questions

## 27. Create a Student class

The class should contain:

* Name
* Roll number
* Marks
* Method to display student details

```python
class Student:

    def __init__(self, name, roll_number, marks):
        self.name = name
        self.roll_number = roll_number
        self.marks = marks

    def display(self):
        print("Name:", self.name)
        print("Roll Number:", self.roll_number)
        print("Marks:", self.marks)


s1 = Student("Revanth", 101, 85)

s1.display()
```

Output:

```text
Name: Revanth
Roll Number: 101
Marks: 85
```

Here the constructor initializes the instance variables and `display()` prints the student information.

---

## 28. Create a BankAccount class

The class should contain:

* Account holder name
* Balance
* Deposit
* Withdraw
* Display balance

```python
class BankAccount:

    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def deposit(self, amount):

        if amount > 0:
            self.balance += amount
            print("Amount deposited")
        else:
            print("Invalid amount")

    def withdraw(self, amount):

        if amount <= 0:
            print("Invalid amount")

        elif amount > self.balance:
            print("Insufficient balance")

        else:
            self.balance -= amount
            print("Amount withdrawn")

    def display_balance(self):
        print("Account Holder:", self.name)
        print("Balance:", self.balance)


account = BankAccount("Revanth", 10000)

account.deposit(2000)
account.withdraw(3000)
account.display_balance()
```

The deposit method increases the balance and the withdraw method decreases it after checking whether sufficient balance is available.

---

## 29. Constructors and Instance Variables

### Employee class

The constructor should initialize:

* Employee ID
* Name
* Salary

```python
class Employee:

    def __init__(self, employee_id, name, salary):
        self.employee_id = employee_id
        self.name = name
        self.salary = salary

    def display(self):
        print("Employee ID:", self.employee_id)
        print("Name:", self.name)
        print("Salary:", self.salary)


employee = Employee(101, "Revanth", 50000)

employee.display()
```

### Laptop class

The class should store:

* Brand
* RAM
* Processor

```python
class Laptop:

    def __init__(self, brand, ram, processor):
        self.brand = brand
        self.ram = ram
        self.processor = processor

    def display(self):
        print("Brand:", self.brand)
        print("RAM:", self.ram)
        print("Processor:", self.processor)


laptop = Laptop("Dell", "16GB", "Intel i7")

laptop.display()
```

In both classes, the constructor initializes the instance variables when the object is created.

---

# 30. Encapsulation

## ATM class

The balance should be private and money should be deposited and withdrawn safely.

```python
class ATM:

    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):

        if amount > 0:
            self.__balance += amount
            print("Deposit successful")
        else:
            print("Invalid amount")

    def withdraw(self, amount):

        if amount <= 0:
            print("Invalid amount")

        elif amount > self.__balance:
            print("Insufficient balance")

        else:
            self.__balance -= amount
            print("Withdrawal successful")

    def display_balance(self):
        print("Balance:", self.__balance)


atm = ATM(10000)

atm.deposit(2000)
atm.withdraw(3000)
atm.display_balance()
```

Here `__balance` is private-like. The user cannot directly change it through the normal attribute name.

The methods provide controlled access to the balance.

---

## Password Manager

The password should be stored as a private attribute.

```python
class PasswordManager:

    def __init__(self, password):
        self.__password = password

    def update_password(self, new_password):
        if len(new_password) >= 8:
            self.__password = new_password
            print("Password updated")
        else:
            print("Password should contain at least 8 characters")

    def validate_password(self, password):

        if password == self.__password:
            print("Password is correct")
        else:
            print("Invalid password")


manager = PasswordManager("password123")

manager.validate_password("password123")

manager.update_password("newpassword123")

manager.validate_password("newpassword123")
```

The password is private and is accessed only through methods.

---

## Student with private marks, getter and setter

```python
class Student:

    def __init__(self, marks):
        self.__marks = marks

    def get_marks(self):
        return self.__marks

    def set_marks(self, marks):

        if marks >= 0 and marks <= 100:
            self.__marks = marks
        else:
            print("Invalid marks")


student = Student(80)

print(student.get_marks())

student.set_marks(90)

print(student.get_marks())
```

The getter reads the private value and the setter updates it after validation.

---

# 31. Inheritance

## Animal, Dog and Cat

Create a parent class `Animal` with `sound()` and override it in `Dog` and `Cat`.

```python
class Animal:

    def sound(self):
        print("Animal makes a sound")


class Dog(Animal):

    def sound(self):
        print("Dog barks")


class Cat(Animal):

    def sound(self):
        print("Cat meows")


dog = Dog()
cat = Cat()

dog.sound()
cat.sound()
```

Here:

* `Animal` is the parent class.
* `Dog` and `Cat` are child classes.
* Both children inherit from `Animal`.
* Both override the `sound()` method.

This is an example of **inheritance and method overriding**.

---

## Vehicle and Bike

Create a `Vehicle` class with speed and fuel, then create `Bike` as a child class.

```python
class Vehicle:

    def __init__(self, speed, fuel):
        self.speed = speed
        self.fuel = fuel

    def display(self):
        print("Speed:", self.speed)
        print("Fuel:", self.fuel)


class Bike(Vehicle):

    def __init__(self, speed, fuel, brand):
        super().__init__(speed, fuel)
        self.brand = brand

    def display_bike(self):
        print("Brand:", self.brand)
        print("Speed:", self.speed)
        print("Fuel:", self.fuel)


bike = Bike(100, "Petrol", "Honda")

bike.display_bike()
```

Here `Bike` inherits the `speed` and `fuel` attributes from `Vehicle`.

`super()` is used to call the parent class constructor.

---

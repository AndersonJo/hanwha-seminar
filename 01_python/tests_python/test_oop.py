import pytest
import math
from abc import ABC, abstractmethod


# =============================================================================
# 섹션 1: BankAccount 클래스
# 아래 클래스 골격을 완성하세요.
# =============================================================================

class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> float:
        """
        amount만큼 입금합니다.
        잔액을 업데이트하고 새로운 잔액을 반환하세요.
        amount가 0 이하이면 ValueError를 발생시키세요.
        """
        if amount <= 0:
            raise ValueError()
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        """
        amount만큼 출금합니다.
        잔액을 업데이트하고 새로운 잔액을 반환하세요.
        잔액이 부족하면 ValueError를 발생시키세요.
        amount가 0 이하이면 ValueError를 발생시키세요.
        """
        if amount <= 0:
            raise ValueError()
        if amount > self.balance:
            raise ValueError()
        self.balance -= amount
        return self.balance

    def __str__(self) -> str:
        """
        "BankAccount(owner=Alice, balance=100.0)" 형식의 문자열을 반환하세요.
        """
        return f"BankAccount(owner={self.owner}, balance={self.balance})"


def test_bank_account_initial_state():
    acc = BankAccount("Alice", 100.0)
    assert acc.owner == "Alice"
    assert acc.balance == 100.0


def test_bank_account_deposit():
    acc = BankAccount("Alice", 100.0)
    new_balance = acc.deposit(50.0)
    assert new_balance == 150.0
    assert acc.balance == 150.0


def test_bank_account_withdraw():
    acc = BankAccount("Alice", 100.0)
    new_balance = acc.withdraw(30.0)
    assert new_balance == 70.0
    assert acc.balance == 70.0


def test_bank_account_insufficient_funds():
    acc = BankAccount("Alice", 50.0)
    with pytest.raises(ValueError):
        acc.withdraw(100.0)


def test_bank_account_invalid_amount():
    acc = BankAccount("Alice", 100.0)
    with pytest.raises(ValueError):
        acc.deposit(-10.0)
    with pytest.raises(ValueError):
        acc.withdraw(0)


def test_bank_account_str():
    acc = BankAccount("Alice", 100.0)
    s = str(acc)
    assert "Alice" in s
    assert "100" in s


# =============================================================================
# 섹션 2: 상속 & 다형성 — Animal / Dog / Cat
# =============================================================================

class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name})"


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name)
        self.indoor = indoor

    def speak(self) -> str:
        return "Meow!"


def test_dog_basic():
    d = Dog("Rex")
    assert d.name == "Rex"
    assert d.speak() == "Woof!"


def test_cat_basic():
    c = Cat("Luna")
    assert c.name == "Luna"
    assert c.speak() == "Meow!"
    assert c.indoor is True


def test_cat_outdoor():
    c = Cat("Tiger", indoor=False)
    assert c.indoor is False


def test_polymorphism():
    animals = [Dog("Rex"), Cat("Luna")]
    sounds = [a.speak() for a in animals]
    assert sounds == ["Woof!", "Meow!"]


def test_isinstance_check():
    d = Dog("Rex")
    c = Cat("Luna")
    assert isinstance(d, Animal)
    assert isinstance(c, Animal)


def test_animal_speak_raises():
    class UnknownAnimal(Animal):
        pass
    a = UnknownAnimal("X")
    with pytest.raises(NotImplementedError):
        a.speak()


def test_repr_contains_name():
    d = Dog("Rex")
    assert "Rex" in repr(d)


# =============================================================================
# 섹션 3: 추상 클래스 — Shape / Rectangle / Circle
# =============================================================================

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self) -> str:
        # 이미 구현된 메서드입니다 — 수정하지 마세요.
        return f"넓이: {self.area():.4f}, 둘레: {self.perimeter():.4f}"


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * (self.radius ** 2)

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


def test_rectangle_area():
    r = Rectangle(4, 5)
    assert r.area() == 20.0


def test_rectangle_perimeter():
    r = Rectangle(4, 5)
    assert r.perimeter() == 18.0


def test_circle_area():
    c = Circle(3)
    assert abs(c.area() - math.pi * 9) < 1e-6


def test_circle_perimeter():
    c = Circle(3)
    assert abs(c.perimeter() - 2 * math.pi * 3) < 1e-6


def test_shape_cannot_instantiate():
    with pytest.raises(TypeError):
        Shape()


def test_describe_contains_numbers():
    r = Rectangle(3, 4)
    desc = r.describe()
    assert "12" in desc   # 넓이
    assert "14" in desc   # 둘레


# =============================================================================
# 섹션 4: 캡슐화 & 프로퍼티 — Temperature
# =============================================================================

class Temperature:
    ABSOLUTE_ZERO = -273.15

    def __init__(self, celsius: float):
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        if value < self.ABSOLUTE_ZERO:
            raise ValueError()
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self.celsius * 9 / 5 + 32


def test_temperature_celsius_init():
    t = Temperature(100.0)
    assert t.celsius == 100.0


def test_temperature_fahrenheit_zero():
    t = Temperature(0.0)
    assert abs(t.fahrenheit - 32.0) < 1e-6


def test_temperature_fahrenheit_hundred():
    t = Temperature(100.0)
    assert abs(t.fahrenheit - 212.0) < 1e-6


def test_temperature_setter():
    t = Temperature(20.0)
    t.celsius = -10.0
    assert t.celsius == -10.0
    assert abs(t.fahrenheit - 14.0) < 1e-6


def test_temperature_invalid_init():
    with pytest.raises(ValueError):
        Temperature(-300.0)


def test_temperature_invalid_setter():
    t = Temperature(20.0)
    with pytest.raises(ValueError):
        t.celsius = -274.0


def test_temperature_boundary():
    # 절대 영도 정확히는 허용
    t = Temperature(-273.15)
    assert t.celsius == -273.15


# =============================================================================
# 섹션 5: 매직 메서드 — Vector
# =============================================================================

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y

    def __abs__(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __repr__(self) -> str:
        return f"Vector(x={self.x}, y={self.y})"


def test_vector_add():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    v3 = v1 + v2
    assert v3.x == 4
    assert v3.y == 6


def test_vector_mul():
    v = Vector(2, 3)
    v2 = v * 3
    assert v2.x == 6
    assert v2.y == 9


def test_vector_eq():
    assert Vector(1, 2) == Vector(1, 2)
    assert Vector(1, 2) != Vector(1, 3)
    assert Vector(0, 0) != "not a vector"


def test_vector_abs():
    v = Vector(3, 4)
    assert abs(v) == 5.0


def test_vector_abs_origin():
    v = Vector(0, 0)
    assert abs(v) == 0.0


def test_vector_repr():
    v = Vector(1, 2)
    r = repr(v)
    assert "1" in r
    assert "2" in r


def test_vector_chaining():
    v = Vector(1, 0)
    result = (v + Vector(0, 1)) * 3
    assert result.x == 3
    assert result.y == 3

import pytest
from abc import ABC, abstractmethod


# =============================================================================
# S — Single Responsibility Principle (단일 책임 원칙)
#
# [나쁜 예시 - 이해를 위해 주석으로만 제공]
# class UserManager:
#     def create_user(self, user_id, data): ...  # DB 저장
#     def send_welcome_email(self, email): ...   # 이메일 발송
#     def log_action(self, action): ...          # 로그 기록
#
# [할 일] 세 가지 책임을 분리하세요.
# =============================================================================

class UserRepository:
    """사용자 데이터 저장/조회만 담당합니다."""

    def __init__(self):
        self._store = {}

    def save(self, user_id: str, data: dict) -> None:
        """
        user_id를 키로 data 딕셔너리를 저장하세요.
        """
        self._store[user_id] = data

    def find(self, user_id: str) -> dict:
        """
        user_id로 저장된 data를 반환하세요.
        없으면 None을 반환하세요.
        """
        return self._store.get(user_id)


class EmailService:
    """이메일 발송만 담당합니다."""

    def __init__(self):
        self._sent = []

    def send_welcome(self, email: str) -> None:
        """
        email을 self._sent 리스트에 추가하세요.
        """
        self._sent.append(email)


class Logger:
    """로그 기록만 담당합니다."""

    def __init__(self):
        self._logs = []

    def log(self, message: str) -> None:
        """
        message를 self._logs 리스트에 추가하세요.
        """
        self._logs.append(message)


def test_srp_user_repository_save_and_find():
    repo = UserRepository()
    repo.save("u1", {"name": "Alice", "email": "alice@test.com"})
    result = repo.find("u1")
    assert result is not None
    assert result["name"] == "Alice"


def test_srp_user_repository_not_found():
    repo = UserRepository()
    assert repo.find("nonexistent") is None


def test_srp_email_service():
    svc = EmailService()
    svc.send_welcome("alice@test.com")
    svc.send_welcome("bob@test.com")
    assert "alice@test.com" in svc._sent
    assert "bob@test.com" in svc._sent
    assert len(svc._sent) == 2


def test_srp_logger():
    logger = Logger()
    logger.log("user created")
    logger.log("email sent")
    assert len(logger._logs) == 2
    assert "user created" in logger._logs[0]


# =============================================================================
# O — Open/Closed Principle (개방-폐쇄 원칙)
#
# [나쁜 예시]
# def calculate_discount(order_type, amount):
#     if order_type == "regular": return amount * 0.05
#     elif order_type == "premium": return amount * 0.10
#     # 새 타입 추가 시 이 함수를 수정해야 함!
#
# [할 일] 전략 패턴으로 리팩토링하세요.
#         Order 클래스는 수정 없이 새로운 DiscountStrategy를 받을 수 있어야 합니다.
# =============================================================================

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        """할인 금액을 반환합니다."""
        pass


class RegularDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.05


class PremiumDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.10


class VIPDiscount(DiscountStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.20


class Order:
    def __init__(self, amount: float, discount_strategy: DiscountStrategy):
        self.amount = amount
        self.discount_strategy = discount_strategy

    def final_price(self) -> float:
        return self.amount - self.discount_strategy.calculate(self.amount)


def test_ocp_regular_discount():
    order = Order(1000.0, RegularDiscount())
    assert order.final_price() == 950.0


def test_ocp_premium_discount():
    order = Order(1000.0, PremiumDiscount())
    assert order.final_price() == 900.0


def test_ocp_vip_discount():
    order = Order(1000.0, VIPDiscount())
    assert order.final_price() == 800.0


def test_ocp_extensible_without_modification():
    """기존 코드를 전혀 수정하지 않고 새 할인 전략을 추가할 수 있어야 합니다."""
    class StudentDiscount(DiscountStrategy):
        def calculate(self, amount: float) -> float:
            return amount * 0.15

    order = Order(1000.0, StudentDiscount())
    assert order.final_price() == 850.0


# =============================================================================
# L — Liskov Substitution Principle (리스코프 치환 원칙)
#
# [나쁜 예시]
# class Bird:
#     def fly(self): return "날고 있습니다."
# class Penguin(Bird):
#     def fly(self): raise Exception("펭귄은 날 수 없습니다!")  # LSP 위반!
#
# [할 일] Bird 계층을 FlyingBird / SwimmingBird 로 올바르게 분리하세요.
#         make_move(bird)는 어떤 Bird 서브클래스를 받아도 예외 없이 동작해야 합니다.
# =============================================================================

class Bird(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def move(self) -> str:
        pass


class FlyingBird(Bird):
    def move(self) -> str:
        return f"{self.name} is flying"


class SwimmingBird(Bird):
    def move(self) -> str:
        return f"{self.name} is swimming"


class Eagle(FlyingBird):
    pass   # FlyingBird에서 move()를 상속받습니다.


class Penguin(SwimmingBird):
    pass   # SwimmingBird에서 move()를 상속받습니다.


def make_move(bird: Bird) -> str:
    """어떤 Bird 서브클래스도 예외 없이 처리합니다."""
    return bird.move()


def test_lsp_eagle_can_move():
    eagle = Eagle("Eagle")
    result = make_move(eagle)
    assert "Eagle" in result
    assert "flying" in result


def test_lsp_penguin_can_move():
    penguin = Penguin("Pingu")
    result = make_move(penguin)
    assert "Pingu" in result
    assert "swimming" in result


def test_lsp_substitutability():
    """모든 Bird 서브클래스가 예외 없이 make_move()를 호출할 수 있어야 합니다."""
    birds = [Eagle("Eagle"), Penguin("Pingu")]
    results = [make_move(b) for b in birds]
    assert len(results) == 2
    assert all(isinstance(r, str) for r in results)


def test_lsp_type_hierarchy():
    assert isinstance(Eagle("E"), Bird)
    assert isinstance(Penguin("P"), Bird)


# =============================================================================
# I — Interface Segregation Principle (인터페이스 분리 원칙)
#
# [나쁜 예시]
# class IWorker(ABC):
#     def work(self): ...
#     def eat(self): ...   # 로봇에게 강요!
#     def sleep(self): ... # 로봇에게 강요!
#
# [할 일] 인터페이스를 IWorkable / IEatable / ISleepable 로 분리하고
#         HumanWorker와 RobotWorker를 구현하세요.
# =============================================================================

class IWorkable(ABC):
    @abstractmethod
    def work(self) -> str:
        pass


class IEatable(ABC):
    @abstractmethod
    def eat(self, food: str) -> str:
        pass


class ISleepable(ABC):
    @abstractmethod
    def sleep(self, hours: int) -> str:
        pass


class HumanWorker(IWorkable, IEatable, ISleepable):
    def __init__(self, name: str):
        self.name = name

    def work(self) -> str:
        return f"{self.name} is working"

    def eat(self, food: str) -> str:
        return f"{self.name} is eating {food}"

    def sleep(self, hours: int) -> str:
        return f"{self.name} is sleeping for {hours} hours"


class RobotWorker(IWorkable):
    def __init__(self, model: str):
        self.model = model

    def work(self) -> str:
        return f"Robot {self.model} is working"


def test_isp_human_all_behaviors():
    h = HumanWorker("Alice")
    assert "Alice" in h.work()
    assert "pizza" in h.eat("pizza")
    assert "8" in h.sleep(8)


def test_isp_robot_only_works():
    r = RobotWorker("R2D2")
    assert "R2D2" in r.work()


def test_isp_robot_interface_check():
    r = RobotWorker("HAL")
    assert isinstance(r, IWorkable)
    assert not isinstance(r, IEatable)
    assert not isinstance(r, ISleepable)


def test_isp_human_interface_check():
    h = HumanWorker("Bob")
    assert isinstance(h, IWorkable)
    assert isinstance(h, IEatable)
    assert isinstance(h, ISleepable)


# =============================================================================
# D — Dependency Inversion Principle (의존성 역전 원칙)
#
# [나쁜 예시]
# class NotificationService:
#     def __init__(self):
#         self.sender = EmailSender()  # 구체 구현에 직접 의존!
#
# [할 일] INotificationSender 인터페이스를 정의하고,
#         NotificationService가 추상화에만 의존하도록 구현하세요.
# =============================================================================

class INotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass


class EmailSender(INotificationSender):
    def __init__(self):
        self._sent = []

    def send(self, recipient: str, message: str) -> bool:
        self._sent.append((recipient, message))
        return True


class SMSSender(INotificationSender):
    def __init__(self):
        self._sent = []

    def send(self, recipient: str, message: str) -> bool:
        self._sent.append((recipient, message))
        return True


class NotificationService:
    def __init__(self, sender: INotificationSender):
        self.sender = sender

    def notify(self, recipient: str, message: str) -> bool:
        return self.sender.send(recipient, message)


def test_dip_email_sender():
    sender = EmailSender()
    svc = NotificationService(sender)
    result = svc.notify("user@test.com", "Hello!")
    assert result is True
    assert len(sender._sent) == 1
    assert sender._sent[0] == ("user@test.com", "Hello!")


def test_dip_sms_sender():
    sender = SMSSender()
    svc = NotificationService(sender)
    result = svc.notify("+82-10-1234-5678", "Hello!")
    assert result is True
    assert len(sender._sent) == 1


def test_dip_swappable_senders():
    """NotificationService를 수정하지 않고 구현체를 자유롭게 교체할 수 있어야 합니다."""
    for SenderClass in [EmailSender, SMSSender]:
        sender = SenderClass()
        svc = NotificationService(sender)
        assert svc.notify("recipient", "msg") is True
        assert len(sender._sent) == 1


def test_dip_multiple_notifications():
    sender = EmailSender()
    svc = NotificationService(sender)
    svc.notify("a@test.com", "msg1")
    svc.notify("b@test.com", "msg2")
    assert len(sender._sent) == 2

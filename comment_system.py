from typing import List, Optional

class Comment:
    """
    Клас для представлення коментаря в ієрархічній системі коментарів.
    Підтримує вкладені відповіді та операції додавання/видалення коментарів.
    """
    
    def __init__(self, text: str, author: str) -> None:
        """
        Ініціалізує новий коментар.
        
        Args:
            text: Текст коментаря
            author: Автор коментаря
        """
        self.text: str = text
        self.author: str = author
        self.replies: List['Comment'] = []
        self.is_deleted: bool = False
    
    def add_reply(self, reply: 'Comment') -> None:
        """
        Додає відповідь до поточного коментаря.
        
        Args:
            reply: Коментар-відповідь для додавання
        """
        if not isinstance(reply, Comment):
            raise TypeError("Відповідь має бути екземпляром класу Comment")
        
        self.replies.append(reply)
    
    def remove_reply(self) -> None:
        """
        Видаляє поточний коментар, замінюючи його текст на стандартне повідомлення.
        
        Встановлює прапорець is_deleted в True, змінює текст на повідомлення про видалення
        та очищує інформацію про автора. Відповіді зберігаються для підтримки цілісності ієрархії.
        """
        self.text = "Цей коментар було видалено."
        self.author = ""  # Очищуємо інформацію про автора
        self.is_deleted = True
    
    def display(self, indent_level: int = 0) -> None:
        """
        Рекурсивно виводить коментар та всі його відповіді з відступами.
        
        Args:
            indent_level: Рівень вкладеності для відступів (внутрішній параметр)
        """
        indent = "    " * indent_level
        
        # Для видалених коментарів не показуємо автора
        if self.is_deleted:
            print(f"{indent}{self.text}")
        else:
            print(f"{indent}{self.author}: {self.text}")
        
        # Рекурсивно виводимо всі відповіді
        for reply in self.replies:
            reply.display(indent_level + 1)
    
    def get_reply_count(self) -> int:
        """
        Повертає загальну кількість відповідей (включаючи вкладені).
        
        Returns:
            Загальна кількість відповідей у всій ієрархії
        """
        total = len(self.replies)
        for reply in self.replies:
            total += reply.get_reply_count()
        return total
    
    def find_replies_by_author(self, author: str) -> List['Comment']:
        """
        Знаходить всі відповіді конкретного автора в ієрархії.
        
        Args:
            author: Ім'я автора для пошуку
            
        Returns:
            Список коментарів зазначеного автора
        """
        found_replies = []
        
        for reply in self.replies:
            if reply.author == author and not reply.is_deleted:
                found_replies.append(reply)
            found_replies.extend(reply.find_replies_by_author(author))
        
        return found_replies

# Тести для перевірки коректності реалізації
def test_comment_system():
    """Базові тести для перевірки функціональності системи коментарів."""
    
    # Тест 1: Створення коментаря
    comment = Comment("Тестовий коментар", "Тестер")
    assert comment.text == "Тестовий коментар"
    assert comment.author == "Тестер"
    assert len(comment.replies) == 0
    assert not comment.is_deleted
    
    # Тест 2: Додавання відповіді
    reply = Comment("Відповідь", "Інший автор")
    comment.add_reply(reply)
    assert len(comment.replies) == 1
    assert comment.replies[0] == reply
    
    # Тест 3: Видалення коментаря
    reply.remove_reply()
    assert reply.is_deleted
    assert reply.text == "Цей коментар було видалено."
    
    # Тест 4: Підрахунок відповідей
    nested_reply = Comment("Вкладена відповідь", "Третій автор")
    reply.add_reply(nested_reply)
    assert comment.get_reply_count() == 2
    
    print("Всі тести пройдено успішно!")

# Демонстрація використання
if __name__ == "__main__":
    test_comment_system()

    print("=== Демонстрація системи коментарів ===\n")
    
    # Створення основного коментаря
    root_comment = Comment("Яка чудова книга!", "Бодя")
    
    # Створення відповідей
    reply1 = Comment("Книга повне розчарування :(", "Андрій")
    reply2 = Comment("Що в ній чудового?", "Марина")
    
    # Додавання відповідей до основного коментаря
    root_comment.add_reply(reply1)
    root_comment.add_reply(reply2)
    
    # Створення відповіді до відповіді
    reply1_1 = Comment("Не книжка, а перевели купу паперу ні нащо...", "Сергій")
    reply1.add_reply(reply1_1)
    
    # Видалення коментаря
    reply1.remove_reply()
    
    # Виведення ієрархії коментарів
    print("Структура коментарів:")
    root_comment.display()
    
    print(f"\nЗагальна кількість відповідей: {root_comment.get_reply_count()}")
    
    # Додаткова демонстрація функціональності
    print("\n=== Додаткова демонстрація ===")
    
    # Додавання ще кількох коментарів
    reply3 = Comment("Я згоден з Бодею!", "Олексій")
    reply2_1 = Comment("Сюжет цікавий, але стиль написання не дуже", "Марина")
    
    root_comment.add_reply(reply3)
    reply2.add_reply(reply2_1)
    
    print("\nОновлена структура:")
    root_comment.display()
    
    # Пошук коментарів конкретного автора
    marina_comments = root_comment.find_replies_by_author("Марина")
    print(f"\nКоментарі від Марини ({len(marina_comments)}):")
    for comment in marina_comments:
        print(f"  - {comment.text}")
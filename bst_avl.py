import random
import time
import matplotlib.pyplot as plt
from typing import Optional, Callable, Tuple

# -----------------------------
# BST реалізація
# -----------------------------
class BSTNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None
        self.count = 1

class BST:
    def __init__(self) -> None:
        self.root: Optional[BSTNode] = None

    def insert(self, value: int) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node: Optional[BSTNode], value: int) -> BSTNode:
        if node is None:
            return BSTNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            node.count += 1
        return node

    def get_max(self) -> int:
        if self.root is None:
            raise ValueError("Дерево порожнє")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.value

    def get_min(self) -> int:
        if self.root is None:
            raise ValueError("Дерево порожнє")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.value

    def get_sum(self) -> int:
        def _sum(node: Optional[BSTNode]) -> int:
            if node is None:
                return 0
            return node.value * node.count + _sum(node.left) + _sum(node.right)
        return _sum(self.root)

# -----------------------------
# AVL реалізація
# -----------------------------
class AVLNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height = 1
        self.count = 1

class AVL:
    def __init__(self) -> None:
        self.root: Optional[AVLNode] = None

    def insert(self, value: int) -> None:
        self.root = self._insert(self.root, value)

    def _insert(self, node: Optional[AVLNode], value: int) -> AVLNode:
        if node is None:
            return AVLNode(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            node.count += 1
            return node

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._get_balance(node)

        if balance > 1 and value < node.left.value:
            return self._right_rotate(node)
        if balance < -1 and value > node.right.value:
            return self._left_rotate(node)
        if balance > 1 and value > node.left.value:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and value < node.right.value:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        return self._height(node.left) - self._height(node.right) if node else 0

    def _left_rotate(self, z: AVLNode) -> AVLNode:
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def _right_rotate(self, z: AVLNode) -> AVLNode:
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def get_max(self) -> int:
        if self.root is None:
            raise ValueError("Дерево порожнє")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.value

    def get_min(self) -> int:
        if self.root is None:
            raise ValueError("Дерево порожнє")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.value

    def get_sum(self) -> int:
        def _sum(node: Optional[AVLNode]) -> int:
            if node is None:
                return 0
            return node.value * node.count + _sum(node.left) + _sum(node.right)
        return _sum(self.root)

    def verify_avl_property(self) -> bool:
        def check_node(node: Optional[AVLNode]) -> Tuple[bool, int]:
            if node is None:
                return True, 0
            left_ok, left_height = check_node(node.left)
            right_ok, right_height = check_node(node.right)
            balanced = abs(left_height - right_height) <= 1
            height = 1 + max(left_height, right_height)
            return left_ok and right_ok and balanced, height

        ok, _ = check_node(self.root)
        return ok

# -----------------------------
# Benchmarking
# -----------------------------
def benchmark_operation(tree_class: Callable, data: list[int]) -> Tuple[float, float, float]:
    tree = tree_class()
    for value in data:
        tree.insert(value)

    start = time.perf_counter()
    tree.get_max()
    max_time = time.perf_counter() - start

    start = time.perf_counter()
    tree.get_min()
    min_time = time.perf_counter() - start

    start = time.perf_counter()
    tree.get_sum()
    sum_time = time.perf_counter() - start

    return max_time, min_time, sum_time

def run_benchmark(n: int = 100_000, seed: int = 42) -> None:
    random.seed(seed)
    data = [random.randint(1, 100_000) for _ in range(n)]

    bst_times = benchmark_operation(BST, data)
    avl_times = benchmark_operation(AVL, data)

    print(f"Benchmark on {n} elements:")
    print(f"{'Operation':<15} {'BST (s)':>10} {'AVL (s)':>10}")
    for name, b, a in zip(['get_max', 'get_min', 'get_sum'], bst_times, avl_times):
        print(f"{name:<15} {b:>10.6f} {a:>10.6f}")

    labels = ['get_max', 'get_min', 'get_sum']
    x = range(len(labels))
    width = 0.35
    plt.figure(figsize=(8, 4))
    plt.bar(x, bst_times, width=width, label='BST')
    plt.bar([i + width for i in x], avl_times, width=width, label='AVL')
    plt.xticks([i + width / 2 for i in x], labels)
    plt.ylabel("Time (s)")
    plt.title("BST vs AVL Operation Benchmark (n=100,000)")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Тестування BST та AVL з набором значень та дублями
    values = [5, 3, 7, 2, 4, 6, 8, 5]
    bst = BST()
    avl = AVL()
    for v in values:
        bst.insert(v)
        avl.insert(v)

    # Найбільше, найменше, сума
    assert bst.get_max() == 8
    assert bst.get_min() == 2
    assert bst.get_sum() == sum(values)

    assert avl.get_max() == 8
    assert avl.get_min() == 2
    assert avl.get_sum() == sum(values)

    # Окремо: дерево з одного елемента
    bst_single = BST(); avl_single = AVL()
    bst_single.insert(10); avl_single.insert(10)
    assert bst_single.get_max() == 10
    assert bst_single.get_min() == 10
    assert bst_single.get_sum() == 10
    assert avl_single.get_max() == 10
    assert avl_single.get_min() == 10
    assert avl_single.get_sum() == 10

    # Перевірка дубліката
    bst_dup = BST(); avl_dup = AVL()
    bst_dup.insert(5); avl_dup.insert(5)
    bst_dup.insert(5); avl_dup.insert(5)  # вставка другого '5'
    assert bst_dup.get_sum() == 10
    assert avl_dup.get_sum() == 10

    print("Усі тести пройдено успішно!")

    # Запуск бенчмарку
    run_benchmark()
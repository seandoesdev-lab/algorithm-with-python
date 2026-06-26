"""
Day 15 - 자료구조 종합 복습 (Data Structures Review) 예제 모음
--------------------------------------------------
실행:  PYTHONIOENCODING=cp949 python examples.py

Phase 1 의 9개 자료구조를 "신호 -> 자료구조" 관점으로 다시 묶는다.
콘솔 출력 문자열은 cp949 안전 문자만 사용한다(ASCII =,-,O,X). 한글은 OK.
표준 라이브러리만 사용한다.
"""

from collections import deque, Counter
import heapq


# ---------------------------------------------------------
# 1) 스택(Stack, LIFO): "가장 최근 것 먼저" - 괄호 짝 맞추기
# ---------------------------------------------------------
def valid_parentheses(s):
    pair = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in s:
        if ch in '([{':
            stack.append(ch)
        else:
            if not stack or stack.pop() != pair[ch]:
                return False
    return not stack


# ---------------------------------------------------------
# 2) 큐(Queue, FIFO): "먼저 온 것 먼저" - deque 로 O(1)
#    list.pop(0) 은 O(n) 이므로 큐에는 절대 쓰지 않는다.
# ---------------------------------------------------------
def queue_demo(items):
    q = deque()
    order = []
    for x in items:
        q.append(x)          # 뒤로 넣기 O(1)
    while q:
        order.append(q.popleft())   # 앞에서 빼기 O(1)
    return order             # 들어온 순서 그대로


# ---------------------------------------------------------
# 3) 덱(Deque): 양끝에서 넣고 빼기 - 회문(palindrome) 검사
# ---------------------------------------------------------
def is_palindrome(s):
    d = deque(s)
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True


# ---------------------------------------------------------
# 4) 해시(dict): "본 적 있나" - Two Sum 을 O(n) 으로
# ---------------------------------------------------------
def two_sum(nums, target):
    seen = {}                # 값 -> 인덱스
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []


# ---------------------------------------------------------
# 5) 해시(Counter) + 힙: 가장 빈번한 K 개
# ---------------------------------------------------------
def top_k_frequent(nums, k):
    freq = Counter(nums)
    # nlargest 는 내부적으로 크기 K 힙을 사용 -> O(n log k)
    return [v for v, _ in heapq.nlargest(k, freq.items(), key=lambda kv: kv[1])]


# ---------------------------------------------------------
# 6) 힙(Heap): "매 순간 최솟값" - 크기 K 최소 힙으로 K번째 큰 값 유지
# ---------------------------------------------------------
class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)
        while len(self.heap) > k:    # 크기를 K 로 유지
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]          # 힙의 최솟값 = K번째로 큰 값


# ---------------------------------------------------------
# 7) 단조 스택(Monotonic Stack): "다음으로 큰 원소" - 며칠 기다리나
# ---------------------------------------------------------
def daily_temperatures(temps):
    ans = [0] * len(temps)
    stack = []                       # 아직 더 큰 값을 못 만난 인덱스들
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans


# ---------------------------------------------------------
# 8) 연결 리스트(Linked List): 포인터 재배선으로 뒤집기
# ---------------------------------------------------------
class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt


def build_list(values):
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_pylist(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reverse_list(head):
    prev = None
    while head:
        nxt = head.next      # 끊기 전에 다음 노드 저장 (포인터 꼬임 방지)
        head.next = prev
        prev = head
        head = nxt
    return prev


# ---------------------------------------------------------
# 9) 트리(Tree): 깊이는 재귀(DFS), 레벨은 큐(BFS)
# ---------------------------------------------------------
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def level_order(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):      # 현재 레벨 노드 수만큼만
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        out.append(level)
    return out


def demo():
    print("=== 1) 스택: 괄호 짝 맞추기 ===")
    print("'()[]{}' ->", valid_parentheses("()[]{}"), "(기대 True)")
    print("'(]'     ->", valid_parentheses("(]"), "(기대 False)")

    print()
    print("=== 2) 큐(deque): FIFO 순서 유지 ===")
    print("[1,2,3] 넣고 빼기 ->", queue_demo([1, 2, 3]), "(기대 [1, 2, 3])")

    print()
    print("=== 3) 덱: 회문 검사 ===")
    print("'level' ->", is_palindrome("level"), "(기대 True)")
    print("'hello' ->", is_palindrome("hello"), "(기대 False)")

    print()
    print("=== 4) 해시: Two Sum O(n) ===")
    print("[2,7,11,15], t=9 ->", two_sum([2, 7, 11, 15], 9), "(기대 [0, 1])")

    print()
    print("=== 5) 해시+힙: 가장 빈번한 K 개 ===")
    print("[1,1,1,2,2,3], k=2 ->", sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)),
          "(기대 [1, 2])")

    print()
    print("=== 6) 힙: K번째 큰 값 스트림 ===")
    kl = KthLargest(3, [4, 5, 8, 2])
    print("add(3) ->", kl.add(3), "(기대 4)")
    print("add(5) ->", kl.add(5), "(기대 5)")
    print("add(10) ->", kl.add(10), "(기대 5)")

    print()
    print("=== 7) 단조 스택: Daily Temperatures ===")
    print("[73,74,75,71,69,72,76,73] ->",
          daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]),
          "(기대 [1,1,4,2,1,1,0,0])")

    print()
    print("=== 8) 연결 리스트: 뒤집기 ===")
    head = build_list([1, 2, 3, 4, 5])
    print("[1,2,3,4,5] reverse ->", to_pylist(reverse_list(head)),
          "(기대 [5,4,3,2,1])")

    print()
    print("=== 9) 트리: 깊이(DFS) / 레벨(BFS) ===")
    #        3
    #       / 9 ... 20  (15, 7)
    root = TreeNode(3,
                    TreeNode(9),
                    TreeNode(20, TreeNode(15), TreeNode(7)))
    print("max_depth ->", max_depth(root), "(기대 3)")
    print("level_order ->", level_order(root), "(기대 [[3],[9,20],[15,7]])")


if __name__ == "__main__":
    demo()

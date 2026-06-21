"""Day 10 해설 - 연결 리스트 (Linked List).

각 문제마다 접근 방식을 주석으로 설명하고, 가능하면 여러 접근을 제시한다.
플랫폼 시그니처: LeetCode = class Solution 메서드.
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용 - =,-,O,X)
"""

from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


# ---- 테스트용 헬퍼 --------------------------------------------
def build(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# ---- 문제 1: Reverse Linked List (LeetCode #206) --------------
class Solution206:
    # 접근 1) 반복문(세 포인터)  | 시간 O(n) / 공간 O(1)
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        cur = head
        while cur:
            nxt = cur.next        # 끊기 전 백업
            cur.next = prev       # 화살표 반대로
            prev = cur
            cur = nxt
        return prev

    # 접근 2) 재귀  | 시간 O(n) / 공간 O(n) (콜 스택)
    def reverseList_rec(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        new_head = self.reverseList_rec(head.next)
        head.next.next = head     # 뒤 노드가 나를 가리키게
        head.next = None
        return new_head


# ---- 문제 2: Merge Two Sorted Lists (LeetCode #21) ------------
class Solution21:
    # 접근) 더미 헤드 + tail로 작은 값 잇기  | 시간 O(n+m) / 공간 O(1)
    def mergeTwoLists(self, l1: Optional[ListNode],
                      l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        while l1 and l2:
            if l1.val <= l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        tail.next = l1 if l1 else l2   # 남은 쪽 통째로 연결
        return dummy.next


# ---- 문제 3: Middle of the Linked List (LeetCode #876) --------
class Solution876:
    # 접근) fast/slow  | 시간 O(n) / 공간 O(1)
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow            # 짝수면 두 번째 중앙


# ---- 문제 4: Linked List Cycle (LeetCode #141) ----------------
class Solution141:
    # 접근 1) 방문 노드 set  | 시간 O(n) / 공간 O(n)
    def hasCycle_set(self, head: Optional[ListNode]) -> bool:
        seen = set()
        cur = head
        while cur:
            if cur in seen:    # 노드 객체 동일성으로 판단
                return True
            seen.add(cur)
            cur = cur.next
        return False

    # 접근 2) 플로이드(토끼와 거북이)  | 시간 O(n) / 공간 O(1)
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:   # 만나면 사이클
                return True
        return False


# ---- 문제 5: Remove Nth Node From End (LeetCode #19) ----------
class Solution19:
    # 접근) 더미 + 두 포인터(간격 n)  | 시간 O(n) / 공간 O(1), one pass
    def removeNthFromEnd(self, head: Optional[ListNode],
                         n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n):     # fast를 먼저 n칸 전진
            fast = fast.next
        while fast.next:       # 둘이 함께 끝까지
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next   # slow가 삭제 대상의 앞 노드
        return dummy.next


# ---- 문제 6: Add Two Numbers (LeetCode #2) --------------------
class Solution2:
    # 접근) 더미 + carry(올림)  | 시간 O(max(n,m)) / 공간 O(max(n,m))
    def addTwoNumbers(self, l1: Optional[ListNode],
                      l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        carry = 0
        while l1 or l2 or carry:
            a = l1.val if l1 else 0
            b = l2.val if l2 else 0
            carry, digit = divmod(a + b + carry, 10)
            tail.next = ListNode(digit)
            tail = tail.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next


# ---- 문제 7: Linked List Cycle II (LeetCode #142) -------------
class Solution142:
    # 접근 1) set  | 시간 O(n) / 공간 O(n)
    def detectCycle_set(self, head: Optional[ListNode]) -> Optional[ListNode]:
        seen = set()
        cur = head
        while cur:
            if cur in seen:
                return cur
            seen.add(cur)
            cur = cur.next
        return None

    # 접근 2) 플로이드 2단계  | 시간 O(n) / 공간 O(1)
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:           # 1단계: 만남
                p = head
                while p is not slow:   # 2단계: head와 1칸씩
                    p = p.next
                    slow = slow.next
                return p               # 사이클 시작점
        return None


# ---- 문제 8: Palindrome Linked List (LeetCode #234) ----------
class Solution234:
    # 접근 1) 값 배열 비교  | 시간 O(n) / 공간 O(n)
    def isPalindrome_array(self, head: Optional[ListNode]) -> bool:
        vals = to_list(head)
        return vals == vals[::-1]

    # 접근 2) 중간 찾고 후반부 뒤집어 비교  | 시간 O(n) / 공간 O(1)
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        # 중간 찾기
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # 후반부 뒤집기
        prev = None
        while slow:
            nxt = slow.next
            slow.next = prev
            prev = slow
            slow = nxt
        # 전반부 vs 뒤집은 후반부 비교
        left, right = head, prev
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next
        return True


# ---- 문제 9: Intersection of Two Linked Lists (LeetCode #160) -
class Solution160:
    # 접근 1) set  | 시간 O(n+m) / 공간 O(n)
    def getIntersectionNode_set(self, headA: ListNode,
                                headB: ListNode) -> Optional[ListNode]:
        nodes = set()
        cur = headA
        while cur:
            nodes.add(cur)
            cur = cur.next
        cur = headB
        while cur:
            if cur in nodes:
                return cur
            cur = cur.next
        return None

    # 접근 2) 두 포인터 길이 상쇄  | 시간 O(n+m) / 공간 O(1)
    def getIntersectionNode(self, headA: ListNode,
                            headB: ListNode) -> Optional[ListNode]:
        pa, pb = headA, headB
        while pa is not pb:
            pa = pa.next if pa else headB   # 끝나면 상대 head로
            pb = pb.next if pb else headA
        return pa                            # 교차점 또는 None


# ---- 사이클 만들기 헬퍼: 꼬리를 인덱스 pos 노드로 연결 --------
def build_cycle(values, pos):
    head = build(values)
    nodes = []
    cur = head
    while cur:
        nodes.append(cur)
        cur = cur.next
    nodes[-1].next = nodes[pos]   # 꼬리 -> pos
    return head, nodes[pos]


if __name__ == "__main__":
    # 문제 1
    s206 = Solution206()
    assert to_list(s206.reverseList(build([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert to_list(s206.reverseList_rec(build([1, 2]))) == [2, 1]
    assert to_list(s206.reverseList(build([]))) == []
    print("[OK] 문제 1 Reverse Linked List")

    # 문제 2
    s21 = Solution21()
    merged = s21.mergeTwoLists(build([1, 2, 4]), build([1, 3, 4]))
    assert to_list(merged) == [1, 1, 2, 3, 4, 4]
    assert to_list(s21.mergeTwoLists(build([]), build([0]))) == [0]
    print("[OK] 문제 2 Merge Two Sorted Lists")

    # 문제 3
    s876 = Solution876()
    assert s876.middleNode(build([1, 2, 3, 4, 5])).val == 3
    assert s876.middleNode(build([1, 2, 3, 4, 5, 6])).val == 4
    print("[OK] 문제 3 Middle of the Linked List")

    # 문제 4
    s141 = Solution141()
    h, _ = build_cycle([3, 2, 0, -4], 1)
    assert s141.hasCycle(h) is True
    assert s141.hasCycle_set(build_cycle([1, 2], 0)[0]) is True
    assert s141.hasCycle(build([1, 2, 3])) is False
    assert s141.hasCycle(build([])) is False
    print("[OK] 문제 4 Linked List Cycle")

    # 문제 5
    s19 = Solution19()
    assert to_list(s19.removeNthFromEnd(build([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert to_list(s19.removeNthFromEnd(build([1]), 1)) == []
    assert to_list(s19.removeNthFromEnd(build([1, 2]), 2)) == [2]
    print("[OK] 문제 5 Remove Nth Node From End")

    # 문제 6
    s2 = Solution2()
    assert to_list(s2.addTwoNumbers(build([2, 4, 3]), build([5, 6, 4]))) == [7, 0, 8]
    assert to_list(s2.addTwoNumbers(build([9, 9]), build([1]))) == [0, 0, 1]
    assert to_list(s2.addTwoNumbers(build([0]), build([0]))) == [0]
    print("[OK] 문제 6 Add Two Numbers")

    # 문제 7
    s142 = Solution142()
    h, start = build_cycle([3, 2, 0, -4], 1)
    assert s142.detectCycle(h) is start
    h2, start2 = build_cycle([1, 2], 0)
    assert s142.detectCycle_set(h2) is start2
    assert s142.detectCycle(build([1, 2, 3])) is None
    print("[OK] 문제 7 Linked List Cycle II")

    # 문제 8
    s234 = Solution234()
    assert s234.isPalindrome(build([1, 2, 2, 1])) is True
    assert s234.isPalindrome(build([1, 2, 3, 2, 1])) is True
    assert s234.isPalindrome_array(build([1, 2, 3])) is False
    assert s234.isPalindrome(build([1])) is True
    print("[OK] 문제 8 Palindrome Linked List")

    # 문제 9 (공유 꼬리 만들기)
    common = build([8, 4, 5])
    a = build([4, 1])
    b = build([5, 6, 1])
    ta = a
    while ta.next:
        ta = ta.next
    ta.next = common         # a의 꼬리 -> common
    tb = b
    while tb.next:
        tb = tb.next
    tb.next = common         # b의 꼬리 -> common
    s160 = Solution160()
    assert s160.getIntersectionNode(a, b) is common
    assert s160.getIntersectionNode_set(a, b) is common
    assert s160.getIntersectionNode(build([2, 6, 4]), build([1, 5])) is None
    print("[OK] 문제 9 Intersection of Two Linked Lists")

    print("=== 모든 테스트 통과 ===")

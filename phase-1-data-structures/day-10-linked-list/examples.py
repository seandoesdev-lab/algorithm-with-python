"""Day 10 예제 - 연결 리스트 (Linked List).

파이썬에는 표준 연결 리스트가 없으므로 ListNode를 직접 정의한다.
list <-> 연결 리스트 변환 헬퍼(build/to_list)로 결과를 눈으로 확인한다.
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용 - =,-,O,X)
"""

from typing import List, Optional


class ListNode:
    """단일 연결 리스트의 노드: 값 val + 다음 노드 next."""

    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


# ---- 변환 헬퍼 (테스트/출력용) ---------------------------------
def build(values: List[int]) -> Optional[ListNode]:
    """파이썬 리스트 -> 연결 리스트. 더미 헤드로 깔끔하게 만든다."""
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    """연결 리스트 -> 파이썬 리스트. 순회하며 값을 모은다."""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# ---- 1) 순회 (Traversal) --------------------------------------
def traverse(head: Optional[ListNode]) -> List[int]:
    out = []
    cur = head
    while cur is not None:        # next가 None이면 끝
        out.append(cur.val)
        cur = cur.next
    return out


# ---- 2) 맨 앞 삽입 (Prepend, O(1)) ----------------------------
def prepend(head: Optional[ListNode], val: int) -> ListNode:
    node = ListNode(val)
    node.next = head             # 새 노드의 next를 기존 head로
    return node                  # 새 head 반환


# ---- 3) 뒤집기 (Reverse, O(n) 시간 / O(1) 공간) ---------------
def reverse(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    cur = head
    while cur:
        nxt = cur.next           # 끊기 전 백업 (가장 중요!)
        cur.next = prev          # 화살표 반대로
        prev = cur               # prev 전진
        cur = nxt                # cur 전진
    return prev                  # prev가 새 head


# ---- 4) 중간 노드 찾기 (fast/slow) ----------------------------
def middle(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next         # +1
        fast = fast.next.next    # +2
    return slow                  # 짝수 길이면 두 번째 중앙


# ---- 5) 값이 target인 노드 모두 삭제 (더미 헤드) --------------
def remove_all(head: Optional[ListNode], target: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    prev = dummy
    cur = head
    while cur:
        if cur.val == target:
            prev.next = cur.next  # 건너뛰기 (삭제)
        else:
            prev = cur            # 유지하면 prev 전진
        cur = cur.next
    return dummy.next


# ---- 6) 길이 세기 ---------------------------------------------
def length(head: Optional[ListNode]) -> int:
    n = 0
    cur = head
    while cur:
        n += 1
        cur = cur.next
    return n


if __name__ == "__main__":
    src = [10, 20, 30, 40, 50]
    head = build(src)
    print("원본:", to_list(head))                 # [10, 20, 30, 40, 50]

    print("순회:", traverse(head))                 # [10, 20, 30, 40, 50]
    print("길이:", length(head))                   # 5

    head2 = prepend(build([20, 30]), 10)
    print("맨 앞 삽입:", to_list(head2))            # [10, 20, 30]

    rev = reverse(build(src))
    print("뒤집기:", to_list(rev))                  # [50, 40, 30, 20, 10]

    mid = middle(build([1, 2, 3, 4, 5]))
    print("중간(홀수):", mid.val)                   # 3
    mid_even = middle(build([1, 2, 3, 4]))
    print("중간(짝수, 두번째):", mid_even.val)      # 3

    removed = remove_all(build([1, 9, 2, 9, 3, 9]), 9)
    print("9 모두 삭제:", to_list(removed))         # [1, 2, 3]

    print("빈 리스트 순회:", traverse(build([])))   # []
    print("=== 예제 실행 완료 ===")

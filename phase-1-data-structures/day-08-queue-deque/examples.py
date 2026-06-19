"""Day 8 - 큐와 덱 (Queue & Deque) 예제 코드.

각 예제는 단독 실행 가능하며, 개념을 단계별 주석으로 설명한다.
실행: python examples.py
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""

from collections import deque


def example_1_queue_basic() -> None:
    """큐 기본 연산: enqueue(append), dequeue(popleft), front(q[0])."""
    print("=== 예제 1) 큐 기본 연산 (FIFO) ===")
    q = deque()
    q.append(10)            # enqueue 10
    q.append(20)            # enqueue 20
    q.append(30)            # enqueue 30
    print("enqueue 후 :", list(q))     # [10, 20, 30]
    print("front      :", q[0])        # 10 (제거 안 함)
    print("dequeue    :", q.popleft()) # 10 반환 (가장 먼저 들어온 것)
    print("dequeue 후 :", list(q))     # [20, 30]
    print("isEmpty    :", not q)       # False
    print("size       :", len(q))      # 2


def example_2_deque_both_ends() -> None:
    """덱: 양쪽 끝 모두 O(1) 삽입/삭제."""
    print("=== 예제 2) 덱 양끝 연산 ===")
    dq = deque([1, 2, 3])
    dq.appendleft(0)        # 앞에 넣기
    dq.append(4)            # 뒤에 넣기
    print("양끝 추가 후 :", list(dq))   # [0, 1, 2, 3, 4]
    print("popleft     :", dq.popleft())  # 0 (앞에서)
    print("pop         :", dq.pop())       # 4 (뒤에서)
    print("결과         :", list(dq))      # [1, 2, 3]


def example_3_list_pop0_is_slow() -> None:
    """왜 list.pop(0)을 큐에 쓰면 안 되는가: 앞 원소 시프트(O(n))."""
    print("=== 예제 3) list.pop(0) vs deque.popleft ===")
    # list.pop(0): 맨 앞을 빼면 나머지를 전부 한 칸 당김 -> O(n)
    lst = [1, 2, 3, 4, 5]
    print("list      :", lst)
    print("list.pop(0):", lst.pop(0), "-> 남은 원소 시프트 발생(O(n))")
    print("이후 list  :", lst)
    # deque.popleft(): 포인터만 이동 -> O(1)
    dq = deque([1, 2, 3, 4, 5])
    print("deque.popleft:", dq.popleft(), "-> 이동 없음(O(1))")
    print("큐 용도면 항상 deque + popleft 를 쓴다")


def example_4_deque_as_stack_and_queue() -> None:
    """덱 하나로 스택(LIFO)도 큐(FIFO)도 흉내 낸다."""
    print("=== 예제 4) 덱으로 스택/큐 흉내 ===")
    # 스택처럼: append + pop (양쪽 끝이 같음)
    st = deque()
    st.append("a")
    st.append("b")
    st.append("c")
    print("스택(LIFO) pop 순서:", st.pop(), st.pop(), st.pop())   # c b a
    # 큐처럼: append + popleft
    q = deque()
    q.append("a")
    q.append("b")
    q.append("c")
    print("큐(FIFO) pop 순서  :", q.popleft(), q.popleft(), q.popleft())  # a b c


def example_5_maxlen_buffer() -> None:
    """maxlen: 최근 N개만 유지하는 슬라이딩 버퍼(오래된 것 자동 제거)."""
    print("=== 예제 5) deque(maxlen=N) 최근 N개 ===")
    recent = deque(maxlen=3)
    for v in [1, 2, 3, 4, 5]:
        recent.append(v)        # 꽉 차면 왼쪽(가장 오래된 것)이 자동으로 밀려남
        print("append", v, "->", list(recent))
    print("최종 (최근 3개):", list(recent))   # [3, 4, 5]


def example_6_rotate() -> None:
    """rotate: 덱만의 회전 기능."""
    print("=== 예제 6) rotate 회전 ===")
    dq = deque([1, 2, 3, 4, 5])
    dq.rotate(2)                # 오른쪽으로 2칸
    print("rotate(2)  :", list(dq))    # [4, 5, 1, 2, 3]
    dq.rotate(-1)               # 왼쪽으로 1칸
    print("rotate(-1) :", list(dq))    # [5, 1, 2, 3, 4]


def example_7_empty_guard() -> None:
    """빈 큐 popleft 방어: IndexError 예방."""
    print("=== 예제 7) 빈 큐 방어 ===")
    q = deque()
    safe = q.popleft() if q else None
    print("빈 큐 안전 dequeue :", safe)      # None
    try:
        deque().popleft()
    except IndexError as e:
        print("IndexError 발생 :", e)        # pop from an empty deque


def example_8_bfs_with_queue() -> None:
    """BFS: 큐로 '가까운 것부터' 방문(Day 26 예고)."""
    print("=== 예제 8) 큐로 BFS ===")
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }
    start = "A"
    visited = {start}
    q = deque([start])
    order = []
    while q:
        node = q.popleft()      # 가까운(먼저 들어온) 노드부터
        order.append(node)
        for nxt in graph[node]:
            if nxt not in visited:
                visited.add(nxt)
                q.append(nxt)
    print("BFS 방문 순서 :", order)   # A B C D E F


def example_9_monotonic_deque() -> None:
    """모노토닉 덱: 슬라이딩 윈도우 최댓값을 O(n)에."""
    print("=== 예제 9) 모노토닉 덱 (창 최댓값) ===")
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    dq = deque()                # 인덱스 저장, 값 내림차순 유지
    ans = []
    for i, v in enumerate(nums):
        while dq and nums[dq[-1]] < v:    # 뒤에서 작은 값 제거
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:                # 앞에서 범위 벗어난 인덱스 제거
            dq.popleft()
        if i >= k - 1:
            ans.append(nums[dq[0]])       # 맨 앞 = 현재 창 최댓값
    print("nums :", nums)
    print("k    :", k)
    print("창 최댓값:", ans)       # [3, 3, 5, 5, 6, 7]


if __name__ == "__main__":
    example_1_queue_basic()
    print()
    example_2_deque_both_ends()
    print()
    example_3_list_pop0_is_slow()
    print()
    example_4_deque_as_stack_and_queue()
    print()
    example_5_maxlen_buffer()
    print()
    example_6_rotate()
    print()
    example_7_empty_guard()
    print()
    example_8_bfs_with_queue()
    print()
    example_9_monotonic_deque()
    print()
    print("=== 모든 예제 실행 완료 ===")

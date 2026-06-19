"""Day 8 해설 - 큐와 덱 (Queue & Deque).

각 문제마다 접근 방식을 주석으로 먼저 설명하고,
가능하면 여러 접근(브루트포스 -> 최적화)을 함께 제시한다.
플랫폼 시그니처: LeetCode = class Solution 메서드 / 프로그래머스 = def solution(...).
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""

import math
from collections import deque
from typing import List


# ---- 문제 1: 기능개발 (프로그래머스 #42586) ---------------------
# 각 기능 완성까지 남은 일수 = ceil((100 - progress) / speed).
# 앞에서부터 배포되며, 앞 기능 완성일 이하인 뒤 기능들이 함께 배포된다.
# 접근) 큐(deque)로 앞에서부터 처리  | 시간복잡도: O(n)
def solution_42586(progresses: List[int], speeds: List[int]) -> List[int]:
    days = deque(
        math.ceil((100 - p) / s) for p, s in zip(progresses, speeds)
    )
    answer = []
    while days:
        front = days.popleft()          # 가장 먼저 배포될 기능의 완성일
        count = 1
        while days and days[0] <= front:  # 그 이하인 뒤 기능들 함께 배포
            days.popleft()
            count += 1
        answer.append(count)
    return answer


# ---- 문제 2: 프로세스 (프로그래머스 #42587) ---------------------
# 큐 앞을 꺼내되, 뒤에 더 높은 우선순위가 있으면 맨 뒤로 보낸다.
# 접근) 덱 + (인덱스, 우선순위) 튜플 회전  | 시간복잡도: O(n^2) (매번 max 확인)
def solution_42587(priorities: List[int], location: int) -> int:
    q = deque(enumerate(priorities))    # (원래 인덱스, 우선순위)
    order = 0
    while q:
        idx, prio = q.popleft()
        if any(prio < other for _, other in q):   # 뒤에 더 높은 게 있으면
            q.append((idx, prio))                  # 맨 뒤로 회전
        else:
            order += 1                             # 실행
            if idx == location:
                return order
    return order                                   # 도달하지 않음(안전용)


# ---- 문제 3: Implement Queue using Stacks (LeetCode #232) -------
# 스택 두 개(in/out)로 FIFO 큐. out이 비면 in 전체를 뒤집어 옮긴다.
# 접근) 두 스택  | 시간복잡도: push O(1), pop/peek 분할상환 O(1)
class MyQueue:
    def __init__(self) -> None:
        self._in: List[int] = []        # 들어오는 곳(LIFO)
        self._out: List[int] = []       # 나가는 곳(FIFO 순서로 뒤집힌 상태)

    def push(self, x: int) -> None:     # O(1)
        self._in.append(x)

    def _move(self) -> None:
        if not self._out:               # out이 비었을 때만 한 번에 옮김
            while self._in:
                self._out.append(self._in.pop())

    def pop(self) -> int:               # 분할상환 O(1)
        self._move()
        return self._out.pop()

    def peek(self) -> int:              # 분할상환 O(1)
        self._move()
        return self._out[-1]

    def empty(self) -> bool:            # O(1)
        return not self._in and not self._out


# ---- 문제 4: Design Circular Queue (LeetCode #622) -------------
# 고정 배열 + head 인덱스 + count. 모듈러 연산으로 회전(ring buffer).
# 접근) 배열 + 모듈러  | 시간복잡도: 모든 연산 O(1)
class MyCircularQueue:
    def __init__(self, k: int) -> None:
        self._data: List[int] = [0] * k
        self._cap = k
        self._head = 0                  # 맨 앞 원소 위치
        self._count = 0                 # 현재 원소 수

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self._data[(self._head + self._count) % self._cap] = value  # 뒤에 삽입
        self._count += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self._head = (self._head + 1) % self._cap   # 앞을 한 칸 회전
        self._count -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self._data[self._head]

    def Rear(self) -> int:
        if self.isEmpty():
            return -1
        return self._data[(self._head + self._count - 1) % self._cap]

    def isEmpty(self) -> bool:
        return self._count == 0

    def isFull(self) -> bool:
        return self._count == self._cap


# ---- 문제 5: Sliding Window Maximum (LeetCode #239) ------------
# 각 크기 k 창의 최댓값들.
class Solution239:
    # 접근 1) 매 창마다 max  | 시간복잡도: O(n*k) (k 크면 느림)
    def maxSlidingWindow_brute(self, nums: List[int], k: int) -> List[int]:
        return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]

    # 접근 2) 모노토닉 덱(인덱스, 값 내림차순)  | 시간복잡도: O(n)
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        dq = deque()                    # 인덱스 저장, nums 값이 내림차순
        ans = []
        for i, v in enumerate(nums):
            while dq and nums[dq[-1]] < v:   # 뒤에서 더 작은 값 제거(쓸모없음)
                dq.pop()
            dq.append(i)
            if dq[0] <= i - k:               # 앞에서 창 벗어난 인덱스 제거
                dq.popleft()
            if i >= k - 1:
                ans.append(nums[dq[0]])      # 맨 앞 = 현재 창 최댓값
        return ans


# ---- 문제 6: 두 큐 합 같게 만들기 (프로그래머스 #118667, 카카오) -
# 한 큐에서 빼서 다른 큐로 넘기는 연산을 반복해 두 합을 같게.
# 접근) 합이 큰 쪽에서 빼서 작은 쪽으로 넘기는 그리디 + 횟수 상한
#       | 시간복잡도: O(n) (각 원소 상수 번 이동)
def solution_118667(queue1: List[int], queue2: List[int]) -> int:
    q1, q2 = deque(queue1), deque(queue2)
    s1, s2 = sum(q1), sum(q2)
    if (s1 + s2) % 2 != 0:              # 전체 합이 홀수면 절대 못 나눔
        return -1
    count = 0
    limit = (len(queue1) + len(queue2)) * 4   # 무한 루프 방지 상한
    while count <= limit:
        if s1 == s2:
            return count
        if s1 > s2:                     # 큰 쪽(q1)에서 빼서 q2로
            x = q1.popleft()
            q2.append(x)
            s1 -= x
            s2 += x
        else:                           # 큰 쪽(q2)에서 빼서 q1로
            x = q2.popleft()
            q1.append(x)
            s2 -= x
            s1 += x
        count += 1
    return -1


if __name__ == "__main__":
    # 문제 1
    assert solution_42586([93, 30, 55], [1, 30, 5]) == [2, 1]
    assert solution_42586([95, 90, 99, 99, 80, 99], [1, 1, 1, 1, 1, 1]) == [1, 3, 2]
    print("[OK] 문제 1 기능개발")

    # 문제 2
    assert solution_42587([2, 1, 3, 2], 2) == 1
    assert solution_42587([1, 1, 9, 1, 1, 1], 0) == 5
    print("[OK] 문제 2 프로세스")

    # 문제 3
    mq = MyQueue()
    mq.push(1)
    mq.push(2)
    assert mq.peek() == 1
    assert mq.pop() == 1
    assert mq.empty() is False
    mq.push(3)
    assert mq.pop() == 2
    assert mq.pop() == 3
    assert mq.empty() is True
    print("[OK] 문제 3 Implement Queue using Stacks")

    # 문제 4
    cq = MyCircularQueue(3)
    assert cq.enQueue(1) is True
    assert cq.enQueue(2) is True
    assert cq.enQueue(3) is True
    assert cq.enQueue(4) is False      # 꽉 참
    assert cq.Rear() == 3
    assert cq.isFull() is True
    assert cq.deQueue() is True
    assert cq.enQueue(4) is True       # 앞 공간 재사용(원형)
    assert cq.Rear() == 4
    assert cq.Front() == 2
    print("[OK] 문제 4 Design Circular Queue")

    # 문제 5
    s239 = Solution239()
    nums, k = [1, 3, -1, -3, 5, 3, 6, 7], 3
    expected = [3, 3, 5, 5, 6, 7]
    assert s239.maxSlidingWindow_brute(nums, k) == expected
    assert s239.maxSlidingWindow(nums, k) == expected
    assert s239.maxSlidingWindow([1], 1) == [1]
    assert s239.maxSlidingWindow([9, 8, 7, 6], 2) == [9, 8, 7]
    print("[OK] 문제 5 Sliding Window Maximum")

    # 문제 6
    assert solution_118667([3, 2, 7, 2], [4, 6, 5, 1]) == 2
    assert solution_118667([1, 1], [1, 5]) == -1
    assert solution_118667([1, 2, 1, 2], [1, 10, 1, 2]) == 7
    print("[OK] 문제 6 두 큐 합 같게 만들기")

    print("=== 모든 테스트 통과 ===")

# -*- coding: utf-8 -*-
"""
Day 12 - 힙·우선순위 큐 (Heap & Priority Queue) 문제 해설

- LeetCode 문제는 `class Solution` 시그니처를 따른다.
- 프로그래머스 문제는 `def solution(...)` 시그니처를 따른다.
- 가능한 경우 다중 접근(힙 / 정렬 / 두 힙)을 보여주고 맨 아래 assert 로 자체 검증.
- cp949 콘솔 안전: print 출력에는 ASCII 기호(=, -, O, X)만 사용(한글은 OK).

실행:  PYTHONIOENCODING=cp949 python solutions.py
"""

import heapq
from collections import Counter


# ===========================================================================
# 1) LeetCode #1046 - Last Stone Weight  (최대 힙 기본)
# ===========================================================================
class SolutionLastStone:
    # 접근: 매번 가장 무거운 돌 2개를 꺼내 부딪힌다. 최대 힙 = 부호 뒤집기.
    # O(n log n)
    def lastStoneWeight(self, stones):
        h = [-s for s in stones]
        heapq.heapify(h)
        while len(h) > 1:
            a = -heapq.heappop(h)        # 가장 무거운
            b = -heapq.heappop(h)        # 두 번째
            if a != b:                   # 다르면 차이만큼 남는다
                heapq.heappush(h, -(a - b))
        return -h[0] if h else 0


# ===========================================================================
# 2) LeetCode #215 - Kth Largest Element in an Array
# ===========================================================================
class SolutionKthLargest:
    # 접근 A: 크기 k 최소 힙 유지 - O(n log k) 시간 / O(k) 공간 (실전 추천)
    def findKthLargest(self, nums, k):
        h = []
        for x in nums:
            heapq.heappush(h, x)
            if len(h) > k:
                heapq.heappop(h)         # 작은 것을 버려 k개만 유지
        return h[0]

    # 접근 B: nlargest - O(n log k), 한 줄
    def findKthLargestB(self, nums, k):
        return heapq.nlargest(k, nums)[-1]


# ===========================================================================
# 3) LeetCode #703 - Kth Largest Element in a Stream  (설계형, 크기 k 힙)
# ===========================================================================
class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.h = []
        for x in nums:
            self.add(x)

    def add(self, val):
        heapq.heappush(self.h, val)
        if len(self.h) > self.k:
            heapq.heappop(self.h)        # 항상 가장 큰 k개만 보관
        return self.h[0]                 # 그 중 최솟값 = k번째 큰 값


# ===========================================================================
# 4) LeetCode #347 - Top K Frequent Elements
# ===========================================================================
class SolutionTopK:
    # 접근: 빈도 세고 nlargest(k, key=빈도) - O(n log k)
    def topKFrequent(self, nums, k):
        count = Counter(nums)
        return heapq.nlargest(k, count.keys(), key=count.get)


# ===========================================================================
# 5) LeetCode #973 - K Closest Points to Origin
# ===========================================================================
class SolutionKClosest:
    # 접근: 거리 제곱 기준 크기 k 최대 힙 유지 - O(n log k)
    # (거리 비교만 필요하므로 sqrt 생략, 제곱으로 비교)
    def kClosest(self, points, k):
        h = []
        for x, y in points:
            d = x * x + y * y
            heapq.heappush(h, (-d, x, y))   # 음수 거리 -> 최대 힙
            if len(h) > k:
                heapq.heappop(h)            # 가장 먼 점을 버린다
        return [[x, y] for (_, x, y) in h]


# ===========================================================================
# 6) LeetCode #23 - Merge k Sorted Lists  (힙으로 k-way 병합)
# ===========================================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SolutionMergeK:
    # 접근: 각 리스트의 머리만 힙에 넣고 최솟값을 뽑아 이어붙인다.
    # 힙 크기 = k 이므로 O(N log k) (N = 전체 노드 수)
    # 튜플에 인덱스 i 를 끼워 노드끼리 비교(에러)가 나지 않게 한다.
    def mergeKLists(self, lists):
        h = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(h, (node.val, i, node))
        dummy = ListNode()
        tail = dummy
        while h:
            val, i, node = heapq.heappop(h)
            tail.next = node
            tail = node
            if node.next:
                heapq.heappush(h, (node.next.val, i, node.next))
        return dummy.next


# ===========================================================================
# 7) LeetCode #295 - Find Median from Data Stream  (두 힙)
#    small: 아래 절반(최대 힙, 음수 저장) / large: 위 절반(최소 힙)
#    불변식: max(small) <= min(large), len(small) >= len(large)
# ===========================================================================
class MedianFinder:
    def __init__(self):
        self.small = []   # 최대 힙(부호 반전)
        self.large = []   # 최소 힙

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        # small 의 최댓값을 large 로 넘겨 정렬 불변식 유지
        heapq.heappush(self.large, -heapq.heappop(self.small))
        # 크기 균형: small 이 하나 더 많거나 같게
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0


# ===========================================================================
# 8) 프로그래머스 #42626 - 더 맵게  (최소 힙)
# ===========================================================================
def solution_spicy(scoville, K):
    h = scoville[:]
    heapq.heapify(h)
    count = 0
    # 가장 안 매운 두 개를 섞는다: new = 가장작음 + 두번째*2
    while len(h) >= 2 and h[0] < K:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        heapq.heappush(h, a + b * 2)
        count += 1
    return count if h[0] >= K else -1


# ===========================================================================
# 9) 프로그래머스 #42627 - 디스크 컨트롤러  (SJF + 최소 힙)
# ===========================================================================
def solution_disk(jobs):
    n = len(jobs)
    jobs.sort()                       # 요청 시각 오름차순
    h = []                            # (소요시간, 요청시각) 최소 힙
    time = 0
    idx = 0
    total = 0                         # 총 (완료시각 - 요청시각)
    done = 0
    while done < n:
        # 현재 시각까지 도착한 작업을 모두 대기열에 넣는다
        while idx < n and jobs[idx][0] <= time:
            start, dur = jobs[idx]
            heapq.heappush(h, (dur, start))
            idx += 1
        if h:                         # 가장 짧은 작업부터 처리(SJF)
            dur, start = heapq.heappop(h)
            time += dur
            total += time - start
            done += 1
        else:                         # 대기열이 비면 다음 도착 시각으로 점프
            time = jobs[idx][0]
    return total // n                 # 평균 대기시간(소수점 버림)


# ===========================================================================
# 10) 프로그래머스 #42628 - 이중우선순위큐  (두 힙 + 게으른 삭제)
# ===========================================================================
def solution_dpq(operations):
    min_h, max_h = [], []
    alive = {}                        # 값 -> 살아있는 개수
    size = 0

    def clean(heap, sign):
        # 힙 꼭대기가 이미 삭제된 값이면 버린다(lazy deletion)
        while heap and alive.get(sign * heap[0], 0) == 0:
            heapq.heappop(heap)

    for op in operations:
        cmd, num = op.split()
        num = int(num)
        if cmd == "I":
            heapq.heappush(min_h, num)
            heapq.heappush(max_h, -num)
            alive[num] = alive.get(num, 0) + 1
            size += 1
        else:                          # "D"
            if size == 0:
                continue
            if num == 1:               # 최댓값 삭제
                clean(max_h, -1)
                if max_h:
                    v = -heapq.heappop(max_h)
                    alive[v] -= 1
                    size -= 1
            else:                      # num == -1, 최솟값 삭제
                clean(min_h, 1)
                if min_h:
                    v = heapq.heappop(min_h)
                    alive[v] -= 1
                    size -= 1
    clean(max_h, -1)
    clean(min_h, 1)
    if size == 0 or not max_h or not min_h:
        return [0, 0]
    return [-max_h[0], min_h[0]]


# ===========================================================================
# 자체 검증
# ===========================================================================
def build_list(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


def main():
    print("=" * 56)
    print("Day 12 - 힙·우선순위 큐 solutions 자체 검증")
    print("=" * 56)

    # 1) Last Stone Weight
    s1 = SolutionLastStone()
    assert s1.lastStoneWeight([2, 7, 4, 1, 8, 1]) == 1
    assert s1.lastStoneWeight([1]) == 1
    assert s1.lastStoneWeight([2, 2]) == 0
    print("[1] Last Stone Weight             : OK")

    # 2) Kth Largest in Array
    s2 = SolutionKthLargest()
    assert s2.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
    assert s2.findKthLargestB([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    print("[2] Kth Largest Element in Array  : OK")

    # 3) Kth Largest in Stream
    kl = KthLargest(3, [4, 5, 8, 2])
    assert kl.add(3) == 4
    assert kl.add(5) == 5
    assert kl.add(10) == 5
    assert kl.add(9) == 8
    assert kl.add(4) == 8
    print("[3] Kth Largest in a Stream       : OK")

    # 4) Top K Frequent (순서 무관 -> 집합 비교)
    s4 = SolutionTopK()
    assert set(s4.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == {1, 2}
    assert s4.topKFrequent([1], 1) == [1]
    print("[4] Top K Frequent Elements       : OK")

    # 5) K Closest Points (순서 무관 -> 집합 비교)
    s5 = SolutionKClosest()
    got = {tuple(p) for p in s5.kClosest([[1, 3], [-2, 2]], 1)}
    assert got == {(-2, 2)}
    got2 = {tuple(p) for p in s5.kClosest([[3, 3], [5, -1], [-2, 4]], 2)}
    assert got2 == {(3, 3), (-2, 4)}
    print("[5] K Closest Points to Origin    : OK")

    # 6) Merge k Sorted Lists
    s6 = SolutionMergeK()
    lists = [build_list([1, 4, 5]), build_list([1, 3, 4]), build_list([2, 6])]
    assert to_list(s6.mergeKLists(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert to_list(s6.mergeKLists([])) == []
    assert to_list(s6.mergeKLists([None])) == []
    print("[6] Merge k Sorted Lists          : OK")

    # 7) Find Median from Data Stream
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    assert mf.findMedian() == 1.5
    mf.addNum(3)
    assert mf.findMedian() == 2.0
    print("[7] Find Median from Data Stream  : OK")

    # 8) 더 맵게
    assert solution_spicy([1, 2, 3, 9, 10, 12], 7) == 2
    assert solution_spicy([1, 1], 5) == -1     # 1+1*2=3 < 5, 더 못 섞음
    print("[8] 더 맵게 (프로그래머스)         : OK")

    # 9) 디스크 컨트롤러
    assert solution_disk([[0, 3], [1, 9], [2, 6]]) == 9
    print("[9] 디스크 컨트롤러 (프로그래머스)  : OK")

    # 10) 이중우선순위큐
    assert solution_dpq(["I 16", "I -5643", "D -1", "D 1", "D 1",
                         "I 123", "D -1"]) == [0, 0]
    assert solution_dpq(["I -45", "I 653", "D 1", "I -642", "I 45",
                         "I 97", "D 1", "D -1", "I 333"]) == [333, -45]
    print("[10] 이중우선순위큐 (프로그래머스) : OK")

    print("\n모든 solutions 검증 통과")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Day 22 - 재귀와 분할정복 (Recursion & Divide-Conquer): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(재귀 vs 반복, 분할정복 vs 선형)을 두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

import heapq
import random
from functools import lru_cache


# ===========================================================================
# 1. Fibonacci Number (LeetCode #509)
#    재귀 vs 메모 vs 반복(상향식). 재귀의 지수 폭발 -> 메모 O(n) -> 반복 O(1) 공간.
# ===========================================================================
class SolutionFib:
    def fib(self, n):
        """상향식 반복. O(n) 시간, O(1) 공간."""
        if n < 2:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def fib_memo(self, n):
        """하향식 재귀 + 메모이제이션. O(n)."""
        @lru_cache(maxsize=None)
        def go(k):
            if k < 2:
                return k
            return go(k - 1) + go(k - 2)
        return go(n)


# ===========================================================================
# 2. 하노이의 탑 (프로그래머스 #12946)
#    n-1개를 보조로 -> 큰 원반을 목적지로 -> n-1개를 목적지로. 이동 2^n - 1회.
# ===========================================================================
def solution_hanoi(n):
    answer = []

    def move(cnt, src, dst, via):
        if cnt == 0:
            return
        move(cnt - 1, src, via, dst)
        answer.append([src, dst])
        move(cnt - 1, via, dst, src)

    move(n, 1, 3, 2)
    return answer


# ===========================================================================
# 3. Pow(x, n) (LeetCode #50)
#    분할정복 거듭제곱 x^n = (x^(n/2))^2. O(log n). 음수 지수 처리.
# ===========================================================================
class SolutionPow:
    def myPow(self, x, n):
        if n < 0:
            x, n = 1 / x, -n
        return self._pow(x, n)

    def _pow(self, x, n):
        if n == 0:
            return 1.0
        half = self._pow(x, n // 2)
        return half * half if n % 2 == 0 else half * half * x


# ===========================================================================
# 4. Sort an Array (LeetCode #912)
#    병합 정렬(분할정복). 안정적 O(n log n).
# ===========================================================================
class SolutionSortArray:
    def sortArray(self, nums):
        if len(nums) <= 1:
            return nums
        mid = len(nums) // 2
        left = self.sortArray(nums[:mid])
        right = self.sortArray(nums[mid:])
        return self._merge(left, right)

    def _merge(self, a, b):
        out, i, j = [], 0, 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                out.append(a[i]); i += 1
            else:
                out.append(b[j]); j += 1
        out.extend(a[i:]); out.extend(b[j:])
        return out


# ===========================================================================
# 5. Maximum Subarray (LeetCode #53)
#    분할정복 O(n log n) vs 카데인 O(n). 두 접근 비교.
# ===========================================================================
class SolutionMaxSubarray:
    def maxSubArray(self, nums):
        """카데인(Kadane). O(n) / O(1)."""
        best = cur = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best

    def maxSubArray_dc(self, nums):
        """분할정복. O(n log n)."""
        def go(lo, hi):
            if lo == hi:
                return nums[lo]
            mid = (lo + hi) // 2
            left = go(lo, mid)
            right = go(mid + 1, hi)
            # 중앙을 걸치는 최대 합
            s, best_l = 0, float("-inf")
            for i in range(mid, lo - 1, -1):
                s += nums[i]; best_l = max(best_l, s)
            s, best_r = 0, float("-inf")
            for i in range(mid + 1, hi + 1):
                s += nums[i]; best_r = max(best_r, s)
            return max(left, right, best_l + best_r)
        return go(0, len(nums) - 1)


# ===========================================================================
# 6. 쿼드압축 후 개수 세기 (프로그래머스 #68936)
#    2D 분할정복: 영역이 모두 같으면 1개, 아니면 4사분면 재귀 후 합산.
# ===========================================================================
def solution_quad(arr):
    n = len(arr)
    zeros_ones = [0, 0]   # [0의 개수, 1의 개수]

    def compress(r, c, size):
        first = arr[r][c]
        uniform = all(
            arr[r + i][c + j] == first
            for i in range(size) for j in range(size)
        )
        if uniform:
            zeros_ones[first] += 1
            return
        half = size // 2
        compress(r, c, half)
        compress(r, c + half, half)
        compress(r + half, c, half)
        compress(r + half, c + half, half)

    compress(0, 0, n)
    return zeros_ones


# ===========================================================================
# 7. Majority Element (LeetCode #169)
#    분할정복 O(n log n) vs 보이어-무어 투표 O(n)/O(1).
# ===========================================================================
class SolutionMajority:
    def majorityElement(self, nums):
        """보이어-무어 투표. O(n) / O(1)."""
        count = 0
        cand = None
        for x in nums:
            if count == 0:
                cand = x
            count += 1 if x == cand else -1
        return cand

    def majorityElement_dc(self, nums):
        """분할정복. O(n log n)."""
        def go(lo, hi):
            if lo == hi:
                return nums[lo]
            mid = (lo + hi) // 2
            left = go(lo, mid)
            right = go(mid + 1, hi)
            if left == right:
                return left
            lc = sum(1 for i in range(lo, hi + 1) if nums[i] == left)
            rc = sum(1 for i in range(lo, hi + 1) if nums[i] == right)
            return left if lc > rc else right
        return go(0, len(nums) - 1)


# ===========================================================================
# 8. Kth Largest Element in an Array (LeetCode #215)
#    퀵셀렉트(랜덤 피벗) 평균 O(n) vs 힙 O(n log k).
# ===========================================================================
class SolutionKthLargest:
    def findKthLargest(self, nums, k):
        """퀵셀렉트. 평균 O(n), 최악 O(n^2)."""
        target = len(nums) - k          # k번째 큰 값 = (n-k)번째 작은 값(0-index)
        lo, hi = 0, len(nums) - 1
        nums = nums[:]                  # 원본 보존
        while True:
            p = self._partition(nums, lo, hi)
            if p == target:
                return nums[p]
            if p < target:
                lo = p + 1
            else:
                hi = p - 1

    def _partition(self, a, lo, hi):
        rnd = random.randint(lo, hi)    # 랜덤 피벗으로 최악 회피
        a[rnd], a[hi] = a[hi], a[rnd]
        pivot = a[hi]
        i = lo
        for j in range(lo, hi):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        return i

    def findKthLargest_heap(self, nums, k):
        """비교용 최소 힙. O(n log k)."""
        return heapq.nlargest(k, nums)[-1]


# ===========================================================================
# 9. Different Ways to Add Parentheses (LeetCode #241)
#    연산자 기준 분할 + 메모이제이션. 좌/우 결과 목록의 모든 조합.
# ===========================================================================
class SolutionDiffWays:
    def diffWaysToCompute(self, expression):
        @lru_cache(maxsize=None)
        def go(expr):
            if expr.isdigit():
                return (int(expr),)
            results = []
            for i, ch in enumerate(expr):
                if ch in "+-*":
                    left = go(expr[:i])
                    right = go(expr[i + 1:])
                    for a in left:
                        for b in right:
                            if ch == "+":
                                results.append(a + b)
                            elif ch == "-":
                                results.append(a - b)
                            else:
                                results.append(a * b)
            return tuple(results)
        return list(go(expression))


# ===========================================================================
# 10. Merge k Sorted Lists (LeetCode #23)
#     분할정복으로 리스트를 쌍으로 병합. O(N log k).
#     LeetCode ListNode 시그니처 + 배열 변환 헬퍼로 자체 검증.
# ===========================================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SolutionMergeK:
    def mergeKLists(self, lists):
        if not lists:
            return None
        if len(lists) == 1:
            return lists[0]
        mid = len(lists) // 2
        left = self.mergeKLists(lists[:mid])
        right = self.mergeKLists(lists[mid:])
        return self._merge_two(left, right)

    def _merge_two(self, a, b):
        dummy = ListNode()
        tail = dummy
        while a and b:
            if a.val <= b.val:
                tail.next = a; a = a.next
            else:
                tail.next = b; b = b.next
            tail = tail.next
        tail.next = a if a else b
        return dummy.next


def _to_list(arr):
    dummy = ListNode()
    tail = dummy
    for x in arr:
        tail.next = ListNode(x)
        tail = tail.next
    return dummy.next


def _to_array(node):
    out = []
    while node:
        out.append(node.val)
        node = node.next
    return out


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    f = SolutionFib()
    assert f.fib(2) == 1 and f.fib(4) == 3 and f.fib(10) == 55
    assert f.fib_memo(10) == 55 and f.fib_memo(20) == 6765

    assert solution_hanoi(2) == [[1, 2], [1, 3], [2, 3]]
    assert len(solution_hanoi(3)) == 7        # 2^3 - 1
    assert len(solution_hanoi(5)) == 31       # 2^5 - 1

    p = SolutionPow()
    assert abs(p.myPow(2.0, 10) - 1024.0) < 1e-9
    assert abs(p.myPow(2.0, -2) - 0.25) < 1e-9
    assert abs(p.myPow(2.1, 3) - 9.261) < 1e-9

    sa = SolutionSortArray()
    assert sa.sortArray([5, 2, 3, 1]) == [1, 2, 3, 5]
    assert sa.sortArray([5, 1, 1, 2, 0, 0]) == [0, 0, 1, 1, 2, 5]

    ms = SolutionMaxSubarray()
    data = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    assert ms.maxSubArray(data) == 6
    assert ms.maxSubArray_dc(data) == 6
    assert ms.maxSubArray([-1, -2, -3]) == -1
    assert ms.maxSubArray_dc([-1, -2, -3]) == -1

    assert solution_quad([[1, 1, 0, 0], [1, 0, 0, 0],
                          [1, 0, 0, 1], [1, 1, 1, 1]]) == [4, 9]
    assert solution_quad([[1, 1], [1, 1]]) == [0, 1]
    assert solution_quad([[0]]) == [1, 0]

    mj = SolutionMajority()
    assert mj.majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2
    assert mj.majorityElement_dc([2, 2, 1, 1, 1, 2, 2]) == 2
    assert mj.majorityElement([3, 3, 4]) == 3

    kl = SolutionKthLargest()
    assert kl.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
    assert kl.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert kl.findKthLargest_heap([3, 2, 1, 5, 6, 4], 2) == 5

    dw = SolutionDiffWays()
    assert sorted(dw.diffWaysToCompute("2-1-1")) == [0, 2]
    assert sorted(dw.diffWaysToCompute("2*3-4*5")) == [-34, -14, -10, -10, 10]

    mk = SolutionMergeK()
    lists = [_to_list([1, 4, 5]), _to_list([1, 3, 4]), _to_list([2, 6])]
    assert _to_array(mk.mergeKLists(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert mk.mergeKLists([]) is None
    assert _to_array(mk.mergeKLists([_to_list([])])) == []

    print("Day 22 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()

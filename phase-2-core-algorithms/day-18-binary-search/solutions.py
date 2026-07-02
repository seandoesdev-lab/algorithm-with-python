# -*- coding: utf-8 -*-
"""
Day 18 - 이분 탐색 (Binary Search): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(직접 구현 vs bisect 모듈)을 함께 두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

import bisect


# ===========================================================================
# 1. Binary Search (LeetCode #704)
#    정렬 배열에서 target 위치, 없으면 -1. O(log n)
# ===========================================================================
class SolutionBinarySearch:
    def search(self, nums, target):
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2          # 오버플로 걱정 없는 파이썬
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    def search_bisect(self, nums, target):
        """bisect로 한 줄: 위치를 찾고 값이 맞는지 확인."""
        i = bisect.bisect_left(nums, target)
        return i if i < len(nums) and nums[i] == target else -1


# ===========================================================================
# 2. Search Insert Position (LeetCode #35)
#    target 이상이 처음 나오는 위치 = lower_bound. O(log n)
# ===========================================================================
class SolutionSearchInsert:
    def searchInsert(self, nums, target):
        lo, hi = 0, len(nums)             # 반열린 구간 [lo, hi)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def searchInsert_bisect(self, nums, target):
        return bisect.bisect_left(nums, target)


# ===========================================================================
# 3. First Bad Version (LeetCode #278)
#    F..F,T..T 경계 찾기(가장 작은 T). API 호출 최소화가 목표. O(log n)
#    isBadVersion API는 팩토리로 주입해 테스트한다.
# ===========================================================================
class SolutionFirstBadVersion:
    def __init__(self, is_bad):
        self.isBadVersion = is_bad

    def firstBadVersion(self, n):
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if self.isBadVersion(mid):    # 여기가 나쁘면 답은 mid 이하
                hi = mid
            else:
                lo = mid + 1
        return lo                         # lo == hi == 첫 나쁜 버전


# ===========================================================================
# 4. Find First and Last Position (LeetCode #34)
#    lower_bound / upper_bound 로 시작~끝. O(log n)
# ===========================================================================
class SolutionSearchRange:
    def searchRange(self, nums, target):
        left = bisect.bisect_left(nums, target)
        if left == len(nums) or nums[left] != target:
            return [-1, -1]
        right = bisect.bisect_right(nums, target) - 1
        return [left, right]

    def searchRange_manual(self, nums, target):
        """bisect 없이 lower/upper bound 직접 구현."""
        def lower(t):
            lo, hi = 0, len(nums)
            while lo < hi:
                mid = (lo + hi) // 2
                if nums[mid] < t:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
        left = lower(target)
        if left == len(nums) or nums[left] != target:
            return [-1, -1]
        return [left, lower(target + 1) - 1]


# ===========================================================================
# 5. Search in Rotated Sorted Array (LeetCode #33)
#    회전된 배열에서 target 위치. 한 쪽은 항상 정렬돼 있음을 이용. O(log n)
# ===========================================================================
class SolutionSearchRotated:
    def search(self, nums, target):
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[lo] <= nums[mid]:         # 왼쪽 절반이 정렬됨
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:                              # 오른쪽 절반이 정렬됨
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1


# ===========================================================================
# 6. Koko Eating Bananas (LeetCode #875)
#    결정 문제형: 속도 k로 h시간 안에 다 먹을 수 있는가? -> 가장 작은 k
#    O(n log M), M = max(piles)
# ===========================================================================
class SolutionKoko:
    def minEatingSpeed(self, piles, h):
        def hours_needed(k):
            # ceil(p/k) 합. 정수 연산: (p + k - 1) // k
            return sum((p + k - 1) // k for p in piles)

        lo, hi = 1, max(piles)                # 속도 후보 범위
        while lo < hi:
            mid = (lo + hi) // 2
            if hours_needed(mid) <= h:        # 충분히 빠름 -> 더 느리게 시도
                hi = mid
            else:
                lo = mid + 1
        return lo


# ===========================================================================
# 7. 입국심사 (프로그래머스 #43238)
#    결정 문제형: 시간 t 안에 심사 가능한 인원 = sum(t // time) >= n ?
#    가장 작은 t. O(k log(n * max_time))
# ===========================================================================
def solution_immigration(n, times):
    def can_process(t):
        return sum(t // time for time in times) >= n

    lo, hi = 1, min(times) * n                # 최악: 가장 빠른 심사관 혼자
    while lo < hi:
        mid = (lo + hi) // 2
        if can_process(mid):                  # 충분 -> 시간을 줄여본다
            hi = mid
        else:
            lo = mid + 1
    return lo


# ===========================================================================
# 8. 징검다리 (프로그래머스 #43236)
#    결정 문제형(최소 간격 최대화): 바위 n개 제거 후 "최소 점프 거리"의 최댓값.
#    간격 >= x 를 유지하려면 제거할 바위 수 <= n 인가? 가장 큰 x. O(len log distance)
# ===========================================================================
def solution_stepping_stones(distance, rocks, n):
    rocks = sorted(rocks) + [distance]        # 도착점 포함

    def removable(gap):
        """최소 간격을 gap 이상으로 만들 때 제거해야 하는 바위 수."""
        removed = 0
        prev = 0
        for r in rocks:
            if r - prev < gap:
                removed += 1                  # 너무 가까우면 제거
            else:
                prev = r
        return removed

    lo, hi = 1, distance
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if removable(mid) <= n:               # n개 이하로 가능 -> 간격 늘려본다
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    bs = SolutionBinarySearch()
    assert bs.search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert bs.search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert bs.search_bisect([-1, 0, 3, 5, 9, 12], 9) == 4
    assert bs.search_bisect([-1, 0, 3, 5, 9, 12], 2) == -1

    si = SolutionSearchInsert()
    assert si.searchInsert([1, 3, 5, 6], 5) == 2
    assert si.searchInsert([1, 3, 5, 6], 2) == 1
    assert si.searchInsert([1, 3, 5, 6], 7) == 4
    assert si.searchInsert_bisect([1, 3, 5, 6], 0) == 0

    # First Bad Version: 4가 첫 나쁜 버전
    fbv = SolutionFirstBadVersion(lambda v: v >= 4)
    assert fbv.firstBadVersion(5) == 4
    assert SolutionFirstBadVersion(lambda v: v >= 1).firstBadVersion(1) == 1

    sr = SolutionSearchRange()
    assert sr.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert sr.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert sr.searchRange([], 0) == [-1, -1]
    assert sr.searchRange_manual([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert sr.searchRange_manual([1], 1) == [0, 0]

    rot = SolutionSearchRotated()
    assert rot.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert rot.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert rot.search([1], 0) == -1

    koko = SolutionKoko()
    assert koko.minEatingSpeed([3, 6, 7, 11], 8) == 4
    assert koko.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30
    assert koko.minEatingSpeed([30, 11, 23, 4, 20], 6) == 23

    assert solution_immigration(6, [7, 10]) == 28

    assert solution_stepping_stones(25, [2, 14, 11, 21, 17], 2) == 4

    print("Day 18 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()

# -*- coding: utf-8 -*-
"""
Day 23 - 알고리즘 기초 복습 (Core Algorithms Review): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(예: 그리디 vs DP, 투 포인터 vs 이분 탐색)을 두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

import bisect


# ===========================================================================
# 1. Binary Search (LeetCode #704)
#    이분 탐색 기본형. 직접 구현 vs bisect. 둘 다 O(log n).
# ===========================================================================
class SolutionBinarySearch:
    def search(self, nums, target):
        """직접 구현. O(log n) / O(1)."""
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    def search_bisect(self, nums, target):
        """표준 라이브러리 bisect. off-by-one 버그를 줄인다."""
        i = bisect.bisect_left(nums, target)
        return i if i < len(nums) and nums[i] == target else -1


# ===========================================================================
# 2. Two Sum II - Input Array Is Sorted (LeetCode #167)
#    투 포인터 O(n) vs 원소마다 이분 탐색 O(n log n). 정렬 전제.
# ===========================================================================
class SolutionTwoSumII:
    def twoSum(self, numbers, target):
        """투 포인터. O(n) / O(1). (1-indexed 반환)"""
        lo, hi = 0, len(numbers) - 1
        while lo < hi:
            s = numbers[lo] + numbers[hi]
            if s == target:
                return [lo + 1, hi + 1]
            if s < target:
                lo += 1
            else:
                hi -= 1
        return []

    def twoSum_bsearch(self, numbers, target):
        """각 원소마다 짝을 이분 탐색. O(n log n)."""
        for i, x in enumerate(numbers):
            need = target - x
            j = bisect.bisect_left(numbers, need, i + 1)
            if j < len(numbers) and numbers[j] == need:
                return [i + 1, j + 1]
        return []


# ===========================================================================
# 3. 체육복 (프로그래머스 #42862)
#    그리디: 앞 번호부터 빌려준다. 교집합(잃고+여벌) 먼저 제거가 함정.
# ===========================================================================
def solution_gym(n, lost, reserve):
    lost_set = set(lost) - set(reserve)      # 여벌 있으나 잃은 학생은 자기 것 사용
    reserve_set = set(reserve) - set(lost)
    for r in sorted(reserve_set):
        if r - 1 in lost_set:                # 앞 번호부터 우선
            lost_set.remove(r - 1)
        elif r + 1 in lost_set:
            lost_set.remove(r + 1)
    return n - len(lost_set)


# ===========================================================================
# 4. Longest Substring Without Repeating Characters (LeetCode #3)
#    가변 슬라이딩 윈도우. dict로 마지막 위치 관리. O(n).
# ===========================================================================
class SolutionLongestUnique:
    def lengthOfLongestSubstring(self, s):
        seen = {}
        start = best = 0
        for i, ch in enumerate(s):
            if ch in seen and seen[ch] >= start:
                start = seen[ch] + 1         # 창의 왼쪽을 중복 다음으로
            seen[ch] = i
            best = max(best, i - start + 1)
        return best


# ===========================================================================
# 5. Container With Most Water (LeetCode #11)
#    투 포인터: 더 낮은 쪽을 안으로. O(n) / O(1).
# ===========================================================================
class SolutionMaxArea:
    def maxArea(self, height):
        lo, hi = 0, len(height) - 1
        best = 0
        while lo < hi:
            area = min(height[lo], height[hi]) * (hi - lo)
            best = max(best, area)
            if height[lo] < height[hi]:      # 낮은 쪽을 옮겨야 커질 여지
                lo += 1
            else:
                hi -= 1
        return best


# ===========================================================================
# 6. Merge Intervals (LeetCode #56)
#    정렬 + 그리디. 시작점 정렬 후 겹치면 끝을 max로 확장. O(n log n).
# ===========================================================================
class SolutionMergeIntervals:
    def merge(self, intervals):
        intervals.sort()
        merged = []
        for s, e in intervals:
            if merged and s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e])
        return merged


# ===========================================================================
# 7. Jump Game (LeetCode #55)
#    그리디(farthest) O(n) vs 뒤에서부터 DP O(n).
# ===========================================================================
class SolutionJumpGame:
    def canJump(self, nums):
        """그리디: 닿을 수 있는 가장 먼 인덱스를 추적. O(n) / O(1)."""
        farthest = 0
        for i, step in enumerate(nums):
            if i > farthest:                 # 현재 칸에 못 닿음
                return False
            farthest = max(farthest, i + step)
        return True

    def canJump_dp(self, nums):
        """뒤에서부터 도달 가능 지점(last)을 당긴다. O(n)."""
        last = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= last:
                last = i
        return last == 0


# ===========================================================================
# 8. Koko Eating Bananas (LeetCode #875)
#    정답 이분 탐색: k의 범위를 이분 탐색, 판정 함수는 총 시간 <= h.
#    O(n log(max(piles))).
# ===========================================================================
class SolutionKoko:
    def minEatingSpeed(self, piles, h):
        def hours(k):
            return sum((p + k - 1) // k for p in piles)   # ceil(p/k)

        lo, hi = 1, max(piles)
        while lo < hi:
            mid = (lo + hi) // 2
            if hours(mid) <= h:              # 이 속도로 가능하면 더 줄여본다
                hi = mid
            else:
                lo = mid + 1
        return lo


# ===========================================================================
# 9. 구명보트 (프로그래머스 #42885)
#    정렬 + 양 끝 투 포인터 그리디. 무거운 사람에 가벼운 사람을 붙인다.
# ===========================================================================
def solution_boat(people, limit):
    people.sort()
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo <= hi:
        if people[lo] + people[hi] <= limit:  # 둘이 함께 탈 수 있으면
            lo += 1
        hi -= 1                                # 무거운 사람은 무조건 태운다
        boats += 1
    return boats


# ===========================================================================
# 10. Sort List (LeetCode #148)
#     분할정복(병합 정렬)을 연결 리스트에 적용.
#     slow/fast 포인터로 가운데를 찾아 반으로 끊고, 재귀 정렬 후 병합. O(n log n).
# ===========================================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SolutionSortList:
    def sortList(self, head):
        if not head or not head.next:
            return head
        # 1) 가운데 찾기 (slow는 앞 절반의 끝)
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        mid = slow.next
        slow.next = None                 # 반으로 끊기
        # 2) 각 절반 재귀 정렬
        left = self.sortList(head)
        right = self.sortList(mid)
        # 3) 병합
        return self._merge(left, right)

    def _merge(self, a, b):
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
    bs = SolutionBinarySearch()
    assert bs.search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert bs.search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert bs.search_bisect([-1, 0, 3, 5, 9, 12], 9) == 4
    assert bs.search_bisect([-1, 0, 3, 5, 9, 12], 2) == -1

    ts = SolutionTwoSumII()
    assert ts.twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert ts.twoSum([2, 3, 4], 6) == [1, 3]
    assert ts.twoSum_bsearch([2, 7, 11, 15], 9) == [1, 2]
    assert ts.twoSum_bsearch([-1, 0], -1) == [1, 2]

    assert solution_gym(5, [2, 4], [1, 3, 5]) == 5
    assert solution_gym(5, [2, 4], [3]) == 4
    assert solution_gym(3, [3], [1]) == 2
    assert solution_gym(3, [1, 2], [2, 3]) == 2   # 교집합 처리 확인

    lu = SolutionLongestUnique()
    assert lu.lengthOfLongestSubstring("abcabcbb") == 3
    assert lu.lengthOfLongestSubstring("bbbbb") == 1
    assert lu.lengthOfLongestSubstring("pwwkew") == 3
    assert lu.lengthOfLongestSubstring("") == 0

    ma = SolutionMaxArea()
    assert ma.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert ma.maxArea([1, 1]) == 1

    mi = SolutionMergeIntervals()
    assert mi.merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert mi.merge([[1, 4], [4, 5]]) == [[1, 5]]

    jg = SolutionJumpGame()
    assert jg.canJump([2, 3, 1, 1, 4]) is True
    assert jg.canJump([3, 2, 1, 0, 4]) is False
    assert jg.canJump_dp([2, 3, 1, 1, 4]) is True
    assert jg.canJump_dp([3, 2, 1, 0, 4]) is False

    kk = SolutionKoko()
    assert kk.minEatingSpeed([3, 6, 7, 11], 8) == 4
    assert kk.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30
    assert kk.minEatingSpeed([30, 11, 23, 4, 20], 6) == 23

    assert solution_boat([70, 50, 80, 50], 100) == 3
    assert solution_boat([70, 50, 80], 100) == 3
    assert solution_boat([40, 40, 40], 100) == 2

    sl = SolutionSortList()
    assert _to_array(sl.sortList(_to_list([4, 2, 1, 3]))) == [1, 2, 3, 4]
    assert _to_array(sl.sortList(_to_list([-1, 5, 3, 4, 0]))) == [-1, 0, 3, 4, 5]
    assert _to_array(sl.sortList(_to_list([]))) == []
    assert _to_array(sl.sortList(_to_list([1]))) == [1]

    print("Day 23 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()

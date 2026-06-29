# -*- coding: utf-8 -*-
"""
Day 16 - 시간복잡도와 Big-O: 연습문제 해설

각 문제마다 느린 접근(brute force)과 빠른 접근을 함께 두고 복잡도를 비교한다.
플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from collections import Counter


# ===========================================================================
# 1. Contains Duplicate (LeetCode #217)
#    brute force O(n^2)  vs  set O(n)
# ===========================================================================
class SolutionContainsDuplicate:
    def containsDuplicate_brute(self, nums):
        """O(n^2) 시간 / O(1) 공간 - 모든 쌍 비교."""
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j]:
                    return True
        return False

    def containsDuplicate(self, nums):
        """O(n) 시간 / O(n) 공간 - set 멤버십."""
        return len(set(nums)) != len(nums)


# ===========================================================================
# 2. Two Sum (LeetCode #1)
#    brute force O(n^2)  vs  dict O(n)
# ===========================================================================
class SolutionTwoSum:
    def twoSum_brute(self, nums, target):
        """O(n^2) - 모든 쌍."""
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

    def twoSum(self, nums, target):
        """O(n) - 본 값을 dict에 (값 -> 인덱스)."""
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return []


# ===========================================================================
# 3. Binary Search (LeetCode #704)
#    linear O(n)  vs  binary search O(log n)
# ===========================================================================
class SolutionBinarySearch:
    def search_linear(self, nums, target):
        """O(n) - 처음부터 훑기."""
        for i, x in enumerate(nums):
            if x == target:
                return i
        return -1

    def search(self, nums, target):
        """O(log n) - 절반씩 좁히기 (정렬 전제)."""
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


# ===========================================================================
# 4. Best Time to Buy and Sell Stock (LeetCode #121)
#    brute force O(n^2)  vs  one pass O(n)
# ===========================================================================
class SolutionMaxProfit:
    def maxProfit_brute(self, prices):
        """O(n^2) - 모든 (사는 날, 파는 날)."""
        best = 0
        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):
                best = max(best, prices[j] - prices[i])
        return best

    def maxProfit(self, prices):
        """O(n) - 지금까지의 최저가를 들고 한 번 순회."""
        min_price = float("inf")
        best = 0
        for p in prices:
            min_price = min(min_price, p)
            best = max(best, p - min_price)
        return best


# ===========================================================================
# 5. Maximum Subarray (LeetCode #53)
#    brute force O(n^2)  vs  Kadane O(n)
# ===========================================================================
class SolutionMaxSubArray:
    def maxSubArray_brute(self, nums):
        """O(n^2) - 모든 구간 합을 누적하며 비교."""
        best = nums[0]
        for i in range(len(nums)):
            cur = 0
            for j in range(i, len(nums)):
                cur += nums[j]
                best = max(best, cur)
        return best

    def maxSubArray(self, nums):
        """O(n) - Kadane: 이어갈지 새로 시작할지."""
        best = cur = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best


# ===========================================================================
# 6. 완주하지 못한 선수 (프로그래머스 #42576)
#    정렬 O(n log n)  vs  Counter O(n)
# ===========================================================================
def solution_marathon_sort(participant, completion):
    """O(n log n) - 정렬 후 어긋나는 첫 지점."""
    participant.sort()
    completion.sort()
    for p, c in zip(participant, completion):
        if p != c:
            return p
    return participant[-1]


def solution(participant, completion):
    """O(n) - Counter 차집합. 동명이인을 개수로 처리."""
    diff = Counter(participant) - Counter(completion)
    # 차집합 결과에 남은 단 하나의 키
    return list(diff.elements())[0]


# ===========================================================================
# 7. 두 개 뽑아서 더하기 (프로그래머스 #68644)
#    n <= 100 이라 O(n^2) 로 충분. (굳이 최적화가 불필요한 사례)
# ===========================================================================
def solution_two_sums(numbers):
    """O(n^2) 시간 / O(n^2) 공간 - 모든 쌍의 합을 set에 모으고 정렬."""
    sums = set()
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            sums.add(numbers[i] + numbers[j])
    return sorted(sums)


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    cd = SolutionContainsDuplicate()
    assert cd.containsDuplicate([1, 2, 3, 1]) is True
    assert cd.containsDuplicate([1, 2, 3, 4]) is False
    assert cd.containsDuplicate_brute([1, 2, 3, 1]) is True
    assert cd.containsDuplicate_brute([1, 2, 3, 4]) is False

    ts = SolutionTwoSum()
    assert ts.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert ts.twoSum_brute([3, 2, 4], 6) == [1, 2]

    bs = SolutionBinarySearch()
    assert bs.search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert bs.search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert bs.search_linear([-1, 0, 3, 5, 9, 12], 9) == 4

    mp = SolutionMaxProfit()
    assert mp.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert mp.maxProfit([7, 6, 4, 3, 1]) == 0
    assert mp.maxProfit_brute([7, 1, 5, 3, 6, 4]) == 5

    ms = SolutionMaxSubArray()
    assert ms.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert ms.maxSubArray([-1, -2, -3]) == -1  # 전부 음수
    assert ms.maxSubArray_brute([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

    assert solution(["leo", "kiki", "eden"], ["eden", "kiki"]) == "leo"
    # 동명이인 케이스
    assert solution(["mislav", "stanko", "mislav", "ana"],
                    ["stanko", "ana", "mislav"]) == "mislav"
    assert solution_marathon_sort(["leo", "kiki", "eden"],
                                  ["eden", "kiki"]) == "leo"

    assert solution_two_sums([2, 1, 3, 4, 1]) == [2, 3, 4, 5, 6, 7]
    assert solution_two_sums([5, 0, 2, 7]) == [2, 5, 7, 9, 12]

    print("Day 16 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()

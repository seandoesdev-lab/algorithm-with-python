# -*- coding: utf-8 -*-
"""
Day 19 - 투 포인터 (Two Pointers): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(브루트포스 vs 투 포인터 등)을 두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""


# ===========================================================================
# 1. Valid Palindrome (LeetCode #125)
#    영숫자만, 대소문자 무시하고 회문인지. O(n) / O(1)
# ===========================================================================
class SolutionValidPalindrome:
    def isPalindrome(self, s):
        lo, hi = 0, len(s) - 1
        while lo < hi:
            while lo < hi and not s[lo].isalnum():
                lo += 1
            while lo < hi and not s[hi].isalnum():
                hi -= 1
            if s[lo].lower() != s[hi].lower():
                return False
            lo += 1
            hi -= 1
        return True

    def isPalindrome_clean(self, s):
        """가독성 우선: 정제 후 뒤집기 비교. O(n) 시간, O(n) 공간."""
        t = [c.lower() for c in s if c.isalnum()]
        return t == t[::-1]


# ===========================================================================
# 2. Two Sum II - Input Array Is Sorted (LeetCode #167)
#    정렬 배열에서 합이 target인 두 수의 1-indexed 위치. O(n) / O(1)
# ===========================================================================
class SolutionTwoSumII:
    def twoSum(self, numbers, target):
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

    def twoSum_hash(self, numbers, target):
        """비교용: 해시맵 O(n) 시간, O(n) 공간. 정렬 배열엔 투 포인터가 O(1)로 우세."""
        seen = {}
        for i, x in enumerate(numbers):
            if target - x in seen:
                return [seen[target - x] + 1, i + 1]
            seen[x] = i
        return []


# ===========================================================================
# 3. Remove Duplicates from Sorted Array (LeetCode #26)
#    정렬 배열 in-place 중복 제거, 유일 개수 반환. O(n) / O(1)
# ===========================================================================
class SolutionRemoveDuplicates:
    def removeDuplicates(self, nums):
        if not nums:
            return 0
        slow = 0
        for fast in range(1, len(nums)):
            if nums[fast] != nums[slow]:
                slow += 1
                nums[slow] = nums[fast]
        return slow + 1


# ===========================================================================
# 4. Squares of a Sorted Array (LeetCode #977)
#    정렬 배열(음수 포함)의 제곱을 정렬 상태로. O(n) / O(n)
# ===========================================================================
class SolutionSortedSquares:
    def sortedSquares(self, nums):
        n = len(nums)
        res = [0] * n
        lo, hi, pos = 0, n - 1, n - 1
        while lo <= hi:
            if abs(nums[lo]) > abs(nums[hi]):
                res[pos] = nums[lo] * nums[lo]
                lo += 1
            else:
                res[pos] = nums[hi] * nums[hi]
                hi -= 1
            pos -= 1
        return res

    def sortedSquares_naive(self, nums):
        """비교용: 제곱 후 정렬. O(n log n)."""
        return sorted(x * x for x in nums)


# ===========================================================================
# 5. Container With Most Water (LeetCode #11)
#    양끝에서 낮은 쪽을 옮기며 최대 넓이. O(n) / O(1)
# ===========================================================================
class SolutionMaxArea:
    def maxArea(self, height):
        lo, hi = 0, len(height) - 1
        best = 0
        while lo < hi:
            h = min(height[lo], height[hi])
            best = max(best, h * (hi - lo))
            if height[lo] < height[hi]:
                lo += 1
            else:
                hi -= 1
        return best

    def maxArea_brute(self, height):
        """비교용: 모든 쌍 완전 탐색. O(n^2)."""
        n = len(height)
        best = 0
        for i in range(n):
            for j in range(i + 1, n):
                best = max(best, min(height[i], height[j]) * (j - i))
        return best


# ===========================================================================
# 6. 숫자의 표현 (프로그래머스 #12924)
#    n을 연속한 자연수의 합으로 표현하는 경우의 수. 투 포인터 O(n)
# ===========================================================================
def solution_express_number(n):
    left = 1
    total = 0
    count = 0
    for right in range(1, n + 1):
        total += right                # 창을 오른쪽으로 확장
        while total > n:              # 넘치면 왼쪽을 줄인다
            total -= left
            left += 1
        if total == n:
            count += 1
    return count


def solution_express_number_math(n):
    """비교용: 연속합은 홀수 약수의 개수와 같다. O(sqrt(n))."""
    count = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            if d % 2 == 1:
                count += 1
            other = n // d
            if other != d and other % 2 == 1:
                count += 1
        d += 1
    return count


# ===========================================================================
# 7. 3Sum (LeetCode #15)
#    합이 0인 유일한 세 원소 조합. 정렬 + 고정 + 투 포인터. O(n^2) / O(1)
# ===========================================================================
class SolutionThreeSum:
    def threeSum(self, nums):
        nums.sort()
        n = len(nums)
        res = []
        for i in range(n - 2):
            if nums[i] > 0:                       # 이후 전부 양수 -> 합 0 불가
                break
            if i > 0 and nums[i] == nums[i - 1]:  # 고정 원소 중복 스킵
                continue
            lo, hi = i + 1, n - 1
            while lo < hi:
                s = nums[i] + nums[lo] + nums[hi]
                if s < 0:
                    lo += 1
                elif s > 0:
                    hi -= 1
                else:
                    res.append([nums[i], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1                   # lo 쪽 중복 스킵
                    while lo < hi and nums[hi] == nums[hi + 1]:
                        hi -= 1                   # hi 쪽 중복 스킵
        return res


# ===========================================================================
# 8. Trapping Rain Water (LeetCode #42)
#    양끝 투 포인터 + 좌우 최대높이 추적. O(n) / O(1)
# ===========================================================================
class SolutionTrap:
    def trap(self, height):
        if not height:
            return 0
        lo, hi = 0, len(height) - 1
        left_max, right_max = height[lo], height[hi]
        water = 0
        while lo < hi:
            if left_max < right_max:
                lo += 1
                left_max = max(left_max, height[lo])
                water += left_max - height[lo]
            else:
                hi -= 1
                right_max = max(right_max, height[hi])
                water += right_max - height[hi]
        return water

    def trap_prefix(self, height):
        """비교용: 좌/우 최대 접두 배열. O(n) 시간, O(n) 공간."""
        n = len(height)
        if n == 0:
            return 0
        left = [0] * n
        right = [0] * n
        left[0] = height[0]
        for i in range(1, n):
            left[i] = max(left[i - 1], height[i])
        right[-1] = height[-1]
        for i in range(n - 2, -1, -1):
            right[i] = max(right[i + 1], height[i])
        return sum(min(left[i], right[i]) - height[i] for i in range(n))


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    vp = SolutionValidPalindrome()
    assert vp.isPalindrome("A man, a plan, a canal: Panama") is True
    assert vp.isPalindrome("race a car") is False
    assert vp.isPalindrome(" ") is True
    assert vp.isPalindrome_clean("A man, a plan, a canal: Panama") is True

    ts = SolutionTwoSumII()
    assert ts.twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert ts.twoSum([2, 3, 4], 6) == [1, 3]
    assert ts.twoSum([-1, 0], -1) == [1, 2]
    assert ts.twoSum_hash([2, 7, 11, 15], 9) == [1, 2]

    rd = SolutionRemoveDuplicates()
    arr = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = rd.removeDuplicates(arr)
    assert k == 5 and arr[:k] == [0, 1, 2, 3, 4]

    ss = SolutionSortedSquares()
    assert ss.sortedSquares([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]
    assert ss.sortedSquares([-7, -3, 2, 3, 11]) == [4, 9, 9, 49, 121]
    assert ss.sortedSquares_naive([-4, -1, 0, 3, 10]) == [0, 1, 9, 16, 100]

    ma = SolutionMaxArea()
    assert ma.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert ma.maxArea([1, 1]) == 1
    assert ma.maxArea_brute([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

    assert solution_express_number(15) == 4
    assert solution_express_number(1) == 1
    assert solution_express_number(100) == 3
    assert solution_express_number_math(15) == 4
    assert solution_express_number_math(100) == 3

    tsum = SolutionThreeSum()
    assert sorted(tsum.threeSum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
    assert tsum.threeSum([0, 1, 1]) == []
    assert tsum.threeSum([0, 0, 0]) == [[0, 0, 0]]

    tr = SolutionTrap()
    assert tr.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert tr.trap([4, 2, 0, 3, 2, 5]) == 9
    assert tr.trap_prefix([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6

    print("Day 19 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()

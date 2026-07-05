# -*- coding: utf-8 -*-
"""
Day 20 - 슬라이딩 윈도우 (Sliding Window): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(완전 탐색 vs 슬라이딩 윈도우 등)을 두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from collections import deque, Counter


# ===========================================================================
# 1. Maximum Average Subarray I (LeetCode #643)
#    길이 k 부분 배열의 최대 평균. 고정 창. O(n) / O(1)
# ===========================================================================
class SolutionMaxAverage:
    def findMaxAverage(self, nums, k):
        window = sum(nums[:k])
        best = window
        for right in range(k, len(nums)):
            window += nums[right] - nums[right - k]
            best = max(best, window)
        return best / k

    def findMaxAverage_brute(self, nums, k):
        """비교용: 모든 구간을 다시 합산. O(n*k)."""
        best = sum(nums[:k])
        for i in range(len(nums) - k + 1):
            best = max(best, sum(nums[i:i + k]))
        return best / k


# ===========================================================================
# 2. Minimum Size Subarray Sum (LeetCode #209)
#    합이 target 이상인 최소 길이. 가변 창(양수 전제). O(n) / O(1)
# ===========================================================================
class SolutionMinSubarrayLen:
    def minSubArrayLen(self, target, nums):
        left = 0
        total = 0
        best = len(nums) + 1
        for right in range(len(nums)):
            total += nums[right]
            while total >= target:
                best = min(best, right - left + 1)
                total -= nums[left]
                left += 1
        return best if best <= len(nums) else 0

    def minSubArrayLen_prefix_bisect(self, target, nums):
        """비교용: 누적 합 + 이분 탐색. O(n log n)."""
        import bisect
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]
        best = n + 1
        for i in range(n):
            need = prefix[i] + target          # prefix[j] >= need 인 최소 j
            j = bisect.bisect_left(prefix, need)
            if j <= n:
                best = min(best, j - i)
        return best if best <= n else 0


# ===========================================================================
# 3. Longest Substring Without Repeating Characters (LeetCode #3)
#    중복 없는 최장 부분 문자열 길이. 가변 창 + 해시. O(n) / O(k)
# ===========================================================================
class SolutionLongestUnique:
    def lengthOfLongestSubstring(self, s):
        last = {}
        left = 0
        best = 0
        for right, c in enumerate(s):
            if c in last and last[c] >= left:
                left = last[c] + 1             # left는 되돌아가지 않는다
            last[c] = right
            best = max(best, right - left + 1)
        return best

    def lengthOfLongestSubstring_set(self, s):
        """비교용: 집합으로 창을 유지하며 수축. O(n) 시간, O(k) 공간."""
        seen = set()
        left = 0
        best = 0
        for right, c in enumerate(s):
            while c in seen:
                seen.remove(s[left])
                left += 1
            seen.add(c)
            best = max(best, right - left + 1)
        return best


# ===========================================================================
# 4. Find All Anagrams in a String (LeetCode #438)
#    p의 아나그램 시작 인덱스 모두. 고정 창 + 문자 카운트. O(n) / O(1)
# ===========================================================================
class SolutionFindAnagrams:
    def findAnagrams(self, s, p):
        if len(p) > len(s):
            return []
        need = Counter(p)
        window = Counter()
        k = len(p)
        res = []
        for right, c in enumerate(s):
            window[c] += 1
            if right >= k:
                left_c = s[right - k]
                window[left_c] -= 1
                if window[left_c] == 0:
                    del window[left_c]
            if window == need:
                res.append(right - k + 1)
        return res


# ===========================================================================
# 5. Permutation in String (LeetCode #567)
#    s1의 순열이 s2의 부분 문자열로 존재하는지. 고정 창 카운트. O(n) / O(1)
# ===========================================================================
class SolutionCheckInclusion:
    def checkInclusion(self, s1, s2):
        if len(s1) > len(s2):
            return False
        need = Counter(s1)
        window = Counter()
        k = len(s1)
        for right, c in enumerate(s2):
            window[c] += 1
            if right >= k:
                left_c = s2[right - k]
                window[left_c] -= 1
                if window[left_c] == 0:
                    del window[left_c]
            if window == need:
                return True
        return False


# ===========================================================================
# 6. 보석 쇼핑 (프로그래머스 #67258)
#    모든 종류의 보석을 포함하는 최소 길이 연속 구간 [시작, 끝] (1-indexed).
#    가변 창 + 해시. O(n) / O(k)
# ===========================================================================
def solution_gem_shopping(gems):
    kinds = len(set(gems))            # 전체 보석 종류 수
    window = {}
    left = 0
    best_len = len(gems) + 1
    answer = [1, len(gems)]
    for right, g in enumerate(gems):
        window[g] = window.get(g, 0) + 1
        while len(window) == kinds:   # 모든 종류 포함 -> 왼쪽을 조인다
            if right - left + 1 < best_len:
                best_len = right - left + 1
                answer = [left + 1, right + 1]   # 1-indexed
            window[gems[left]] -= 1
            if window[gems[left]] == 0:
                del window[gems[left]]
            left += 1
    return answer


# ===========================================================================
# 7. Minimum Window Substring (LeetCode #76)
#    t의 모든 문자(중복 포함)를 담는 최소 부분 문자열. 가변 창 + formed. O(n)
# ===========================================================================
class SolutionMinWindow:
    def minWindow(self, s, t):
        if not s or not t or len(t) > len(s):
            return ""
        need = Counter(t)
        required = len(need)          # 만족해야 하는 문자 "종류" 수
        window = {}
        formed = 0                    # 개수까지 만족한 문자 종류 수
        left = 0
        best = (len(s) + 1, 0, 0)     # (길이, 시작, 끝)
        for right, c in enumerate(s):
            window[c] = window.get(c, 0) + 1
            if c in need and window[c] == need[c]:
                formed += 1
            while formed == required:            # 유효하면 최대한 조인다
                if right - left + 1 < best[0]:
                    best = (right - left + 1, left, right)
                lc = s[left]
                window[lc] -= 1
                if lc in need and window[lc] < need[lc]:
                    formed -= 1
                left += 1
        return "" if best[0] > len(s) else s[best[1]:best[2] + 1]


# ===========================================================================
# 8. Sliding Window Maximum (LeetCode #239)
#    각 창의 최댓값 모두. 단조 덱(인덱스 단조 감소). O(n) / O(k)
# ===========================================================================
class SolutionMaxSlidingWindow:
    def maxSlidingWindow(self, nums, k):
        dq = deque()          # 인덱스 저장, 대응 값이 단조 감소
        res = []
        for i, x in enumerate(nums):
            while dq and nums[dq[-1]] <= x:
                dq.pop()
            dq.append(i)
            if dq[0] <= i - k:            # 창을 벗어난 앞쪽 제거
                dq.popleft()
            if i >= k - 1:
                res.append(nums[dq[0]])
        return res

    def maxSlidingWindow_brute(self, nums, k):
        """비교용: 매 창마다 max. O(n*k)."""
        return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    ma = SolutionMaxAverage()
    assert abs(ma.findMaxAverage([1, 12, -5, -6, 50, 3], 4) - 12.75) < 1e-9
    assert abs(ma.findMaxAverage([5], 1) - 5.0) < 1e-9
    assert abs(ma.findMaxAverage_brute([1, 12, -5, -6, 50, 3], 4) - 12.75) < 1e-9

    ms = SolutionMinSubarrayLen()
    assert ms.minSubArrayLen(7, [2, 3, 1, 2, 4, 3]) == 2
    assert ms.minSubArrayLen(4, [1, 4, 4]) == 1
    assert ms.minSubArrayLen(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0
    assert ms.minSubArrayLen_prefix_bisect(7, [2, 3, 1, 2, 4, 3]) == 2
    assert ms.minSubArrayLen_prefix_bisect(11, [1, 1, 1, 1, 1, 1, 1, 1]) == 0

    lu = SolutionLongestUnique()
    assert lu.lengthOfLongestSubstring("abcabcbb") == 3
    assert lu.lengthOfLongestSubstring("bbbbb") == 1
    assert lu.lengthOfLongestSubstring("pwwkew") == 3
    assert lu.lengthOfLongestSubstring("") == 0
    assert lu.lengthOfLongestSubstring_set("abcabcbb") == 3
    assert lu.lengthOfLongestSubstring_set("pwwkew") == 3

    fa = SolutionFindAnagrams()
    assert fa.findAnagrams("cbaebabacd", "abc") == [0, 6]
    assert fa.findAnagrams("abab", "ab") == [0, 1, 2]
    assert fa.findAnagrams("a", "aa") == []

    ci = SolutionCheckInclusion()
    assert ci.checkInclusion("ab", "eidbaooo") is True
    assert ci.checkInclusion("ab", "eidboaoo") is False
    assert ci.checkInclusion("adc", "dcda") is True

    assert solution_gem_shopping(
        ["DIA", "RUBY", "RUBY", "DIA", "DIA", "EMERALD", "SAPPHIRE", "DIA"]
    ) == [3, 7]
    assert solution_gem_shopping(["AA", "AB", "AC", "AA", "AC"]) == [1, 3]
    assert solution_gem_shopping(["XYZ", "XYZ", "XYZ"]) == [1, 1]
    assert solution_gem_shopping(["ZZZ", "YYY", "NNNN", "YYY", "BBB"]) == [1, 5]

    mw = SolutionMinWindow()
    assert mw.minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert mw.minWindow("a", "a") == "a"
    assert mw.minWindow("a", "aa") == ""

    mx = SolutionMaxSlidingWindow()
    assert mx.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert mx.maxSlidingWindow([1], 1) == [1]
    assert mx.maxSlidingWindow_brute([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]

    print("Day 20 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()

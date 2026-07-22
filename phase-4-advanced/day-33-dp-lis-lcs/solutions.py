# -*- coding: utf-8 -*-
"""
Day 33 - 부분 수열 DP (LIS / LCS) 해설

플랫폼 시그니처 유지:
  - LeetCode  : class Solution 의 메서드
  - 프로그래머스 : def solution(...)
각 문제에 assert 자체 테스트 포함. 가능한 곳은 다중 접근 + 복잡도 비교.

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from bisect import bisect_left


# ===========================================================================
# 1. Longest Increasing Subsequence (LeetCode #300) - LIS
#    접근 A: O(N^2) DP  /  접근 B: O(N log N) 이분 탐색
# ===========================================================================
class SolutionLIS:
    def lengthOfLIS(self, nums) -> int:
        """O(N log N): tails 길이가 곧 LIS 길이."""
        tails = []
        for x in nums:
            pos = bisect_left(tails, x)          # strictly increasing
            if pos == len(tails):
                tails.append(x)
            else:
                tails[pos] = x
        return len(tails)

    def lengthOfLIS_dp(self, nums) -> int:
        """O(N^2) DP: dp[i]=i로 끝나는 LIS. 답은 max(dp)."""
        if not nums:
            return 0
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)


# ===========================================================================
# 2. Longest Continuous Increasing Subsequence (LeetCode #674)
#    부분 배열(연속) -> DP 아님, O(N) 한 번 훑기.
# ===========================================================================
class SolutionLCIS:
    def findLengthOfLCIS(self, nums) -> int:
        if not nums:
            return 0
        best = cur = 1
        for i in range(1, len(nums)):
            cur = cur + 1 if nums[i] > nums[i - 1] else 1
            if cur > best:
                best = cur
        return best


# ===========================================================================
# 3. Longest Common Subsequence (LeetCode #1143) - LCS 2차원 DP
#    같으면 dp[i-1][j-1]+1, 다르면 max(dp[i-1][j], dp[i][j-1]).
# ===========================================================================
class SolutionLCS:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]


# ===========================================================================
# 4. Longest Palindromic Subsequence (LeetCode #516)
#    접근 A: LPS(s) = LCS(s, reverse(s))
#    접근 B: 구간 DP  dp[i][j] = s[i..j] 의 LPS
# ===========================================================================
class SolutionLPS:
    def longestPalindromeSubseq(self, s: str) -> int:
        """접근 A - 뒤집어서 LCS."""
        return SolutionLCS().longestCommonSubsequence(s, s[::-1])

    def longestPalindromeSubseq_interval(self, s: str) -> int:
        """접근 B - 구간 DP. 양끝 같으면 +2, 아니면 안쪽 max."""
        n = len(s)
        if n == 0:
            return 0
        dp = [[0] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = 1
        for length in range(2, n + 1):           # 구간 길이
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] == s[j]:
                    inner = dp[i + 1][j - 1] if length > 2 else 0
                    dp[i][j] = inner + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        return dp[0][n - 1]


# ===========================================================================
# 5. Edit Distance (LeetCode #72) - 편집 거리 (LCS 사촌)
#    같으면 dp[i-1][j-1], 다르면 1 + min(삭제, 삽입, 교체).
# ===========================================================================
class SolutionEditDistance:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i                          # word1 -> "" : i 번 삭제
        for j in range(n + 1):
            dp[0][j] = j                          # "" -> word2 : j 번 삽입
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j],      # 삭제
                                       dp[i][j - 1],      # 삽입
                                       dp[i - 1][j - 1])  # 교체
        return dp[m][n]


# ===========================================================================
# 6. 가장 긴 팰린드롬 (프로그래머스 #12904)
#    부분 문자열(연속) 팰린드롬 -> 중심 확장 O(N^2).
#    (문제 4 의 부분 수열과 달리 LCS 트릭이 안 통함)
# ===========================================================================
def solution(s):
    n = len(s)
    if n < 2:
        return n
    best = 1

    def expand(lo, hi):
        while lo >= 0 and hi < n and s[lo] == s[hi]:
            lo -= 1
            hi += 1
        return hi - lo - 1                        # 확장된 팰린드롬 길이

    for center in range(n):
        best = max(best,
                   expand(center, center),        # 홀수 길이 중심
                   expand(center, center + 1))    # 짝수 길이 중심
    return best


def run_tests():
    print("=" * 60)
    print("Day 33 - LIS / LCS 해설 self-test")
    print("=" * 60)

    # 1. LIS - 두 접근이 같은 답
    lis = SolutionLIS()
    for nums, exp in [([10, 9, 2, 5, 3, 7, 101, 18], 4),
                      ([0, 1, 0, 3, 2, 3], 4),
                      ([7, 7, 7, 7], 1),
                      ([], 0)]:
        assert lis.lengthOfLIS(nums) == exp
        assert lis.lengthOfLIS_dp(nums) == exp
    print("[1] LIS (O(NlogN) == O(N^2))      OK")

    # 2. Longest Continuous Increasing Subsequence
    lcis = SolutionLCIS()
    assert lcis.findLengthOfLCIS([1, 3, 5, 4, 7]) == 3      # [1,3,5]
    assert lcis.findLengthOfLCIS([2, 2, 2, 2]) == 1
    assert lcis.findLengthOfLCIS([1, 3, 5, 7]) == 4
    print("[2] Continuous IS (부분 배열/O(N)) OK")

    # 3. LCS
    lcs = SolutionLCS()
    assert lcs.longestCommonSubsequence("abcde", "ace") == 3
    assert lcs.longestCommonSubsequence("abc", "abc") == 3
    assert lcs.longestCommonSubsequence("abc", "def") == 0
    assert lcs.longestCommonSubsequence("ABCBDAB", "BDCAB") == 4
    print("[3] Longest Common Subsequence     OK")

    # 4. LPS - 두 접근이 같은 답
    lps = SolutionLPS()
    for s, exp in [("bbbab", 4), ("cbbd", 2), ("a", 1), ("agbdba", 5)]:
        assert lps.longestPalindromeSubseq(s) == exp
        assert lps.longestPalindromeSubseq_interval(s) == exp
    print("[4] Longest Palindromic Subseq     OK  (LCS == 구간DP)")

    # 5. Edit Distance
    ed = SolutionEditDistance()
    assert ed.minDistance("horse", "ros") == 3
    assert ed.minDistance("intention", "execution") == 5
    assert ed.minDistance("", "abc") == 3
    assert ed.minDistance("abc", "abc") == 0
    print("[5] Edit Distance                  OK")

    # 6. 가장 긴 팰린드롬 (프로그래머스, 연속 부분 문자열)
    assert solution("abcdcba") == 7
    assert solution("abacde") == 3            # "aba"
    assert solution("abba") == 4              # 짝수 길이
    assert solution("a") == 1
    print("[6] 가장 긴 팰린드롬 (연속/중심확장) OK")

    print("=" * 60)
    print("모든 테스트 통과 (All tests passed)")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()

# -*- coding: utf-8 -*-
"""
Day 31 - 동적 계획법 입문 (Dynamic Programming) 해설

플랫폼 시그니처 유지:
  - LeetCode  : class Solution 의 메서드
  - 프로그래머스 : def solution(...)
각 문제에 assert 자체 테스트 포함. 가능한 곳은 다중 접근 + 복잡도 비교.

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

import sys
from functools import lru_cache
from bisect import bisect_left

sys.setrecursionlimit(10 ** 6)


# ===========================================================================
# 1. Fibonacci Number (LeetCode #509)
#    접근 A: Top-Down 메모  / 접근 B: Bottom-Up O(1) 공간
# ===========================================================================
class SolutionFib:
    def fib_memo(self, n: int) -> int:
        @lru_cache(maxsize=None)
        def f(k):
            if k < 2:
                return k
            return f(k - 1) + f(k - 2)
        return f(n)

    def fib(self, n: int) -> int:          # O(n) 시간, O(1) 공간
        prev, cur = 0, 1
        for _ in range(n):
            prev, cur = cur, prev + cur
        return prev


# ===========================================================================
# 2. Climbing Stairs (LeetCode #70)
#    dp[i] = dp[i-1] + dp[i-2]
# ===========================================================================
class SolutionClimb:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        a, b = 1, 2
        for _ in range(3, n + 1):
            a, b = b, a + b
        return b


# ===========================================================================
# 3. Min Cost Climbing Stairs (LeetCode #746)
#    dp[i] = min(dp[i-1]+cost[i-1], dp[i-2]+cost[i-2]),  dp[0]=dp[1]=0
# ===========================================================================
class SolutionMinCost:
    def minCostClimbingStairs(self, cost) -> int:
        one, two = 0, 0
        for i in range(2, len(cost) + 1):
            cur = min(one + cost[i - 1], two + cost[i - 2])
            two, one = one, cur
        return one


# ===========================================================================
# 4. House Robber (LeetCode #198)
#    dp[i] = max(dp[i-1], dp[i-2] + nums[i])
# ===========================================================================
class SolutionRob:
    def rob(self, nums) -> int:
        take, skip = 0, 0
        for x in nums:
            take, skip = skip + x, max(skip, take)
        return max(take, skip)


# ===========================================================================
# 5. Maximum Subarray (LeetCode #53) - Kadane
#    cur = max(x, cur + x);  best = max(best, cur)
# ===========================================================================
class SolutionMaxSub:
    def maxSubArray(self, nums) -> int:
        best = cur = nums[0]
        for x in nums[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best


# ===========================================================================
# 6. Unique Paths (LeetCode #62)
#    dp[c] += dp[c-1]  (한 행만 유지, O(n) 공간)
# ===========================================================================
class SolutionPaths:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n
        for _ in range(1, m):
            for c in range(1, n):
                dp[c] += dp[c - 1]
        return dp[-1]


# ===========================================================================
# 7. Coin Change (LeetCode #322) - 배낭형(무한)
#    dp[a] = min(dp[a], dp[a-c] + 1)
# ===========================================================================
class SolutionCoin:
    def coinChange(self, coins, amount: int) -> int:
        INF = float("inf")
        dp = [0] + [INF] * amount
        for a in range(1, amount + 1):
            for c in coins:
                if c <= a and dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1
        return dp[amount] if dp[amount] != INF else -1


# ===========================================================================
# 8. Longest Increasing Subsequence (LeetCode #300)
#    접근 A: O(n^2) DP  / 접근 B: O(n log n) 이분 탐색
# ===========================================================================
class SolutionLIS:
    def lengthOfLIS_n2(self, nums) -> int:
        if not nums:
            return 0
        dp = [1] * len(nums)
        for i in range(len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)

    def lengthOfLIS(self, nums) -> int:     # O(n log n)
        tails = []                          # tails[k] = 길이 k+1 수열의 최소 끝값
        for x in nums:
            i = bisect_left(tails, x)
            if i == len(tails):
                tails.append(x)
            else:
                tails[i] = x
        return len(tails)


# ===========================================================================
# 9. Longest Common Subsequence (LeetCode #1143)
#    같으면 dp[i-1][j-1]+1, 다르면 max(dp[i-1][j], dp[i][j-1])
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
# 10. 정수 삼각형 (프로그래머스 #43105)
#     dp[c] += max(위-왼, 위-오른).  아래 행부터 접어 올려도 됨.
# ===========================================================================
def solution_triangle(triangle):
    dp = triangle[0][:]                      # 첫 행 복사
    for r in range(1, len(triangle)):
        row = triangle[r]
        nxt = [0] * len(row)
        for c in range(len(row)):
            up_left = dp[c - 1] if c - 1 >= 0 else float("-inf")
            up = dp[c] if c < len(dp) else float("-inf")
            nxt[c] = row[c] + max(up_left, up)
        dp = nxt
    return max(dp)


# ===========================================================================
# 11. N으로 표현 (프로그래머스 #42895)
#     dp[k] = N을 k번 써서 만들 수 있는 값들의 집합.
# ===========================================================================
def solution_n_repr(N, number):
    if N == number:
        return 1
    dp = [set() for _ in range(9)]           # 1..8 사용
    for k in range(1, 9):
        dp[k].add(int(str(N) * k))           # NN...N (k개)
        for i in range(1, k):
            for a in dp[i]:
                for b in dp[k - i]:
                    dp[k].add(a + b)
                    dp[k].add(a - b)
                    dp[k].add(a * b)
                    if b != 0:
                        dp[k].add(a // b)
        if number in dp[k]:
            return k
    return -1


# ===========================================================================
# 12. 등굣길 (프로그래머스 #42898)
#     dp[r][c] = (위 + 왼) % MOD, 물웅덩이는 0.
# ===========================================================================
def solution_school(m, n, puddles):
    MOD = 1_000_000_007
    blocked = {(x, y) for x, y in puddles}   # (열, 행) 좌표
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    dp[1][1] = 1
    for r in range(1, n + 1):
        for c in range(1, m + 1):
            if r == 1 and c == 1:
                continue
            if (c, r) in blocked:
                dp[r][c] = 0
            else:
                dp[r][c] = (dp[r - 1][c] + dp[r][c - 1]) % MOD
    return dp[n][m]


def run_tests():
    print("=" * 60)
    print("Day 31 - DP 해설 self-test")
    print("=" * 60)

    # 1. Fibonacci
    s = SolutionFib()
    for n, exp in [(0, 0), (1, 1), (10, 55), (20, 6765)]:
        assert s.fib(n) == exp and s.fib_memo(n) == exp
    print("[1] Fibonacci            OK  (memo == O(1)-space)")

    # 2. Climbing Stairs
    c = SolutionClimb()
    assert c.climbStairs(2) == 2 and c.climbStairs(3) == 3 and c.climbStairs(5) == 8
    print("[2] Climbing Stairs      OK")

    # 3. Min Cost Climbing Stairs
    mc = SolutionMinCost()
    assert mc.minCostClimbingStairs([10, 15, 20]) == 15
    assert mc.minCostClimbingStairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]) == 6
    print("[3] Min Cost Climbing    OK")

    # 4. House Robber
    r = SolutionRob()
    assert r.rob([1, 2, 3, 1]) == 4 and r.rob([2, 7, 9, 3, 1]) == 12
    print("[4] House Robber         OK")

    # 5. Maximum Subarray
    ms = SolutionMaxSub()
    assert ms.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert ms.maxSubArray([-1, -2, -3]) == -1
    print("[5] Maximum Subarray     OK")

    # 6. Unique Paths
    up = SolutionPaths()
    assert up.uniquePaths(3, 7) == 28 and up.uniquePaths(3, 2) == 3
    print("[6] Unique Paths         OK")

    # 7. Coin Change
    cc = SolutionCoin()
    assert cc.coinChange([1, 2, 5], 11) == 3
    assert cc.coinChange([2], 3) == -1
    assert cc.coinChange([1, 3, 4], 6) == 2      # 그리디는 3, DP는 2
    print("[7] Coin Change          OK  (DP beats greedy on [1,3,4],6)")

    # 8. LIS - 두 접근이 같은 답
    lis = SolutionLIS()
    for arr, exp in [([10, 9, 2, 5, 3, 7, 101, 18], 4),
                     ([0, 1, 0, 3, 2, 3], 4),
                     ([7, 7, 7, 7], 1)]:
        assert lis.lengthOfLIS(arr) == exp
        assert lis.lengthOfLIS_n2(arr) == exp
    print("[8] LIS                  OK  (O(n^2) == O(n log n))")

    # 9. LCS
    lcs = SolutionLCS()
    assert lcs.longestCommonSubsequence("abcde", "ace") == 3
    assert lcs.longestCommonSubsequence("abc", "def") == 0
    print("[9] LCS                  OK")

    # 10. 정수 삼각형
    tri = [[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
    assert solution_triangle(tri) == 30
    print("[10] 정수 삼각형         OK  (result=30)")

    # 11. N으로 표현
    assert solution_n_repr(5, 12) == 4
    assert solution_n_repr(2, 11) == 3
    assert solution_n_repr(5, 5) == 1
    print("[11] N으로 표현          OK")

    # 12. 등굣길
    assert solution_school(4, 3, [[2, 2]]) == 4
    assert solution_school(2, 2, []) == 2
    print("[12] 등굣길              OK  (result=4)")

    print("=" * 60)
    print("모든 테스트 통과 (All tests passed)")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()

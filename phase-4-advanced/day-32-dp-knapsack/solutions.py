# -*- coding: utf-8 -*-
"""
Day 32 - 배낭 문제 (Knapsack DP) 해설

플랫폼 시그니처 유지:
  - LeetCode  : class Solution 의 메서드
  - 프로그래머스 : def solution(...)
각 문제에 assert 자체 테스트 포함. 가능한 곳은 다중 접근 + 복잡도 비교.

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python solutions.py
"""


# ===========================================================================
# 1. Coin Change (LeetCode #322) - 무한 배낭(최소 개수)
#    dp[a] = min(dp[a], dp[a-c] + 1),  금액 정순(무한)
# ===========================================================================
class SolutionCoinChange:
    def coinChange(self, coins, amount: int) -> int:
        INF = float("inf")
        dp = [0] + [INF] * amount
        for c in coins:
            for a in range(c, amount + 1):           # 무한 -> 정순
                if dp[a - c] + 1 < dp[a]:
                    dp[a] = dp[a - c] + 1
        return dp[amount] if dp[amount] != INF else -1


# ===========================================================================
# 2. Coin Change II (LeetCode #518) - 무한 배낭(조합 카운팅)
#    dp[a] += dp[a-c].  조합이므로 coins 바깥 / amount 안쪽.
# ===========================================================================
class SolutionCoinChange2:
    def change(self, amount: int, coins) -> int:
        dp = [0] * (amount + 1)
        dp[0] = 1
        for c in coins:                              # 동전 바깥 = 조합
            for a in range(c, amount + 1):           # 무한 -> 정순
                dp[a] += dp[a - c]
        return dp[amount]


# ===========================================================================
# 3. Partition Equal Subset Sum (LeetCode #416) - 0/1 부분집합 합(가능여부)
#    합 S 가 홀수면 False. 아니면 T=S//2 를 만들 수 있는가.
#    dp[s] = dp[s] or dp[s-x],  합 역순(0/1)
# ===========================================================================
class SolutionPartition:
    def canPartition(self, nums) -> bool:
        S = sum(nums)
        if S % 2 == 1:
            return False
        T = S // 2
        dp = [False] * (T + 1)
        dp[0] = True
        for x in nums:
            for s in range(T, x - 1, -1):            # 0/1 -> 역순
                if dp[s - x]:
                    dp[s] = True
            if dp[T]:
                return True
        return dp[T]


# ===========================================================================
# 4. Target Sum (LeetCode #494) - 0/1 부분집합 합(카운팅) + 변환
#    P - N = target, P + N = S  =>  P = (S + target)/2
#    P 를 만드는 부분집합의 개수. (S+target) 이 홀/음수면 0.
#    접근 A: 변환 후 0/1 카운팅 배낭  /  접근 B: 완전탐색(검증용)
# ===========================================================================
class SolutionTargetSum:
    def findTargetSumWays(self, nums, target: int) -> int:
        S = sum(nums)
        if abs(target) > S or (S + target) % 2 == 1:
            return 0
        P = (S + target) // 2
        dp = [0] * (P + 1)
        dp[0] = 1
        for x in nums:
            for s in range(P, x - 1, -1):            # 0/1 -> 역순
                dp[s] += dp[s - x]
        return dp[P]

    def findTargetSumWays_bruteforce(self, nums, target: int) -> int:
        """검증용 완전탐색 O(2^n): 각 수에 +/- 부여."""
        n = len(nums)

        def dfs(i, total):
            if i == n:
                return 1 if total == target else 0
            return dfs(i + 1, total + nums[i]) + dfs(i + 1, total - nums[i])

        return dfs(0, 0)


# ===========================================================================
# 5. Ones and Zeroes (LeetCode #474) - 2차원 0/1 배낭(제약 2개)
#    각 문자열 = 물건, 용량 축 = (0의 개수 m, 1의 개수 n)
#    dp[i][j] = max(dp[i][j], dp[i-z][j-o] + 1),  i,j 둘 다 역순
# ===========================================================================
class SolutionOnesZeroes:
    def findMaxForm(self, strs, m: int, n: int) -> int:
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for s in strs:
            z = s.count("0")
            o = len(s) - z
            for i in range(m, z - 1, -1):            # 0/1 -> 역순
                for j in range(n, o - 1, -1):        # 0/1 -> 역순
                    if dp[i - z][j - o] + 1 > dp[i][j]:
                        dp[i][j] = dp[i - z][j - o] + 1
        return dp[m][n]


# ===========================================================================
# 6. 도둑질 (프로그래머스 #42897) - 원형 선택 DP(House Robber 원형)
#    원형이라 첫 집/마지막 집을 동시에 못 턴다.
#    -> [0:n-1] 과 [1:n] 두 일자형 구간의 House Robber 중 max.
# ===========================================================================
def _rob_line(money):
    """일자형 House Robber: dp[i] = max(dp[i-1], dp[i-2] + money[i])."""
    take, skip = 0, 0
    for x in money:
        take, skip = skip + x, max(skip, take)
    return max(take, skip)


def solution(money):
    n = len(money)
    if n == 1:
        return money[0]
    # (A) 0번 포함 가능 -> 마지막 제외,  (B) 마지막 포함 가능 -> 0번 제외
    return max(_rob_line(money[:-1]), _rob_line(money[1:]))


def run_tests():
    print("=" * 60)
    print("Day 32 - Knapsack DP 해설 self-test")
    print("=" * 60)

    # 1. Coin Change
    cc = SolutionCoinChange()
    assert cc.coinChange([1, 2, 5], 11) == 3
    assert cc.coinChange([2], 3) == -1
    assert cc.coinChange([1], 0) == 0
    print("[1] Coin Change (무한/최소)        OK")

    # 2. Coin Change II - 조합
    cc2 = SolutionCoinChange2()
    assert cc2.change(5, [1, 2, 5]) == 4       # {5},{2,2,1},{2,1,1,1},{1x5}
    assert cc2.change(3, [2]) == 0
    assert cc2.change(0, [7]) == 1
    print("[2] Coin Change II (무한/조합)     OK")

    # 3. Partition Equal Subset Sum
    pt = SolutionPartition()
    assert pt.canPartition([1, 5, 11, 5]) is True    # {1,5,5} vs {11}
    assert pt.canPartition([1, 2, 3, 5]) is False
    print("[3] Partition Equal Subset Sum     OK")

    # 4. Target Sum - DP 와 완전탐색이 같은 답
    ts = SolutionTargetSum()
    for nums, tgt, exp in [([1, 1, 1, 1, 1], 3, 5),
                           ([1], 1, 1),
                           ([1], 2, 0)]:
        assert ts.findTargetSumWays(nums, tgt) == exp
        assert ts.findTargetSumWays_bruteforce(nums, tgt) == exp
    print("[4] Target Sum (0/1 카운팅+변환)   OK  (DP == bruteforce)")

    # 5. Ones and Zeroes
    oz = SolutionOnesZeroes()
    assert oz.findMaxForm(["10", "0001", "111001", "1", "0"], 5, 3) == 4
    assert oz.findMaxForm(["10", "0", "1"], 1, 1) == 2
    print("[5] Ones and Zeroes (2D 0/1)       OK")

    # 6. 도둑질 (원형)
    assert solution([1, 2, 3, 1]) == 4         # 원형: 1+3 (0번,2번) = 4
    assert solution([2, 3, 2]) == 3            # 원형: 가운데 3만
    assert solution([200, 3, 140, 20, 10]) == 340   # 200+140
    print("[6] 도둑질 (원형 House Robber)     OK")

    print("=" * 60)
    print("모든 테스트 통과 (All tests passed)")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()

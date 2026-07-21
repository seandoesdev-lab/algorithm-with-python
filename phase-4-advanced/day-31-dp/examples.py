# -*- coding: utf-8 -*-
"""
Day 31 - 동적 계획법 입문 (Dynamic Programming) 예제 모음

핵심 주제:
  1) 피보나치 - 순진 재귀 vs Top-Down(메모) vs Bottom-Up(표) vs O(1) 공간
  2) 계단 오르기 (경우의 수)
  3) 최소 비용 계단 오르기
  4) 집도둑 (선택/건너뛰기)
  5) 최대 부분합 (Kadane)
  6) 격자 경로 수 (Unique Paths)
  7) 동전 교환 최소 개수 (배낭형) - 그리디로는 틀린다
  8) DP 설계 4단계 요약 출력

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from functools import lru_cache


# ---------------------------------------------------------------------------
# 1) 피보나치 - 4가지 구현 비교
# ---------------------------------------------------------------------------
def fib_naive(n):
    """순진 재귀: O(2^n). 작은 n에서만 사용(중복 계산 폭발)."""
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@lru_cache(maxsize=None)
def fib_topdown(n):
    """Top-Down 메모이제이션: 재귀 + 캐시. O(n)."""
    if n < 2:
        return n
    return fib_topdown(n - 1) + fib_topdown(n - 2)


def fib_bottomup(n):
    """Bottom-Up 타뷸레이션: 표를 작은 값부터 채움. O(n) 시간, O(n) 공간."""
    if n < 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def fib_optimized(n):
    """공간 최적화: 직전 두 값만 유지. O(n) 시간, O(1) 공간."""
    prev, cur = 0, 1
    for _ in range(n):
        prev, cur = cur, prev + cur
    return prev


# ---------------------------------------------------------------------------
# 2) 계단 오르기 - 경우의 수 (한 번에 1칸 또는 2칸)
#    dp[i] = dp[i-1] + dp[i-2]  (피보나치와 동일 구조)
# ---------------------------------------------------------------------------
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# ---------------------------------------------------------------------------
# 3) 최소 비용 계단 오르기
#    각 계단 비용 cost[i]를 내고 1칸 또는 2칸 오른다. 꼭대기(len) 도달 최소 비용.
#    dp[i] = cost[i] + min(dp[i-1], dp[i-2])
# ---------------------------------------------------------------------------
def min_cost_climbing_stairs(cost):
    n = len(cost)
    down_one, down_two = 0, 0  # 꼭대기 바로 아래 두 계단에서의 최소 비용
    for i in range(2, n + 1):
        cur = min(down_one + cost[i - 1], down_two + cost[i - 2])
        down_two, down_one = down_one, cur
    return down_one


# ---------------------------------------------------------------------------
# 4) 집도둑 (House Robber)
#    인접한 집은 못 턴다. 최대 금액.
#    take: 현재 집을 털 때, skip: 현재 집을 안 털 때
# ---------------------------------------------------------------------------
def rob(nums):
    take, skip = 0, 0
    for x in nums:
        take, skip = skip + x, max(skip, take)
    return max(take, skip)


# ---------------------------------------------------------------------------
# 5) 최대 부분합 (Maximum Subarray, Kadane)
#    dp[i] = max(a[i], dp[i-1] + a[i])  ("이어붙일까 / 새로 시작할까")
# ---------------------------------------------------------------------------
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


# ---------------------------------------------------------------------------
# 6) 격자 경로 수 (Unique Paths)
#    좌상->우하, 오른쪽/아래로만 이동. dp[c] += dp[c-1] (행 하나로 압축)
# ---------------------------------------------------------------------------
def unique_paths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            dp[c] += dp[c - 1]
    return dp[-1]


# ---------------------------------------------------------------------------
# 7) 동전 교환 최소 개수 (Coin Change) - 배낭형(무한 사용)
#    dp[a] = min(dp[a], dp[a-c] + 1). 불가능 금액은 INF로 유지.
#    NOTE: 그리디로 풀면 반례가 생긴다(아래 데모 참고).
# ---------------------------------------------------------------------------
def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != INF else -1


def coin_change_greedy(coins, amount):
    """(반례 시연용) 큰 동전부터 욕심내는 그리디 - 최적을 보장하지 못함."""
    cnt, rest = 0, amount
    for c in sorted(coins, reverse=True):
        take = rest // c
        cnt += take
        rest -= take * c
    return cnt if rest == 0 else -1


def main():
    print("=" * 60)
    print("Day 31 - Dynamic Programming (DP) 예제")
    print("=" * 60)

    print("\n[1] 피보나치 - 네 구현이 같은 값을 내는가")
    for n in [0, 1, 5, 10, 20]:
        v1 = fib_naive(n)
        v2 = fib_topdown(n)
        v3 = fib_bottomup(n)
        v4 = fib_optimized(n)
        ok = "O" if v1 == v2 == v3 == v4 else "X"
        print("  n=%2d  naive=%d topdown=%d bottomup=%d opt=%d  [%s]"
              % (n, v1, v2, v3, v4, ok))
    print("  fib(50) =", fib_optimized(50), "(순진 재귀로는 사실상 계산 불가)")

    print("\n[2] 계단 오르기 (경우의 수)")
    for n in [1, 2, 3, 5, 10]:
        print("  n=%2d -> %d 가지" % (n, climb_stairs(n)))

    print("\n[3] 최소 비용 계단 오르기")
    cost = [10, 15, 20]
    print("  cost=%s -> 최소 비용 %d" % (cost, min_cost_climbing_stairs(cost)))
    cost2 = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
    print("  cost=%s -> 최소 비용 %d" % (cost2, min_cost_climbing_stairs(cost2)))

    print("\n[4] 집도둑 (House Robber)")
    for arr in ([1, 2, 3, 1], [2, 7, 9, 3, 1], [5, 5, 10, 100, 10, 5]):
        print("  %s -> 최대 %d" % (arr, rob(arr)))

    print("\n[5] 최대 부분합 (Kadane)")
    for arr in ([-2, 1, -3, 4, -1, 2, 1, -5, 4], [-1, -2, -3], [5, 4, -1, 7, 8]):
        print("  %s -> %d" % (arr, max_subarray(arr)))

    print("\n[6] 격자 경로 수 (Unique Paths)")
    for m, n in [(3, 7), (3, 2), (1, 1), (10, 10)]:
        print("  격자 %dx%d -> %d 경로" % (m, n, unique_paths(m, n)))

    print("\n[7] 동전 교환 최소 개수 : DP vs 그리디(반례)")
    demo = [([1, 3, 4], 6), ([1, 2, 5], 11), ([2], 3)]
    for coins, amount in demo:
        d = coin_change(coins, amount)
        g = coin_change_greedy(coins, amount)
        flag = "same" if d == g else "GREEDY WRONG"
        print("  coins=%s amount=%d -> DP=%s, Greedy=%s  [%s]"
              % (coins, amount, d, g, flag))
    print("  * coins=[1,3,4], amount=6 에서 그리디는 3개(4+1+1), DP는 2개(3+3)")

    print("\n[요약] DP 설계 4단계")
    print("  1) 상태 정의  : dp[i] 가 '무엇의 답'인지 한 문장으로")
    print("  2) 점화식     : dp[i] 를 더 작은 dp[...] 로 표현")
    print("  3) 초기값     : 가장 작은 상태의 값을 직접 채움")
    print("  4) 계산 순서  : 의존 상태가 먼저 채워지도록")

    print("\n" + "=" * 60)
    print("모든 예제 실행 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()

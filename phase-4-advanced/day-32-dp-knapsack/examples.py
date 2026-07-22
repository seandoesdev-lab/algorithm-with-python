# -*- coding: utf-8 -*-
"""
Day 32 - 배낭 문제 (Knapsack DP) 예제 모음

핵심 주제:
  1) 0/1 배낭 - 2차원 표(직관형) vs 1차원 역순(실전형) vs Top-Down 메모
  2) 무한 배낭 - 1차원 정순
  3) 0/1 과 무한의 차이 = 루프 방향(역순 vs 정순) 실증
  4) 부분집합 합(Subset Sum) - 가치=무게인 0/1 배낭(bool)
  5) 카운팅: 조합(coins 바깥) vs 순열(amount 바깥) - 루프 순서 실증
  6) 담은 물건 복원(2D 표 역추적)

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from functools import lru_cache


# ---------------------------------------------------------------------------
# 1) 0/1 배낭 - 2차원 표 (직관형)
#    dp[i][w] = 물건 1..i 까지, 용량 w 에서의 최대 가치
#    dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt] + val)
# ---------------------------------------------------------------------------
def knapsack_2d(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = weights[i - 1], values[i - 1]
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]                       # 안 담기
            if w >= wt:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wt] + val)  # 담기
    return dp[n][W]


# ---------------------------------------------------------------------------
# 2) 0/1 배낭 - 1차원 역순 (실전형, O(W) 공간)
#    같은 물건을 두 번 담지 않으려면 용량을 큰 쪽 -> 작은 쪽(역순)으로.
# ---------------------------------------------------------------------------
def knapsack_01(weights, values, W):
    dp = [0] * (W + 1)
    for wt, val in zip(weights, values):
        for w in range(W, wt - 1, -1):                    # 역순!
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[W]


# ---------------------------------------------------------------------------
# 3) 0/1 배낭 - Top-Down 메모이제이션 (점화식과 1:1)
# ---------------------------------------------------------------------------
def knapsack_topdown(weights, values, W):
    n = len(weights)

    @lru_cache(maxsize=None)
    def knap(i, cap):
        if i == n or cap == 0:
            return 0
        best = knap(i + 1, cap)                           # i 안 담기
        if weights[i] <= cap:
            best = max(best, values[i] + knap(i + 1, cap - weights[i]))  # 담기
        return best

    result = knap(0, W)
    knap.cache_clear()
    return result


# ---------------------------------------------------------------------------
# 4) 무한 배낭 - 1차원 정순 (같은 물건 무제한)
#    0/1 과 코드가 거의 같고 루프 방향만 반대(작은 쪽 -> 큰 쪽).
# ---------------------------------------------------------------------------
def knapsack_unbounded(weights, values, W):
    dp = [0] * (W + 1)
    for wt, val in zip(weights, values):
        for w in range(wt, W + 1):                        # 정순!
            dp[w] = max(dp[w], dp[w - wt] + val)
    return dp[W]


# ---------------------------------------------------------------------------
# 5) 부분집합 합 (Subset Sum) - 합 T 를 만들 수 있는가? (bool 0/1 배낭)
# ---------------------------------------------------------------------------
def subset_sum(nums, T):
    dp = [False] * (T + 1)
    dp[0] = True
    for x in nums:
        for s in range(T, x - 1, -1):                     # 0/1 역순
            if dp[s - x]:
                dp[s] = True
    return dp[T]


# ---------------------------------------------------------------------------
# 6) 카운팅 - 조합(순서 무시) vs 순열(순서 구분)
#    coins 로 amount 를 만드는 방법 수. 루프 순서가 의미를 바꾼다.
# ---------------------------------------------------------------------------
def count_combinations(coins, amount):
    """조합: coins 루프가 바깥. {1,2}와 {2,1}을 같은 것으로 센다."""
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]


def count_permutations(coins, amount):
    """순열: amount 루프가 바깥. {1,2}와 {2,1}을 다른 것으로 센다."""
    dp = [0] * (amount + 1)
    dp[0] = 1
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] += dp[a - c]
    return dp[amount]


# ---------------------------------------------------------------------------
# 7) 담은 물건 복원 - 2D 표를 역추적
# ---------------------------------------------------------------------------
def knapsack_items(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = weights[i - 1], values[i - 1]
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]
            if w >= wt:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wt] + val)
    # 역추적: dp[i][w] != dp[i-1][w] 이면 물건 i 를 담은 것
    chosen, w = [], W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(i - 1)                          # 0-index 물건 번호
            w -= weights[i - 1]
    chosen.reverse()
    return dp[n][W], chosen


def main():
    print("=" * 60)
    print("Day 32 - Knapsack DP 예제")
    print("=" * 60)

    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    W = 5

    print("\n[1] 0/1 배낭 - 세 구현이 같은 값을 내는가")
    v1 = knapsack_2d(weights, values, W)
    v2 = knapsack_01(weights, values, W)
    v3 = knapsack_topdown(weights, values, W)
    ok = "O" if v1 == v2 == v3 else "X"
    print("  weights=%s values=%s W=%d" % (weights, values, W))
    print("  2d=%d  1d=%d  topdown=%d  [%s]  (기대값 7)" % (v1, v2, v3, ok))

    print("\n[2] 무한 배낭 vs 0/1 배낭 - 루프 방향 차이 실증")
    ub = knapsack_unbounded(weights, values, W)
    print("  0/1(역순)      = %d  (각 물건 최대 1번)" % knapsack_01(weights, values, W))
    print("  무한(정순)     = %d  (물건을 무제한 사용)" % ub)
    print("  * 무한이면 (2,3) 을 여러 번 담아 더 큰 값이 가능하다")

    print("\n[3] 부분집합 합 (Subset Sum)")
    nums = [3, 34, 4, 12, 5, 2]
    for T in [9, 10, 30, 11]:
        print("  nums=%s, T=%2d -> %s" % (nums, T, subset_sum(nums, T)))
    print("  * 9=4+5, 10=3+5+2 처럼 합을 만들 수 있는지 판정")

    print("\n[4] 카운팅 - 조합 vs 순열 (coins=[1,2,3], amount=4)")
    coins = [1, 2, 3]
    comb = count_combinations(coins, 4)
    perm = count_permutations(coins, 4)
    print("  조합(순서 무시) = %d" % comb)
    print("  순열(순서 구분) = %d" % perm)
    print("  * 루프 순서만 바꿨는데 의미가 달라진다 (조합 %d != 순열 %d)"
          % (comb, perm))

    print("\n[5] 담은 물건 복원 (2D 역추적)")
    best, chosen = knapsack_items(weights, values, W)
    print("  최대 가치 = %d, 담은 물건(0-index) = %s" % (best, chosen))
    picked = [(weights[i], values[i]) for i in chosen]
    print("  담은 (무게,가치) = %s" % picked)

    print("\n[요약] 배낭 4문(問)")
    print("  1) 물건/용량 축은 무엇인가")
    print("  2) 각 물건 몇 번 쓰나 -> 0/1(역순) or 무한(정순)")
    print("  3) 무엇을 최적화 -> max/min / 개수(+=) / 가능여부(or)")
    print("  4) 초기값 -> 가치 0 / 가능 True / 개수 1")

    print("\n" + "=" * 60)
    print("모든 예제 실행 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()

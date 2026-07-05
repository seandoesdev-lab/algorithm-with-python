# -*- coding: utf-8 -*-
"""
Day 21 - 그리디 (Greedy): 핵심 개념 예제 모음

각 예제는 "정렬 기준 -> 순차 확정" 이라는 그리디 골격을 보여준다.
그리디가 통하는 경우와, 통하지 않는 반례(거스름돈)를 함께 다룬다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""


# ---------------------------------------------------------------------------
# 1) 구간 스케줄링 - 겹치지 않는 최대 개수 (Activity Selection)
#    핵심: "끝나는 시간(end)이 이른 순"으로 정렬하면 남는 시간이 최대가 된다.
# ---------------------------------------------------------------------------
def max_non_overlapping(intervals):
    intervals = sorted(intervals, key=lambda x: x[1])   # end 오름차순
    count = 0
    last_end = float("-inf")
    for start, end in intervals:
        if start >= last_end:            # 직전 회의가 끝난 뒤 시작
            count += 1
            last_end = end
    return count


# ---------------------------------------------------------------------------
# 2) 보트 태우기 - 정렬 + 투 포인터 그리디
#    핵심: 가장 무거운 사람과 가장 가벼운 사람을 짝지어 태운다.
# ---------------------------------------------------------------------------
def num_rescue_boats(people, limit):
    people = sorted(people)
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo <= hi:
        if people[lo] + people[hi] <= limit:
            lo += 1                      # 가벼운 사람도 함께 태움
        hi -= 1                          # 무거운 사람은 무조건 태움
        boats += 1
    return boats


# ---------------------------------------------------------------------------
# 3) Jump Game - 도달 가능한 최대 위치만 갱신 (정렬 불필요, O(n))
#    핵심: reach 를 넘어서는 인덱스에 도달하면 실패.
# ---------------------------------------------------------------------------
def can_jump(nums):
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True


# ---------------------------------------------------------------------------
# 4) 거스름돈 - "큰 동전부터" 그리디 (정준 체계에서만 최적!)
#    아래 4-b 에서 그리디가 틀리는 반례를 DP 와 비교한다.
# ---------------------------------------------------------------------------
def coin_change_greedy(amount, coins=(500, 100, 50, 10)):
    count = 0
    for c in sorted(coins, reverse=True):
        count += amount // c
        amount %= c
    return count if amount == 0 else -1


def coin_change_dp(amount, coins):
    """비교용: 항상 최적을 주는 DP. O(amount * len(coins))."""
    INF = amount + 1
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1


# ---------------------------------------------------------------------------
# 5) 회의실 개수 - "가장 급한 것 먼저"를 힙으로 (그리디 + 우선순위 큐)
#    핵심: 시작 시간 순으로 보며, 끝난 방(가장 이른 end)을 재사용한다.
# ---------------------------------------------------------------------------
def min_meeting_rooms(intervals):
    import heapq
    if not intervals:
        return 0
    intervals = sorted(intervals, key=lambda x: x[0])   # start 오름차순
    heap = []                                           # 현재 사용중 방들의 end
    for start, end in intervals:
        if heap and heap[0] <= start:   # 가장 먼저 끝난 방을 재사용
            heapq.heappop(heap)
        heapq.heappush(heap, end)
    return len(heap)


def _demo():
    meetings = [(1, 3), (2, 4), (3, 5), (0, 6), (5, 7), (8, 9)]
    print("1) max non-overlapping meetings:", max_non_overlapping(meetings))  # 4

    people = [3, 2, 2, 1]
    print("2) rescue boats (limit=3):", num_rescue_boats(people, 3))          # 3

    print("3) can jump [2,3,1,1,4]:", can_jump([2, 3, 1, 1, 4]))              # True
    print("3) can jump [3,2,1,0,4]:", can_jump([3, 2, 1, 0, 4]))             # False

    # 정준 체계에서는 그리디 == DP
    print("4) change 850 greedy:", coin_change_greedy(850))                   # 5
    # 반례: coins=[1,3,4], amount=6 -> greedy 3개, dp 2개
    g = coin_change_greedy(6, coins=(1, 3, 4))
    d = coin_change_dp(6, coins=[1, 3, 4])
    print("4) change 6 with [1,3,4] greedy vs dp:", g, "vs", d, "-> greedy WRONG")

    print("5) min meeting rooms:", min_meeting_rooms(meetings))               # 3


if __name__ == "__main__":
    _demo()

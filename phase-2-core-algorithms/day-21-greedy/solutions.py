# -*- coding: utf-8 -*-
"""
Day 21 - 그리디 (Greedy): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(그리디 vs DP/완전 탐색 등)을 두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""


# ===========================================================================
# 1. Assign Cookies (LeetCode #455)
#    두 배열 정렬 후 "작은 기준 아이에 가장 작은 만족 쿠키" 매칭. O(n log n)
# ===========================================================================
class SolutionAssignCookies:
    def findContentChildren(self, g, s):
        g.sort()
        s.sort()
        i = j = 0                     # i: 아이 인덱스, j: 쿠키 인덱스
        while i < len(g) and j < len(s):
            if s[j] >= g[i]:          # 이 쿠키로 이 아이를 만족
                i += 1
            j += 1                    # 못 만족해도 쿠키는 다음으로
        return i


# ===========================================================================
# 2. 체육복 (프로그래머스 #42862)
#    앞 번호부터 빌려주는 그리디. O(n log n) (정렬)
# ===========================================================================
def solution_gym(n, lost, reserve):
    # 여벌이 있으나 도난당한 학생은 자기 것만 사용(빌려주지도, 빌리지도 않음)
    reserve_only = set(reserve) - set(lost)
    lost_only = set(lost) - set(reserve)
    for r in sorted(reserve_only):
        if r - 1 in lost_only:        # 앞 번호에게 우선
            lost_only.remove(r - 1)
        elif r + 1 in lost_only:      # 없으면 뒤 번호에게
            lost_only.remove(r + 1)
    return n - len(lost_only)


# ===========================================================================
# 3. 큰 수 만들기 (프로그래머스 #42883)
#    단조 감소 스택: 뒤에 더 큰 수가 오면 앞의 작은 수를 지운다. O(n)
# ===========================================================================
def solution_make_big(number, k):
    stack = []
    for d in number:
        while stack and k > 0 and stack[-1] < d:
            stack.pop()
            k -= 1
        stack.append(d)
    if k > 0:                          # 다 돌고 남으면 뒤에서 자른다
        stack = stack[:len(stack) - k]
    return "".join(stack)


# ===========================================================================
# 4. Jump Game (LeetCode #55)
#    도달 가능한 최대 위치 reach 만 갱신. O(n) / O(1)
# ===========================================================================
class SolutionJumpGame:
    def canJump(self, nums):
        reach = 0
        for i, step in enumerate(nums):
            if i > reach:
                return False
            reach = max(reach, i + step)
        return True


# ===========================================================================
# 5. Jump Game II (LeetCode #45)
#    구간 확장 그리디(BFS 레벨). O(n). 비교용 DP O(n^2).
# ===========================================================================
class SolutionJumpGame2:
    def jump(self, nums):
        jumps = cur_end = farthest = 0
        for i in range(len(nums) - 1):
            farthest = max(farthest, i + nums[i])
            if i == cur_end:               # 현재 점프 구간의 끝에 도달
                jumps += 1
                cur_end = farthest         # 다음 점프로 갈 수 있는 최대까지
        return jumps

    def jump_dp(self, nums):
        """비교용: dp[i] = i까지 최소 점프. O(n^2) / O(n)."""
        n = len(nums)
        INF = float("inf")
        dp = [0] + [INF] * (n - 1)
        for i in range(n):
            for j in range(1, nums[i] + 1):
                if i + j < n:
                    dp[i + j] = min(dp[i + j], dp[i] + 1)
        return dp[n - 1]


# ===========================================================================
# 6. 구명보트 (프로그래머스 #42885)
#    정렬 + 양끝 투 포인터. O(n log n)
# ===========================================================================
def solution_boats(people, limit):
    people.sort()
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo <= hi:
        if people[lo] + people[hi] <= limit:
            lo += 1                        # 가벼운 사람도 함께
        hi -= 1                            # 무거운 사람은 무조건
        boats += 1
    return boats


# ===========================================================================
# 7. Gas Station (LeetCode #134)
#    총합 판정 + 누적 잔량이 음수면 시작점 재설정. O(n) / O(1)
# ===========================================================================
class SolutionGasStation:
    def canCompleteCircuit(self, gas, cost):
        if sum(gas) < sum(cost):
            return -1                      # 전체가 부족하면 불가능
        start = 0
        tank = 0
        for i in range(len(gas)):
            tank += gas[i] - cost[i]
            if tank < 0:                   # 여기까지 못 버티면
                start = i + 1              # 다음 지점을 새 시작점으로
                tank = 0
        return start


# ===========================================================================
# 8. Non-overlapping Intervals (LeetCode #435)
#    end 정렬 후 겹치지 않는 최대 개수 -> 나머지가 제거 수. O(n log n)
# ===========================================================================
class SolutionEraseOverlap:
    def eraseOverlapIntervals(self, intervals):
        intervals.sort(key=lambda x: x[1])
        keep = 0
        last_end = float("-inf")
        for s, e in intervals:
            if s >= last_end:              # 경계가 닿으면 겹치지 않음
                keep += 1
                last_end = e
        return len(intervals) - keep


# ===========================================================================
# 9. 단속카메라 (프로그래머스 #42884)
#    진출(out) 정렬 후, 커버 못 하는 차가 오면 그 out 지점에 카메라. O(n log n)
# ===========================================================================
def solution_cameras(routes):
    routes.sort(key=lambda x: x[1])        # 진출 지점 오름차순
    cameras = 0
    last = float("-inf")                   # 마지막 카메라 위치
    for enter, leave in routes:
        if enter > last:                   # 현재 차가 카메라 범위 밖
            cameras += 1
            last = leave                   # 진출 지점에 새 카메라
    return cameras


# ===========================================================================
# 10. 조이스틱 (프로그래머스 #42860)
#    상하(문자 변경) 최소 + 좌우 이동 그리디 최소. O(n^2)
# ===========================================================================
def solution_joystick(name):
    n = len(name)
    # (1) 상하: 각 자리 A로부터의 최소 회전
    change = sum(min(ord(c) - ord("A"), ord("Z") - ord(c) + 1) for c in name)
    # (2) 좌우: 기본은 끝까지 직진(n-1). 연속된 A 구간을 되돌아 건너뛰는 경로 비교
    move = n - 1
    for i in range(n):
        nxt = i + 1
        while nxt < n and name[nxt] == "A":   # 연속 A 구간 건너뛰기
            nxt += 1
        # i까지 간 뒤 되돌아 왼쪽 끝 구간 처리 vs 그 반대
        move = min(move, i + (n - nxt) + min(i, n - nxt))
    return change + move


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    ac = SolutionAssignCookies()
    assert ac.findContentChildren([1, 2, 3], [1, 1]) == 1
    assert ac.findContentChildren([1, 2], [1, 2, 3]) == 2

    assert solution_gym(5, [2, 4], [1, 3, 5]) == 5
    assert solution_gym(5, [2, 4], [3]) == 4
    assert solution_gym(3, [3], [1]) == 2

    assert solution_make_big("1924", 2) == "94"
    assert solution_make_big("1231234", 3) == "3234"
    assert solution_make_big("4177252841", 4) == "775841"

    jg = SolutionJumpGame()
    assert jg.canJump([2, 3, 1, 1, 4]) is True
    assert jg.canJump([3, 2, 1, 0, 4]) is False

    jg2 = SolutionJumpGame2()
    assert jg2.jump([2, 3, 1, 1, 4]) == 2
    assert jg2.jump([2, 3, 0, 1, 4]) == 2
    assert jg2.jump([0]) == 0
    assert jg2.jump_dp([2, 3, 1, 1, 4]) == 2
    assert jg2.jump_dp([2, 3, 0, 1, 4]) == 2

    assert solution_boats([70, 50, 80, 50], 100) == 3
    assert solution_boats([70, 80, 50], 100) == 3

    gs = SolutionGasStation()
    assert gs.canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert gs.canCompleteCircuit([2, 3, 4], [3, 4, 3]) == -1

    eo = SolutionEraseOverlap()
    assert eo.eraseOverlapIntervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert eo.eraseOverlapIntervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert eo.eraseOverlapIntervals([[1, 2], [2, 3]]) == 0

    assert solution_cameras([[-20, -15], [-14, -5], [-18, -13], [-5, -3]]) == 2
    assert solution_cameras([[0, 5], [1, 2], [3, 8]]) == 2   # 교집합이 비어 2대
    assert solution_cameras([[0, 5], [1, 4], [2, 3]]) == 1   # 공통점 존재 1대

    assert solution_joystick("JEROEN") == 56
    assert solution_joystick("JAN") == 23
    assert solution_joystick("AAA") == 0
    assert solution_joystick("BBBBAAAB") == 10

    print("Day 21 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()

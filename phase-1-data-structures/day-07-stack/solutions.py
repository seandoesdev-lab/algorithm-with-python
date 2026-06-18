"""Day 7 해설 — 스택 (Stack).

각 문제마다 접근 방식을 주석으로 먼저 설명하고,
가능하면 여러 접근(브루트포스 -> 최적화)을 함께 제시한다.
플랫폼 시그니처: LeetCode = class Solution 메서드 / 프로그래머스 = def solution(...).
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""

from typing import List


# ---- 문제 1: 올바른 괄호 (프로그래머스 #12909) -------------------
# 접근 1) 카운터  | 시간복잡도: O(n), 공간 O(1)
# '(' 면 +1, ')' 면 -1. 도중 음수면 실패, 끝에 0이 아니면 실패.
def solution_12909_counter(s: str) -> bool:
    depth = 0
    for ch in s:
        depth += 1 if ch == "(" else -1
        if depth < 0:               # 닫는 괄호가 여는 것보다 먼저 많이 옴
            return False
    return depth == 0


# 접근 2) 스택  | 시간복잡도: O(n), 공간 O(n)
def solution_12909_stack(s: str) -> bool:
    st = []
    for ch in s:
        if ch == "(":
            st.append(ch)
        else:
            if not st:              # 닫을 짝이 없음
                return False
            st.pop()
    return not st                   # 끝에 남으면 실패


# ---- 문제 2: Valid Parentheses (LeetCode #20) --------------------
# 여러 종류 괄호. 닫힘->열림 매핑으로 top 과 비교.
class Solution20:
    # 접근) 스택 + 매핑 딕셔너리  | 시간복잡도: O(n), 공간 O(n)
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}
        st = []
        for ch in s:
            if ch in "([{":
                st.append(ch)
            else:                           # 닫는 괄호
                if not st or st[-1] != pairs[ch]:
                    return False
                st.pop()
        return not st


# ---- 문제 3: Min Stack (LeetCode #155) ---------------------------
# push/pop/top/getMin 모두 O(1).
# 접근) 값과 '그 시점까지의 최솟값'을 함께 쌓는 보조 스택
class MinStack:
    def __init__(self) -> None:
        self._stack: List[int] = []
        self._mins: List[int] = []          # _mins[-1] = 현재 최솟값

    def push(self, val: int) -> None:       # O(1)
        self._stack.append(val)
        cur_min = val if not self._mins else min(val, self._mins[-1])
        self._mins.append(cur_min)

    def pop(self) -> None:                  # O(1)
        self._stack.pop()
        self._mins.pop()

    def top(self) -> int:                   # O(1)
        return self._stack[-1]

    def getMin(self) -> int:                # O(1)
        return self._mins[-1]


# ---- 문제 4: 주식가격 (프로그래머스 #42584) ----------------------
# 가격이 떨어지지 않은 기간(초).
# 접근 1) 이중 루프 (직관)  | 시간복잡도: O(n^2)
def solution_42584_bruteforce(prices: List[int]) -> List[int]:
    n = len(prices)
    answer = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            answer[i] += 1
            if prices[j] < prices[i]:       # 떨어진 순간 멈춤
                break
    return answer


# 접근 2) 모노토닉 스택  | 시간복잡도: O(n)
# 인덱스를 쌓다가 가격이 낮아지면 pop 하며 기간(현재 i - 그 인덱스) 확정.
def solution_42584_stack(prices: List[int]) -> List[int]:
    n = len(prices)
    answer = [0] * n
    st = []                                 # 아직 안 떨어진 인덱스들
    for i, price in enumerate(prices):
        while st and prices[st[-1]] > price:
            j = st.pop()
            answer[j] = i - j               # j 시점에서 i 초 만에 떨어짐
        st.append(i)
    for j in st:                            # 끝까지 안 떨어진 것들
        answer[j] = n - 1 - j
    return answer


# ---- 문제 5: Daily Temperatures (LeetCode #739) ------------------
# 더 따뜻한 날까지 며칠(없으면 0).
class Solution739:
    # 접근) 모노토닉 스택(인덱스)  | 시간복잡도: O(n), 공간 O(n)
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        st = []                             # 아직 더 따뜻한 날 못 만난 인덱스
        for i, t in enumerate(temperatures):
            while st and temperatures[st[-1]] < t:
                j = st.pop()
                answer[j] = i - j
            st.append(i)
        return answer


# ---- 문제 6: 크레인 인형뽑기 게임 (프로그래머스 #64061, 카카오) ---
# 바구니를 스택으로. 같은 인형이 연속이면 둘 다 터진다.
# 접근) 스택 시뮬레이션  | 시간복잡도: O(len(moves) * N)
def solution_64061(board: List[List[int]], moves: List[int]) -> int:
    basket: List[int] = []
    popped = 0
    for move in moves:
        col = move - 1                      # 1-based -> 0-based
        for row in range(len(board)):       # 위에서 아래로 첫 인형 탐색
            doll = board[row][col]
            if doll != 0:
                board[row][col] = 0         # 집어 올림
                if basket and basket[-1] == doll:
                    basket.pop()            # 같은 인형 -> 둘 다 터짐
                    popped += 2
                else:
                    basket.append(doll)
                break                       # 한 번에 하나만 집음
    return popped


if __name__ == "__main__":
    # 문제 1
    for fn in (solution_12909_counter, solution_12909_stack):
        assert fn("()()") is True
        assert fn("(())()") is True
        assert fn(")()(") is False
        assert fn("(()(") is False
        assert fn("(") is False
        assert fn("") is True
    print("[OK] 문제 1 올바른 괄호")

    # 문제 2
    s20 = Solution20()
    assert s20.isValid("()[]{}") is True
    assert s20.isValid("([{}])") is True
    assert s20.isValid("(]") is False
    assert s20.isValid("([)]") is False
    assert s20.isValid("(") is False
    assert s20.isValid("]") is False
    print("[OK] 문제 2 Valid Parentheses")

    # 문제 3
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.getMin() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.getMin() == -2
    ms.push(-5)
    assert ms.getMin() == -5
    print("[OK] 문제 3 Min Stack")

    # 문제 4
    for fn in (solution_42584_bruteforce, solution_42584_stack):
        assert fn([1, 2, 3, 2, 3]) == [4, 3, 1, 1, 0]
        assert fn([1, 1, 1]) == [2, 1, 0]
        assert fn([5, 4, 3, 2, 1]) == [1, 1, 1, 1, 0]
    print("[OK] 문제 4 주식가격")

    # 문제 5
    s739 = Solution739()
    assert s739.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert s739.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert s739.dailyTemperatures([30, 60, 90]) == [1, 1, 0]
    print("[OK] 문제 5 Daily Temperatures")

    # 문제 6
    board = [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 3],
        [0, 2, 5, 0, 1],
        [4, 2, 4, 4, 2],
        [3, 5, 1, 3, 1],
    ]
    moves = [1, 5, 3, 5, 1, 2, 1, 4]
    assert solution_64061(board, moves) == 4
    assert solution_64061([[1], [1]], [1, 1]) == 2
    print("[OK] 문제 6 크레인 인형뽑기 게임")

    print("=== 모든 테스트 통과 ===")

"""Day 5 해설 — 수학·진법·비트 기초.

각 문제마다 접근 방식을 주석으로 먼저 설명하고,
가능하면 여러 접근(브루트포스 -> 최적화)을 함께 제시한다.
플랫폼 시그니처: LeetCode = class Solution 메서드 / 프로그래머스 = def solution(...).
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""


# ---- 문제 1: Number of 1 Bits (LeetCode #191) ---------------------
# 정수 n의 이진 표현에서 1의 개수(popcount)를 구한다.
class Solution191:
    # 접근 1) 내장 변환 후 '1' 세기  | 시간복잡도: O(비트 수)
    def hammingWeight_builtin(self, n: int) -> int:
        return bin(n).count("1")

    # 접근 2) n & (n-1) 로 최하위 켜진 비트를 하나씩 제거  | O(켜진 비트 수)
    def hammingWeight_kernighan(self, n: int) -> int:
        count = 0
        while n:
            n &= n - 1      # 가장 낮은 1 비트 제거
            count += 1
        return count


# ---- 문제 2: Power of Two (LeetCode #231) -------------------------
# n이 2의 거듭제곱이면 True.
class Solution231:
    # 접근 1) 비트 트릭  | 시간복잡도: O(1)
    def isPowerOfTwo_bit(self, n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0

    # 접근 2) 2로 계속 나누기  | 시간복잡도: O(log n)
    def isPowerOfTwo_loop(self, n: int) -> bool:
        if n <= 0:
            return False
        while n % 2 == 0:
            n //= 2
        return n == 1


# ---- 문제 3: 이진 변환 반복하기 (프로그래머스 #70129) --------------
# "0 제거 -> 남은 길이를 2진수로 변환"을 "1"이 될 때까지 반복.
# 반환: [변환 횟수, 제거된 0의 총개수]
# 시간복잡도: O(len(s) * 변환 횟수). 변환마다 길이가 대략 절반(log)으로 줄어든다.
def solution_70129(s: str):
    convert_count = 0
    zero_removed = 0
    while s != "1":
        zero_removed += s.count("0")
        ones = s.count("1")          # 0을 제거하면 1만 남음
        s = bin(ones)[2:]            # 남은 길이를 2진수 문자열로
        convert_count += 1
    return [convert_count, zero_removed]


# ---- 문제 4: Reverse Integer (LeetCode #7) ------------------------
# 32비트 부호 정수 x의 자릿수를 뒤집는다. 범위를 벗어나면 0.
class Solution7:
    # 접근) 자릿수를 divmod로 떼어 누적  | 시간복잡도: O(자릿수)
    def reverse(self, x: int) -> int:
        INT_MIN, INT_MAX = -(2 ** 31), 2 ** 31 - 1
        sign = -1 if x < 0 else 1
        x = abs(x)
        res = 0
        while x:
            x, digit = divmod(x, 10)
            res = res * 10 + digit
        res *= sign
        return res if INT_MIN <= res <= INT_MAX else 0


# ---- 문제 5: Pow(x, n) (LeetCode #50) -----------------------------
# x ** n 계산 (n은 음수 가능).
class Solution50:
    # 접근 1) 빠른 거듭제곱(반복, 비트 기반)  | 시간복잡도: O(log n)
    def myPow_iter(self, x: float, n: int) -> float:
        if n < 0:
            x = 1 / x
            n = -n
        result = 1.0
        while n:
            if n & 1:           # 현재 비트가 1이면 현재 x를 곱함
                result *= x
            x *= x              # x 를 제곱
            n >>= 1
        return result

    # 접근 2) 빠른 거듭제곱(재귀, 분할정복)  | 시간복잡도: O(log n)
    def myPow_rec(self, x: float, n: int) -> float:
        if n < 0:
            return 1 / self.myPow_rec(x, -n)
        if n == 0:
            return 1.0
        half = self.myPow_rec(x, n // 2)
        return half * half * (x if n & 1 else 1)


# ---- 문제 6: [3차] n진수 게임 (프로그래머스 #17687, 카카오 2018) ----
# 0,1,2,... 를 n진수로 길게 이어 붙인 뒤 p번째부터 m간격으로 t개를 추출.
# 시간복잡도: 필요한 자리 수에 비례 (대략 O(t * m * 자릿수)).
def solution_17687(n: int, t: int, m: int, p: int) -> str:
    digits = "0123456789ABCDEF"

    def to_base(num: int, base: int) -> str:
        if num == 0:
            return "0"
        out = []
        while num > 0:
            num, r = divmod(num, base)
            out.append(digits[r])
        return "".join(reversed(out))

    # 게임판 문자열을 충분히 길게 만든다.
    # 튜브가 t개를 말하려면 board 길이가 (p-1) + m*(t-1) + 1 자 이상이어야 한다.
    need = (p - 1) + m * (t - 1) + 1
    board = []
    num = 0
    while len(board) < need:
        board.extend(to_base(num, n))
        num += 1

    # 튜브는 p번째(1-indexed)부터 m 간격으로 말한다 -> 인덱스 p-1, p-1+m, ...
    answer = []
    idx = p - 1
    for _ in range(t):
        answer.append(board[idx])
        idx += m
    return "".join(answer)


if __name__ == "__main__":
    # 문제 1
    s191 = Solution191()
    for fn in (s191.hammingWeight_builtin, s191.hammingWeight_kernighan):
        assert fn(11) == 3       # 1011
        assert fn(128) == 1      # 10000000
        assert fn(0) == 0
    print("[OK] 문제 1 Number of 1 Bits")

    # 문제 2
    s231 = Solution231()
    for fn in (s231.isPowerOfTwo_bit, s231.isPowerOfTwo_loop):
        assert fn(1) is True     # 2^0
        assert fn(16) is True
        assert fn(0) is False
        assert fn(12) is False
        assert fn(-2) is False
    print("[OK] 문제 2 Power of Two")

    # 문제 3
    assert solution_70129("110010101001") == [3, 8]
    assert solution_70129("01110") == [3, 3]
    assert solution_70129("1111111") == [4, 1]
    print("[OK] 문제 3 이진 변환 반복하기")

    # 문제 4
    s7 = Solution7()
    assert s7.reverse(123) == 321
    assert s7.reverse(-123) == -321
    assert s7.reverse(120) == 21
    assert s7.reverse(1534236469) == 0   # 범위 초과 -> 0
    print("[OK] 문제 4 Reverse Integer")

    # 문제 5
    s50 = Solution50()
    for fn in (s50.myPow_iter, s50.myPow_rec):
        assert abs(fn(2.0, 10) - 1024.0) < 1e-9
        assert abs(fn(2.0, -2) - 0.25) < 1e-9
        assert abs(fn(2.1, 3) - 9.261) < 1e-9
        assert abs(fn(5.0, 0) - 1.0) < 1e-9
    print("[OK] 문제 5 Pow(x, n)")

    # 문제 6 (직접 손으로 검산한 케이스)
    assert solution_17687(2, 4, 2, 1) == "0111"
    assert solution_17687(10, 2, 1, 1) == "01"
    assert solution_17687(16, 3, 2, 2) == "135"
    print("[OK] 문제 6 n진수 게임")

    print("=== 모든 테스트 통과 ===")

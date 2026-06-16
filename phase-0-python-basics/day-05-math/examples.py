"""Day 5 — 수학·진법·비트 기초 예제 코드.

각 예제는 단독 실행 가능하며, 개념을 단계별 주석으로 설명한다.
실행: python examples.py
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""

import math


def example_1_floor_div_mod() -> None:
    """정수 나눗셈(//), 나머지(%), divmod 와 음수 함정."""
    print("=== 예제 1) //, %, divmod 와 음수 ===")
    print("7 // 2   =", 7 // 2)      # 3
    print("-7 // 2  =", -7 // 2)     # -4 (음의 무한대로 내림)
    print("7 % 3    =", 7 % 3)       # 1
    print("-7 % 3   =", -7 % 3)      # 2 (나머지는 제수 부호를 따름)
    print("divmod(17, 5) =", divmod(17, 5))  # (3, 2)
    # 항등식: a == (a // b) * b + (a % b)
    a, b = -7, 3
    print("항등식 검증:", (a // b) * b + (a % b) == a)  # True


def example_2_pow_modular() -> None:
    """거듭제곱과 모듈러 거듭제곱."""
    print("=== 예제 2) pow 와 모듈러 거듭제곱 ===")
    print("2 ** 10        =", 2 ** 10)          # 1024
    print("pow(2, 10)     =", pow(2, 10))       # 1024
    print("pow(2, 10, 1000) =", pow(2, 10, 1000))  # 24
    # 큰 지수도 O(log b)로 즉시 계산
    print("pow(7, 100, 10**9+7) =", pow(7, 100, 10 ** 9 + 7))


def example_3_gcd_lcm() -> None:
    """최대공약수/최소공배수 (유클리드 호제법)."""
    print("=== 예제 3) GCD / LCM ===")
    print("math.gcd(12, 18) =", math.gcd(12, 18))  # 6

    def my_gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    print("my_gcd(48, 36)   =", my_gcd(48, 36))    # 12
    a, b = 4, 6
    print("lcm(4, 6)        =", a * b // math.gcd(a, b))  # 12


def example_4_prime_sieve() -> None:
    """소수 판별과 에라토스테네스의 체."""
    print("=== 예제 4) 소수 판별 / 에라토스테네스의 체 ===")

    def is_prime(n):
        if n < 2:
            return False
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i += 1
        return True

    print("is_prime(97) =", is_prime(97))   # True
    print("is_prime(91) =", is_prime(91))   # False (7 * 13)

    def sieve(n):
        is_p = [True] * (n + 1)
        is_p[0] = is_p[1] = False
        i = 2
        while i * i <= n:
            if is_p[i]:
                for j in range(i * i, n + 1, i):
                    is_p[j] = False
            i += 1
        return [x for x in range(n + 1) if is_p[x]]

    print("30 이하 소수:", sieve(30))


def example_5_base_conversion() -> None:
    """진법 변환 (내장 함수 + 직접 구현)."""
    print("=== 예제 5) 진법 변환 ===")
    print("bin(10) =", bin(10))             # 0b1010
    print("hex(255) =", hex(255))           # 0xff
    print("format(255, 'b') =", format(255, "b"))  # 11111111
    print("int('1010', 2) =", int("1010", 2))      # 10
    print("int('ff', 16)  =", int("ff", 16))       # 255

    def to_base(num, base):
        if num == 0:
            return "0"
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        out = []
        while num > 0:
            num, r = divmod(num, base)
            out.append(digits[r])
        return "".join(reversed(out))

    print("to_base(255, 16) =", to_base(255, 16))  # ff
    print("to_base(13, 2)   =", to_base(13, 2))    # 1101
    print("to_base(100, 5)  =", to_base(100, 5))   # 400


def example_6_bits() -> None:
    """비트 연산과 단골 트릭."""
    print("=== 예제 6) 비트 연산 ===")
    print("12 & 10 =", 12 & 10)   # 8
    print("12 | 10 =", 12 | 10)   # 14
    print("12 ^ 10 =", 12 ^ 10)   # 6
    print("~5      =", ~5)        # -6
    print("1 << 3  =", 1 << 3)    # 8
    print("8 >> 2  =", 8 >> 2)    # 2

    n = 16
    print("16은 2의 거듭제곱?", n > 0 and (n & (n - 1)) == 0)  # True
    print("12는 2의 거듭제곱?", 12 > 0 and (12 & 11) == 0)      # False
    print("popcount(13) =", bin(13).count("1"))  # 3 (1101)
    print("13 & -13 (최하위 비트) =", 13 & -13)   # 1

    # XOR 상쇄: 한 번만 등장하는 원소 찾기
    arr = [4, 1, 2, 1, 2]
    single = 0
    for x in arr:
        single ^= x
    print("한 번만 등장하는 원소:", single)  # 4


if __name__ == "__main__":
    example_1_floor_div_mod()
    print()
    example_2_pow_modular()
    print()
    example_3_gcd_lcm()
    print()
    example_4_prime_sieve()
    print()
    example_5_base_conversion()
    print()
    example_6_bits()

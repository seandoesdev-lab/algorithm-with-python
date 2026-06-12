"""Day 01 - 빠른 입출력(Fast I/O) 풀이 모음.

플랫폼: 프로그래머스(Programmers), LeetCode
I/O 방식: 함수 기반(function-based) - stdin 직접 읽기 없음.

문제 목록:
  - p_120906  : 자릿수 더하기  (https://school.programmers.co.kr/learn/courses/30/lessons/120906)
  - p_12912   : 두 정수 사이의 합  (https://school.programmers.co.kr/learn/courses/30/lessons/12912)
  - lc_258    : Add Digits  (https://leetcode.com/problems/add-digits/)
  - p_81301   : 숫자 문자열과 영단어  (https://school.programmers.co.kr/learn/courses/30/lessons/81301)
"""

import sys
import io


# ============================================================
# 프로그래머스 120906 - 자릿수 더하기
# https://school.programmers.co.kr/learn/courses/30/lessons/120906
#
# 제한: 0 <= n <= 1,000,000
# 시간복잡도(Time Complexity): O(d)  - d = 자릿수 개수 (최대 7)
# ============================================================

def p_120906_approach1(n: int) -> int:
    """접근법 1: str 변환 후 제너레이터 표현식.

    str(n)으로 각 문자를 순회하면서 int 변환 후 합산한다.
    가독성이 높고 파이썬다운(Pythonic) 방식이다.
    """
    return sum(int(c) for c in str(n))


def p_120906_approach2(n: int) -> int:
    """접근법 2: map(int, str(n)) + sum.

    제너레이터 표현식 대신 map()을 사용한다.
    map()은 C 레벨에서 동작하므로 이론적으로 더 빠르다.
    """
    return sum(map(int, str(n)))


def p_120906_approach3(n: int) -> int:
    """접근법 3: divmod 반복 (문자열 변환 없음).

    n을 10으로 거듭 나눠 각 자릿수를 추출한다.
    문자열 메모리 할당 없이 순수 정수 연산만 사용한다.
    n == 0 엣지케이스를 명시적으로 처리한다.
    """
    if n == 0:
        return 0
    total = 0
    while n > 0:
        n, r = divmod(n, 10)
        total += r
    return total


# 프로그래머스 함수 시그니처 (정답 제출용)
def solution_120906(n: int) -> int:
    return sum(map(int, str(n)))


# ============================================================
# 프로그래머스 12912 - 두 정수 사이의 합
# https://school.programmers.co.kr/learn/courses/30/lessons/12912
#
# 제한: -10,000,000 <= a, b <= 10,000,000
# 시간복잡도(Time Complexity): O(1) (수학 공식) / O(n) (range+sum)
# ============================================================

def p_12912_approach1(a: int, b: int) -> int:
    """접근법 1: range + sum.

    min/max로 범위를 정규화한 뒤 range 합산.
    직관적이고 음수 범위도 올바르게 처리한다.
    """
    lo, hi = min(a, b), max(a, b)
    return sum(range(lo, hi + 1))


def p_12912_approach2(a: int, b: int) -> int:
    """접근법 2: 등차수열 합 공식 O(1).

    (lo + hi) * (원소 개수) // 2
    범위가 매우 클 때 O(1)로 처리된다.
    """
    lo, hi = min(a, b), max(a, b)
    return (lo + hi) * (hi - lo + 1) // 2


# 프로그래머스 함수 시그니처 (정답 제출용)
def solution_12912(a: int, b: int) -> int:
    lo, hi = min(a, b), max(a, b)
    return (lo + hi) * (hi - lo + 1) // 2


# ============================================================
# LeetCode 258 - Add Digits
# https://leetcode.com/problems/add-digits/
#
# 제한: 0 <= num <= 2^31 - 1
# 시간복잡도(Time Complexity): O(log n) [반복] / O(1) [digital root]
# ============================================================

class Solution_258:
    def addDigits_approach1(self, num: int) -> int:
        """접근법 1: 반복 자릿수 합산 O(log n).

        결과가 한 자릿수(< 10)가 될 때까지 자릿수 합을 반복 계산한다.
        num == 0은 루프 조건에서 자동으로 처리된다.
        """
        while num >= 10:
            num = sum(int(c) for c in str(num))
        return num

    def addDigits_approach2(self, num: int) -> int:
        """접근법 2: Digital Root 수학 공식 O(1).

        수론(number theory) 성질:
          - 자릿수를 거듭 더한 결과는 num % 9 와 같다.
          - 단, num == 0이면 0, num이 9의 배수이면 9.
        공식: 0 if num == 0 else 1 + (num - 1) % 9
        """
        if num == 0:
            return 0
        return 1 + (num - 1) % 9

    # LeetCode 제출용 메서드 (기본 이름)
    def addDigits(self, num: int) -> int:
        return self.addDigits_approach2(num)


# ============================================================
# 프로그래머스 81301 - 숫자 문자열과 영단어 (2021 카카오 인턴십)
# https://school.programmers.co.kr/learn/courses/30/lessons/81301
#
# 제한: 1 <= s.length <= 50
# 시간복잡도(Time Complexity): O(len(s) * 9)  - 9개 단어 replace
# ============================================================

WORD_MAP = [
    ("zero", "0"), ("one", "1"), ("two", "2"), ("three", "3"),
    ("four", "4"), ("five", "5"), ("six", "6"),
    ("seven", "7"), ("eight", "8"), ("nine", "9"),
]


def p_81301_approach1(s: str) -> int:
    """접근법 1: str.replace 반복 적용.

    WORD_MAP의 각 (영단어, 숫자) 쌍에 대해 s.replace(word, digit)를 순서대로 적용한다.
    구현이 단순하고 가독성이 높다.
    """
    for word, digit in WORD_MAP:
        s = s.replace(word, digit)
    return int(s)


def p_81301_approach2(s: str) -> int:
    """접근법 2: split + join 방식.

    s.split(word)로 단어를 기준으로 나눈 뒤 digit으로 join한다.
    replace와 결과는 동일하지만, split/join 메커니즘을 이해하기 좋다.
    """
    for word, digit in WORD_MAP:
        s = digit.join(s.split(word))
    return int(s)


# 프로그래머스 함수 시그니처 (정답 제출용)
def solution_81301(s: str) -> int:
    for word, digit in WORD_MAP:
        s = s.replace(word, digit)
    return int(s)


# ============================================================
# 실행 데모 - 각 풀이를 assert로 검증한다
# ============================================================

def _run_tests() -> None:
    print("=" * 50)
    print("Day 01 - Fast I/O Solutions Test")
    print("=" * 50)

    # --- 120906: 자릿수 더하기 ---
    print("\n[120906] 자릿수 더하기")
    cases_120906 = [(1234, 10), (930211, 16), (0, 0), (9, 9)]
    for n, expected in cases_120906:
        r1 = p_120906_approach1(n)
        r2 = p_120906_approach2(n)
        r3 = p_120906_approach3(n)
        assert r1 == expected, f"approach1({n}): {r1} != {expected}"
        assert r2 == expected, f"approach2({n}): {r2} != {expected}"
        assert r3 == expected, f"approach3({n}): {r3} != {expected}"
        print(f"  n={n}  =>  {r1}  [OK]")

    # --- 12912: 두 정수 사이의 합 ---
    print("\n[12912] 두 정수 사이의 합")
    cases_12912 = [(3, 5, 12), (3, 3, 3), (5, 3, 12), (-2, 2, 0)]
    for a, b, expected in cases_12912:
        r1 = p_12912_approach1(a, b)
        r2 = p_12912_approach2(a, b)
        assert r1 == expected, f"approach1({a},{b}): {r1} != {expected}"
        assert r2 == expected, f"approach2({a},{b}): {r2} != {expected}"
        print(f"  a={a}, b={b}  =>  {r1}  [OK]")

    # --- LeetCode 258: Add Digits ---
    print("\n[LeetCode 258] Add Digits")
    sol = Solution_258()
    cases_258 = [(38, 2), (0, 0), (9, 9), (18, 9), (100, 1)]
    for num, expected in cases_258:
        r1 = sol.addDigits_approach1(num)
        r2 = sol.addDigits_approach2(num)
        assert r1 == expected, f"approach1({num}): {r1} != {expected}"
        assert r2 == expected, f"approach2({num}): {r2} != {expected}"
        print(f"  num={num}  =>  {r1}  [OK]")

    # --- 81301: 숫자 문자열과 영단어 ---
    print("\n[81301] 숫자 문자열과 영단어")
    cases_81301 = [
        ("one4seveneight", 1478),
        ("23four5six7", 234567),
        ("2three45sixseven", 234567),
        ("123", 123),
        ("zeroonetwothreefourfivesixseveneightnine", 123456789),
    ]
    for s, expected in cases_81301:
        r1 = p_81301_approach1(s)
        r2 = p_81301_approach2(s)
        assert r1 == expected, f"approach1({s!r}): {r1} != {expected}"
        assert r2 == expected, f"approach2({s!r}): {r2} != {expected}"
        print(f"  s={s!r}  =>  {r1}  [OK]")

    print("\n" + "=" * 50)
    print("모든 테스트 통과.")
    print("=" * 50)


if __name__ == "__main__":
    _run_tests()

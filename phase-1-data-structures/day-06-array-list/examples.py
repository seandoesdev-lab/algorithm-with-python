"""Day 6 — 배열과 동적 리스트 (Array & List) 예제 코드.

각 예제는 단독 실행 가능하며, 개념을 단계별 주석으로 설명한다.
실행: python examples.py
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""

import copy
import sys
from itertools import accumulate


def example_1_basic_ops() -> None:
    """리스트 기본 연산: 접근, append, pop, insert."""
    print("=== 예제 1) 기본 연산 ===")
    a = [10, 20, 30]
    print("a[0]    =", a[0])        # 10  (O(1) 접근)
    print("a[-1]   =", a[-1])       # 30  (마지막)
    a.append(40)                    # 맨 뒤 추가 (분할상환 O(1))
    print("append  =", a)           # [10, 20, 30, 40]
    last = a.pop()                  # 맨 뒤 제거 (O(1))
    print("pop()   =", last, a)     # 40 [10, 20, 30]
    a.insert(0, 5)                  # 맨 앞 삽입 (O(n) - 뒤 전부 밀기)
    print("insert  =", a)           # [5, 10, 20, 30]


def example_2_slicing() -> None:
    """슬라이싱과 음수 인덱스. 슬라이싱은 항상 복사본을 만든다."""
    print("=== 예제 2) 슬라이싱 ===")
    a = [0, 1, 2, 3, 4, 5]
    print("a[1:4]  =", a[1:4])      # [1, 2, 3]
    print("a[:3]   =", a[:3])       # [0, 1, 2]
    print("a[3:]   =", a[3:])       # [3, 4, 5]
    print("a[::2]  =", a[::2])      # [0, 2, 4]
    print("a[::-1] =", a[::-1])     # [5, 4, 3, 2, 1, 0]  역순 복사
    b = a[:]                        # 얕은 복사본
    b[0] = 99
    print("원본 a  =", a)            # a 는 영향 없음 (1차원이라 안전)


def example_3_amortized_append() -> None:
    """append 가 분할상환 O(1) 인 이유: 초과 할당으로 빈칸을 미리 잡는다."""
    print("=== 예제 3) 초과 할당 (over-allocation) ===")
    a = []
    prev = -1
    for i in range(9):
        a.append(i)
        size = sys.getsizeof(a)     # 바이트 크기 (용량이 계단식으로 증가)
        grew = "재할당" if size != prev else "그대로"
        print("len=", len(a), " bytes=", size, " ", grew)
        prev = size
    # 용량이 1,2,3,... 가 아니라 계단식으로 커지는 것을 확인할 수 있다.


def example_4_2d_pitfall() -> None:
    """2차원 리스트 생성: 컴프리헨션 O, [[..]]*n 은 X (앨리어싱)."""
    print("=== 예제 4) 2차원 리스트 함정 ===")
    rows, cols = 3, 3

    good = [[0] * cols for _ in range(rows)]   # 올바른 생성
    good[0][0] = 1
    print("good (컴프리헨션):", good)            # 한 행만 바뀜

    bad = [[0] * cols] * rows                  # 위험: 같은 리스트 참조
    bad[0][0] = 1
    print("bad  ([[..]]*n)  :", bad)           # 모든 행이 같이 바뀜!


def example_5_shallow_deep_copy() -> None:
    """얕은 복사 vs 깊은 복사 (중첩 리스트)."""
    print("=== 예제 5) 얕은 복사 vs 깊은 복사 ===")
    a = [[1, 2], [3, 4]]

    shallow = a[:]                  # 또는 a.copy(), list(a)
    shallow[0][0] = 99
    print("얕은 복사 후 원본:", a)     # [[99, 2], [3, 4]]  안쪽 공유됨!

    a = [[1, 2], [3, 4]]
    deep = copy.deepcopy(a)
    deep[0][0] = 99
    print("깊은 복사 후 원본:", a)     # [[1, 2], [3, 4]]  영향 없음


def example_6_comprehension_patterns() -> None:
    """컴프리헨션·누적합·전치·평탄화 관용구."""
    print("=== 예제 6) 관용구 ===")
    squares = [i * i for i in range(6)]
    print("제곱      :", squares)            # [0, 1, 4, 9, 16, 25]
    evens = [x for x in range(10) if x % 2 == 0]
    print("짝수 필터 :", evens)              # [0, 2, 4, 6, 8]

    ps = list(accumulate([1, 2, 3, 4]))
    print("누적 합   :", ps)                 # [1, 3, 6, 10]

    grid = [[1, 2, 3], [4, 5, 6]]
    flat = [x for row in grid for x in row]
    print("평탄화    :", flat)               # [1, 2, 3, 4, 5, 6]
    trans = [list(r) for r in zip(*grid)]
    print("전치      :", trans)              # [[1, 4], [2, 5], [3, 6]]


def example_7_common_bug() -> None:
    """순회 중 수정 버그와 올바른 대안."""
    print("=== 예제 7) 순회 중 수정 함정 ===")
    # 잘못된 방식 (원소를 건너뛴다)
    wrong = [1, 2, 2, 3, 2]
    for x in wrong:
        if x == 2:
            wrong.remove(x)         # 순회 중 크기 변경 -> 일부 2가 남음
    print("순회중 remove (버그):", wrong)

    # 올바른 방식: 새 리스트 컴프리헨션
    a = [1, 2, 2, 3, 2]
    right = [x for x in a if x != 2]
    print("컴프리헨션 (정답)   :", right)     # [1, 3]


if __name__ == "__main__":
    example_1_basic_ops()
    print()
    example_2_slicing()
    print()
    example_3_amortized_append()
    print()
    example_4_2d_pitfall()
    print()
    example_5_shallow_deep_copy()
    print()
    example_6_comprehension_patterns()
    print()
    example_7_common_bug()
    print()
    print("=== 모든 예제 실행 완료 ===")

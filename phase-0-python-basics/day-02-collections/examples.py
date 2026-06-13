# -*- coding: utf-8 -*-
"""Day 02 -- 자료형과 컬렉션 (Types & Collections) 예제 코드.

각 예제는 단독 실행 가능하며, 개념을 단계별 주석으로 설명한다.
실행: python examples.py
"""

import copy
import sys

# Windows 콘솔에서 한글 출력을 위해 UTF-8로 강제 설정
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


# ── 예제 1: list 기본 동작 ──────────────────────────────────────────────────
def example_list_basics() -> None:
    """list 생성, 인덱싱, 추가, 삭제."""
    print("=== [1] list 기본 동작 ===")

    # 리스트 생성
    fruits = ["apple", "banana", "cherry"]
    print("원본:", fruits)

    # 인덱싱(indexing) - O(1)
    print("첫 번째:", fruits[0])        # 양수 인덱스
    print("마지막:", fruits[-1])        # 음수 인덱스 (뒤에서부터)

    # 슬라이싱(slicing) - O(k)
    print("슬라이스 [0:2]:", fruits[0:2])  # ['apple', 'banana']
    print("역순 [::-1]:", fruits[::-1])    # 역순 복사

    # 원소 추가
    fruits.append("date")           # 맨 뒤 추가 - amortized O(1)
    fruits.insert(1, "avocado")     # 인덱스 1에 삽입 - O(n) (시프트 발생)
    print("추가 후:", fruits)

    # 원소 제거
    fruits.pop()                    # 맨 뒤 제거 - O(1)
    fruits.remove("avocado")        # 값으로 제거 - O(n) (검색 후 시프트)
    print("제거 후:", fruits)

    # in 검색 - O(n) (순서대로 비교)
    print("'banana' in fruits:", "banana" in fruits)
    print()


# ── 예제 2: 슬라이싱이 복사임을 증명 ─────────────────────────────────────────
def example_slice_is_copy() -> None:
    """슬라이싱은 항상 새 리스트(얕은 복사, shallow copy)를 반환한다."""
    print("=== [2] 슬라이싱은 새 리스트 복사 ===")

    a = [1, 2, 3, 4, 5]
    b = a[:]            # 전체 슬라이스 = 얕은 복사

    # is: 동일 객체 여부 확인
    print("b = a[:]  →  b is a:", b is a)   # False - 다른 객체!

    # b를 수정해도 a는 유지됨
    b[0] = 99
    print("b[0] = 99 수정 후")
    print("  a:", a)    # [1, 2, 3, 4, 5] - 원본 유지
    print("  b:", b)    # [99, 2, 3, 4, 5]

    # ── 함정: 중첩 리스트의 얕은 복사 ──
    print("\n--- 중첩 리스트(2D) 얕은 복사 함정 ---")
    matrix = [[1, 2], [3, 4]]
    shallow = matrix[:]             # 내부 리스트는 공유됨!
    deep = copy.deepcopy(matrix)    # 완전 독립 복사

    shallow[0][0] = 999             # 내부 리스트 수정
    deep[1][1] = 888

    print("matrix after shallow[0][0]=999:", matrix)   # [[999,2],[3,4]] 공유!
    print("matrix after deep[1][1]=888  :", matrix)    # 영향 없음
    print()


# ── 예제 3: 가변 기본 인자(mutable default argument) 함정 ────────────────────
def example_mutable_default_arg() -> None:
    """같은 기본값 리스트가 호출마다 누적되는 함정을 직접 확인한다."""
    print("=== [3] 가변 기본 인자 함정 ===")

    # 위험한 패턴 - 기본값 [] 는 함수 정의 시 딱 한 번 생성됨
    def dangerous_append(element, to=[]):
        to.append(element)
        return to

    print("dangerous_append(1):", dangerous_append(1))  # [1]
    print("dangerous_append(2):", dangerous_append(2))  # [1, 2] ← 누적!
    print("dangerous_append(3):", dangerous_append(3))  # [1, 2, 3] ← 더 누적!

    # 기본값 리스트 객체 id 확인
    print("기본값 리스트 id:", id(dangerous_append.__defaults__[0]))

    print()

    # 올바른 패턴 - None 사용
    def safe_append(element, to=None):
        if to is None:
            to = []        # 매 호출마다 새 리스트 생성
        to.append(element)
        return to

    print("safe_append(1):", safe_append(1))  # [1]
    print("safe_append(2):", safe_append(2))  # [2] ← 누적 없음!
    print()


# ── 예제 4: dict 기본 동작 + get / setdefault ─────────────────────────────────
def example_dict_basics() -> None:
    """dict 생성, 조회, get, setdefault, 삭제, 순회."""
    print("=== [4] dict 기본 동작 ===")

    # dict 생성 (Python 3.7+ 삽입 순서 보존)
    score = {"Alice": 95, "Bob": 82, "Charlie": 78}
    print("dict:", score)
    print("삽입 순서 유지 keys:", list(score.keys()))

    # 키 조회 - O(1)
    print("Alice 점수:", score["Alice"])

    # get - KeyError 없이 기본값 반환
    print("Dave 점수 (없음, get):", score.get("Dave", 0))

    # setdefault - 없을 때만 초기값 설정
    score.setdefault("Dave", 0)    # Dave 없으므로 0으로 설정
    score.setdefault("Alice", 0)   # Alice 이미 있으므로 무시
    print("setdefault 후:", score)

    # 삭제
    del score["Dave"]

    # 빈도 카운팅 관용구
    text = "mississippi"
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    print(f"'{text}' 빈도:", freq)

    # items() 순회
    print("키-값 순회:")
    for k, v in score.items():
        print(f"  {k}: {v}")
    print()


# ── 예제 5: set 교집합·합집합·차집합 ──────────────────────────────────────────
def example_set_operations() -> None:
    """set 생성과 집합 연산."""
    print("=== [5] set 집합 연산 ===")

    s1 = {1, 2, 3, 4, 5}
    s2 = {3, 4, 5, 6, 7}
    print("s1:", s1)
    print("s2:", s2)

    # 교집합(intersection) - 둘 다 있는 원소
    print("교집합 s1 & s2:", s1 & s2)          # {3, 4, 5}
    print("교집합 s1.intersection(s2):", s1.intersection(s2))

    # 합집합(union) - 둘 중 하나라도 있는 원소
    print("합집합 s1 | s2:", s1 | s2)           # {1,2,3,4,5,6,7}

    # 차집합(difference) - s1에만 있는 원소
    print("차집합 s1 - s2:", s1 - s2)           # {1, 2}

    # 대칭차집합(symmetric difference) - 한쪽에만 있는 원소
    print("대칭차집합 s1 ^ s2:", s1 ^ s2)       # {1, 2, 6, 7}

    # 중복 제거 - list → set → list
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    unique = list(set(nums))
    print("중복 제거:", sorted(unique))   # 순서 보장 위해 sort

    # in 연산 O(1) 확인
    big_set = set(range(1_000_000))
    print("999_999 in big_set (O(1)):", 999_999 in big_set)
    print()


# ── 예제 6: tuple 언패킹(unpacking) ───────────────────────────────────────────
def example_tuple_unpacking() -> None:
    """tuple 생성, hashable 특성, 언패킹 패턴."""
    print("=== [6] tuple 언패킹 ===")

    # 기본 언패킹
    point = (3, 7)
    x, y = point
    print(f"point={point}  →  x={x}, y={y}")

    # 변수 교환 - temp 없이
    a, b = 10, 20
    a, b = b, a
    print(f"교환 후: a={a}, b={b}")

    # 확장 언패킹 (Python 3+)
    first, *middle, last = (1, 2, 3, 4, 5)
    print(f"first={first}, middle={middle}, last={last}")

    # 함수 다중 반환값
    def min_max(lst):
        return min(lst), max(lst)   # 튜플 반환

    lo, hi = min_max([5, 3, 8, 1, 9, 2])
    print(f"min={lo}, max={hi}")

    # tuple은 hashable → dict 키, set 원소로 사용 가능
    visited = set()
    visited.add((0, 0))    # (행, 열) 좌표를 set에 저장
    visited.add((1, 2))
    print("visited set:", visited)

    graph = {}
    graph[(0, 0)] = "start"   # tuple을 dict 키로 사용
    print("graph dict:", graph)

    # list는 unhashable → 오류 발생 예시
    try:
        bad_set = {[1, 2]}   # TypeError: unhashable type: 'list'
    except TypeError as e:
        print(f"list를 set에 넣으면: TypeError - {e}")
    print()


# ── 예제 7: == vs is ─────────────────────────────────────────────────────────
def example_eq_vs_is() -> None:
    """값 동등(==)과 객체 동일성(is) 구분."""
    print("=== [7] == vs is ===")

    a = [1, 2, 3]
    b = [1, 2, 3]   # 값은 같지만 다른 객체
    c = a            # 같은 객체 참조

    print("a == b (값 비교):", a == b)    # True
    print("a is b (동일 객체):", a is b)  # False - 다른 객체
    print("a is c (동일 객체):", a is c)  # True - 같은 참조

    # None 비교는 반드시 is
    x = None
    print("x is None:", x is None)       # True (권장)
    print("x == None:", x == None)       # True (작동하지만 비권장)

    # 작은 정수 캐싱 - CPython 구현 세부사항
    p = 256
    q = 256
    print(f"256 is 256: {p is q}")    # True - CPython이 -5~256 캐싱
    r = 257
    s = 257
    print(f"257 is 257: {r is s}")    # CPython 구현에 따라 다를 수 있음
    print()


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    example_list_basics()
    example_slice_is_copy()
    example_mutable_default_arg()
    example_dict_basics()
    example_set_operations()
    example_tuple_unpacking()
    example_eq_vs_is()
    print("모든 예제 완료!")

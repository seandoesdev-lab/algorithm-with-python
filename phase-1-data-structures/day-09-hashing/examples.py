"""Day 9 - 해시: dict / set (Hashing) 예제 코드.

각 예제는 단독 실행 가능하며, 개념을 단계별 주석으로 설명한다.
실행: python examples.py
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""

from collections import Counter, defaultdict


def example_1_dict_set_basic() -> None:
    """dict는 키->값, set은 멤버십/중복 제거. 둘 다 평균 O(1)."""
    print("=== 예제 1) dict와 set 기본 ===")
    ages = {"Tom": 20, "Amy": 22}
    print("Tom 나이      :", ages["Tom"])      # 20
    ages["Bob"] = 19                            # 삽입 O(1)
    print("Amy in ages   :", "Amy" in ages)    # True (키 멤버십)
    seen = {1, 2, 3}
    seen.add(4)
    print("3 in seen     :", 3 in seen)        # True
    print("중복 제거      :", sorted(set([1, 1, 2, 3, 3])))  # [1, 2, 3]


def example_2_in_speed() -> None:
    """list의 in은 O(n), set의 in은 평균 O(1). 결과는 같지만 속도가 다르다."""
    print("=== 예제 2) list in vs set in ===")
    data_list = list(range(1000))
    data_set = set(data_list)
    target = 999
    print("list 멤버십 결과:", target in data_list, "(내부적으로 O(n) 순차 탐색)")
    print("set  멤버십 결과:", target in data_set, "(평균 O(1) 인덱스 계산)")
    print("반복 검사가 많으면 list를 set으로 바꿔두면 빠르다")


def example_3_counter() -> None:
    """Counter: 개수 세기 전용. most_common, 없는 키 0 반환."""
    print("=== 예제 3) Counter 개수 세기 ===")
    c = Counter("banana")
    print("Counter        :", dict(c))         # {'b':1,'a':3,'n':2}
    print("a 개수         :", c["a"])           # 3
    print("없는 키 z      :", c["z"])           # 0 (KeyError 아님)
    print("상위 1개       :", c.most_common(1)) # [('a', 3)]
    print("Counter 덧셈   :", dict(Counter([1, 1, 2]) + Counter([1, 3])))


def example_4_defaultdict_group() -> None:
    """defaultdict(list): 키별로 모으기. 없는 키도 바로 append."""
    print("=== 예제 4) defaultdict 그룹화 ===")
    words = ["apple", "avocado", "banana", "cherry", "blueberry"]
    groups = defaultdict(list)
    for w in words:
        groups[w[0]].append(w)                 # 첫 글자로 그룹
    for first, items in groups.items():
        print("  ", first, "->", items)


def example_5_two_sum() -> None:
    """보수 찾기: target - x 가 이미 있나? 한 번 순회로 O(n)."""
    print("=== 예제 5) Two Sum (보수 찾기) ===")
    nums = [2, 7, 11, 15]
    target = 9
    seen = {}                                  # 값 -> 인덱스
    answer = []
    for i, x in enumerate(nums):
        if target - x in seen:
            answer = [seen[target - x], i]
            break
        seen[x] = i
    print("nums   :", nums, "target :", target)
    print("정답 인덱스:", answer)               # [0, 1]


def example_6_group_anagrams() -> None:
    """정렬한 글자 tuple을 키로 애너그램 묶기."""
    print("=== 예제 6) Group Anagrams ===")
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    groups = defaultdict(list)
    for w in strs:
        key = tuple(sorted(w))                 # list는 키 불가 -> tuple
        groups[key].append(w)
    for g in groups.values():
        print("  ", g)


def example_7_safe_access() -> None:
    """없는 키: d[k]는 KeyError, get은 안전."""
    print("=== 예제 7) 없는 키 안전 접근 ===")
    d = {"a": 1}
    print("get('b')       :", d.get("b"))       # None
    print("get('b', 0)    :", d.get("b", 0))    # 0
    try:
        _ = d["b"]
    except KeyError as e:
        print("d['b'] 예외    :", "KeyError", e) # KeyError 'b'


def example_8_hashable() -> None:
    """tuple은 키 가능, list는 unhashable."""
    print("=== 예제 8) hashable (키로 쓸 수 있는 것) ===")
    d = {}
    d[(1, 2)] = "tuple ok"                      # tuple 키 가능
    print("tuple 키       :", d[(1, 2)])
    try:
        d[[1, 2]] = "list?"
    except TypeError as e:
        print("list 키 예외   :", "TypeError", e) # unhashable type: 'list'


def example_9_set_ops() -> None:
    """집합 연산: 교집합/합집합/차집합/대칭차."""
    print("=== 예제 9) 집합 연산 ===")
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    print("교집합 a & b   :", sorted(a & b))    # [3, 4]
    print("합집합 a | b   :", sorted(a | b))    # [1..6]
    print("차집합 a - b   :", sorted(a - b))    # [1, 2]
    print("대칭차 a ^ b   :", sorted(a ^ b))    # [1, 2, 5, 6]


if __name__ == "__main__":
    example_1_dict_set_basic()
    print()
    example_2_in_speed()
    print()
    example_3_counter()
    print()
    example_4_defaultdict_group()
    print()
    example_5_two_sum()
    print()
    example_6_group_anagrams()
    print()
    example_7_safe_access()
    print()
    example_8_hashable()
    print()
    example_9_set_ops()
    print()
    print("=== 모든 예제 실행 완료 ===")

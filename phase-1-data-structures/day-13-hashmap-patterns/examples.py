# -*- coding: utf-8 -*-
"""
Day 13 - 해시맵 응용 (Hashmap Patterns) 예제 모음

Day 09에서 배운 dict / set / Counter / defaultdict 를 "패턴"으로 끌어올린다.
표준 라이브러리만 사용한다. cp949 콘솔에서도 안전하도록 print 출력에는
ASCII 기호(=, -, O, X)만 쓴다(한글은 OK).

다루는 7가지 핵심 패턴
  1) 보수 찾기 (complement)          - 합/차의 짝을 dict로 한 번에 찾기
  2) 누적합 + 해시맵 (prefix sum)     - 연속 구간 합 문제를 O(n)으로
  3) 빈도수 비교 (frequency)          - Counter 로 다중 집합 비교
  4) 그룹으로 묶기 (grouping)         - defaultdict 로 키별 수집
  5) 양방향 매핑 (bijection)          - 두 dict 로 1:1 대응 검증
  6) 마지막 등장 위치 (last-seen)     - 값 -> 인덱스 dict
  7) 설계형 (dict + 다른 자료구조)    - O(1) 삽입/삭제/조회 설계

실행:  PYTHONIOENCODING=cp949 python examples.py
"""

from collections import Counter, defaultdict


# ---------------------------------------------------------------------------
# 1) 보수 찾기(complement): "두 값의 합이 target" 을 한 번 순회로
#    값 -> 인덱스 dict 를 만들며, 매 원소에서 target - x 가 이미 있는지 확인.
#    이중 루프 O(n^2) -> O(n).
# ---------------------------------------------------------------------------
def two_sum(nums, target):
    seen = {}                       # 값 -> 인덱스
    for i, x in enumerate(nums):
        if target - x in seen:      # 보수가 이미 있으면 정답
            return [seen[target - x], i]
        seen[x] = i
    return []


# ---------------------------------------------------------------------------
# 2) 누적합 + 해시맵(prefix sum + hashmap): 합이 K 인 "연속 구간" 개수
#    prefix[j] - prefix[i] == K  <=>  prefix[i] == prefix[j] - K
#    지금까지 본 누적합의 "등장 횟수"를 dict 에 쌓으며 즉시 카운트. O(n).
#    핵심 초기값: 누적합 0 을 1번 본 것으로 시작(앞부분 전체가 K 인 경우 포함).
# ---------------------------------------------------------------------------
def subarray_sum_count(nums, K):
    count = 0
    prefix = 0
    seen = defaultdict(int)
    seen[0] = 1                     # 빈 접두부 = 합 0 이 1번
    for x in nums:
        prefix += x
        count += seen[prefix - K]   # prefix-K 를 만든 시작점 개수만큼 구간 추가
        seen[prefix] += 1
    return count


# ---------------------------------------------------------------------------
# 3) 빈도수 비교(frequency): 두 다중집합이 같은가 (애너그램 판별)
#    Counter 끼리 == 비교는 "각 원소 개수가 모두 같은가"를 본다.
# ---------------------------------------------------------------------------
def is_anagram(a, b):
    return Counter(a) == Counter(b)


# ---------------------------------------------------------------------------
# 4) 그룹으로 묶기(grouping): 같은 키를 가진 것끼리 모으기
#    여기서는 단어들을 첫 글자로 그룹화.
# ---------------------------------------------------------------------------
def group_by_first_letter(words):
    groups = defaultdict(list)      # 없는 키는 자동으로 빈 리스트
    for w in words:
        groups[w[0]].append(w)
    return dict(groups)


# ---------------------------------------------------------------------------
# 5) 양방향 매핑(bijection): 두 문자열이 1:1 대응(동형, isomorphic)인가
#    s->t 매핑과 t->s 매핑을 동시에 검증해야 "서로 다른 두 글자가
#    같은 글자로 합쳐지는" 위반을 막을 수 있다.
# ---------------------------------------------------------------------------
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    st, ts = {}, {}
    for a, b in zip(s, t):
        if a in st and st[a] != b:
            return False
        if b in ts and ts[b] != a:
            return False
        st[a] = b
        ts[b] = a
    return True


# ---------------------------------------------------------------------------
# 6) 마지막 등장 위치(last-seen index): 값 -> 최근 인덱스
#    "거리 k 이내에 중복이 있는가" 같은 질문을 O(n) 으로.
# ---------------------------------------------------------------------------
def contains_nearby_duplicate(nums, k):
    last = {}                       # 값 -> 마지막으로 본 인덱스
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i
    return False


# ---------------------------------------------------------------------------
# 7) 설계형: dict + 리스트로 평균 O(1) 삽입/삭제/임의접근 집합
#    값 -> 리스트 인덱스 dict 를 함께 들고, 삭제는 "맨 끝 원소와 swap 후 pop".
# ---------------------------------------------------------------------------
class O1Set:
    def __init__(self):
        self.vals = []              # 실제 값들
        self.pos = {}               # 값 -> vals 안에서의 인덱스

    def insert(self, x):
        if x in self.pos:
            return False
        self.pos[x] = len(self.vals)
        self.vals.append(x)
        return True

    def remove(self, x):
        if x not in self.pos:
            return False
        i = self.pos[x]
        last = self.vals[-1]
        self.vals[i] = last         # 마지막 값을 빈 자리로 이동
        self.pos[last] = i
        self.vals.pop()             # 끝을 제거 -> O(1)
        del self.pos[x]
        return True

    def contains(self, x):
        return x in self.pos


# ---------------------------------------------------------------------------
# 데모
# ---------------------------------------------------------------------------
def main():
    print("=" * 56)
    print("Day 13 - 해시맵 응용 (Hashmap Patterns) 예제")
    print("=" * 56)

    print("\n[1] 보수 찾기 (complement)")
    print("two_sum([2,7,11,15], 9) =", two_sum([2, 7, 11, 15], 9))   # [0, 1]

    print("\n[2] 누적합 + 해시맵 (합이 K 인 연속 구간 개수)")
    print("subarray_sum_count([1,1,1], 2) =", subarray_sum_count([1, 1, 1], 2))  # 2
    print("subarray_sum_count([1,2,3], 3) =", subarray_sum_count([1, 2, 3], 3))  # 2

    print("\n[3] 빈도수 비교 (애너그램 판별)")
    print("is_anagram('anagram','nagaram') =", is_anagram("anagram", "nagaram"))  # True
    print("is_anagram('rat','car')         =", is_anagram("rat", "car"))          # False

    print("\n[4] 그룹으로 묶기 (defaultdict)")
    print(group_by_first_letter(["apple", "ant", "bee", "cat", "car"]))

    print("\n[5] 양방향 매핑 (isomorphic)")
    print("is_isomorphic('egg','add')   =", is_isomorphic("egg", "add"))   # True
    print("is_isomorphic('foo','bar')   =", is_isomorphic("foo", "bar"))   # False

    print("\n[6] 마지막 등장 위치 (거리 k 이내 중복)")
    print("contains_nearby_duplicate([1,2,3,1], 3) =",
          contains_nearby_duplicate([1, 2, 3, 1], 3))     # True
    print("contains_nearby_duplicate([1,2,3,1], 2) =",
          contains_nearby_duplicate([1, 2, 3, 1], 2))     # False

    print("\n[7] 설계형 dict + 리스트 (평균 O(1) 집합)")
    s = O1Set()
    print("insert 1 :", s.insert(1))     # True
    print("insert 1 :", s.insert(1))     # False (이미 있음)
    print("contains :", s.contains(1))   # True
    print("remove 1 :", s.remove(1))     # True
    print("contains :", s.contains(1))   # False

    print("\n모든 예제 실행 완료")


if __name__ == "__main__":
    main()

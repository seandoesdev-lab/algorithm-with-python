---
day: 2
phase: phase-0-python-basics
title: 자료형과 컬렉션 (Types & Collections)
category: [자료구조, 해시]
difficulty: 기초
status: done
prev: [[day-01-fast-io/concept|Day 01 — 빠른 입출력]]
next: [[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]]
related:
  - "[[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]]"
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
sources:
  - https://leetcode.com/problems/two-sum/
  - https://leetcode.com/problems/contains-duplicate/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42577
  - https://school.programmers.co.kr/learn/courses/30/lessons/42576
tags: [phase/0, topic/collections]
---

# Day 02 — 자료형과 컬렉션 (Types & Collections)

> [!abstract] 한눈 요약 (TL;DR)
> 파이썬의 4대 컬렉션 `list`, `tuple`, `dict`, `set`은 알고리즘 문제의 거의 모든 상황에 등장한다. `list`는 동적 배열(인덱싱 O(1), 앞 삽입 O(n)), `dict`/`set`은 해시 테이블(평균 O(1) 조회/삽입), `tuple`은 불변 시퀀스다. "있냐/없냐" 검색에는 `set`, 키-값 매핑에는 `dict`, 순서 있는 인덱싱에는 `list`를 선택한다.

> [!note]- 1. 정의와 직관
>
> 파이썬의 **4대 컬렉션** — `list`, `tuple`, `dict`, `set` — 은 알고리즘 문제를 풀 때 거의 모든 상황에서 등장한다.
>
> | 타입 | 가변성(mutability) | 순서(ordered) | 해시 가능성(hashable) | 중복 허용 |
> |------|-------------------|--------------|----------------------|----------|
> | `list` | 가변(mutable) | ✅ | ❌ (unhashable) | ✅ |
> | `tuple` | 불변(immutable) | ✅ | ✅ (원소가 모두 hashable이면) | ✅ |
> | `dict` | 가변(mutable) | ✅ (삽입 순서, Python 3.7+) | ❌ (unhashable) | 키 중복 ❌, 값 중복 ✅ |
> | `set` | 가변(mutable) | ❌ | ❌ (unhashable) | ❌ |
>
> **일상 비유**:
> - `list` → 번호가 붙은 줄서기 대기열. 순서 있고, 언제든 추가·삭제·수정 가능.
> - `tuple` → 주민등록번호처럼 한 번 발급되면 바꿀 수 없는 레코드.
> - `dict` → 사전(辭典). 단어(키, key)로 의미(값, value)를 즉시 찾아줌.
> - `set` → 도장(stamp) 모음. 같은 도장은 하나만 보관, 순서 없음.

> [!gear]- 2. 동작 원리
>
> ### 2-1. list — 동적 배열(dynamic array)
>
> CPython 내부에서 `list`는 **연속된 메모리 블록(포인터 배열)** 으로 구현된다.
>
> ```
> index:  [0]   [1]   [2]   [3]   [4]   ...
>         ptr→A ptr→B ptr→C  None  None  (예약 공간)
> ```
>
> - **인덱싱(indexing)**: 포인터 배열에서 `base + i * sizeof(ptr)` → O(1).
> - **append**: 예약 공간이 있으면 O(1). 꽉 차면 약 2배 크기로 **재할당(reallocation)** 후 복사 → 분할상환(amortized) O(1).
> - **insert(0, x)**: 모든 기존 원소를 오른쪽으로 한 칸씩 **시프트(shift)** → O(n). 큐(queue)처럼 앞에서 꺼내야 하면 `collections.deque`를 쓸 것.
>
> ### 2-2. dict / set — 해시 테이블(hash table)
>
> `dict`와 `set` 모두 내부적으로 **해시 테이블**을 사용한다.
>
> ```
> key  →  hash(key)  →  slot_index = hash % capacity
>                        ↓
>                     [slot_0] [slot_1] [slot_2] ... [slot_n]
> ```
>
> 1. 키를 `hash()` 함수로 정수(해시값, hash value)로 변환.
> 2. `hash % capacity`로 슬롯(bucket) 인덱스 계산.
> 3. 해당 슬롯에 키-값 쌍 저장.
>
> - **탐색/삽입/삭제 평균 O(1)**: 슬롯 인덱스를 한 번에 계산하므로.
> - **최악 O(n)**: 서로 다른 키가 같은 슬롯에 몰리는 **해시 충돌(hash collision)** 발생 시 선형 탐사(linear probing)로 처리.
> - **hashable 조건**: 해시값이 존재하고 생애주기 동안 변하지 않아야 함. `int`, `str`, `tuple`(원소가 모두 hashable)은 hashable. `list`, `dict`, `set`은 mutable이라 unhashable → `dict` 키나 `set` 원소로 사용 불가.
>
> ### 2-3. tuple — 불변 시퀀스(immutable sequence)
>
> `list`와 동일한 포인터 배열 구조지만 생성 후 **수정 불가**. CPython은 길이 0~1의 튜플을 **캐싱(caching)** 하여 메모리 절약.
>
> ### 파이썬 관용구
>
> ```python
> # ── list ──────────────────────────────────────────────────
> a = [1, 2, 3, 4, 5]
> print(a[0], a[-1])          # 인덱싱: 1, 5
> print(a[1:4])               # 슬라이싱: [2, 3, 4]
> print(a[::-1])              # 역순: [5, 4, 3, 2, 1]
> a.append(6)                 # 맨 뒤 추가 O(1)
> a.insert(0, 0)              # 맨 앞 삽입 O(n) — 느림!
>
> # ── tuple ─────────────────────────────────────────────────
> point = (3, 5)
> x, y = point               # 언패킹(unpacking)
> a2, *rest = (1, 2, 3, 4)   # 확장 언패킹: a2=1, rest=[2,3,4]
>
> # ── dict ──────────────────────────────────────────────────
> d = {"apple": 3, "banana": 2}
> print(d.get("cherry", 0))           # 없으면 0 반환 (KeyError 방지)
> freq = {}
> for ch in "hello":
>     freq[ch] = freq.get(ch, 0) + 1  # 빈도 카운트 관용구
>
> # ── set ───────────────────────────────────────────────────
> s1 = {1, 2, 3, 4}
> s2 = {3, 4, 5, 6}
> print(s1 & s2)   # 교집합(intersection): {3, 4}
> print(s1 | s2)   # 합집합(union):        {1,2,3,4,5,6}
> print(s1 - s2)   # 차집합(difference):   {1, 2}
> print(s1 ^ s2)   # 대칭차집합(symmetric difference): {1,2,5,6}
> ```

> [!chart]- 3. 복잡도 (시간/공간)
>
> ### list
>
> | 연산 | 시간복잡도 | 설명 |
> |------|-----------|------|
> | `a[i]` 인덱싱 | O(1) | 포인터 배열 직접 접근 |
> | `x in a` 검색 | O(n) | 앞에서부터 하나씩 비교(선형 탐색) |
> | `a.append(x)` | 분할상환 O(1) | 가끔 재할당 발생, 평균 O(1) |
> | `a.insert(0, x)` 맨 앞 삽입 | O(n) | 기존 원소 전체 시프트 |
> | `a.pop()` 맨 뒤 제거 | O(1) | 마지막 슬롯 해제 |
> | `a.pop(0)` 맨 앞 제거 | O(n) | 원소 전체 시프트 |
> | 슬라이싱 `a[i:j]` | O(k), k=j-i | 새 리스트 복사(shallow copy) |
>
> ### dict / set
>
> | 연산 | 평균 시간복잡도 | 최악 시간복잡도 | 설명 |
> |------|--------------|--------------|------|
> | `k in d` / `k in s` | O(1) | O(n) | 해시 테이블 직접 조회 |
> | `d[k] = v` 삽입 | O(1) | O(n) | 슬롯 계산 후 기록 |
> | `del d[k]` 삭제 | O(1) | O(n) | 슬롯 무효화 |
> | `d[k]` 조회 | O(1) | O(n) | 슬롯 조회 |
>
> 최악 O(n)은 악의적으로 설계된 키로 인한 대규모 충돌 시 발생. 실제 코테에서는 사실상 O(1)로 취급.

> [!tip]- 💡 이해를 돕는 팁
>
> ### set/dict vs list — 검색 성능 차이
>
> - **리스트 `in` 연산은 O(n)**: 원소 100만 개짜리 리스트에서 `x in list`는 최대 100만 번 비교.
> - **set/dict `in` 연산은 평균 O(1)**: 해시값 계산 한 번으로 슬롯을 직접 찾아감.
> - 실전 팁: 입력값 목록에서 **"있냐/없냐"만 묻는다면** 리스트 대신 `set`으로 변환 후 사용.
>
> ```python
> # 느림 (O(n * m))
> nums_list = [1, 2, 3, ..., 1_000_000]
> for q in queries:
>     if q in nums_list:   # O(n) 매번
>         print("found")
>
> # 빠름 (O(n + m))
> nums_set = set(nums_list)  # O(n) 변환 한 번
> for q in queries:
>     if q in nums_set:      # O(1) 매번
>         print("found")
> ```
>
> ### 리스트로 큐(queue) 쓰지 말 것 — deque 사용
>
> ```python
> from collections import deque
> q = deque([1, 2, 3])
> q.appendleft(0)   # O(1) — 양방향 O(1)
> q.popleft()       # O(1) — list.pop(0)는 O(n)!
> ```
>
> 참고: Python 공식 문서 — [collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
> 참고: [파이썬 자료구조 시간복잡도 정리 (Wiki)](https://wiki.python.org/moin/TimeComplexity)
> 참고: [해시 테이블 개념 (Wikipedia)](https://en.wikipedia.org/wiki/Hash_table)

> [!warning]- ⚠️ 개발자 필수 상식
>
> ### ① 슬라이싱은 항상 새 리스트를 만든다 (shallow copy)
>
> ```python
> a = [1, 2, 3]
> b = a[:]        # 얕은 복사(shallow copy) — 새 리스트 객체
> print(b is a)   # False — 다른 객체
> b[0] = 99
> print(a)        # [1, 2, 3] — 원본 유지
> ```
>
> 슬라이싱 `a[i:j]`은 O(k) 시간과 O(k) 메모리를 소비한다 (k = j - i).
> **중첩 리스트(2D)** 를 얕은 복사하면 내부 리스트는 공유된다:
>
> ```python
> matrix = [[1,2],[3,4]]
> copy = matrix[:]
> copy[0][0] = 99
> print(matrix)   # [[99,2],[3,4]] — 내부 리스트 공유!
> import copy
> deep = copy.deepcopy(matrix)  # 진짜 독립 복사
> ```
>
> ### ② 가변 기본 인자(mutable default argument) 함정
>
> ```python
> # 위험한 코드 — 절대 쓰지 말 것
> def append_to(element, to=[]):   # 기본값 [] 는 함수 정의 시 한 번만 생성
>     to.append(element)
>     return to
>
> print(append_to(1))   # [1]
> print(append_to(2))   # [1, 2]  ← 이전 호출 결과가 누적!
>
> # 올바른 방법 — None을 기본값으로
> def append_to_safe(element, to=None):
>     if to is None:
>         to = []
>     to.append(element)
>     return to
> ```
>
> **이유**: 파이썬에서 함수의 기본 인자는 함수 객체의 `__defaults__` 속성에 **모듈 로드 시점에 한 번** 생성되어 저장된다. 가변 객체(list, dict 등)는 매 호출마다 새로 생성되지 않고 **같은 객체를 재사용**한다.
>
> ### ③ list.insert(0, x)가 느린 이유
>
> 리스트는 연속 메모리 배열이므로, 인덱스 0에 삽입하려면 기존 모든 원소를 오른쪽으로 한 칸씩 밀어야 한다. 원소 n개 → O(n) 시프트 발생. 앞에서 자주 추가·제거한다면 `collections.deque`(이중 연결 리스트 기반)가 O(1).
>
> ### ④ 튜플 언패킹(tuple unpacking)
>
> ```python
> # 변수 교환 — 임시 변수 없이
> a, b = 1, 2
> a, b = b, a      # 파이썬 관용구
>
> # 확장 언패킹 (Python 3+)
> first, *middle, last = [1, 2, 3, 4, 5]
> # first=1, middle=[2,3,4], last=5
> ```
>
> ### ⑤ dict 삽입 순서 보존 (Python 3.7+)
>
> Python 3.7부터 `dict`는 **삽입 순서(insertion order)** 를 공식적으로 보장한다. 이전 버전에서는 `collections.OrderedDict`가 필요했다.
>
> ```python
> d = {}
> d["c"] = 3; d["a"] = 1; d["b"] = 2
> list(d.keys())   # ['c', 'a', 'b'] — 삽입 순서 보장
> ```
>
> ### ⑥ == vs is
>
> ```python
> a = [1, 2, 3]
> b = [1, 2, 3]
> c = a
>
> print(a == b)   # True  — 값(value) 비교
> print(a is b)   # False — 객체 동일성(identity) 비교: 다른 객체
> print(a is c)   # True  — 같은 객체를 참조
>
> # None 비교는 반드시 is 사용
> x = None
> if x is None:   # 올바름
>     pass
> ```
>
> ### ⑦ 얕은 복사 vs 깊은 복사 (shallow copy vs deep copy)
>
> | 방법 | 동작 | 중첩 객체 |
> |------|------|----------|
> | `b = a` | 참조 복사(reference copy) | 완전 공유 |
> | `b = a[:]` / `b = a.copy()` / `b = list(a)` | 얕은 복사(shallow copy) | 내부 객체 공유 |
> | `import copy; b = copy.deepcopy(a)` | 깊은 복사(deep copy) | 완전 독립 |
>
> ### 언제 쓰는가 — 한 줄 판단 기준
>
> ```
> 검색 빈번?       → set (존재 여부) 또는 dict (키-값)
> 순서 + 인덱싱?  → list
> 불변 키/레코드?  → tuple
> ```

> [!example]- 예제 코드
>
> ```python
> # list — 슬라이싱, append, pop 비교
> a = [1, 2, 3, 4, 5]
> print(a[::-1])              # 역순: [5, 4, 3, 2, 1]
> a.append(6)                 # O(1)
> a.insert(0, 0)              # O(n) — 느림!
>
> # dict — get / setdefault / 빈도 카운팅
> d = {"apple": 3}
> print(d.get("cherry", 0))   # KeyError 방지
> freq = {}
> for ch in "hello":
>     freq[ch] = freq.get(ch, 0) + 1
>
> # set — 교집합·합집합·중복 제거
> s1, s2 = {1, 2, 3, 4}, {3, 4, 5, 6}
> print(s1 & s2, s1 | s2, s1 - s2)
>
> # deque — 앞·뒤 O(1) 삽입/삭제
> from collections import deque
> q = deque([1, 2, 3])
> q.appendleft(0); q.popleft()  # list.pop(0)는 O(n)!
> ```
>
> 전체 실행 예제: [examples.py](examples.py)

> [!question]- 연습문제
>
> | # | 문제 | 플랫폼 | 난이도 | 핵심 개념 |
> |---|---|---|---|---|
> | 1 | Two Sum | LeetCode #1 | 🟢 기초 | dict, 해시, 배열 |
> | 2 | Contains Duplicate | LeetCode #217 | 🟢 기초 | set, 해시, 배열 |
> | 3 | 전화번호 목록 | 프로그래머스 해시 Lv.2 | 🟡 중급 | dict, set, 문자열 해시 |
> | 4 | 완주하지 못한 선수 | 프로그래머스 해시 Lv.1 | ⚫ 기출 | dict, Counter, 해시 |
>
> 전체 문제 목록 및 힌트: [problems.md](problems.md)

> [!check]- 해설
>
> 각 문제의 접근법, 복잡도 분석, 다중 풀이 비교는 [solutions.py](solutions.py) 참고.

---
## 🔗 관계 (Relationships)

- ⬅️ 이전: [[day-01-fast-io/concept|Day 01 — 빠른 입출력]]
- ➡️ 다음: [[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]]
- 🧭 관련:
  - [[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]] — list 심화 (내부 동작과 복잡도)
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — list로 큐의 한계, deque 대안
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — dict/set 원리 심화 (해시 테이블)
- 🗺️ 지도: [[Phase-0 MOC]] · [[00 Algorithm MOC]]

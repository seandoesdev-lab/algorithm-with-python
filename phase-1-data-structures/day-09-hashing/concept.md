---
day: 9
phase: 1-data-structures
title: 해시 dict/set (Hashing)
category: [자료구조, 해시]
difficulty: 기초
status: done
prev: [[day-08-queue-deque/concept|Day 08 — 큐와 덱]]
next: "[[day-10-linked-list/concept|Day 10 — 연결 리스트]]"
related:
  - "[[day-02-collections/concept|Day 02 — 자료형과 컬렉션]]"
  - "[[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/lessons/42576
  - https://school.programmers.co.kr/learn/courses/30/lessons/1845
  - https://leetcode.com/problems/two-sum/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42577
  - https://school.programmers.co.kr/learn/courses/30/lessons/42578
  - https://leetcode.com/problems/group-anagrams/
  - https://leetcode.com/problems/top-k-frequent-elements/
  - https://leetcode.com/problems/longest-consecutive-sequence/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42579
tags: [phase/1, topic/hash]
---

# Day 09 — 해시 dict/set (Hashing)

> [!abstract] 한눈 요약 (TL;DR)
> 해시 테이블은 키를 해시 함수로 정수 인덱스로 바꿔 **직접** 저장·조회하므로 삽입·조회·삭제·멤버십 검사가 모두 **평균 O(1)**이다. 파이썬의 `dict`와 `set`이 해시 테이블 기반이며, `Counter`와 `defaultdict`가 빈도 세기·그룹화를 간결하게 해결한다. "본 적 있나 / 몇 번 나왔나 / 어떤 그룹인가"가 보이면 해시를 먼저 의심하라.

> [!note]- 1. 정의와 직관
> **해시 테이블(hash table)**은 **키(key)를 받아 값을 거의 즉시 찾아내는** 자료구조다. 핵심 아이디어는 **해시 함수(hash function)**로 키를 정수(해시값)로 바꾼 뒤, 그 정수를 배열의 인덱스로 사용해 값을 **직접** 저장/조회하는 것이다. 처음부터 끝까지 훑지 않고 "계산해서 바로 그 칸으로 간다"는 점이 비결이다.
>
> 일상 비유는 **사물함(locker)**이다. 학번(키)을 정해진 규칙으로 계산해 사물함 번호를 얻으면, 모든 사물함을 열어보지 않고 **계산된 번호의 사물함 하나만** 열면 된다. 사전(dictionary)에서 단어를 찾을 때 첫 글자로 대략 위치를 잡아 펴는 것과도 닮았다.
>
> ```
> 키 "apple"  --[해시 함수]-->  정수 8721023...  --[ % 버킷수 ]-->  인덱스 3
>                                                                      |
>    buckets:  [0][1][2][ 3:("apple", 값) ][4][5][6][7]   <- 인덱스 3 칸에 바로 저장/조회
> ```
>
> **왜 평균 O(1)인가**
>
> 리스트에서 "x가 있나?"를 확인하려면 앞에서부터 하나씩 비교한다 -> 최악 **O(n)**. 해시 테이블은 **키를 해시값으로 바꿔 인덱스를 계산**하고, 그 칸만 확인하면 된다. 계산은 키 길이에만 비례하는 상수 시간으로 보며, 칸 접근은 배열 인덱싱이라 O(1)이다. 따라서 삽입·조회·삭제·멤버십 검사가 **평균 O(1)**이다.
>
> > **주의:** "평균"이다. 충돌이 몰리면(해시 충돌 참고) 최악 O(n)이 될 수 있다. 실무·코테에서는 거의 항상 평균 O(1)로 동작하지만, 원리상 보장이 아니라 기댓값임을 알아야 한다.
>
> **파이썬의 dict와 set:**
>
> | 자료형 | 정체 | 저장하는 것 | 용도 |
> |---|---|---|---|
> | `dict` | 해시 테이블 | **키 -> 값** 쌍 | "이 키에 대응하는 값은?" (매핑) |
> | `set` | 해시 테이블 | **키만** (값 없음) | "이 원소가 있나?" (멤버십·중복 제거) |
>
> `set`은 값이 없는 `dict`라고 생각하면 된다. 둘 다 내부적으로 같은 해시 테이블 메커니즘을 쓴다.
>
> > **CPython 3.7+**: `dict`는 **삽입 순서를 보존(insertion order)**한다. 즉 순회 시 넣은 순서대로 나온다. 단 `set`은 **순서를 보장하지 않는다**(정렬도 아님). 순서가 중요하면 `set`을 믿으면 안 된다.

> [!gear]- 2. 동작 원리
> **해시 충돌 (Hash Collision)**
>
> 서로 다른 키가 **같은 인덱스**로 계산될 수 있다. 이를 **충돌(collision)**이라 한다. 버킷 수는 유한한데 키는 무한하므로 충돌은 피할 수 없다. 해결 방식은 두 가지가 대표적이다.
>
> 1. **체이닝(separate chaining):** 한 칸에 여러 (키,값)을 **연결 리스트/목록**으로 매단다.
> 2. **개방 주소법(open addressing):** 충돌 시 **다음 빈 칸을 찾아** 옮겨 담는다(CPython이 사용하는 방식).
>
> ```
> 충돌 예 (둘 다 인덱스 3으로 계산된 경우, 개방 주소법):
>    "apple" -> 3 (빈칸) 저장:   [.][.][.][apple][.]...
>    "grape" -> 3 (이미 참)  ->  다음 빈칸 4 탐색:  [.][.][.][apple][grape]...
> ```
>
> 충돌이 한 칸에 몰리면 그 칸 처리가 길어져 **최악 O(n)**이 된다. 파이썬은 적재율(load factor)이 높아지면 내부 배열을 키워 **재해싱(rehashing)**해서 충돌을 분산한다(그래서 평균 O(1) 유지).
>
> **해시 가능(hashable)이란**
>
> 해시 테이블의 키가 되려면 **해시값이 변하지 않아야** 한다. 그래서 **불변(immutable) 객체만** 키가 될 수 있다.
>
> | 키로 가능 (hashable) | 키로 불가능 (unhashable) |
> |---|---|
> | `int`, `float`, `str`, `bool` | `list` |
> | `tuple` (안의 원소도 전부 hashable일 때) | `dict` |
> | `frozenset` | `set` |
>
> > **자주 쓰는 트릭:** 여러 값을 묶어 키로 쓰고 싶으면 **`tuple`로 변환**한다. 예) 정렬한 문자 빈도 `tuple`을 키로 애너그램을 묶는다.
>
> **collections의 강력한 도구: Counter, defaultdict**
>
> **`Counter`** — 개수 세기 전용 dict. "몇 번 나왔는가" 문제의 정답 도구.
>
> ```python
> from collections import Counter
> c = Counter("banana")        # Counter({'a': 3, 'n': 2, 'b': 1})
> c["a"]                        # 3
> c["z"]                        # 0  (없는 키도 KeyError 없이 0 반환)
> c.most_common(2)             # [('a', 3), ('n', 2)]  상위 2개
> Counter([1,1,2]) + Counter([1,3])   # Counter({1: 3, 2: 1, 3: 1})  덧셈 지원
> ```
>
> **`defaultdict`** — 없는 키에 자동으로 기본값을 만들어주는 dict. "그룹으로 묶기"에 최적.
>
> ```python
> from collections import defaultdict
> groups = defaultdict(list)   # 없는 키는 자동으로 빈 리스트 []
> groups["fruit"].append("apple")   # KeyError 없이 바로 append 가능
> # defaultdict(int)는 없는 키를 0으로 -> 직접 개수 세기에 사용
> ```
>
> | 상황 | 추천 도구 |
> |---|---|
> | 원소별 등장 횟수 | `Counter` |
> | 키별로 리스트/집합에 모으기 | `defaultdict(list)` / `defaultdict(set)` |
> | 직접 카운팅 로직이 필요 | `defaultdict(int)` 또는 `dict.get(k, 0)` |
>
> **해시가 빛나는 문제 패턴 (Key Patterns)**
>
> 1. **본 적 있는가? (seen set):** 지나온 값을 `set`에 모아두고, 새 값이 이미 있는지 O(1)로 확인. 중복 탐지, "처음 등장하는/두 번 등장하는 원소" 문제.
> 2. **보수 찾기 (complement):** Two Sum류. `target - x`가 이미 dict에 있는지 확인하며 한 번만 순회 -> O(n).
> 3. **개수 세기 (frequency):** `Counter`로 빈도를 만든 뒤 비교/정렬. 애너그램 판별, 최빈값, 완주 못한 선수.
> 4. **그룹으로 묶기 (grouping):** 같은 성질을 가진 것끼리 같은 키 아래 모으기. 정렬·빈도 `tuple`을 키로 사용.
> 5. **빠른 멤버십 (set membership):** `list in` 대신 `set in`으로 바꿔 전체 알고리즘을 O(n^2) -> O(n)로.

> [!chart]- 3. 복잡도 (시간/공간)
> | 연산 | `dict` / `set` (평균) | 최악 | `list` 비교 |
> |---|---|---|---|
> | 삽입 `d[k]=v` / `s.add(x)` | O(1) | O(n) | append O(1) |
> | 조회 `d[k]` | O(1) | O(n) | 인덱스 O(1) / 값탐색 O(n) |
> | 멤버십 `x in d` / `x in s` | **O(1)** | O(n) | **O(n)** |
> | 삭제 `del d[k]` / `s.remove(x)` | O(1) | O(n) | O(n) (값 삭제) |
> | 전체 순회 | O(n) | O(n) | O(n) |
> | 공간 | O(n) | O(n) | O(n) |
>
> **요약:** "있는지/몇 번/어떤 키에" 묻는 모든 질문 -> 해시(평균 O(1)). 최악 O(n)은 의도적으로 충돌을 유발하는 극단 입력에서만 문제 되며, 일반 코테에선 평균 O(1)로 본다.
>
> 집합 연산도 강력하다(평균, n/m은 두 집합 크기):
>
> | 집합 연산 | 의미 | 복잡도 |
> |---|---|---|
> | `a & b` 교집합 | 둘 다 있는 것 | O(min(n, m)) |
> | `a \| b` 합집합 | 둘 중 하나라도 | O(n + m) |
> | `a - b` 차집합 | a에만 있는 것 | O(n) |
> | `a ^ b` 대칭차 | 한쪽에만 있는 것 | O(n + m) |

> [!tip]- 💡 이해를 돕는 팁
> - **"본 적 있나 / 몇 번 나왔나 / 어떤 그룹인가"가 보이면 해시를 의심하라.** 이 세 질문은 거의 항상 `set`·`Counter`·`defaultdict`로 평균 O(1)에 풀린다. 이중 루프(O(n^2))가 떠오르면 "한쪽을 해시로 미리 넣어두면 O(n)이 되지 않을까?"를 먼저 자문한다.
>   - 참고: [Python sets & dicts as hash tables (Real Python)](https://realpython.com/python-hash-table/)
>
> - **`in` 검사는 자료형에 따라 복잡도가 다르다.** `x in list`는 O(n), `x in set/dict`는 평균 O(1). 반복적으로 멤버십을 검사한다면 리스트를 **한 번 `set`으로 바꿔두는** 것만으로 큰 차이가 난다.
>   - 참고: [Time Complexity of Python operations (Python Wiki)](https://wiki.python.org/moin/TimeComplexity)
>
> - **개수 세기는 `Counter`가 거의 항상 정답.** 직접 `d[k]=d.get(k,0)+1`을 쓰기 전에 `Counter`를 먼저 떠올린다. `most_common`, `+`/`-`, `elements()`까지 무료로 따라온다.
>   - 참고: [collections.Counter (Python 공식 문서)](https://docs.python.org/3/library/collections.html#collections.Counter)
>
> - **`dict`는 삽입 순서를 지키지만 `set`은 안 지킨다.** "처음 등장 순서대로"가 필요한데 `set`을 쓰면 틀린다. 순서가 필요하면 `dict`(키만 써서 순서 보존 집합처럼)나 리스트+`seen` 조합을 쓴다.
>   - 참고: [What's New in Python 3.7 — dict insertion order](https://docs.python.org/3/whatsnew/3.7.html)
>
> - **키로 묶고 싶은 여러 값은 `tuple`로 만든다.** `list`는 unhashable이라 키가 못 된다. 좌표 `(r, c)`, 정렬한 글자 `tuple(sorted(w))`, 빈도 벡터 `tuple` 등이 단골 키다.
>   - 참고: [Why lists can't be dictionary keys (Python FAQ)](https://docs.python.org/3/faq/design.html#why-can-t-i-use-a-list-as-a-dict-key)
>
> - **해시는 평균 O(1)이지 보장 O(1)이 아니다.** 충돌이 몰리면 최악 O(n). 면접에서 "왜 평균인가, 최악은 언제인가(충돌·악의적 입력), 파이썬은 어떻게 분산하나(재해싱)"를 답할 수 있어야 한다.
>   - 참고: [Hashing Data Structure (GeeksforGeeks)](https://www.geeksforgeeks.org/hashing-data-structure/)

> [!warning]- ⚠️ 개발자 필수 상식
> 1. **`list`의 `in`은 O(n)이다.** 큰 리스트에서 반복 멤버십 검사를 하면 O(n^2)로 시간초과(TLE) 나기 쉽다. "있는지"만 궁금하면 **`set`으로 바꿔라**. 코테 시간초과의 단골 원인 1순위.
>
> 2. **없는 키 직접 접근은 `KeyError`.** `d[k]`는 키가 없으면 예외가 난다. 안전하게는 `d.get(k, 기본값)`, 또는 `defaultdict`/`Counter`를 쓴다. `if k in d:`로 먼저 확인해도 된다.
>
> 3. **`set`/`dict`의 키는 hashable(불변)이어야 한다.** `list`·`dict`·`set`은 키가 될 수 없다. `TypeError: unhashable type`을 보면 "키로 list를 썼구나"를 떠올린다 -> `tuple`로 변환.
>
> 4. **`set`은 순서가 없다(정렬도 아니다).** `set`을 순회해 나온 순서에 의존하면 안 된다. "처음 등장 순서"가 필요하면 `dict`의 키 순서(3.7+)나 별도 리스트로 순서를 관리한다.
>
> 5. **`Counter`는 없는 키를 0으로 본다(에러 없음).** `c["없는것"]`은 `KeyError`가 아니라 `0`. 다만 이렇게 조회하면 그 키가 `Counter`에 **생기지는 않는다**(0 반환만). 일반 dict와 다른 점.
>
> 6. **`Counter`끼리 빼면 음수/0은 사라진다.** `Counter(a) - Counter(b)`는 0 이하 항목을 버린다. 순수 차이를 원하면 `subtract()` 메서드(제자리 수정, 음수 유지)를 쓴다. 동작 차이를 알아둘 것.
>
> 7. **부동소수점 키는 위험하다.** `0.1 + 0.2 != 0.3`이라 float를 키로 쓰면 의도와 다른 칸에 들어갈 수 있다. 키로는 가급적 `int`·`str`·`tuple`을 쓴다.
>
> 8. **딕셔너리를 순회하면서 크기를 바꾸지 말라.** 순회 중 `del`/추가는 `RuntimeError: dictionary changed size during iteration`. 지울 키를 먼저 모은 뒤 순회 밖에서 삭제한다.
>
> 9. **메모리 트레이드오프를 의식하라.** 해시는 속도를 위해 추가 메모리(버킷·적재 여유분)를 쓴다. "시간 O(1)을 공간 O(n)으로 산다"는 전형적 시간-공간 트레이드오프(time-space tradeoff)다.

> [!example]- 예제 코드
> ```python
> from collections import Counter, defaultdict
>
> # 1) 멤버십: list 대신 set (O(n^2) -> O(n))
> nums = [1, 2, 3, 4]
> target_set = set(nums)            # 한 번 O(n)으로 set 변환
> print(3 in target_set)            # 이후 매 검사가 평균 O(1)
>
> # 2) 중복 제거
> unique = list(set([1, 1, 2, 3, 3]))   # 순서는 보장 안 됨
>
> # 3) 보수 찾기 (Two Sum)
> def two_sum(nums, target):
>     seen = {}                     # 값 -> 인덱스
>     for i, x in enumerate(nums):
>         if target - x in seen:    # 보수가 이미 있으면 정답
>             return [seen[target - x], i]
>         seen[x] = i
>     return []
>
> # 4) 개수 세기
> freq = Counter("mississippi")     # Counter({'s':4,'i':4,'p':2,'m':1})
> print(freq.most_common(1))        # [('s', 4)] (또는 i, 동률 시 먼저 등장한 것)
>
> # 5) 그룹으로 묶기 (애너그램)
> def group_anagrams(words):
>     groups = defaultdict(list)
>     for w in words:
>         key = tuple(sorted(w))    # 정렬한 글자 튜플을 키로
>         groups[key].append(w)
>     return list(groups.values())
>
> # 6) 없는 키 안전 접근
> scores = {"a": 1}
> print(scores.get("b", 0))         # 0
>
> # 7) 집합 연산으로 공통 원소
> common = set([1, 2, 3]) & set([2, 3, 4])   # {2, 3}
>
> # 8) dict 순회 (키/값/쌍)
> m = {"x": 1, "y": 2}
> for k, v in m.items(): ...        # 쌍 (삽입 순서 보존, 3.7+)
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제
> | 번호 | 문제 | 출처 | 난이도 | 카테고리 |
> |---|---|---|---|---|
> | 1 | 완주하지 못한 선수 | [프로그래머스 #42576](https://school.programmers.co.kr/learn/courses/30/lessons/42576) | 🟢기초 | 개수 세기 |
> | 2 | 폰켓몬 | [프로그래머스 #1845](https://school.programmers.co.kr/learn/courses/30/lessons/1845) | 🟢기초 | set |
> | 3 | Two Sum | [LeetCode #1](https://leetcode.com/problems/two-sum/) | 🟢기초 | 보수 찾기 |
> | 4 | 전화번호 목록 | [프로그래머스 #42577](https://school.programmers.co.kr/learn/courses/30/lessons/42577) | 🟡중급 | 접두사 검사 |
> | 5 | 위장 | [프로그래머스 #42578](https://school.programmers.co.kr/learn/courses/30/lessons/42578) | 🟡중급 | 경우의 수 |
> | 6 | Group Anagrams | [LeetCode #49](https://leetcode.com/problems/group-anagrams/) | 🟡중급 | 그룹화 |
> | 7 | Top K Frequent Elements | [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/) | 🟡중급 | 빈도+정렬 |
> | 8 | Longest Consecutive Sequence | [LeetCode #128](https://leetcode.com/problems/longest-consecutive-sequence/) | 🔴심화 | set 멤버십 |
> | 9 | 베스트앨범 | [프로그래머스 #42579](https://school.programmers.co.kr/learn/courses/30/lessons/42579) | ⚫기출 | 그룹별 집계+정렬 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ 이전: [[day-08-queue-deque/concept|Day 08 — 큐와 덱]]
- ➡️ 다음: [[day-10-linked-list/concept|Day 10 — 연결 리스트]]
- 🧭 관련:
  - [[day-02-collections/concept|Day 02 — 자료형과 컬렉션]] — dict/set 입문
  - [[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]] — Counter·defaultdict
- 🗺️ 지도: [[Phase-1 MOC]] · [[00 Algorithm MOC]]

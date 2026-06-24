---
day: 13
phase: 1-data-structures
title: 해시맵 응용 (Hashmap Patterns)
category: [자료구조, 해시]
difficulty: 중급
status: done
prev: "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
next: "[[day-14-prefix-sum/concept|Day 14 — 구간 자료구조 입문 (누적 합)]]"
related:
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-14-prefix-sum/concept|Day 14 — 누적 합]]"
  - "[[day-04-strings/concept|Day 04 — 문자열 다루기]]"
  - "[[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]]"
sources:
  - https://leetcode.com/problems/subarray-sum-equals-k/
  - https://leetcode.com/problems/continuous-subarray-sum/
  - https://leetcode.com/problems/4sum-ii/
  - https://leetcode.com/problems/isomorphic-strings/
  - https://leetcode.com/problems/word-pattern/
  - https://leetcode.com/problems/insert-delete-getrandom-o1/
  - https://leetcode.com/problems/lru-cache/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42888
  - https://school.programmers.co.kr/learn/courses/30/lessons/92334
  - https://school.programmers.co.kr/learn/courses/30/lessons/72411
  - https://docs.python.org/3/library/collections.html
tags: [phase/1, topic/hashmap]
---

# Day 13 — 해시맵 응용 (Hashmap Patterns)

> [!abstract] 한눈 요약 (TL;DR)
> [[day-09-hashing/concept|Day 09]]에서 배운 `dict`·`set`·`Counter`·`defaultdict`는 "도구"였다. 오늘은 그 도구로 실제 코테 문제를 푸는 **반복되는 설계 패턴(design pattern)** 7가지를 익힌다. 핵심은 단 하나 — **"이미 본 것을 평균 O(1)에 기억한다"**는 해시의 능력을, 문제 유형별로 *무엇을 키로, 무엇을 값으로 저장할지*로 번역하는 것이다. 대표 패턴은 ① **보수 찾기(complement)**, ② **누적합 + 해시맵(prefix sum)**, ③ **빈도수 비교(frequency)**, ④ **그룹으로 묶기(grouping)**, ⑤ **양방향 매핑(bijection)**, ⑥ **마지막 등장 위치(last-seen)**, ⑦ **설계형(dict + 다른 자료구조)**이다. 이중 루프 O(n²)가 떠오르면 "**한쪽을 해시에 미리 넣어 O(n)으로** 만들 수 있나?"를 먼저 자문하라. 이 패턴들은 카카오·LeetCode 빈출의 절반 이상을 차지한다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **해시맵 응용**이란 새로운 자료구조가 아니라, 해시 테이블(평균 O(1) 저장·조회)을 **문제의 구조에 맞게 쓰는 사고법**이다. 거의 모든 패턴은 다음 한 문장의 변주다.
>
> > **"지금 필요한 답이 과거에 본 어떤 값으로 결정된다면, 그 과거 값을 해시에 쌓아두고 즉시 조회하라."**
>
> 일상 비유는 **전화번호부**다. 매번 모든 사람에게 전화를 걸어 "혹시 철수니?"라고 묻는 대신(완전 탐색 O(n)), 이름(키)으로 번호(값)를 바로 찾는다. 코테에서 "지금까지 본 것 중에 ~인 게 있었나?"라는 질문이 보이면, 그 "본 것"을 적절한 키로 해시에 적재하는 순간 O(n²)가 O(n)으로 무너진다.
>
> **무엇을 키/값으로 둘지가 패턴의 전부다.**
>
> | 패턴 | 키(key) | 값(value) | 푸는 질문 |
> |---|---|---|---|
> | 보수 찾기 | 원소 값 | 인덱스 | "합/차가 target인 짝이 있나?" |
> | 누적합+해시맵 | 누적합(prefix) | 등장 횟수/첫 인덱스 | "합이 K인 연속 구간 개수는?" |
> | 빈도수 비교 | 원소 | 개수 | "두 묶음이 같은 구성인가?" |
> | 그룹으로 묶기 | 그룹 식별자 | 원소 리스트 | "같은 성질끼리 모으면?" |
> | 양방향 매핑 | 한쪽 글자/토큰 | 대응되는 다른 쪽 | "1:1 대응이 일관적인가?" |
> | 마지막 등장 위치 | 원소 | 최근 인덱스 | "거리 k 이내 중복?" |
> | 설계형 | 사용자 정의 | 사용자 정의 | "삽입/삭제/조회 전부 O(1)?" |

> [!gear]- 2. 동작 원리 (How It Works)
> 패턴별로 "왜 한 번 순회로 끝나는가"를 본다.
>
> **(1) 보수 찾기 (complement) — Two Sum의 일반화**
> 합이 `target`인 두 수를 찾을 때, `x`를 보면 짝은 `target - x`로 **결정**된다. 그래서 지나온 값을 `{값: 인덱스}`로 쌓아두고, 매 원소에서 보수가 이미 있는지 O(1)로 확인한다.
> ```
> nums=[2,7,11,15], target=9
>   x=2 : 보수 7 없음 -> seen={2:0}
>   x=7 : 보수 2 있음! -> 정답 [0,1]
> ```
> 4Sum II(#454)는 네 배열을 **2+2로 쪼개** 한쪽 두 배열의 모든 합 빈도를 dict에 모으고, 다른 쪽 합의 보수(`-합`)를 조회한다. O(n⁴) -> O(n²).
>
> **(2) 누적합 + 해시맵 (prefix sum + hashmap) — 오늘의 핵심**
> 연속 구간 `[i+1 .. j]`의 합은 `prefix[j] - prefix[i]`다. 이 값이 `K`가 되려면 `prefix[i] = prefix[j] - K`. 즉 **현재 누적합에서 K를 뺀 값을 과거에 몇 번 봤는지**가 곧 정답 개수다.
> ```
> nums=[1,2,3], K=3,  seen={0:1}(빈 접두부)
>   prefix=1 : 1-3=-2 없음        seen={0:1, 1:1}
>   prefix=3 : 3-3= 0 있음(1번) -> count=1   seen={...,3:1}
>   prefix=6 : 6-3= 3 있음(1번) -> count=2   (구간 [3]과 [1,2])
> ```
> **초기값 `seen[0]=1`이 핵심**: "배열 앞부분 전체"가 K인 경우(시작점이 인덱스 0)를 빠뜨리지 않기 위해 *빈 접두부의 합 0*을 미리 1번 본 것으로 둔다. Day 14의 누적합을 해시와 결합한 형태로, [[day-14-prefix-sum/concept|Day 14]]에서 누적합 자체를 더 깊게 다룬다.
>
> **(3) 빈도수 비교 (frequency)** — `Counter(a) == Counter(b)`는 "모든 원소의 개수가 같은가"를 본다. 애너그램·다중집합 동등성을 한 줄로.
>
> **(4) 그룹으로 묶기 (grouping)** — `defaultdict(list)`에 `groups[key].append(x)`. 키 설계가 전부다(예: 정렬한 글자 `tuple(sorted(w))`로 애너그램 묶기).
>
> **(5) 양방향 매핑 (bijection) — 두 개의 dict가 필요한 이유**
> "egg <-> add"처럼 글자를 1:1 대응시킬 때, `s->t` 한 방향만 검사하면 **서로 다른 두 글자가 같은 글자로 합쳐지는** 위반("badc" vs "baba")을 못 잡는다. `s->t`와 `t->s`를 **동시에** 검증해야 진짜 일대일(전단사)이다.
> ```
> "foo","bar":  f->b, o->a, o->? (o는 a로 약속됐는데 r 요구) -> 위반
> ```
>
> **(6) 마지막 등장 위치 (last-seen index)** — `{값: 최근 인덱스}`. "거리 k 이내 중복"(#219)처럼 *얼마나 가까이* 있었는지를 O(n)에 판정. 이 발상이 [[day-20-sliding-window/concept|Day 20]] 슬라이딩 윈도우로 확장된다.
>
> **(7) 설계형 (dict + 다른 자료구조)** — 해시 하나로 부족할 때 결합한다.
> - **dict + 리스트**(RandomizedSet #380): dict로 `값->인덱스`를 들고, 삭제는 *마지막 원소와 swap 후 pop*해서 삽입·삭제·임의접근을 모두 평균 O(1)로.
> - **dict + 이중 연결 리스트**(LRU Cache #146): "가장 오래 안 쓴 것 추방"을 O(1)에. 파이썬은 `OrderedDict`(내부가 정확히 해시+이중 연결 리스트)의 `move_to_end`/`popitem(last=False)`로 한 방에 해결.

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> 모든 패턴의 공통 효과는 **이중 루프 O(n²) -> 단일 순회 O(n)** 또는 **O(n⁴) -> O(n²)**이다(추가 공간 O(n)을 시간으로 바꾸는 거래).
>
> | 패턴 / 문제 | 순진한 풀이 | 해시 적용 | 공간 |
> |---|---|---|---|
> | 보수 찾기(Two Sum) | O(n²) 모든 쌍 | **O(n)** | O(n) |
> | 4Sum II(2+2 분할) | O(n⁴) | **O(n²)** | O(n²) |
> | 누적합+해시맵(구간 합) | O(n²) 모든 구간 | **O(n)** | O(n) |
> | 빈도수 비교(애너그램) | O(n log n) 정렬 | **O(n)** | O(1)~O(k) |
> | 그룹으로 묶기 | — | **O(nk)** | O(nk) |
> | 양방향 매핑 | — | **O(n)** | O(1)(문자 26종) |
> | 설계형(LRU/RandomizedSet) | O(n) 탐색 | **O(1) 평균** | O(n) |
>
> > **핵심 직관:** 해시는 "평균 O(1)"이지 보장이 아니다([[day-09-hashing/concept|Day 09]] 충돌 참고). 하지만 코테 입력에서는 거의 항상 평균으로 동작하므로, "한쪽을 해시에 넣으면 한 차원 내려간다"를 기본 전략으로 삼는다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"지금까지 본 것 중에 ~"가 들리면 해시를 깐다.** 보수·중복·구간합·매핑 거의 전부 이 한마디로 환원된다.
>   - 참고: [Hash Table cheat sheet for coding interviews (LeetCode Discuss)](https://leetcode.com/discuss/post/6120029/Hashmaps/)
>
> - **누적합+해시맵은 `seen[0]=1`(또는 `{0:-1}`) 초기화를 절대 잊지 마라.** 배열 맨 앞부터 시작하는 구간을 놓치는 1순위 버그다. 개수를 셀 땐 `seen[0]=1`, 인덱스/길이를 구할 땐 `{0:-1}`로 둔다.
>   - 참고: [Subarray Sum Equals K (LeetCode #560)](https://leetcode.com/problems/subarray-sum-equals-k/)
>
> - **"배수(mod) 구간"은 누적합의 나머지를 키로.** 합이 k의 배수 <=> 두 누적합의 `% k`가 같다. 나머지를 처음 본 인덱스만 저장해 거리(길이 2 이상)를 잰다.
>   - 참고: [Continuous Subarray Sum (LeetCode #523)](https://leetcode.com/problems/continuous-subarray-sum/)
>
> - **매핑 문제는 "두 방향 모두" 검사.** 한 방향만 보면 전단사(bijection) 위반을 놓친다. `dict.setdefault(k, v)`가 기존 값과 다르면 즉시 실패시키는 패턴이 깔끔하다.
>   - 참고: [Isomorphic Strings (LeetCode #205)](https://leetcode.com/problems/isomorphic-strings/)
>
> - **O(1) 삭제가 필요하면 "swap-and-pop".** 리스트 중간 삭제는 O(n)이지만, `값->인덱스` dict를 함께 들고 마지막 원소와 자리를 바꾼 뒤 끝을 pop하면 O(1).
>   - 참고: [Insert Delete GetRandom O(1) (LeetCode #380)](https://leetcode.com/problems/insert-delete-getrandom-o1/)
>
> - **"최근 사용/오래된 것 추방"은 `OrderedDict`.** 직접 이중 연결 리스트를 짜기 전에 표준 라이브러리부터 떠올린다. `move_to_end`, `popitem(last=False)` 두 메서드가 LRU의 전부다.
>   - 참고: [collections.OrderedDict (Python 공식 문서)](https://docs.python.org/3/library/collections.html#collections.OrderedDict)

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **누적합 해시맵의 `seen[0]` 초기화.** 개수 문제는 `defaultdict(int)`에 `seen[0]=1`, 최장 길이 문제는 `{0:-1}`. 빠뜨리면 "배열 처음부터의 구간"이 통째로 누락된다.
>
> 2. **음수가 있으면 슬라이딩 윈도우가 아니라 누적합+해시맵이다.** "합이 K인 구간"에서 원소에 음수가 섞이면 투 포인터/윈도우([[day-20-sliding-window/concept|Day 20]])는 단조성이 깨져 틀린다. 이때 누적합+해시맵이 정답.
>
> 3. **`% k`에서 k가 0이거나 음수일 수 있는지 확인.** 모듈러 패턴은 `k==0` 예외, 음수 나머지(파이썬은 `-1 % 5 == 4`로 양수화되어 대체로 유리) 처리에 주의.
>
> 4. **매핑은 반드시 양방향.** 단방향 dict 하나로는 전단사를 보장 못 한다. 길이가 다르면 곧장 `False`(토큰 수 != 패턴 길이).
>
> 5. **`dict`는 삽입 순서 보존(3.7+), `set`은 미보존.** "처음 등장 순서"가 결과에 영향을 주는 문제(오픈채팅방 출력 순서 등)에서 `set` 순회에 의존하면 틀린다.
>
> 6. **중복 신고/중복 입력은 `set`으로 1회화.** 신고 결과(#92334)에서 같은 (신고자,피신고자) 쌍을 여러 번 세면 오답. `set(report)`로 먼저 중복을 제거한다.
>
> 7. **조합 폭발을 경계하라.** 메뉴 리뉴얼(#72411)처럼 `combinations`를 쓰면 주문 길이가 길 때 경우의 수가 급증한다. 제약(문자 종류·길이 상한)을 보고 `itertools.combinations`가 감당 가능한지 가늠한다.
>
> 8. **해시 키는 hashable이어야 한다.** 여러 값을 묶어 키로 쓸 땐 `tuple`로(좌표 `(r,c)`, 조합 결과 등). `list`를 키로 쓰면 `TypeError: unhashable type`.
>
> 9. **`Counter` 산술의 함정.** `Counter(a) - Counter(b)`는 0 이하를 버린다. 순수 차이가 필요하면 `subtract()`. ([[day-09-hashing/concept|Day 09]] 참고.)

> [!example]- 예제 코드 (Examples)
> ```python
> from collections import Counter, defaultdict, OrderedDict
>
> # 1) 보수 찾기 (complement): O(n^2) -> O(n)
> def two_sum(nums, target):
>     seen = {}                       # 값 -> 인덱스
>     for i, x in enumerate(nums):
>         if target - x in seen:
>             return [seen[target - x], i]
>         seen[x] = i
>     return []
>
> # 2) 누적합 + 해시맵: 합이 K 인 "연속 구간" 개수, O(n)
> def subarray_sum_count(nums, K):
>     count, prefix = 0, 0
>     seen = defaultdict(int)
>     seen[0] = 1                     # 핵심: 빈 접두부(합 0)를 1번 본 것으로
>     for x in nums:
>         prefix += x
>         count += seen[prefix - K]
>         seen[prefix] += 1
>     return count
>
> # 3) 양방향 매핑: 1:1 대응(동형)인가
> def is_isomorphic(s, t):
>     st, ts = {}, {}
>     for a, b in zip(s, t):
>         if st.setdefault(a, b) != b: return False
>         if ts.setdefault(b, a) != a: return False
>     return len(s) == len(t)
>
> # 4) 설계형: LRU 캐시 (OrderedDict = 해시 + 이중 연결 리스트)
> class LRUCache:
>     def __init__(self, cap):
>         self.cap, self.od = cap, OrderedDict()
>     def get(self, key):
>         if key not in self.od: return -1
>         self.od.move_to_end(key)            # 최근 사용 표시
>         return self.od[key]
>     def put(self, key, val):
>         if key in self.od: self.od.move_to_end(key)
>         self.od[key] = val
>         if len(self.od) > self.cap:
>             self.od.popitem(last=False)     # 가장 오래된 것 추방
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> | 번호 | 문제 | 출처 | 난이도 | 카테고리 |
> |---|---|---|---|---|
> | 1 | Subarray Sum Equals K | [LeetCode #560](https://leetcode.com/problems/subarray-sum-equals-k/) | 🟡중급 | 누적합+해시맵 |
> | 2 | Continuous Subarray Sum | [LeetCode #523](https://leetcode.com/problems/continuous-subarray-sum/) | 🟡중급 | 누적합 mod |
> | 3 | 4Sum II | [LeetCode #454](https://leetcode.com/problems/4sum-ii/) | 🟡중급 | 보수·분할 |
> | 4 | Isomorphic Strings | [LeetCode #205](https://leetcode.com/problems/isomorphic-strings/) | 🟢기초 | 양방향 매핑 |
> | 5 | Word Pattern | [LeetCode #290](https://leetcode.com/problems/word-pattern/) | 🟢기초 | 양방향 매핑 |
> | 6 | Insert Delete GetRandom O(1) | [LeetCode #380](https://leetcode.com/problems/insert-delete-getrandom-o1/) | 🟡중급 | 설계(dict+리스트) |
> | 7 | LRU Cache | [LeetCode #146](https://leetcode.com/problems/lru-cache/) | 🔴심화 | 설계(LRU) |
> | 8 | 오픈채팅방 | [프로그래머스 #42888](https://school.programmers.co.kr/learn/courses/30/lessons/42888) | ⚫기출 | uid 매핑(카카오) |
> | 9 | 신고 결과 받기 | [프로그래머스 #92334](https://school.programmers.co.kr/learn/courses/30/lessons/92334) | ⚫기출 | 다중 해시(카카오) |
> | 10 | 메뉴 리뉴얼 | [프로그래머스 #72411](https://school.programmers.co.kr/learn/courses/30/lessons/72411) | ⚫기출 | 조합+Counter(카카오) |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — Top-K 문제에서 힙은 종종 해시(빈도 카운트)와 짝지어 쓰인다
- ➡️ **다음(next):** [[day-14-prefix-sum/concept|Day 14 — 구간 자료구조 입문 (누적 합)]] — 오늘의 "누적합+해시맵" 패턴에서 누적합 자체를 더 깊게 파고든다
- 🧭 **관련(related):**
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — 오늘 패턴들이 딛고 선 dict·set·Counter·defaultdict의 토대
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — 빈도 해시 + 힙으로 Top-K를 푸는 조합
  - [[day-14-prefix-sum/concept|Day 14 — 누적 합]] — 구간 합 문제의 정공법, 해시맵과 결합되는 핵심 도구
  - [[day-04-strings/concept|Day 04 — 문자열 다루기]] — 애너그램·매핑·토큰화의 기초
  - [[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]] — "마지막 등장 위치" 해시가 윈도우 기법으로 확장
- 🗺️ **지도(MOC):** [[Phase-1 MOC]] · [[00 Algorithm MOC]]

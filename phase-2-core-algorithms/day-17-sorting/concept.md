---
day: 17
phase: 2-core-algorithms
title: 정렬 (Sorting)
category: [알고리즘, 정렬]
difficulty: 중급
status: done
prev: "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
next: "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
related:
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-19-two-pointers/concept|Day 19 — 투 포인터]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
sources:
  - https://leetcode.com/problems/sort-an-array/
  - https://leetcode.com/problems/sort-colors/
  - https://leetcode.com/problems/merge-intervals/
  - https://leetcode.com/problems/merge-sorted-array/
  - https://leetcode.com/problems/largest-number/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42746
  - https://school.programmers.co.kr/learn/courses/30/lessons/42747
  - https://school.programmers.co.kr/learn/courses/30/lessons/42748
  - https://docs.python.org/3/howto/sorting.html
  - https://en.wikipedia.org/wiki/Timsort
tags: [phase/2, topic/sorting, topic/algorithm]
---

# Day 17 — 정렬 (Sorting)

> [!abstract] 한눈 요약 (TL;DR)
> **정렬(sorting)은 "원소를 일정한 기준(key)으로 줄 세우는 것"이며, 코딩테스트에서 가장 자주 쓰이는 전처리(pre-processing) 도구**다. 정렬 자체를 묻는 문제도 많지만, 그보다 **정렬을 한 번 해두면 그 뒤의 탐색이 극적으로 쉬워진다**는 점이 핵심이다. 정렬된 배열에서는 이분 탐색(O(log n)), 투 포인터(O(n)), 중복 제거, 그리디 선택이 자연스럽게 가능해진다. 파이썬에서는 `sorted(iterable)`와 `list.sort()`가 **Timsort**(안정 정렬, 최악 O(n log n))로 구현돼 있어, 실전에서 직접 정렬 알고리즘을 짤 일은 거의 없다. 대신 **`key` 함수로 "무엇을 기준으로 정렬할지"를 설계하는 능력**이 점수를 가른다. 이 노트는 비교 기반 정렬의 하한이 왜 O(n log n)인지, 버블·삽입·병합·퀵·힙 정렬의 동작과 트레이드오프, **안정 정렬(stable sort)** 의 의미, `key`·다중 키·`cmp_to_key` 활용, 그리고 비교를 하지 않아 O(n)이 가능한 계수 정렬(counting sort)까지 다룬다. [[day-16-big-o/concept|Big-O]]에서 배운 O(n log n)의 가장 대표적인 사례가 바로 정렬이다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **정렬(sorting)** 은 원소들의 모음을 **전순서(total order)** — 즉 어떤 두 원소든 "누가 앞인지" 비교할 수 있는 기준 — 에 따라 비내림차순(non-decreasing) 또는 비오름차순으로 재배열하는 것이다. 기준은 숫자의 크기일 수도, 문자열의 사전순(lexicographic order)일 수도, "어떤 함수에 넣은 결과값"일 수도 있다.
>
> **일상 비유 — 카드 정리.** 손에 든 트럼프 카드를 정리할 때 우리는 보통 카드를 한 장씩 뽑아 이미 정리된 왼쪽 더미의 올바른 위치에 끼워 넣는다. 이게 바로 **삽입 정렬(insertion sort)** 의 직관이다. 한편 큰 책장을 정리할 땐 절반씩 나눠 각각 정리한 뒤 합치는 게 빠른데, 이게 **병합 정렬(merge sort)** 의 직관이다.
>
> 코테에서 정렬이 중요한 이유는 두 가지다:
> 1. **정렬 자체가 답인 문제** — "가장 큰 수 만들기", "회의실 배정(끝나는 시간 순)" 등 *어떤 기준으로 정렬하느냐*가 곧 풀이.
> 2. **정렬은 만능 전처리** — 정렬해 두면 이분 탐색·투 포인터·그리디·중복 제거·구간 병합이 쉬워진다. "막히면 일단 정렬해 보라"는 격언이 있을 정도.
>
> 정렬을 분류하는 두 축:
> - **비교 정렬(comparison sort)** vs **비비교 정렬(non-comparison sort):** 원소끼리 `<` 비교만 쓰면 비교 정렬(하한 O(n log n)), 값 자체를 인덱스로 쓰면 비비교 정렬(계수·기수 정렬, 조건부 O(n)).
> - **안정 정렬(stable)** vs **불안정 정렬(unstable):** 같은 key를 가진 원소들의 **원래 순서가 보존되면** 안정. 다중 기준 정렬에서 결정적으로 중요하다.

> [!gear]- 2. 동작 원리 (How It Works) — 대표 정렬 알고리즘
> **(1) 삽입 정렬 (Insertion Sort) — O(n²), 안정**
> 왼쪽부터 한 칸씩 "이미 정렬된 영역"을 넓히며, 새 원소를 제자리에 끼워 넣는다. 거의 정렬된 입력엔 매우 빠르다(O(n)에 근접). Timsort의 부분 루틴으로도 쓰인다.
> ```
> [5] 2  8  1      <- 5는 정렬됨
> [2 5] 8  1       <- 2를 앞으로 삽입
> [2 5 8] 1        <- 8 제자리
> [1 2 5 8]        <- 1을 맨 앞까지 밀어 삽입
> ```
>
> **(2) 병합 정렬 (Merge Sort) — O(n log n), 안정, 분할정복**
> 배열을 절반으로 쪼개 각각 정렬한 뒤, 정렬된 두 조각을 **병합(merge)** 한다. 분할 단계가 log n번, 각 단계에서 전체 n을 훑으므로 O(n log n). 추가 배열이 필요해 공간 O(n).
> ```
> 분할:  [38 27 43 3 9 82 10]
>        -> [38 27 43]      [3 9 82 10]
>        -> [38][27 43]     [3 9][82 10]
> 병합:  [27 38 43] + [3 9 10 82] -> [3 9 10 27 38 43 82]
> ```
>
> **(3) 퀵 정렬 (Quick Sort) — 평균 O(n log n), 최악 O(n²), 불안정**
> 기준 원소(pivot)를 잡아 "pivot보다 작은 것 / 큰 것"으로 분할한 뒤 각각 재귀. 제자리(in-place)라 공간 효율이 좋고 상수가 작아 실전에서 빠르다. 단, 이미 정렬된 입력에 pivot을 끝으로 잡으면 최악 O(n²).
>
> **(4) 힙 정렬 (Heap Sort) — O(n log n), 불안정**
> [[day-12-heap/concept|힙]]에 전부 넣고 하나씩 꺼내면 정렬된다. 최악도 O(n log n) 보장이지만 캐시 효율이 낮아 실측은 퀵/병합보다 느린 편.
>
> **(5) 계수 정렬 (Counting Sort) — O(n + k), 비교 안 함**
> 값의 범위가 0..k로 좁을 때, 각 값의 개수를 세어(count) 위치를 직접 계산. 비교를 안 하므로 O(n log n) 하한을 깬다. 단 k가 크면 메모리 폭발.
>
> **파이썬의 선택 — Timsort.** `sorted()`/`list.sort()`는 **Timsort**(병합 정렬 + 삽입 정렬 하이브리드)를 쓴다. 이미 정렬된 구간(run)을 찾아 활용해 실데이터에서 매우 빠르고, **안정 정렬**이며 최악 O(n log n)을 보장한다.

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> **(A) 정렬 알고리즘 비교**
>
> | 알고리즘 | 평균 | 최악 | 공간 | 안정성 | 비고 |
> |---|---|---|---|---|---|
> | 버블 정렬 | O(n²) | O(n²) | O(1) | 안정 | 교육용, 실전 X |
> | 선택 정렬 | O(n²) | O(n²) | O(1) | 불안정 | 교환 횟수 최소 |
> | 삽입 정렬 | O(n²) | O(n²) | O(1) | 안정 | 거의 정렬된 입력 O(n) |
> | 병합 정렬 | O(n log n) | O(n log n) | O(n) | 안정 | 분할정복, 추가 메모리 |
> | 퀵 정렬 | O(n log n) | **O(n²)** | O(log n) | 불안정 | 평균 최速, pivot 의존 |
> | 힙 정렬 | O(n log n) | O(n log n) | O(1) | 불안정 | 최악 보장, 제자리 |
> | **Timsort (파이썬)** | O(n log n) | O(n log n) | O(n) | **안정** | `sorted`/`sort` |
> | 계수 정렬 | O(n + k) | O(n + k) | O(n + k) | 안정 | 값 범위 k 작을 때 |
>
> **(B) 파이썬 정렬 연산**
>
> | 연산 | 시간복잡도 | 설명 |
> |---|---|---|
> | `sorted(a)` / `a.sort()` | O(n log n) | Timsort, 안정 |
> | `a.sort(key=f)` | O(n log n) + n번의 f 호출 | key는 원소당 1번만 계산(Decorate-Sort-Undecorate) |
> | 이미 정렬된 입력 | **O(n)** | Timsort가 run을 감지 |
> | `sorted(a)[:k]` (상위 k) | O(n log n) | 전부 정렬 |
> | `heapq.nsmallest(k, a)` | O(n log k) | k가 작으면 정렬보다 빠름 |

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"정렬 알고리즘을 직접 짜지 마라."** 코테에서 `nums.sort()` / `sorted(nums)`면 99% 충분하다. 채점관이 원하는 건 정렬 구현이 아니라 *어떤 key로 정렬할지*에 대한 통찰이다. (예외: "내장 정렬 금지" 명시 문제, [LeetCode #912 Sort an Array](https://leetcode.com/problems/sort-an-array/).)
> - **`key`는 "변환 함수"다.** `sorted(words, key=len)`은 길이순, `sorted(pts, key=lambda p: (p[0], -p[1]))`은 x오름·y내림 다중 정렬. key는 [Decorate-Sort-Undecorate](https://docs.python.org/3/howto/sorting.html) 방식이라 원소당 한 번만 호출돼 효율적이다.
> - **내림차순은 `reverse=True`** 또는 숫자라면 `key=lambda x: -x`. 문자열은 음수화가 안 되니 `reverse=True`나 [`functools.cmp_to_key`](https://docs.python.org/3/library/functools.html#functools.cmp_to_key)를 쓴다.
> - **"가장 큰 수" 류는 커스텀 비교가 핵심.** `"3"+"30"` vs `"30"+"3"`을 비교해 정렬 → [프로그래머스 가장 큰 수 #42746](https://school.programmers.co.kr/learn/courses/30/lessons/42746). `cmp_to_key`로 두 원소를 이어붙여 비교한다.
> - **안정 정렬을 활용한 다중 기준:** 1차 기준으로 정렬한 뒤 안정 정렬로 2차 기준을 또 돌리면, 같은 2차 값 안에서 1차 순서가 유지된다. 하지만 보통은 **튜플 key 한 방**(`key=lambda x: (k1, k2)`)이 더 간단하다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **비교 정렬의 하한은 O(n log n)이다(증명됨).** n개의 가능한 순열은 n!개이고, 비교 한 번이 결과를 둘로 가르므로 최소 log₂(n!) ≈ n log n번의 비교가 필요하다. 그래서 "비교만으로" O(n)은 불가능하다. 더 빠르려면 계수·기수 정렬처럼 값의 구조를 이용해야 한다.
> 2. **안정성(stability)을 반드시 이해하라.** 안정 정렬은 같은 key의 원소 순서를 보존한다. "점수 같으면 먼저 들어온 사람 우선" 같은 요구에서 결정적. 파이썬 `sorted`/`sort`는 **안정**이지만, C++ `std::sort`, 일반적 퀵 정렬은 **불안정**이다.
> 3. **`sort()`는 제자리 정렬, 반환값은 `None`.** `a = a.sort()`는 흔한 버그(`a`가 `None`이 됨). 원본을 유지하고 새 리스트가 필요하면 `b = sorted(a)`.
> 4. **퀵 정렬 최악 O(n²)을 기억하라.** 이미 정렬됐거나 같은 값이 많은 입력에 단순 pivot을 쓰면 O(n²)으로 터진다(stdin 기반 사이트에서 "정렬 후 TLE"의 흔한 원인). 파이썬 Timsort는 이 함정이 없다.
> 5. **`key` vs `cmp`:** 파이썬 3는 `cmp` 인자를 없앴다. 두 원소를 직접 비교해야 하면 `functools.cmp_to_key(비교함수)`로 감싼다. 비교 함수는 `a<b면 음수, 같으면 0, a>b면 양수`를 반환.
> 6. **정렬 후 인덱스가 바뀐다.** "원래 위치"가 필요하면 `enumerate`로 인덱스를 묶어 정렬하거나(`sorted(enumerate(a), key=lambda t: t[1])`), `sorted(range(n), key=lambda i: a[i])`로 정렬된 인덱스를 얻는다(argsort 패턴).
> 7. **부분 정렬이 더 쌀 때가 있다.** "상위 k개"만 필요하면 전체 O(n log n) 정렬 대신 [[day-12-heap/concept|힙]] `heapq.nsmallest/nlargest`로 O(n log k). k≪n이면 큰 이득.
> 8. **정렬은 다음 알고리즘의 토대다.** [[day-18-binary-search/concept|이분 탐색]]은 정렬을 전제하고, [[day-19-two-pointers/concept|투 포인터]]·구간 병합·그리디 다수가 "정렬부터" 시작한다. 정렬을 자유자재로 쓰면 Phase 2 후반이 쉬워진다.

> [!example]- 예제 코드 (Examples)
> ```python
> # 1) 기본 정렬: sorted(새 리스트) vs sort(제자리)
> a = [3, 1, 2]
> b = sorted(a)          # b=[1,2,3], a는 그대로
> a.sort()               # a 자체가 [1,2,3], 반환은 None
>
> # 2) key로 기준 바꾸기
> words = ["banana", "kiwi", "apple"]
> by_len = sorted(words, key=len)              # 길이순
> by_last = sorted(words, key=lambda w: w[-1]) # 끝글자순
>
> # 3) 다중 기준: x 오름차순, 같으면 y 내림차순
> pts = [(1, 2), (1, 5), (0, 9)]
> pts.sort(key=lambda p: (p[0], -p[1]))        # [(0,9),(1,5),(1,2)]
>
> # 4) 커스텀 비교: 이어붙여 큰 수 만들기 (cmp_to_key)
> from functools import cmp_to_key
> def cmp(x, y):
>     if x + y > y + x:    # 문자열 이어붙여 비교
>         return -1        # x가 앞
>     if x + y < y + x:
>         return 1
>     return 0
> nums = ["3", "30", "34", "5", "9"]
> largest = "".join(sorted(nums, key=cmp_to_key(cmp)))  # "9534330"
>
> # 5) 계수 정렬 (값 범위 0..k)
> def counting_sort(a, k):
>     count = [0] * (k + 1)
>     for x in a:
>         count[x] += 1
>     out = []
>     for v in range(k + 1):
>         out.extend([v] * count[v])
>     return out
>
> # 6) argsort: 정렬된 "원래 인덱스"
> a = [40, 10, 30]
> order = sorted(range(len(a)), key=lambda i: a[i])  # [1, 2, 0]
> ```
>
> 전체 실행 가능한 예제(병합 정렬 직접 구현 + 정렬 비교 출력 포함): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> "어떤 key로 정렬할지"를 설계하는 연습. 난이도와 출처를 표기했다.
>
> | 번호 | 문제 | 출처 | 난이도 | 핵심 |
> |---|---|---|---|---|
> | 1 | Sort an Array | [LeetCode #912](https://leetcode.com/problems/sort-an-array/) | 🟡중급 | 정렬 직접 구현(병합/힙) |
> | 2 | Sort Colors | [LeetCode #75](https://leetcode.com/problems/sort-colors/) | 🟡중급 | 계수 정렬·3-way 분할 |
> | 3 | Merge Sorted Array | [LeetCode #88](https://leetcode.com/problems/merge-sorted-array/) | 🟢기초 | 뒤에서부터 병합 |
> | 4 | Merge Intervals | [LeetCode #56](https://leetcode.com/problems/merge-intervals/) | 🟡중급 | 시작점 정렬 후 병합 |
> | 5 | Largest Number | [LeetCode #179](https://leetcode.com/problems/largest-number/) | 🟡중급 | 커스텀 비교 정렬 |
> | 6 | K번째수 | [프로그래머스 #42748](https://school.programmers.co.kr/learn/courses/30/lessons/42748) | 🟢기초 | 자르고 정렬 |
> | 7 | 가장 큰 수 | [프로그래머스 #42746](https://school.programmers.co.kr/learn/courses/30/lessons/42746) | 🟡중급 | cmp_to_key |
> | 8 | H-Index | [프로그래머스 #42747](https://school.programmers.co.kr/learn/courses/30/lessons/42747) | 🟡중급 | 정렬 후 조건 탐색 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 핵심 아이디어 + 여러 접근(내장 정렬 vs 직접 구현)과 복잡도 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — O(n log n)이 무엇인지 배웠다면, 오늘은 그 대표 사례인 정렬을 직접 본다
- ➡️ **다음(next):** [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — 정렬은 이분 탐색의 전제 조건. 정렬해 두면 O(log n) 탐색이 가능해진다
- 🧭 **관련(related):**
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — 비교 정렬의 하한 O(n log n)의 근거
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — "정렬된 배열"을 활용하는 첫 알고리즘
  - [[day-19-two-pointers/concept|Day 19 — 투 포인터]] — 정렬 후 양쪽에서 좁히는 패턴
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — 힙 정렬, 상위 k개 부분 정렬
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 병합 정렬·퀵 정렬의 뼈대
- 🗺️ **지도(MOC):** [[Phase-2 MOC]] · [[00 Algorithm MOC]]

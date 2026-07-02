---
day: 18
phase: 2-core-algorithms
title: 이분 탐색 (Binary Search)
category: [알고리즘, 탐색]
difficulty: 중급
status: done
prev: "[[day-17-sorting/concept|Day 17 — 정렬]]"
next: "[[day-19-two-pointers/concept|Day 19 — 투 포인터]]"
related:
  - "[[day-17-sorting/concept|Day 17 — 정렬]]"
  - "[[day-19-two-pointers/concept|Day 19 — 투 포인터]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
sources:
  - https://leetcode.com/problems/binary-search/
  - https://leetcode.com/problems/search-insert-position/
  - https://leetcode.com/problems/first-bad-version/
  - https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
  - https://leetcode.com/problems/search-in-rotated-sorted-array/
  - https://leetcode.com/problems/koko-eating-bananas/
  - https://school.programmers.co.kr/learn/courses/30/lessons/43238
  - https://school.programmers.co.kr/learn/courses/30/lessons/43236
  - https://docs.python.org/3/library/bisect.html
tags: [phase/2, topic/binary-search, topic/algorithm]
---

# Day 18 — 이분 탐색 (Binary Search)

> [!abstract] 한눈 요약 (TL;DR)
> **이분 탐색(binary search)은 "정렬된" 대상을 매번 절반씩 버려 가며 원하는 값을 O(log n)에 찾아내는 기법**이다. 100만 개(2²⁰)에서도 약 20번의 비교면 끝난다. 코테에서 두 가지 얼굴로 나온다. (1) **정렬된 배열에서 값/삽입 위치 찾기** — `bisect_left`/`bisect_right`로 거의 끝난다. (2) **"정답 자체"를 탐색하는 결정 문제형(parametric / answer binary search)** — "속도를 k로 하면 조건을 만족하는가?"처럼 답 후보 공간이 **단조(monotonic)** 하면, 값을 직접 이분 탐색한다(입국심사·징검다리·Koko). 실전 난이도의 핵심은 사실상 (2)에 있다. 이 노트는 `lo <= hi`(닫힌 구간)와 `lo < hi`(반열린 구간) 두 표준 틀, off-by-one과 무한 루프 함정, `bisect` 모듈 활용, 그리고 결정 문제형으로의 확장을 다룬다. 전제 조건인 [[day-17-sorting/concept|정렬]]을 먼저 이해하면 자연스럽게 이어진다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **이분 탐색**은 **정렬된(단조로운) 탐색 공간**에서, 중앙값을 확인해 답이 왼쪽 절반에 있는지 오른쪽 절반에 있는지 판단하고, **매번 후보를 절반으로 줄이는** 분할 탐색이다. n개를 절반씩 줄이면 1이 될 때까지 log₂n번이면 되므로 O(log n)이다.
>
> **일상 비유 — 사전에서 단어 찾기.** 국어사전에서 "이분법"을 찾을 때 첫 장부터 넘기지 않는다. 책을 가운데쯤 펴서 "ㅇ보다 앞이네" 하면 앞쪽 절반을, "뒤네" 하면 뒤쪽 절반을 다시 펴 본다. **숫자 맞히기 게임**(1~100 중 하나, up/down 힌트)도 똑같다. 50 → 25 → 37 … 매번 범위를 반으로 접기 때문에 최대 7번이면 맞힌다.
>
> **결정적 전제 — 단조성(monotonicity).** 이분 탐색이 성립하려면 탐색 공간이 **한 방향으로 정렬**돼 있어야 한다. 값 탐색이라면 배열이 정렬돼 있어야 하고, 결정 문제형이라면 판별식 `pred(x)`가 어떤 경계를 기준으로 `F, F, ..., F, T, T, ..., T`(또는 그 반대)처럼 **한 번만 바뀌어야** 한다. "이 값이면 가능한가?"라는 질문의 답이 x가 커질수록 계속 True(혹은 계속 False)로 유지될 때, 그 경계를 log 번에 찾는 것이 결정 문제형 이분 탐색이다.
>
> 그래서 문제를 만나면 스스로 물어야 한다: **"내가 답 후보를 하나 정했을 때, 그게 되는지/안 되는지를 빠르게 판별할 수 있고, 그 판별이 단조로운가?"** Yes면 이분 탐색이 보인다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 값 찾기 — 닫힌 구간 `[lo, hi]`, 조건 `lo <= hi`**
> ```
> 배열: [1, 3, 5, 7, 9, 11]   target = 9
>        lo=0 .......... hi=5   mid=2 -> a[2]=5 < 9  => lo=3
>              lo=3 .... hi=5   mid=4 -> a[4]=9 == 9 => 발견! index 4
> ```
> 규칙: `mid = (lo+hi)//2`. `a[mid] < target`이면 왼쪽은 버리고 `lo = mid+1`, `a[mid] > target`이면 `hi = mid-1`. 루프가 끝나면(lo > hi) 없는 것.
>
> **(B) 경계 찾기 — 반열린 구간 `[lo, hi)`, 조건 `lo < hi`**
> "target 이상이 처음 나오는 위치"(lower_bound) 같은 **경계**를 찾을 때 쓰는 틀. `hi = len(a)`로 시작(범위 밖을 가리킴), 조건을 만족하면 `hi = mid`(mid를 버리지 않음), 아니면 `lo = mid+1`. 끝나면 `lo == hi`가 곧 경계.
> ```
> [1, 2, 2, 2, 5, 7]  lower_bound(2):
>   조건 "a[mid] >= 2" 가 처음 참이 되는 자리를 좁힌다 -> index 1
>   upper_bound(2): "a[mid] > 2" 가 처음 참 -> index 4  (2의 개수 = 4-1 = 3)
> ```
>
> **(C) 결정 문제형(parametric) — "정답 x"를 이분 탐색**
> 값이 아니라 **답 자체의 범위** `[lo, hi]`를 잡고, 판별식 `pred(x)`의 경계를 찾는다.
> ```
> Koko 바나나: "속도 k면 h시간 안에 다 먹나?" pred(k) = (필요시간 <= h)
>   k가 커질수록 필요시간은 줄어 pred는 F..F,T..T (단조)
>   -> pred가 처음 True가 되는 가장 작은 k 를 이분 탐색
> 징검다리: "최소 간격을 x 이상으로? 제거 바위 <= n?" -> pred 참인 가장 큰 x
> ```
> 뼈대는 (B)와 동일하다. **탐색 대상이 "배열의 인덱스"에서 "답의 값"으로 바뀌었을 뿐이다.**

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> | 연산 | 시간복잡도 | 설명 |
> |---|---|---|
> | 이분 탐색(값 찾기) | O(log n) | 매 단계 후보 절반 |
> | `bisect_left/right` | O(log n) | 위치 탐색(리스트) |
> | `bisect.insort` | O(n) | 탐색 O(log n) + **이동 O(n)** |
> | 결정 문제형 | O(f · log R) | R=답 범위 폭, f=판별식 pred 비용 |
> | 정렬 후 이분 탐색 | O(n log n + q log n) | 정렬 1회 + q번 질의 |
> | 공간 | O(1) | 반복 구현 시. 재귀는 O(log n) 스택 |
>
> - **왜 O(log n)?** n → n/2 → n/4 → … → 1 이 되기까지의 횟수가 log₂n. n=10억이라도 약 30번.
> - **한 번만 찾으면 정렬 비용이 아깝다.** 단발 질의는 O(n) 선형 탐색이 오히려 낫다. 이분 탐색은 **정렬을 이미 해뒀거나(전처리), 같은 배열에 질의가 여러 번**일 때 이득이다.
> - **결정 문제형**은 답 범위 R이 10¹⁸이어도 log₂R ≈ 60. 판별식 pred가 O(n)이면 전체 O(n log R).

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **직접 짜기 전에 [`bisect`](https://docs.python.org/3/library/bisect.html)부터.** 단순 값/삽입 위치는 `bisect_left`(== lower_bound)·`bisect_right`(== upper_bound)로 끝난다. "값 존재?"는 `i = bisect_left(a, x); i < len(a) and a[i] == x`.
> - **개수 세기 관용구:** 정렬 배열에서 `x`의 개수 = `bisect_right(a, x) - bisect_left(a, x)`. `x` 미만 개수 = `bisect_left(a, x)`.
> - **`mid = (lo + hi) // 2`는 파이썬에선 오버플로가 없다.** C/Java에선 `lo + (hi - lo) // 2`로 써야 하지만([유명한 20년 묵은 JDK 버그](https://ai.googleblog.com/2006/06/extra-extra-read-all-about-it-nearly.html)), 파이썬 정수는 무제한이라 안전하다. 그래도 습관으로 알아두면 좋다.
> - **"두 틀 중 하나만 골라 익혀라."** `lo <= hi`(닫힌 구간, 정확한 값 찾기)와 `lo < hi`(반열린 구간, 경계 찾기)를 섞으면 off-by-one·무한 루프가 난다. 각 틀의 초기값(hi = len-1 vs len)과 갱신(hi = mid-1 vs hi = mid)을 세트로 외운다.
> - **결정 문제형 신호어:** "최소의 최대", "최대의 최소", "가능한 가장 작은/큰 값", "~ 이내에 되도록", "몇 개까지". 이 표현이 보이면 답을 이분 탐색해 보라.
> - **실수(float) 이분 탐색은 `while hi-lo > eps` 대신 고정 반복(100회)** 이 정밀도 함정을 피하기 쉽다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **무한 루프 함정.** 반열린 틀(`lo < hi`)에서 조건 미충족 시 `lo = mid`로 쓰면(‑1 없이) `lo`가 안 움직여 무한 루프. 반드시 한쪽은 `mid + 1` 또는 `mid - 1`로 **범위를 실제로 줄여야** 한다.
> 2. **off-by-one은 "경계 정의"에서 갈린다.** 닫힌 구간 `[lo, hi]`면 `hi = len-1`·조건 `lo <= hi`·갱신 `hi = mid-1`. 반열린 `[lo, hi)`면 `hi = len`·조건 `lo < hi`·갱신 `hi = mid`. 이 3종 세트를 절대 섞지 마라.
> 3. **정렬돼 있지 않으면 이분 탐색은 틀린다.** 이분 탐색의 대전제는 단조성이다. 값 탐색이면 먼저 [[day-17-sorting/concept|정렬]]해야 하고(정렬 O(n log n)이 붙는다), 결정 문제형이면 `pred`가 진짜 단조인지 반드시 검증하라.
> 4. **`lower_bound`와 `upper_bound`를 구분하라.** `bisect_left`는 "같은 값이 있으면 그 앞", `bisect_right`는 "그 뒤"를 반환한다. 삽입 위치·구간 개수·`[first, last]`(LeetCode #34)가 전부 이 둘의 조합이다.
> 5. **`bisect.insort`는 O(n).** 이분 탐색으로 위치는 O(log n)에 찾지만 리스트 삽입은 뒤 원소를 밀어야 해 O(n). "정렬 유지하며 대량 삽입"이 필요하면 리스트 insort 반복(O(n²))보다 [[day-17-sorting/concept|한꺼번에 정렬]]이 낫다.
> 6. **답 범위(lo, hi) 설정 실수.** 결정 문제형에서 hi를 너무 작게 잡으면 정답을 놓친다. 입국심사의 hi는 `min(times) * n`(가장 빠른 심사관 혼자 n명), Koko의 hi는 `max(piles)`. **"가장 극단적으로 안전한 값"** 을 hi로 잡아라.
> 7. **회전 정렬 배열(#33)은 "한 쪽은 항상 정렬"** 을 이용한다. `a[lo] <= a[mid]`면 왼쪽 절반이 정렬 → target이 그 범위면 왼쪽, 아니면 오른쪽. 회전·중복이 섞이면 최악 O(n)로 퇴화할 수 있다.
> 8. **재귀 vs 반복.** 이분 탐색은 [[day-22-recursion/concept|분할정복]]의 사촌이지만, 꼬리 재귀라 반복문으로 쓰는 게 스택 O(1)이고 파이썬 재귀 한도(기본 1000)에서도 안전하다.

> [!example]- 예제 코드 (Examples)
> ```python
> # 1) 값 찾기 (닫힌 구간 [lo, hi])
> def binary_search(a, target):
>     lo, hi = 0, len(a) - 1
>     while lo <= hi:
>         mid = (lo + hi) // 2
>         if a[mid] == target:
>             return mid
>         if a[mid] < target:
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return -1
>
> # 2) 경계 찾기 (반열린 구간 [lo, hi)) = lower_bound
> def lower_bound(a, target):
>     lo, hi = 0, len(a)
>     while lo < hi:
>         mid = (lo + hi) // 2
>         if a[mid] < target:
>             lo = mid + 1
>         else:
>             hi = mid          # mid를 버리지 않음
>     return lo
>
> # 3) 표준 라이브러리 bisect
> import bisect
> a = [1, 2, 2, 2, 5, 7]
> bisect.bisect_left(a, 2)      # 1  (== lower_bound)
> bisect.bisect_right(a, 2)     # 4  (== upper_bound)
> cnt = bisect.bisect_right(a, 2) - bisect.bisect_left(a, 2)   # 2의 개수 = 3
>
> # 4) 결정 문제형: 조건 pred가 단조일 때 "가장 작은 참"
> def smallest_true(lo, hi, pred):
>     while lo < hi:
>         mid = (lo + hi) // 2
>         if pred(mid):
>             hi = mid
>         else:
>             lo = mid + 1
>     return lo
> # 예) x*x >= 26 인 가장 작은 x -> smallest_true(0, 26, lambda x: x*x >= 26) == 6
> ```
>
> 전체 실행 가능한 예제(lower/upper bound 구현, bisect, 정수/실수 제곱근 결정 탐색): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 앞의 4문제는 **값/경계 탐색**, 뒤의 4문제는 **결정 문제형(parametric)**. 결정 문제형이 실전의 핵심이다.
>
> | 번호 | 문제 | 출처 | 난이도 | 핵심 |
> |---|---|---|---|---|
> | 1 | Binary Search | [LeetCode #704](https://leetcode.com/problems/binary-search/) | 🟢기초 | 표준 이분 탐색 |
> | 2 | Search Insert Position | [LeetCode #35](https://leetcode.com/problems/search-insert-position/) | 🟢기초 | lower_bound |
> | 3 | First Bad Version | [LeetCode #278](https://leetcode.com/problems/first-bad-version/) | 🟢기초 | F..F,T..T 경계 |
> | 4 | Find First and Last Position | [LeetCode #34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | 🟡중급 | bisect_left/right |
> | 5 | Search in Rotated Sorted Array | [LeetCode #33](https://leetcode.com/problems/search-in-rotated-sorted-array/) | 🟡중급 | 회전 배열, 한쪽 정렬 |
> | 6 | Koko Eating Bananas | [LeetCode #875](https://leetcode.com/problems/koko-eating-bananas/) | 🟡중급 | 결정 문제형(속도) |
> | 7 | 입국심사 | [프로그래머스 #43238](https://school.programmers.co.kr/learn/courses/30/lessons/43238) | 🟡중급 | 결정 문제형(시간) |
> | 8 | 징검다리 | [프로그래머스 #43236](https://school.programmers.co.kr/learn/courses/30/lessons/43236) | 🔴심화 | 최소 간격 최대화 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 핵심 아이디어 + 여러 접근(직접 구현 vs `bisect`)과 복잡도 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-17-sorting/concept|Day 17 — 정렬]] — 이분 탐색의 대전제인 "정렬"을 배웠다. 정렬해 두면 O(log n) 탐색이 가능해진다
- ➡️ **다음(next):** [[day-19-two-pointers/concept|Day 19 — 투 포인터]] — 정렬된 배열을 훑는 또 다른 축. 이분 탐색이 "반씩 접기"라면 투 포인터는 "양쪽에서 좁히기"
- 🧭 **관련(related):**
  - [[day-17-sorting/concept|Day 17 — 정렬]] — 값 탐색형 이분 탐색의 필수 전처리
  - [[day-19-two-pointers/concept|Day 19 — 투 포인터]] — 정렬 배열을 O(n)에 훑는 사촌 기법
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — O(log n)이 왜 강력한지의 근거
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 이분 탐색은 분할정복의 가장 단순한 형태
- 🗺️ **지도(MOC):** [[Phase-2 MOC]] · [[00 Algorithm MOC]]

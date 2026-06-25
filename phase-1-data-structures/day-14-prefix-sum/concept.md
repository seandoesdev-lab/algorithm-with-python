---
day: 14
phase: 1-data-structures
title: 누적 합 (Prefix Sum)
category: [자료구조, 누적합]
difficulty: 중급
status: done
prev: "[[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]]"
next: "[[day-15-review/concept|Day 15 — 자료구조 종합 복습]]"
related:
  - "[[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]]"
  - "[[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]]"
  - "[[day-19-two-pointers/concept|Day 19 — 투 포인터]]"
  - "[[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
sources:
  - https://leetcode.com/problems/range-sum-query-immutable/
  - https://leetcode.com/problems/range-sum-query-2d-immutable/
  - https://leetcode.com/problems/find-pivot-index/
  - https://leetcode.com/problems/subarray-sum-equals-k/
  - https://leetcode.com/problems/running-sum-of-1d-array/
  - https://leetcode.com/problems/product-of-array-except-self/
  - https://leetcode.com/problems/count-number-of-nice-subarrays/
  - https://school.programmers.co.kr/learn/courses/30/lessons/134239
  - https://docs.python.org/3/library/itertools.html#itertools.accumulate
tags: [phase/1, topic/prefix-sum]
---

# Day 14 — 누적 합 (Prefix Sum)

> [!abstract] 한눈 요약 (TL;DR)
> **누적 합(prefix sum, 부분합)**은 배열의 "앞에서부터 더한 값"을 미리 한 번 계산해 두고, 임의 구간의 합을 **단 한 번의 뺄셈 O(1)**로 답하는 전처리 기법이다. 핵심 공식 단 하나 — 구간 `[i, j]`의 합 = `P[j+1] - P[i]`. 매 질의마다 구간을 다시 더하면 질의 1개당 O(n)이지만, 누적합 배열 `P`를 한 번(O(n)) 만들어 두면 질의는 전부 O(1)이 된다. "전처리 O(n) + 질의 O(1)"이라는 **시간·공간 거래(trade-off)**의 가장 단순하고 강력한 예다. [[day-13-hashmap-patterns/concept|Day 13]]의 "누적합+해시맵" 패턴, 2차원 구간 합, 차분 배열(difference array), 곱 버전(prefix product)까지 모두 이 한 공식의 변주다. 코테에서 "구간 합/평균/개수"가 보이고 질의가 여러 번이면 **반사적으로 누적합을 의심하라.**

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **누적 합 배열** `P`는 "원본 배열 `A`의 처음부터 각 위치까지의 합"을 저장한 배열이다. 가장 다루기 쉬운 정의는 **길이 `n+1`짜리, 맨 앞에 0을 둔(1-indexed) 형태**다.
>
> $$P[0] = 0, \quad P[k] = A[0] + A[1] + \cdots + A[k-1]$$
>
> 그러면 원본의 구간 `A[i..j]`(양끝 포함)의 합은 다음 한 줄로 끝난다.
>
> $$\text{sum}(i, j) = P[j+1] - P[i]$$
>
> **일상 비유 — 도로의 누적 거리 표지판.** 고속도로에는 "서울 기점 0 km, 100 km, 230 km …"처럼 *시작점부터의 누적 거리*가 적혀 있다. 대전(160 km)에서 대구(290 km)까지의 거리를 알고 싶을 때 그 사이를 다시 재지 않는다. `290 - 160 = 130 km`, **뺄셈 한 번**이면 된다. 누적합이 정확히 이 표지판이다. 매번 구간을 다시 더하는 것은 매번 자로 도로를 재는 것과 같다.
>
> 핵심 통찰: **"구간의 합"이라는 질문을 "두 누적값의 차이"라는 질문으로 바꾼다.** 더하기(반복)를 빼기(상수)로 환원하는 것이 누적합의 본질이다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(1) 누적합 배열 만들기 (1-indexed, 권장)**
> `P[0]=0`에서 시작해 한 칸씩 앞 값에 원소를 더한다.
> ```
> A      = [ 3,  1,  4,  1,  5 ]      (인덱스 0..4)
> P      = [0, 3, 4, 8, 9, 14]        (인덱스 0..5, 길이 n+1)
>            ^P[0]=0
>          P[k] = P[k-1] + A[k-1]
> ```
> 구간 `A[1..3]`(=1,4,1, 합 6)을 구하면: `P[4] - P[1] = 9 - 3 = 6`. 맞다.
>
> **왜 맨 앞에 0(P[0])을 두는가?** `i=0`(배열 맨 앞부터)인 구간을 특수 처리 없이 `P[j+1]-P[0]=P[j+1]`로 일관되게 다루기 위해서다. 0을 빼먹으면 "처음부터의 구간"에서 off-by-one 버그가 난다.
>
> **(2) 질의 처리** — 만들어 둔 `P`로 어떤 구간이 와도 뺄셈 한 번.
> ```
> 질의 (i=2, j=4) -> P[5] - P[2] = 14 - 4 = 10   (4+1+5)
> 질의 (i=0, j=2) -> P[3] - P[0] =  8 - 0 = 8     (3+1+4)
> ```
>
> **(3) 2차원 누적합 (2D prefix sum) — 포함·배제(inclusion-exclusion)**
> 행렬에서 좌상단 `(0,0)`부터 `(r,c)`까지의 합 `P[r+1][c+1]`을 미리 만든다. 직사각형 `(r1,c1)~(r2,c2)`의 합은 큰 사각형에서 위·왼쪽을 빼고 두 번 빠진 좌상단을 다시 더한다.
> ```
> 합 = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]
>        (전체)        (위 제거)      (왼쪽 제거)   (이중 차감 복원)
> ```
>
> **(4) 차분 배열 (difference array) — 누적합의 "역연산"**
> "구간 `[i,j]`에 +v" 같은 **구간 갱신**이 여러 번 들어오면, 차분 배열 `D`에 `D[i]+=v, D[j+1]-=v`만 기록(각 O(1))하고, 마지막에 `D`의 누적합을 한 번 취하면 최종 배열이 나온다. 구간 갱신 O(1) + 복원 O(n).

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> 누적합의 정체성은 **"전처리에 한 번 투자하고, 질의를 공짜로 만든다"**이다.
>
> | 연산 | 시간복잡도 | 설명 |
> |---|---|---|
> | 누적합 배열 구축 | O(n) | 한 번 순회하며 앞 값에 누적 |
> | 단일 구간 합 질의 | **O(1)** | 뺄셈 한 번 `P[j+1]-P[i]` |
> | 질의 q회 (누적합) | O(n + q) | 구축 O(n) + 질의당 O(1) |
> | 질의 q회 (순진한 재계산) | O(n·q) | 매 질의마다 구간 재합산 |
> | 2D 구축 / 직사각형 질의 | O(R·C) / **O(1)** | 포함·배제 4개 항 |
> | 차분 배열: 구간 갱신 1회 | **O(1)** | 양끝 2칸만 수정 |
> | 차분 배열: 최종 복원 | O(n) | 누적합 1회 |
> | 공간(누적합 배열) | O(n) | 원본과 별도 배열 |
>
> > **핵심 직관:** 질의가 **1번뿐**이면 누적합을 만드는 O(n)이 곧 답을 구하는 비용과 같아 이득이 없다. 누적합은 **"여러 번 질의"** 또는 **"모든 구간을 훑어야 하는"** 상황에서 O(n·q)/O(n²)를 O(n)/O(n+q)로 무너뜨릴 때 빛난다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **`P[0]=0` (길이 n+1) 형태를 표준으로 삼아라.** 1-indexed 누적합은 `sum(i,j)=P[j+1]-P[i]`로 경계 케이스가 사라진다. `P[i]=P[i-1]+A[i-1]`. off-by-one 버그의 90%가 0을 안 둬서 생긴다.
>   - 참고: [Range Sum Query - Immutable (LeetCode #303)](https://leetcode.com/problems/range-sum-query-immutable/)
>
> - **파이썬은 `itertools.accumulate`로 한 줄.** `list(accumulate(A))`는 0 없는 누적합, `list(accumulate(A, initial=0))`(3.8+)은 앞에 0이 붙은 표준형이다. `accumulate(A, func)`로 누적 곱·누적 max도 된다.
>   - 참고: [itertools.accumulate (Python 공식 문서)](https://docs.python.org/3/library/itertools.html#itertools.accumulate)
>
> - **"합이 K인 연속 구간 개수"는 누적합 + 해시맵.** 모든 구간을 보면 O(n²)지만, 현재 누적합에서 K를 뺀 값을 과거에 몇 번 봤는지 해시로 세면 O(n). [[day-13-hashmap-patterns/concept|Day 13]]의 핵심 패턴과 그대로 만난다.
>   - 참고: [Subarray Sum Equals K (LeetCode #560)](https://leetcode.com/problems/subarray-sum-equals-k/)
>
> - **음수가 섞인 "구간 합" 문제는 슬라이딩 윈도우가 아니라 누적합이다.** 음수가 있으면 윈도우의 단조성이 깨진다([[day-20-sliding-window/concept|Day 20]]). 누적합+해시맵이 정공법.
>
> - **곱 버전(prefix product)도 같은 발상.** "자기 자신 제외 곱"(#238)은 왼쪽 누적 곱 × 오른쪽 누적 곱. 단, 0이 섞이면 나눗셈으로 풀면 안 되고 좌우 누적으로 풀어야 한다.
>   - 참고: [Product of Array Except Self (LeetCode #238)](https://leetcode.com/problems/product-of-array-except-self/)

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **off-by-one은 누적합의 1순위 버그.** `sum(i,j)`가 양끝 포함인지(`P[j+1]-P[i]`) 반열림인지(`P[j]-P[i]`) 명확히 정하라. `P[0]=0`(길이 n+1) 형태로 통일하면 양끝 포함이 자연스럽다.
>
> 2. **누적합은 "값이 안 바뀔 때(immutable)" 유리하다.** 원소 하나가 자주 갱신되면 누적합 전체를 다시 만들어야 해 갱신이 O(n)이 된다. *갱신 + 구간 합이 둘 다 잦으면* 펜윅 트리(Fenwick/BIT)나 세그먼트 트리(O(log n))로 가야 한다(Phase 4).
>
> 3. **오버플로는 파이썬에선 걱정 없지만, 다른 언어에선 치명적.** 파이썬 `int`는 임의 정밀도라 누적합이 아무리 커져도 안전하다. C++/Java라면 `long long`/`long`을 써야 누적합 오버플로를 피한다(면접 단골).
>
> 4. **부동소수점 누적은 오차가 쌓인다.** 실수 배열의 누적합은 더할수록 반올림 오차가 누적된다. 정밀도가 중요하면 `math.fsum`이나 정수화(스케일링)를 고려한다.
>
> 5. **"평균이 가장 큰/작은 구간", "구간 합이 임계값 이상" 류는 거의 누적합 신호.** 구간 통계를 묻고 질의가 많으면 누적합부터 떠올린다.
>
> 6. **차분 배열은 "여러 구간 갱신 후 한 번 조회"의 정석.** 비행기 좌석 예약(#1109), 버스 정류장 승객 수처럼 "구간마다 +v"가 쌓이는 문제는 매번 구간을 갱신(O(n))하지 말고 차분 배열에 양끝만 찍은 뒤(O(1)) 마지막에 누적합 1회.
>
> 7. **2D 누적합의 부호를 외워라.** 직사각형 합 = `전체 - 위 - 왼쪽 + 좌상단`. 좌상단을 다시 더하는 이유는 위·왼쪽에서 *두 번 빠졌기* 때문(포함·배제 원리).
>
> 8. **누적합 배열을 in-place로 덮어쓸지 별도 배열로 둘지 결정하라.** 원본이 나중에 필요하면 별도 배열(O(n) 공간). 메모리가 빠듯하면 원본을 누적합으로 덮어쓸 수 있지만 가독성·재사용성이 떨어진다.

> [!example]- 예제 코드 (Examples)
> ```python
> from itertools import accumulate
>
> # 1) 표준 누적합 배열 (1-indexed, 맨 앞 0): 구간 합 O(1)
> def build_prefix(A):
>     P = [0] * (len(A) + 1)
>     for i, x in enumerate(A):
>         P[i + 1] = P[i] + x         # P[k] = P[k-1] + A[k-1]
>     return P
>
> def range_sum(P, i, j):             # A[i..j] 양끝 포함
>     return P[j + 1] - P[i]
>
> # 파이썬다운 한 줄 버전 (3.8+): accumulate(initial=0)
> def build_prefix_pythonic(A):
>     return list(accumulate(A, initial=0))   # 길이 n+1, P[0]=0
>
> # 2) 합이 K 인 연속 구간 "개수": 누적합 + 해시맵 O(n)
> def subarray_sum_count(nums, K):
>     from collections import defaultdict
>     seen = defaultdict(int)
>     seen[0] = 1                     # 빈 접두부(합 0) 1번 본 것으로
>     prefix = count = 0
>     for x in nums:
>         prefix += x
>         count += seen[prefix - K]   # 과거 누적합 중 prefix-K 가 몇 번?
>         seen[prefix] += 1
>     return count
>
> # 3) 자기 자신 제외 곱 (prefix product): 나눗셈 없이 O(n)
> def product_except_self(nums):
>     n = len(nums)
>     res = [1] * n
>     left = 1
>     for i in range(n):              # 왼쪽 누적 곱
>         res[i] = left
>         left *= nums[i]
>     right = 1
>     for i in range(n - 1, -1, -1):  # 오른쪽 누적 곱을 곱해 합성
>         res[i] *= right
>         right *= nums[i]
>     return res
>
> # 4) 차분 배열(difference array): 구간 갱신 O(1), 복원 O(n)
> def apply_range_updates(n, updates):    # updates: (l, r, v) 양끝 포함
>     D = [0] * (n + 1)
>     for l, r, v in updates:
>         D[l] += v
>         D[r + 1] -= v
>     out = list(accumulate(D))[:n]       # 누적합으로 최종 배열 복원
>     return out
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> | 번호 | 문제 | 출처 | 난이도 | 카테고리 |
> |---|---|---|---|---|
> | 1 | Running Sum of 1d Array | [LeetCode #1480](https://leetcode.com/problems/running-sum-of-1d-array/) | 🟢기초 | 누적합 기본 |
> | 2 | Range Sum Query - Immutable | [LeetCode #303](https://leetcode.com/problems/range-sum-query-immutable/) | 🟢기초 | 1D 구간 합 |
> | 3 | Find Pivot Index | [LeetCode #724](https://leetcode.com/problems/find-pivot-index/) | 🟢기초 | 좌우 누적합 |
> | 4 | Subarray Sum Equals K | [LeetCode #560](https://leetcode.com/problems/subarray-sum-equals-k/) | 🟡중급 | 누적합+해시맵 |
> | 5 | Product of Array Except Self | [LeetCode #238](https://leetcode.com/problems/product-of-array-except-self/) | 🟡중급 | 누적 곱 |
> | 6 | Count Number of Nice Subarrays | [LeetCode #1248](https://leetcode.com/problems/count-number-of-nice-subarrays/) | 🟡중급 | 누적합+해시맵 |
> | 7 | Range Sum Query 2D - Immutable | [LeetCode #304](https://leetcode.com/problems/range-sum-query-2d-immutable/) | 🟡중급 | 2D 누적합 |
> | 8 | 우박수열 정적분 | [프로그래머스 #134239](https://school.programmers.co.kr/learn/courses/30/lessons/134239) | 🟡중급 | 누적합 응용 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]] — "누적합+해시맵" 패턴에서 누적합 부분을 오늘 정면으로 다룬다
- ➡️ **다음(next):** [[day-15-review/concept|Day 15 — 자료구조 종합 복습]] — Phase 1 전체(배열·스택·큐·해시·트리·힙·누적합)를 묶어 복습
- 🧭 **관련(related):**
  - [[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]] — 합이 K인 구간 개수는 누적합과 해시맵의 결합으로 O(n)
  - [[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]] — 누적합은 배열 위에서 동작하는 전처리 기법
  - [[day-19-two-pointers/concept|Day 19 — 투 포인터]] — 양수 구간 합은 투 포인터로, 음수 포함은 누적합으로 갈린다
  - [[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]] — 고정/가변 윈도우 합 계산의 토대
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — "전처리 O(n) + 질의 O(1)" 거래를 복잡도로 분석
- 🗺️ **지도(MOC):** [[Phase-1 MOC]] · [[00 Algorithm MOC]]

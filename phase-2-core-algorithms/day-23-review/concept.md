---
day: 23
phase: 2-core-algorithms
title: 알고리즘 기초 복습 (Core Algorithms Review)
category: [알고리즘, 복습]
difficulty: 중급
status: done
prev: "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
next: "[[day-24-brute-force/concept|Day 24 — 완전 탐색]]"
related:
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-17-sorting/concept|Day 17 — 정렬]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-19-two-pointers/concept|Day 19 — 투 포인터]]"
  - "[[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]]"
  - "[[day-21-greedy/concept|Day 21 — 그리디]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-24-brute-force/concept|Day 24 — 완전 탐색]]"
sources:
  - https://leetcode.com/problems/binary-search/
  - https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
  - https://leetcode.com/problems/longest-substring-without-repeating-characters/
  - https://leetcode.com/problems/container-with-most-water/
  - https://leetcode.com/problems/merge-intervals/
  - https://leetcode.com/problems/jump-game/
  - https://leetcode.com/problems/koko-eating-bananas/
  - https://leetcode.com/problems/sort-list/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42862
  - https://school.programmers.co.kr/learn/courses/30/lessons/42885
  - https://docs.python.org/3/library/bisect.html
  - https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)
tags: [phase/2, topic/review, topic/algorithm]
---

# Day 23 — 알고리즘 기초 복습 (Core Algorithms Review)

> [!abstract] 한눈 요약 (TL;DR)
> Phase 2에서 배운 7개 무기(복잡도·정렬·이분 탐색·투 포인터·슬라이딩 윈도우·그리디·재귀/분할정복)를 **하나의 "언제 무엇을 꺼낼까" 의사결정표로 묶는 날**이다. Phase 1이 *자료구조 고르기*였다면, Phase 2는 *알고리즘 기법(technique) 고르기*다. 실전에서 점수를 가르는 건 문제 문장의 신호(signal)를 보고 → 알맞은 기법으로 1초 만에 매핑하는 반사신경이다. 예: "정렬돼 있고 값을 찾는다"=이분 탐색, "정렬된 배열에서 두 값의 합/짝"=투 포인터, "연속 구간의 최대/최소"=슬라이딩 윈도우, "매 순간 최선을 골라도 되나?"=그리디, "반으로 나눠 풀고 합친다"=분할정복, "…할 수 있는 최소/최대 K는?"=**정답에 대한 이분 탐색(parametric search)**. 이 노트는 각 기법의 **핵심 한 줄 정체성 + 복잡도 치트시트 + 선택 신호 + 단골 함정**을 한 화면에 정리하고, 10개의 혼합 문제로 "어떤 기법을 꺼낼지" 판단을 훈련한다. Phase 3(탐색·그래프)의 완전 탐색·DFS·BFS로 넘어가기 전, **알고리즘 선택 근육**을 굳히는 마지막 정거장이다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **복습(review)의 본질은 "암기"가 아니라 "검색 인덱스 만들기"다.** 기법을 따로따로 외우면 문제 앞에서 "음... 뭘 쓰지?" 하고 멈춘다. 잘 복습한 사람은 머릿속에 *(문제의 신호 → 기법)* 사전이 있어서, 문장을 읽는 동시에 후보가 떠오른다.
>
> **일상 비유 — 요리사의 칼(knife skills).** 채썰기·다지기·저미기를 각각 할 줄 아는 것과, *재료를 보고 0.5초 만에 알맞은 칼질을 고르는 것*은 다르다. 숙련 요리사는 기법의 방법이 아니라 **"이 재료엔 이 칼질"이라는 매핑**이 몸에 배어 있다. Phase 2의 7개 기법이 칼질이고, 오늘은 칼을 가는 게 아니라 *어떤 재료에 어떤 칼질인지*를 정리하는 날이다.
>
> 각 기법의 **한 줄 정체성**:
> - **시간복잡도/Big-O (Complexity)** — 모든 선택의 심판. "이 방법이 입력 한계 안에서 도느냐"를 수로 판정한다.
> - **정렬 (Sorting)** — "먼저 순서를 만들면" 이분 탐색·투 포인터·그리디가 열린다. 대부분 기법의 **전처리 관문**.
> - **이분 탐색 (Binary Search)** — 정렬(단조성)된 공간을 매번 절반으로 줄여 O(log n). 값 찾기뿐 아니라 **"정답 자체"를 탐색**한다.
> - **투 포인터 (Two Pointers)** — 정렬된 배열/문자열의 양 끝(또는 같은 방향) 두 지표로 O(n²)를 O(n)으로.
> - **슬라이딩 윈도우 (Sliding Window)** — "연속 구간"의 답을 창을 밀며 갱신. 투 포인터의 특수형.
> - **그리디 (Greedy)** — 매 순간 국소 최적을 골라 전체 최적에 도달(정당성이 성립할 때만).
> - **재귀·분할정복 (Recursion & D&C)** — 문제를 같은 모양의 작은 문제로. 반으로 나눠 풀고 합쳐 O(n log n).

> [!gear]- 2. 동작 원리 (How It Works) — 알고리즘 기법 선택 의사결정
> 문제를 읽을 때 아래 신호들을 *체크리스트*처럼 훑는다. 신호가 잡히면 그 기법부터 의심한다.
> ```
> 문제 문장에서 이런 신호가 보이면...              ->  먼저 떠올릴 기법
> ----------------------------------------------------------------------
> "정렬돼 있다", "오름차순/내림차순 배열"           ->  이분 탐색 또는 투 포인터
> "특정 값의 위치/존재를 빠르게"                    ->  이분 탐색 (bisect)
> "...할 수 있는 최소/최대 K는?", "가능한가 판정"   ->  정답에 대한 이분 탐색(parametric)
> "정렬된 두 수의 합/짝", "양 끝에서 좁혀"           ->  투 포인터
> "연속된 부분 배열/부분 문자열의 최대·최소·개수"    ->  슬라이딩 윈도우
> "길이가 정해진 구간을 훑는다"                     ->  고정 크기 슬라이딩 윈도우
> "조건을 만족하는 가장 짧은/긴 구간"               ->  가변 크기 슬라이딩 윈도우
> "매 순간 가장 좋아 보이는 걸 고른다", "회의실/구간" ->  그리디(+정렬)
> "가장 적은/많은 횟수로", "동전/보트/강의실 배정"   ->  그리디 후보 -> 반례 검토
> "반으로 나눠 각각 풀고 합친다", "병합/정렬"        ->  분할정복
> "같은 모양의 더 작은 문제로 정의된다"             ->  재귀
> "이 방법이 시간 안에 도는가?"                     ->  Big-O로 먼저 계산
> ```
>
> **두 개 이상이 결합되는 경우가 실전이다.** Phase 2의 진짜 교훈은 기법이 *섞인다*는 것:
> - 구간 문제 그리디 = **정렬** + 앞에서부터 **그리디** 선택(Merge Intervals, 구명보트).
> - "최소 K 찾기" = **정답 이분 탐색** + 각 K의 **판정 함수**(Koko).
> - 정렬된 배열 두 값 = **투 포인터**(Two Sum II) 또는 각 원소마다 **이분 탐색**.
> - 병합 정렬 = **분할정복** + **투 포인터 병합**.
> - 무엇을 쓰든 최종 판정은 **Big-O**: "이 기법의 복잡도가 입력 한계 안인가?"
>
> **선택의 한 줄 기준:** "무엇이 이미 정렬/단조인가? 답을 어떻게 좁힐 수 있는가?"를 물어라. *정렬+값찾기면 이분 탐색, 정렬+짝찾기면 투 포인터, 연속 구간이면 슬라이딩 윈도우, 국소 최적이 전체 최적이면 그리디, 반으로 쪼개지면 분할정복.*

> [!chart]- 3. 복잡도 (Time / Space Complexity) — Phase 2 마스터 치트시트
> 면접·코테 직전 5분 컷으로 훑는 표. (n = 입력 크기)
>
> | 기법 | 대표 시간복잡도 | 추가 공간 | 전제 조건 | 대표 도구 |
> |---|---|---|---|---|
> | 선형 탐색 | O(n) | O(1) | 없음 | `for` |
> | 정렬 | O(n log n) | O(n) Timsort | 비교 가능 | `sorted` `list.sort` |
> | 이분 탐색(값) | O(log n) | O(1) | **정렬됨** | `bisect` |
> | 정답 이분 탐색 | O(n log(범위)) | O(1) | 답에 **단조성** | 직접 구현 |
> | 투 포인터 | O(n) | O(1) | 대개 **정렬됨** | 인덱스 2개 |
> | 슬라이딩 윈도우 | O(n) | O(k) 창 상태 | 연속 구간 | `deque`/`dict` |
> | 그리디 | O(n log n) (정렬 포함) | O(1) | **교환 논증** 성립 | 정렬 + 1회 순회 |
> | 분할정복(병합형) | O(n log n) | O(n) + O(log n) 스택 | 균등 분할 | 재귀 |
> | 나이브 완전탐색 | O(2^n)·O(n!) | 상태 | 없음(느림) | 재귀/백트래킹 |
>
> > **핵심 직관 — "정렬 O(n log n)이 문을 연다".** 정렬 자체는 O(n log n)이지만, 그 뒤에 이분 탐색(O(log n))·투 포인터(O(n))·그리디(O(n))가 붙는다. 즉 대부분의 "정렬 후 기법"은 정렬 비용이 지배해 **전체 O(n log n)**. O(n²) 이중 루프가 한계를 넘을 때 "정렬로 O(n log n)에 떨어뜨릴 수 있나?"를 가장 먼저 의심하라([[day-16-big-o/concept|Day 16 Big-O]]).

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"정렬돼 있다"는 말은 공짜 힌트다.** 입력이 정렬됐다고 명시되면 출제자가 이분 탐색이나 투 포인터를 기대한다는 신호다. 정렬 안 됐어도 O(n log n) 정렬 후 O(n) 기법이 O(n²)보다 빠른 경우가 많다.
>   - 참고: [Two Sum II — Input Array Is Sorted (LeetCode #167)](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
> - **"최소/최대 K를 구하라 + K가 크면 쉬워지고 작으면 어려워진다"면 정답 이분 탐색.** 답 자체가 단조(monotonic)이면 값이 아니라 *답의 범위*를 이분 탐색한다. 판정 함수 `feasible(K)`만 O(n)에 짜면 된다.
>   - 참고: [Koko Eating Bananas (LeetCode #875)](https://leetcode.com/problems/koko-eating-bananas/)
> - **투 포인터 vs 슬라이딩 윈도우 구별.** 둘 다 지표 두 개지만, 투 포인터는 보통 **양 끝에서 좁히고**(정렬 전제), 슬라이딩 윈도우는 **같은 방향으로 창을 밀며** 연속 구간의 상태를 유지한다.
>   - 참고: [Longest Substring Without Repeating Characters (LeetCode #3)](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
> - **그리디는 "증명 없으면 의심"하라.** 그럴듯해 보여도 반례가 있으면 틀린다. 작은 반례를 손으로 만들어 보고, 안 깨지면 **교환 논증(exchange argument)**(최적해를 그리디 선택으로 바꿔도 나빠지지 않음)으로 확신을 얻는다.
>   - 참고: [Greedy algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Greedy_algorithm)
> - **구간(interval) 문제의 90%는 "정렬부터".** 시작점 또는 끝점 기준 정렬이 거의 첫 수다. Merge Intervals는 시작점 정렬, 회의실 배정류는 끝점 정렬이 정석.
>   - 참고: [Merge Intervals (LeetCode #56)](https://leetcode.com/problems/merge-intervals/)
> - **`bisect`는 손으로 짠 이분 탐색을 대체한다.** `bisect_left`/`bisect_right`로 삽입 위치를 O(log n)에 얻는다. off-by-one 버그를 줄이고 싶으면 표준 라이브러리를 먼저 고려하라.
>   - 참고: [bisect (Python 공식 문서)](https://docs.python.org/3/library/bisect.html)

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **기법 선택은 "이미 정렬/단조인가"가 절반을 결정한다.** 정렬+값찾기→이분 탐색, 정렬+짝찾기→투 포인터, 답이 단조→정답 이분 탐색, 연속 구간→슬라이딩 윈도우. 이 한 줄이 Phase 2의 압축이다.
> 2. **이분 탐색의 3대 버그.** ① 경계: `lo <= hi` vs `lo < hi`를 루프 종료 조건과 맞춰라. ② 중앙: `mid = (lo + hi) // 2`(파이썬은 오버플로 없지만 습관화). ③ 갱신: `lo = mid + 1` / `hi = mid - 1`로 **반드시 구간을 좁혀** 무한 루프를 막는다. 정렬 안 된 배열에 이분 탐색은 무효다.
>    - 참고: [Binary Search (LeetCode #704)](https://leetcode.com/problems/binary-search/)
> 3. **정답 이분 탐색(parametric search)의 조건은 단조성.** `feasible(K)`가 어느 임계값을 넘으면 계속 True(또는 계속 False)여야 이분 탐색이 성립한다. "가능한 최소 K"는 True가 시작되는 경계를, "최대 K"는 True가 끝나는 경계를 찾는 것.
> 4. **투 포인터는 "정렬 전제"를 잊기 쉽다.** 정렬 안 된 배열에서 양 끝 좁히기는 틀린다. 또 중복 처리(같은 값 건너뛰기)를 빼먹으면 3Sum류에서 중복 답이 나온다.
> 5. **슬라이딩 윈도우는 "창 안의 상태"를 O(1)로 갱신해야 이득이다.** 창을 옮길 때마다 전체를 다시 세면 O(n·k)로 이점이 사라진다. `dict`/`Counter`/합 변수로 **들어온 원소 +, 나간 원소 -** 를 유지하라.
> 6. **그리디는 정당성이 생명, DP는 안전망.** 그리디가 반례로 깨지면 대개 **완전 탐색 → 재귀 → 메모이제이션 → DP**로 내려간다. 코테에서 "그리디로 되나?"가 애매하면 입력 크기를 보고 DP/브루트포스 여유가 있는지 Big-O로 판단하라.
> 7. **정렬은 O(n log n)의 하한(비교 정렬).** 비교 기반 정렬은 O(n log n)보다 빠를 수 없다. 파이썬 `sort`는 Timsort로 안정 정렬(stable)이며, 튜플·`key`로 다중 기준 정렬을 한 줄에 처리한다.
>    - 참고: [Sorting HOW TO (Python 공식 문서)](https://docs.python.org/3/howto/sorting.html)
> 8. **분할정복은 "결합 비용"까지 합산.** 시간복잡도는 분할·재귀뿐 아니라 combine 단계 `f(n)`까지 더한다. 병합 정렬이 O(n log n)인 것은 각 레벨 병합 O(n) 때문. 점화식 `T(n)=aT(n/b)+f(n)`은 마스터 정리로 푼다([[day-22-recursion/concept|Day 22]]).
> 9. **"어떤 기법이든 마지막 관문은 Big-O".** 기법을 골랐으면 입력 상한을 넣어 실제 연산 수를 어림하라. n<=10^5에 O(n²)면 10^10으로 시간 초과(TLE), O(n log n)이면 약 1.7×10^6으로 통과. 기법 선택 오류의 90%는 복잡도 오판이다([[day-16-big-o/concept|Day 16]]).

> [!example]- 예제 코드 (Examples)
> ```python
> import bisect
>
> # 1) 이분 탐색: 정렬된 배열에서 target 위치 (없으면 -1)
> def binary_search(nums, target):
>     lo, hi = 0, len(nums) - 1
>     while lo <= hi:
>         mid = (lo + hi) // 2
>         if nums[mid] == target:
>             return mid
>         if nums[mid] < target:
>             lo = mid + 1        # 오른쪽 절반으로
>         else:
>             hi = mid - 1        # 왼쪽 절반으로
>     return -1
>
> # 2) 투 포인터: 정렬된 배열에서 합이 target인 두 값 (Two Sum II)
> def two_sum_sorted(nums, target):
>     lo, hi = 0, len(nums) - 1
>     while lo < hi:
>         s = nums[lo] + nums[hi]
>         if s == target:
>             return [lo + 1, hi + 1]   # 1-indexed
>         if s < target:
>             lo += 1                   # 합을 키운다
>         else:
>             hi -= 1                   # 합을 줄인다
>     return []
>
> # 3) 슬라이딩 윈도우: 중복 없는 가장 긴 부분 문자열 길이
> def longest_unique(s):
>     seen = {}                 # 문자 -> 마지막 위치
>     start = best = 0
>     for i, ch in enumerate(s):
>         if ch in seen and seen[ch] >= start:
>             start = seen[ch] + 1      # 창의 왼쪽을 당긴다
>         seen[ch] = i
>         best = max(best, i - start + 1)
>     return best
>
> # 4) 그리디 + 정렬: 겹치는 구간 병합 (Merge Intervals)
> def merge_intervals(intervals):
>     intervals.sort()                  # 시작점 기준 정렬이 첫 수
>     merged = []
>     for s, e in intervals:
>         if merged and s <= merged[-1][1]:
>             merged[-1][1] = max(merged[-1][1], e)   # 겹치면 확장
>         else:
>             merged.append([s, e])
>     return merged
>
> # 5) 정답 이분 탐색(parametric): 판정 함수의 단조성을 탐색
> def min_feasible_k(lo, hi, feasible):
>     # feasible(K)가 어떤 임계값 이상에서 계속 True일 때, 가장 작은 K
>     while lo < hi:
>         mid = (lo + hi) // 2
>         if feasible(mid):
>             hi = mid            # 더 작아질 수 있나?
>         else:
>             lo = mid + 1        # 더 커야 한다
>     return lo
>
> # 6) bisect: 표준 라이브러리 이분 탐색 (삽입 위치)
> arr = [1, 3, 5, 7, 9]
> pos = bisect.bisect_left(arr, 5)      # -> 2
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> Phase 2 전 범위를 섞은 세트. 각 문제 옆에 "어떤 기법 신호인지"를 표시했다. 뒤로 갈수록 기법이 결합된다.
>
> | 번호 | 문제 | 출처 | 난이도 | 기법 |
> |---|---|---|---|---|
> | 1 | Binary Search | [LeetCode #704](https://leetcode.com/problems/binary-search/) | 🟢기초 | 이분 탐색 |
> | 2 | Two Sum II — Input Array Is Sorted | [LeetCode #167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | 🟢기초 | 투 포인터 |
> | 3 | 체육복 | [프로그래머스 #42862](https://school.programmers.co.kr/learn/courses/30/lessons/42862) | 🟢기초 | 그리디 |
> | 4 | Longest Substring Without Repeating Characters | [LeetCode #3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 🟡중급 | 슬라이딩 윈도우 |
> | 5 | Container With Most Water | [LeetCode #11](https://leetcode.com/problems/container-with-most-water/) | 🟡중급 | 투 포인터 |
> | 6 | Merge Intervals | [LeetCode #56](https://leetcode.com/problems/merge-intervals/) | 🟡중급 | 정렬+그리디 |
> | 7 | Jump Game | [LeetCode #55](https://leetcode.com/problems/jump-game/) | 🟡중급 | 그리디 |
> | 8 | Koko Eating Bananas | [LeetCode #875](https://leetcode.com/problems/koko-eating-bananas/) | 🟡중급 | 정답 이분 탐색 |
> | 9 | 구명보트 | [프로그래머스 #42885](https://school.programmers.co.kr/learn/courses/30/lessons/42885) | 🟡중급 | 정렬+투 포인터+그리디 |
> | 10 | Sort List | [LeetCode #148](https://leetcode.com/problems/sort-list/) | 🔴심화 | 분할정복(병합 정렬)+연결 리스트 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — Phase 2의 마지막 개별 기법. 오늘 전체를 묶는다
- ➡️ **다음(next):** [[day-24-brute-force/concept|Day 24 — 완전 탐색]] — 그리디·이분 탐색이 안 되는 문제를 "모두 시도"로 푸는 Phase 3의 출발
- 🧭 **관련(related):**
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — 모든 기법 선택의 최종 심판
  - [[day-17-sorting/concept|Day 17 — 정렬]] — 이분 탐색·투 포인터·그리디의 전처리 관문
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — 값 탐색과 정답 탐색(parametric)
  - [[day-19-two-pointers/concept|Day 19 — 투 포인터]] — 정렬된 배열의 양 끝 좁히기
  - [[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]] — 연속 구간의 상태 유지
  - [[day-21-greedy/concept|Day 21 — 그리디]] — 국소 최적으로 전체 최적(정당성 전제)
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 반으로 나눠 풀고 합치기
  - [[day-24-brute-force/concept|Day 24 — 완전 탐색]] — 기법이 없을 때의 기본기이자 정당성 검증의 기준선
- 🗺️ **지도(MOC):** [[Phase-2 MOC]] · [[00 Algorithm MOC]]

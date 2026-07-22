---
day: 33
phase: 4-advanced
title: 부분 수열 DP (LIS·LCS)
category: [DP, LIS, LCS, 편집 거리, 문자열 DP]
difficulty: 중급
status: done
prev: "[[day-32-dp-knapsack/concept|Day 32 — 배낭 문제 (Knapsack DP)]]"
next: "[[day-34-dijkstra/concept|Day 34 — 최단 경로 (Dijkstra)]]"
related:
  - "[[day-31-dp/concept|Day 31 — 동적 계획법 입문]]"
  - "[[day-32-dp-knapsack/concept|Day 32 — 배낭 문제 (Knapsack DP)]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-04-strings/concept|Day 04 — 문자열 다루기]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-34-dijkstra/concept|Day 34 — 최단 경로 (Dijkstra)]]"
sources:
  - https://leetcode.com/problems/longest-increasing-subsequence/
  - https://leetcode.com/problems/longest-continuous-increasing-subsequence/
  - https://leetcode.com/problems/longest-common-subsequence/
  - https://leetcode.com/problems/longest-palindromic-subsequence/
  - https://leetcode.com/problems/edit-distance/
  - https://school.programmers.co.kr/learn/courses/30/lessons/12904
  - https://docs.python.org/3/library/bisect.html
tags: [phase/4, topic/dp, topic/lis, topic/lcs, topic/edit-distance, topic/string-dp]
---

# Day 33 — 부분 수열 DP (LIS·LCS)

> [!abstract] 한눈 요약 (TL;DR)
> **부분 수열(subsequence)** 은 원래 순서를 유지한 채 **일부 원소를 골라** 만든 수열이다(연속일 필요 없음). 오늘은 코테 DP의 양대 문자열/수열 골격을 배운다 — **① LIS(Longest Increasing Subsequence, 최장 증가 부분 수열):** 한 수열에서 **증가하며 가장 긴** 부분 수열의 길이. **② LCS(Longest Common Subsequence, 최장 공통 부분 수열):** 두 수열에서 **양쪽에 공통으로** 나타나며 가장 긴 부분 수열의 길이. LIS는 상태 `dp[i]="i로 끝나는 LIS 길이"`로 O(N²), 여기에 [[day-18-binary-search/concept|이분 탐색(Day 18)]]을 얹으면 **O(N log N)** 으로 줄어든다. LCS는 두 문자열의 인덱스를 두 축으로 삼는 **2차원 DP** `dp[i][j]`로, "**끝 글자가 같으면 대각선+1, 다르면 위·왼쪽 max**"라는 한 줄 점화식이 핵심이다. LCS의 사고를 확장하면 **편집 거리(Edit Distance)**, **최장 팰린드롬 부분 수열(LPS = LCS(s, reverse(s)))**, 문자열 유사도 문제로 곧장 이어진다. [[day-32-dp-knapsack/concept|배낭(Day 32)]]이 "어떤 아이템을 담나"였다면, 오늘은 "**어떤 순서·부분 수열을 고르나**"로 DP의 두 번째 큰 골격을 완성한다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **부분 수열 vs 부분 배열(subarray/substring).** 먼저 헷갈리기 쉬운 두 개념을 갈라야 한다. **부분 배열(부분 문자열)** 은 **연속**한 조각이다(`[3,1,2]`의 부분 배열 `[1,2]`). **부분 수열** 은 순서만 지키면 **중간을 건너뛰어도** 된다(`[3,1,2]`의 부분 수열 `[3,2]`). "연속"이면 [[day-20-sliding-window/concept|투 포인터·슬라이딩 윈도우]], "건너뛰어도 됨"이면 대개 **DP**다. 오늘 주제는 모두 후자다.
>
> **LIS — 계단 오르기 비유.** 숫자들이 일렬로 놓여 있다. 왼쪽에서 오른쪽으로 가되 **항상 더 큰 수로만 밟고** 지나갈 때, 가장 많이 밟을 수 있는 발판 수가 LIS다. 예: `[10, 9, 2, 5, 3, 7, 101, 18]` → `[2, 3, 7, 101]` 또는 `[2, 3, 7, 18]`로 길이 **4**. "지금 이 숫자로 끝나는 가장 긴 증가 사슬"을 각 위치마다 기록해두고, 앞쪽에서 나보다 작은 것들 중 가장 긴 사슬에 나를 이어붙이는 것이 핵심 직관이다.
>
> **LCS — 두 유전자/문서 비교 비유.** 두 문자열 `"ABCBDAB"`와 `"BDCAB"`가 있다. 양쪽에서 **순서를 지키며 공통으로 뽑을 수 있는** 가장 긴 글자열이 LCS다(`"BCAB"` 또는 `"BDAB"`, 길이 **4**). 문서 `diff`, 표절 검사, DNA 정렬(sequence alignment), git의 변경 비교가 전부 LCS 계열이다. 두 수열을 나란히 놓고 "**끝 글자를 맞출까 말까**"를 모든 (i, j) 조합에 대해 표로 채운다.
>
> **왜 부분 수열은 DP인가.** 길이 N 수열의 부분 수열은 **2^N개**다(각 원소 포함/제외). 전부 나열하면 지수 시간. 하지만 "**어디서 끝나는가(LIS)**" 또는 "**두 수열의 어디까지 봤는가(LCS)**"를 상태로 잡으면 겹치는 부분 문제(overlapping subproblems)가 드러나 [[day-31-dp/concept|DP(Day 31)]]로 다항 시간에 푼다. 이것이 배낭에 이어 **DP를 적용하는 두 번째 대표 신호**다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) LIS — O(N²) DP (가장 직관적).**
> 상태 `dp[i]` = "`nums[i]`로 **끝나는** 증가 부분 수열의 최대 길이". 나보다 앞이면서 나보다 작은 모든 `j`를 훑어 가장 긴 것에 1을 더한다.
> ```
> dp[i] = 1 + max( dp[j]  for j < i if nums[j] < nums[i] )   # 없으면 dp[i]=1
> 답 = max(dp)          # 어디서 끝나든 가장 긴 것
> ```
> ```
> nums = [10, 9, 2, 5, 3, 7, 101, 18]
> dp   = [ 1, 1, 1, 2, 2, 3,   4,  4]
>          10  9  2  5  3  7  101  18
>   dp[3]=2 : 5 앞의 2(<5)에 이어 [2,5]
>   dp[5]=3 : 7 앞의 [2,3](<7)에 이어 [2,3,7]
>   dp[6]=4 : 101 앞의 [2,3,7]에 이어 [2,3,7,101]  -> 답 4
> ```
>
> **(B) LIS — O(N log N) 이분 탐색 (실전 고속형).**
> "현재까지 만든 여러 증가 수열들의 **각 길이별 마지막 원소의 최솟값**"만 배열 `tails`로 유지한다. 새 원소 `x`가 오면 `tails`에서 **x 이상인 첫 위치**를 이분 탐색으로 찾아 덮어쓴다(없으면 뒤에 추가). `tails`의 **길이**가 곧 LIS 길이다.
> ```
> tails = []
> for x in nums:
>     pos = bisect_left(tails, x)      # x 이상이 처음 나오는 자리
>     if pos == len(tails):
>         tails.append(x)              # x 가 제일 크다 -> 수열 연장
>     else:
>         tails[pos] = x               # 더 작은 값으로 갱신(미래 여지 up)
> LIS = len(tails)
> ```
> 주의: `tails`는 **실제 LIS 수열이 아니다**(길이만 정확). "가장 긴 증가"는 `bisect_left`, "가장 긴 **비감소**(중복 허용, ≤)"는 `bisect_right`를 쓴다. → [[day-18-binary-search/concept|Day 18 이분 탐색]] 응용.
>
> **(C) LCS — 2차원 DP.**
> 두 문자열 `a`(길이 m), `b`(길이 n). 상태 `dp[i][j]` = "`a[:i]`와 `b[:j]`의 LCS 길이". 끝 글자가 같으면 그 글자를 공통으로 쓰고 대각선에서 +1, 다르면 한쪽을 버린 두 경우의 max.
> ```
> if a[i-1] == b[j-1]:
>     dp[i][j] = dp[i-1][j-1] + 1                 # 대각선 + 1
> else:
>     dp[i][j] = max(dp[i-1][j], dp[i][j-1])      # 위 / 왼쪽 중 큰 값
> 답 = dp[m][n]       (첫 행·첫 열은 0으로 초기화 = 빈 문자열)
> ```
> ```
>        ""  B  D  C  A  B      a="ABCBDAB", b="BDCAB"
>    ""   0  0  0  0  0  0
>    A    0  0  0  0  1  1
>    B    0  1  1  1  1  2
>    C    0  1  1  2  2  2
>    B    0  1  1  2  2  3
>    D    0  1  2  2  2  3
>    A    0  1  2  2  3  3
>    B    0  1  2  2  3  4     <- dp[m][n] = 4  (예: "BDAB")
> ```
>
> **(D) 편집 거리 (Edit Distance) — LCS 사촌.**
> `a`를 `b`로 바꾸는 최소 연산 수(삽입/삭제/교체). 끝 글자가 같으면 그대로, 다르면 세 연산 중 최소 +1.
> ```
> if a[i-1] == b[j-1]:
>     dp[i][j] = dp[i-1][j-1]                              # 그대로
> else:
>     dp[i][j] = 1 + min(dp[i-1][j],     # 삭제
>                        dp[i][j-1],     # 삽입
>                        dp[i-1][j-1])   # 교체
> 초기값: dp[i][0]=i (i번 삭제), dp[0][j]=j (j번 삽입)
> ```
>
> **(E) 팰린드롬 부분 수열 (LPS) — LCS 재활용.**
> "가장 긴 팰린드롬 **부분 수열**"의 길이는 놀랍게도 **LPS(s) = LCS(s, reverse(s))** 다. 뒤집은 자기 자신과의 공통 부분 수열이 곧 좌우 대칭 사슬이기 때문. (단, 팰린드롬 **부분 문자열**(연속)은 별개 문제 → 아래 필수 상식·문제 6번 참고.)
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> 부분 수열 DP도 [[day-16-big-o/concept|Big-O(Day 16)]]의 **`상태 개수 × 전이 비용`** 공식을 그대로 따른다.
>
> | 문제 | 상태 | 시간 | 공간 | 비고 |
> |---|---|---|---|---|
> | LIS (DP) | O(N) | O(N²) | O(N) | 전이마다 앞쪽 훑기 |
> | LIS (이분 탐색) | O(N) | **O(N log N)** | O(N) | `tails` 길이만 정확 |
> | LCS | O(m·n) | O(m·n) | O(m·n) → **O(min(m,n))** | 2행만 유지 시 압축 |
> | 편집 거리 | O(m·n) | O(m·n) | O(m·n) → O(n) | LCS와 동일 골격 |
> | LPS (=LCS(s,rev)) | O(N²) | O(N²) | O(N²) → O(N) | 자기 역순과 LCS |
>
> > **LIS의 두 얼굴.** N이 수천 이하면 O(N²) DP로 충분하고 코드가 짧아 실수도 적다. N이 10⁵ 이상이면 반드시 O(N log N) 이분 탐색을 써야 한다. **"N 범위부터 확인"** 하고 방법을 고르는 습관을 들여라.
> >
> > **LCS/편집 거리 공간 압축.** `dp[i][j]`는 바로 윗 행(`i-1`)과 현재 행만 참조하므로 **2행(rolling array)** 으로 O(min(m,n))까지 줄인다. 단, **실제 수열 복원**(어떤 글자가 공통인지)까지 필요하면 전체 표를 남겨야 한다([[day-32-dp-knapsack/concept|Day 32]]의 선택 복원과 같은 트레이드오프).
> >
> > **부분 배열(연속)과 혼동 주의.** "가장 긴 **연속** 증가 부분 배열"(LeetCode #674)은 DP가 아니라 O(N) 한 번 훑기로 끝난다. "부분 수열"과 "부분 배열"을 잘못 읽으면 불필요하게 어려운 풀이로 새거나 틀린다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"연속?"을 가장 먼저 물어라.** 연속(부분 배열/문자열) → 투 포인터/슬라이딩 윈도우/카데인. 건너뛰기 가능(부분 수열) → DP(LIS/LCS). 이 한 번의 분기가 접근을 통째로 가른다.
> - **LIS O(N log N)의 `tails`는 "정답 수열이 아니다".** 길이만 맞다. 실제 수열을 복원하려면 각 원소의 위치(pos)를 부모 포인터로 따로 기록해야 한다. 면접에서 자주 파고드는 지점.
>   - 참고: [Python `bisect` 공식 문서](https://docs.python.org/3/library/bisect.html)
> - **"증가" vs "비감소"는 bisect 함수로 조절.** 강한 증가(strictly increasing, 중복 불가)는 `bisect_left`, 약한 증가(non-decreasing, 중복 허용 ≤)는 `bisect_right`. 문제가 "strictly"인지 반드시 확인.
> - **LCS는 표 그림을 그려라.** "같으면 ↖+1, 다르면 max(↑, ←)" 규칙은 표를 한 번 손으로 채워보면 절대 안 잊는다. 첫 행/열이 0(빈 문자열)인 것이 시작점.
> - **LPS = LCS(s, reverse(s)) 트릭.** 팰린드롬 부분 수열 문제를 보면 뒤집어서 LCS로 환원하는 게 가장 외우기 쉬운 정석. 단 "부분 문자열(연속)"이면 이 트릭이 안 통한다(중심 확장/구간 DP 필요).
> - **편집 거리는 LCS의 형제.** 점화식 구조가 거의 같다(같으면 대각선, 다르면 주변 min/max +1). 하나를 이해하면 나머지도 90% 안다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **부분 수열(subsequence) ≠ 부분 배열(subarray).** 부분 수열은 **건너뛰기 허용**(순서만 유지), 부분 배열/문자열은 **연속**. 문제 지문의 이 한 단어가 알고리즘 전체(DP vs 슬라이딩 윈도우)를 바꾼다. **가장 먼저 확인할 것.**
> 2. **LIS는 N에 따라 알고리즘을 바꾼다.** N≤~5000이면 O(N²) DP, N이 크면 O(N log N) 이분 탐색. 큰 입력에 O(N²)를 쓰면 시간 초과, 작은 입력에 이분 탐색을 무리하게 쓰면 실수만 는다.
> 3. **`tails` 배열은 LIS 실물이 아니다.** O(N log N) LIS의 `tails`는 "길이별 최소 꼬리값"일 뿐 실제 증가 수열이 아니다. 길이는 정확하지만 원소 순서로 읽으면 틀리다 — **길이만 신뢰**하라.
> 4. **strictly vs non-decreasing를 혼동하면 조용히 틀린다.** 중복 원소가 있을 때 `bisect_left`(strict)와 `bisect_right`(≤)의 답이 갈린다. 에러가 안 나서 더 위험하다.
> 5. **LCS 인덱스 오프셋.** `dp`를 `(m+1)×(n+1)`로 잡고 `a[i-1]`, `b[j-1]`로 접근한다(첫 행·열은 빈 문자열=0). 인덱스를 `a[i]`로 잘못 쓰면 범위 초과·오답. DP 표에서 가장 흔한 버그.
> 6. **재귀 Top-Down은 깊이·캐시 주의.** LCS/편집 거리를 `@lru_cache`로 풀면 인자는 인덱스 정수 2개여야 하고, m·n이 크면 재귀 깊이(`sys.setrecursionlimit`)와 캐시 메모리를 신경 써야 한다([[day-22-recursion/concept|Day 22]]).
> 7. **팰린드롬: 부분 수열 vs 부분 문자열.** "가장 긴 팰린드롬 **부분 수열**"은 LCS(s, rev s)로 O(N²). "가장 긴 팰린드롬 **부분 문자열**(연속)"은 중심 확장 O(N²) 또는 Manacher O(N)로 **다른 문제**다. 프로그래머스 '가장 긴 팰린드롬'은 후자(연속)다.
> 8. **공간 압축과 복원은 양립 어렵다.** 2행 압축으로 O(N) 공간을 쓰면 실제 공통 부분 수열을 역추적할 수 없다. "길이만" 필요하면 압축, "무엇인지"까지 필요하면 전체 표를 남겨라.
> 9. **DP는 "끝나는 지점"으로 상태를 잡는다.** LIS의 `dp[i]`는 "i에서 **끝나는**" 길이라 답이 `max(dp)`다(마지막 값 `dp[-1]`이 아님!). "i까지 중 최대"로 정의하면 점화식이 달라진다 — 상태 정의를 흐리면 전부 어긋난다.

> [!example]- 예제 코드 (Examples)
> ```python
> from bisect import bisect_left
>
> # (1) LIS - O(N^2) DP
> def lis_dp(nums):
>     if not nums:
>         return 0
>     dp = [1] * len(nums)
>     for i in range(len(nums)):
>         for j in range(i):
>             if nums[j] < nums[i]:
>                 dp[i] = max(dp[i], dp[j] + 1)
>     return max(dp)
>
> # (2) LIS - O(N log N) 이분 탐색
> def lis_fast(nums):
>     tails = []
>     for x in nums:
>         pos = bisect_left(tails, x)     # strictly increasing
>         if pos == len(tails):
>             tails.append(x)
>         else:
>             tails[pos] = x
>     return len(tails)
>
> # (3) LCS - 2차원 DP
> def lcs(a, b):
>     m, n = len(a), len(b)
>     dp = [[0] * (n + 1) for _ in range(m + 1)]
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if a[i - 1] == b[j - 1]:
>                 dp[i][j] = dp[i - 1][j - 1] + 1
>             else:
>                 dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
>     return dp[m][n]
>
> # (4) 편집 거리 (Edit Distance)
> def edit_distance(a, b):
>     m, n = len(a), len(b)
>     dp = [[0] * (n + 1) for _ in range(m + 1)]
>     for i in range(m + 1):
>         dp[i][0] = i
>     for j in range(n + 1):
>         dp[0][j] = j
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if a[i - 1] == b[j - 1]:
>                 dp[i][j] = dp[i - 1][j - 1]
>             else:
>                 dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
>     return dp[m][n]
>
> # (5) 최장 팰린드롬 부분 수열 = LCS(s, reverse(s))
> def longest_palindromic_subseq(s):
>     return lcs(s, s[::-1])
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> LIS(기초→고속) → 연속과의 대비 → LCS(2D 문자열 DP) → LCS 응용(팰린드롬·편집 거리) → 기출 순으로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Longest Increasing Subsequence | [LeetCode #300](https://leetcode.com/problems/longest-increasing-subsequence/) | 🟡중급 | LIS (O(N²) & O(N log N)) |
> | 2 | Longest Continuous Increasing Subsequence | [LeetCode #674](https://leetcode.com/problems/longest-continuous-increasing-subsequence/) | 🟢기초 | 부분 배열(연속) 대비 |
> | 3 | Longest Common Subsequence | [LeetCode #1143](https://leetcode.com/problems/longest-common-subsequence/) | 🟡중급 | LCS 2D 문자열 DP |
> | 4 | Longest Palindromic Subsequence | [LeetCode #516](https://leetcode.com/problems/longest-palindromic-subsequence/) | 🟡중급 | LPS = LCS(s, rev s) |
> | 5 | Edit Distance | [LeetCode #72](https://leetcode.com/problems/edit-distance/) | 🔴심화 | 편집 거리(LCS 사촌) |
> | 6 | 가장 긴 팰린드롬 | [프로그래머스 #12904](https://school.programmers.co.kr/learn/courses/30/lessons/12904) | ⚫기출 | 팰린드롬 부분 문자열(연속) |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 상태 정의·점화식, LIS의 두 접근(O(N²) vs O(N log N)) 비교, LCS/편집 거리의 2차원 표와 공간 압축, 팰린드롬의 "부분 수열 vs 부분 문자열" 구분: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-32-dp-knapsack/concept|Day 32 — 배낭 문제 (Knapsack DP)]] — 배낭이 "어떤 아이템을 담나(용량 축)"였다면, 오늘은 "어떤 순서·부분 수열을 고르나"로 DP 상태 설계를 확장한다
- ➡️ **다음(next):** [[day-34-dijkstra/concept|Day 34 — 최단 경로 (Dijkstra)]] — DP 골격(배낭·부분 수열)을 마치고, 그래프 위의 최적화인 최단 경로로 넘어간다
- 🧭 **관련(related):**
  - [[day-31-dp/concept|Day 31 — 동적 계획법 입문]] — LIS/LCS 모두 "상태 → 점화식 → 초기값 → 순서" 4단계의 대표 응용. 부분 수열은 DP를 적용하는 두 번째 신호
  - [[day-32-dp-knapsack/concept|Day 32 — 배낭 문제 (Knapsack DP)]] — 배낭과 함께 코테 DP의 양대 골격. 선택 복원·공간 압축의 트레이드오프가 동일하게 나타난다
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — LIS를 O(N²)에서 O(N log N)으로 끌어내리는 `tails` + `bisect`의 토대
  - [[day-04-strings/concept|Day 04 — 문자열 다루기]] — LCS·편집 거리·팰린드롬은 모두 문자열 위의 DP. 인덱싱·슬라이싱 기초가 바탕
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — LCS/편집 거리의 Top-Down 메모(`@lru_cache`)는 재귀 + 캐시. 점화식과 1:1로 대응
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — "상태 수 × 전이"로 O(N²)·O(m·n)을 계산하고, LIS의 O(N log N) 개선을 판별하는 사고의 토대
  - [[day-34-dijkstra/concept|Day 34 — 최단 경로 (Dijkstra)]] — 다음 주제. DP식 최적화 사고를 그래프로 확장한다
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]

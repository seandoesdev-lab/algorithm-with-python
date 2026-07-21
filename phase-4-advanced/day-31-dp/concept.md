---
day: 31
phase: 4-advanced
title: 동적 계획법 입문 (Dynamic Programming)
category: [DP, 메모이제이션, 타뷸레이션, 최적 부분 구조, 점화식]
difficulty: 중급
status: done
prev: "[[day-30-review/concept|Day 30 — 개념 집중기 종합 복습 (Final Review)]]"
next: "[[day-32-dp-knapsack/concept|Day 32 — 배낭 문제 (Knapsack DP)]]"
related:
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-21-greedy/concept|Day 21 — 그리디]]"
  - "[[day-14-prefix-sum/concept|Day 14 — 누적 합]]"
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-32-dp-knapsack/concept|Day 32 — 배낭 문제 (Knapsack DP)]]"
sources:
  - https://leetcode.com/problems/fibonacci-number/
  - https://leetcode.com/problems/climbing-stairs/
  - https://leetcode.com/problems/min-cost-climbing-stairs/
  - https://leetcode.com/problems/house-robber/
  - https://leetcode.com/problems/maximum-subarray/
  - https://leetcode.com/problems/coin-change/
  - https://leetcode.com/problems/longest-increasing-subsequence/
  - https://leetcode.com/problems/longest-common-subsequence/
  - https://leetcode.com/problems/unique-paths/
  - https://school.programmers.co.kr/learn/courses/30/lessons/43105
  - https://school.programmers.co.kr/learn/courses/30/lessons/42895
  - https://school.programmers.co.kr/learn/courses/30/lessons/42898
  - https://docs.python.org/3/library/functools.html#functools.lru_cache
tags: [phase/4, topic/dp, topic/dynamic-programming, topic/memoization, topic/tabulation]
---

# Day 31 — 동적 계획법 입문 (Dynamic Programming)

> [!abstract] 한눈 요약 (TL;DR)
> **동적 계획법(Dynamic Programming, DP)** 은 "**큰 문제를 작은 문제로 쪼개고, 한 번 푼 작은 문제의 답을 저장(memo)해 두어 다시 계산하지 않는**" 기법이다. 오늘부터 시작하는 **Phase 4 심화**의 첫 관문이자, 코테에서 가장 배점이 높고 가장 자주 나오는 주제다. DP가 통하려면 두 조건이 필요하다 — **① 최적 부분 구조(optimal substructure):** 큰 문제의 최적해가 작은 문제의 최적해로 조합된다. **② 중복 부분 문제(overlapping subproblems):** 같은 작은 문제가 여러 번 반복해서 나온다. 이 둘이 있으면 [[day-22-recursion/concept|재귀(Day 22)]]의 지수 시간 폭발을 **저장 한 번으로 다항 시간으로** 끌어내린다. 구현은 두 갈래다 — **Top-Down(메모이제이션):** 재귀 + 캐시(`@lru_cache`). **Bottom-Up(타뷸레이션):** 반복문 + 표(`dp[]` 배열)를 작은 값부터 채운다. DP 문제의 90%는 **"상태(state)를 무엇으로 정의하고 → 점화식(recurrence)을 어떻게 세우고 → 초기값(base case)과 채우는 순서를 어떻게 잡느냐"** 로 귀결된다. **"경우의 수 / 최소·최대 비용 / 가능 여부 / n번째 값"** 이 보이고 **선택이 이전 선택에 의존**하면 곧바로 DP를 의심하라.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **동적 계획법**은 이름과 달리 "동적"이거나 "계획"과 큰 상관이 없다(1950년대 리처드 벨만이 예산 심의를 통과시키려고 붙인 멋있어 보이는 이름일 뿐이다). 실체는 단순하다: **"같은 계산을 두 번 하지 마라(don't repeat work)."** 문제를 작은 하위 문제로 나눠 풀되, **한 번 구한 하위 문제의 답을 어딘가에 적어두고(저장) 다음에 그 답이 필요하면 다시 계산하지 않고 꺼내 쓴다.**
>
> **일상 비유 — 계단 오르기 메모.** 40층 계단을 1칸 또는 2칸씩 올라가는 경우의 수를 센다고 하자. "40층 가는 법 = 39층에서 1칸 + 38층에서 2칸" 이다. 그런데 39층 가는 법을 세려면 다시 38층, 37층이 필요하다. 순진하게 재귀로 세면 **38층을 세는 계산이 수백만 번 중복**된다. 대신 **"1층 가는 법 = 1가지, 2층 = 2가지"** 를 공책에 적고, 3층부터 **"아래 두 칸의 합"** 으로 차곡차곡 위로 채워 올라가면 각 층을 딱 한 번만 계산한다. 이 공책이 `dp[]` 배열이고, 이 방식이 DP다.
>
> **일상 비유 — 프로젝트 견적서.** 큰 공사의 최소 비용을 낼 때, 각 하위 공정(배관·전기·미장)의 최소 비용을 먼저 확정해 표로 붙여두고, 큰 공정은 그 표를 조합해 계산한다. 하위 공정 견적을 매번 다시 뽑지 않는 것 — 그게 최적 부분 구조 + 저장이다.
>
> **핵심 직관 — DP는 "똑똑한 완전탐색"이다.** [[day-24-brute-force/concept|완전탐색]]은 모든 경우를 다 따지지만 같은 상태를 몇 번이고 다시 계산한다. DP는 "모든 경우를 따지되, **각 고유 상태는 딱 한 번만** 계산하고 재사용"한다. 그래서 지수 시간이 상태 개수 × 전이 비용의 다항 시간으로 줄어든다.

> [!gear]- 2. 동작 원리 (How It Works)
> **DP 설계 4단계 — 모든 DP 문제를 이 순서로 공략한다.**
> 1. **상태 정의(state):** `dp[i]`가 "무엇의 답"인지 한 문장으로 못 박는다. (예: `dp[i]` = "i번째 계단까지 오는 경우의 수") — **여기서 실패하면 나머지가 다 틀린다.**
> 2. **점화식(recurrence):** `dp[i]`를 더 작은 `dp[...]`들로 표현한다. (예: `dp[i] = dp[i-1] + dp[i-2]`)
> 3. **초기값(base case):** 재귀/반복이 멈추는 가장 작은 상태의 값을 직접 채운다. (예: `dp[0]=1, dp[1]=1`)
> 4. **계산 순서(order):** 의존하는 하위 상태가 **먼저** 채워지도록 순서를 정한다. (Bottom-Up이면 보통 작은 인덱스부터.)
>
> **(A) 순진한 재귀 — 왜 터지는가.** 피보나치를 그냥 재귀로 짜면:
> ```
> def fib(n):
>     if n < 2: return n
>     return fib(n-1) + fib(n-2)   # 같은 fib 값을 지수적으로 재계산
> ```
> `fib(5)` 호출 트리를 그려보면 `fib(2)`가 3번, `fib(3)`이 2번 계산된다. n이 커지면 **O(2^n)** 으로 폭발한다. 이게 "중복 부분 문제"다.
> ```
>              fib(5)
>            /        \
>       fib(4)         fib(3)      <- fib(3) 등장
>       /    \         /    \
>   fib(3)  fib(2)  fib(2)  fib(1) <- fib(3),fib(2) 또 등장 (중복!)
> ```
>
> **(B) Top-Down (메모이제이션) — 재귀 + 캐시.** 재귀 구조는 그대로 두고, 한 번 구한 값을 저장(memo)해 재계산을 막는다. 파이썬은 `@lru_cache` 한 줄이면 끝.
> ```
> from functools import lru_cache
> @lru_cache(maxsize=None)
> def fib(n):
>     if n < 2: return n
>     return fib(n-1) + fib(n-2)   # 각 n은 딱 한 번만 실제 계산됨 -> O(n)
> ```
> 직접 딕셔너리로도 가능(원리 이해용):
> ```
> memo = {}
> def fib(n):
>     if n < 2: return n
>     if n in memo: return memo[n]        # 저장된 답 재사용
>     memo[n] = fib(n-1) + fib(n-2)       # 처음 계산할 때만 저장
>     return memo[n]
> ```
>
> **(C) Bottom-Up (타뷸레이션) — 반복 + 표.** 재귀를 없애고, 가장 작은 상태부터 표를 채워 올라간다. 재귀 깊이 한계가 없고 상수도 빠르다.
> ```
> def fib(n):
>     if n < 2: return n
>     dp = [0] * (n + 1)
>     dp[0], dp[1] = 0, 1
>     for i in range(2, n + 1):
>         dp[i] = dp[i-1] + dp[i-2]       # 아래(작은 i)가 이미 채워져 있음
>     return dp[n]
> ```
>
> **(D) 공간 최적화 — "필요한 것만 들고 다니기".** 점화식이 바로 아래 몇 칸(`dp[i-1], dp[i-2]`)만 참조하면, 배열 전체 대신 변수 2개면 된다. O(n) 공간 → O(1) 공간.
> ```
> def fib(n):
>     prev, cur = 0, 1
>     for _ in range(n):
>         prev, cur = cur, prev + cur     # 한 칸씩 밀며 진행
>     return prev
> ```
>
> **(E) 대표 점화식 유형 — 이름표를 붙여 외워라.**
> ```
> 계단/피보나치형 :  dp[i] = dp[i-1] + dp[i-2]            (경우의 수 누적)
> 집도둑형(선택)  :  dp[i] = max(dp[i-1], dp[i-2] + a[i]) (택하거나 건너뛰거나)
> 동전/배낭형     :  dp[a] = min(dp[a], dp[a-coin] + 1)   (무한/유한 아이템)
> 격자 경로형     :  dp[r][c] = dp[r-1][c] + dp[r][c-1]   (위 or 왼쪽에서)
> 최대 부분합형   :  dp[i] = max(a[i], dp[i-1] + a[i])    (이어붙일까 새로 시작할까)
> LIS형          :  dp[i] = max(dp[j]+1) for j<i if a[j]<a[i]
> ```
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> DP의 시간복잡도는 거의 항상 **`상태의 개수 × 상태 하나당 전이(transition) 비용`** 이다. 이 공식 하나로 대부분의 DP 복잡도를 즉시 계산할 수 있다.
>
> | 문제 | 상태 개수 | 전이 비용 | 시간 | 공간 |
> |---|---|---|---|---|
> | 피보나치/계단 | O(n) | O(1) | O(n) | O(n) → O(1) 최적화 |
> | 집도둑 (House Robber) | O(n) | O(1) | O(n) | O(1) |
> | 동전 교환 (Coin Change) | O(금액) | O(동전 수) | O(금액×동전수) | O(금액) |
> | 격자 경로 (Unique Paths) | O(m×n) | O(1) | O(m×n) | O(n) 최적화 가능 |
> | LIS (기본 DP) | O(n) | O(n) | O(n²) | O(n) |
> | LIS (이분탐색) | O(n) | O(log n) | O(n log n) | O(n) |
> | LCS | O(m×n) | O(1) | O(m×n) | O(min(m,n)) 최적화 |
>
> > **순진한 재귀 vs DP.** 피보나치 순진 재귀는 O(2^n) — n=50이면 약 10^15회, 사실상 멈춘다. 메모이제이션/타뷸레이션은 O(n) — n=50이면 50회. **저장 하나로 지수 → 선형.** 이게 DP의 존재 이유다.
> >
> > **Top-Down vs Bottom-Up 트레이드오프.** Top-Down은 **필요한 상태만** 계산(희소한 상태 공간에 유리)하고 코드가 점화식과 1:1로 자연스럽다. 단, 재귀 호출 스택이 **상태 깊이만큼** 쌓여 파이썬 기본 한도(1000)를 넘으면 `RecursionError`([[day-25-dfs/concept|Day 25]] 재귀 한계) — `sys.setrecursionlimit` 필요. Bottom-Up은 **모든 상태를 채우지만** 재귀 오버헤드가 없고 상수가 작으며 공간 최적화가 쉽다.
> >
> > **공간은 "점화식이 몇 칸을 보는가"로 결정된다.** `dp[i-1], dp[i-2]`만 보면 변수 2개(O(1)), 2차원 `dp[r][c]`에서 `dp[r-1]`만 보면 행 하나(O(열))로 줄일 수 있다. 답 자체가 아니라 "경로 복원"이 필요하면 표 전체를 남겨야 한다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **먼저 순진한 재귀부터 짜라.** DP의 정석 루트는 "① 완전탐색 재귀로 정답을 맞춘다 → ② `@lru_cache`를 붙여 Top-Down DP로 만든다 → ③ 필요하면 Bottom-Up으로 바꾼다"이다. 처음부터 `dp[]` 배열을 채우려 하면 점화식이 안 잡힌다. **재귀 함수의 인자 = 상태, 반환값 = dp 값**이라는 대응을 기억하라.
>   - 참고: [functools.lru_cache (Python 공식 문서)](https://docs.python.org/3/library/functools.html#functools.lru_cache)
> - **DP vs 그리디 구별법.** 둘 다 최적화 문제지만, [[day-21-greedy/concept|그리디(Day 21)]]는 "매 순간 지역 최선"만으로 전역 최적이 보장될 때만 통한다. **동전 교환에서 그리디가 틀리는 이유**(예: 1,3,4원으로 6원 → 그리디 4+1+1=3개, DP 3+3=2개)가 DP가 필요한 전형적 신호다. "지금 최선이 나중에 손해일 수 있다"면 DP.
> - **상태를 못 잡으면 "무엇을 알면 나머지를 풀 수 있나"를 물어라.** 배낭이면 "몇 번째 물건까지 봤고, 남은 무게가 얼마인가"가 상태다. 문자열이면 보통 "i번째 문자까지"가 상태.
> - **1차원으로 안 되면 차원을 늘려라.** `dp[i]` 하나로 부족하면 `dp[i][j]`, `dp[i][j][k]`처럼 상태에 정보를 추가한다. LCS·배낭·구간 DP가 2차원인 이유다.
> - **파이썬에서 Top-Down은 `@lru_cache`가 반칙급으로 편하다.** 단 인자가 **해시 가능**(불변)해야 한다 — 리스트 대신 `tuple`, 인덱스 정수를 넘겨라. 가변 기본 인자(`def f(memo={})`) 함정도 주의.
> - **"경우의 수"는 큰 수가 되기 쉽다.** 문제에 "10^9+7로 나눈 나머지"가 있으면 매 덧셈·곱셈마다 `% MOD`를 걸어라(파이썬은 큰 정수가 되지만 속도·요구사항 때문에 모듈러가 필요).

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **DP의 두 전제: 최적 부분 구조 + 중복 부분 문제.** 이 둘이 없으면 DP가 아니다. 중복이 없으면 그냥 [[day-22-recursion/concept|분할정복]](병합정렬처럼 저장할 이득이 없음), 부분 구조가 최적이 아니면 DP로 틀린 답이 나온다. 문제를 보면 이 둘부터 확인하라.
> 2. **상태 정의가 DP의 8할.** `dp[i]`가 "정확히 무엇인지" 한 문장으로 못 쓰면 점화식은 절대 못 세운다. "i까지의 최댓값"인지 "i에서 끝나는 최댓값"인지의 미세한 차이가 정답과 오답을 가른다(최대 부분합의 대표 함정).
> 3. **초기값(base case)을 틀리면 전부 틀린다.** `dp[0]`, `dp[1]`을 잘못 두거나, 도달 불가능 상태를 `0`으로 두면(사실은 `inf`여야 하는데) 연쇄적으로 오답. **"불가능/미방문"은 최소화 문제에서 `float('inf')`, 최대화에서 `-inf` 또는 `-1`** 로 명시하라.
> 4. **계산 순서: 의존하는 하위 상태가 먼저 채워져야 한다.** Bottom-Up에서 `dp[i]`가 `dp[i-1]`을 참조하면 i는 오름차순. 격자에서 `dp[r][c]`가 위·왼쪽을 보면 행·열 오름차순. 순서가 어긋나면 아직 안 채운 칸(0)을 읽어 조용히 틀린다.
> 5. **Top-Down 재귀 깊이 폭발.** 상태 깊이가 수만이면 파이썬 기본 재귀 한도(1000)를 넘겨 `RecursionError`. `sys.setrecursionlimit(10**6)`을 올리거나 Bottom-Up으로 전환하라.
> 6. **`@lru_cache` 인자는 반드시 불변(hashable).** 리스트·딕셔너리를 인자로 넘기면 `TypeError: unhashable`. 인덱스나 `tuple`로 바꿔라. 또한 전역 상태(입력 배열)는 인자로 넘기지 말고 클로저/전역으로 참조하는 게 캐시 키를 작게 유지한다.
> 7. **동전 교환 = 그리디로 풀면 틀린다(반례 존재).** 일반 동전 집합에서는 그리디가 최적을 보장하지 못한다. 최소 개수는 DP(`dp[a]=min(dp[a], dp[a-c]+1)`)로 풀어야 하며, **도달 불가능 금액은 `inf`로 유지**해 마지막에 판별한다.
> 8. **공간 최적화는 "점화식 참조 범위" 확인 후에.** `dp[i-1]`만 보면 1차원→변수로 줄일 수 있지만, 경로/부분해 복원이 필요하면 표를 남겨야 한다. 무작정 줄이면 답 추적이 불가능해진다.
> 9. **모듈러 연산 위치.** "경우의 수 % (10^9+7)" 문제는 **누적할 때마다** 나머지를 취해야 오버플로(다른 언어)·요구사항을 만족한다. 파이썬은 오버플로가 없어 방심하기 쉽지만, 문제가 요구하면 반드시 `% MOD`를 넣어라.

> [!example]- 예제 코드 (Examples)
> ```python
> from functools import lru_cache
>
> # (1) 피보나치 - 3가지 구현 비교
> @lru_cache(maxsize=None)
> def fib_topdown(n):
>     if n < 2: return n
>     return fib_topdown(n-1) + fib_topdown(n-2)
>
> def fib_bottomup(n):
>     if n < 2: return n
>     dp = [0]*(n+1); dp[1] = 1
>     for i in range(2, n+1):
>         dp[i] = dp[i-1] + dp[i-2]
>     return dp[n]
>
> def fib_optimized(n):            # O(1) 공간
>     prev, cur = 0, 1
>     for _ in range(n):
>         prev, cur = cur, prev + cur
>     return prev
>
> # (2) 계단 오르기 - 경우의 수 (LeetCode #70)
> def climb_stairs(n):
>     if n <= 2: return n
>     a, b = 1, 2
>     for _ in range(3, n+1):
>         a, b = b, a + b
>     return b
>
> # (3) 집도둑 - 택하거나 건너뛰거나 (LeetCode #198)
> def rob(nums):
>     take, skip = 0, 0            # take: 이전 집을 털었을 때, skip: 안 털었을 때
>     for x in nums:
>         take, skip = skip + x, max(skip, take)
>     return max(take, skip)
>
> # (4) 동전 교환 - 최소 개수 (LeetCode #322) - 그리디로는 틀림!
> def coin_change(coins, amount):
>     INF = float('inf')
>     dp = [0] + [INF]*amount
>     for a in range(1, amount+1):
>         for c in coins:
>             if c <= a:
>                 dp[a] = min(dp[a], dp[a-c] + 1)
>     return dp[amount] if dp[amount] != INF else -1
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 1차원 점화식(피보나치·계단·집도둑)에서 시작해 격자·최대 부분합·동전(배낭 맛보기)·LIS·LCS까지, DP의 대표 유형을 기초→기출로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Fibonacci Number | [LeetCode #509](https://leetcode.com/problems/fibonacci-number/) | 🟢기초 | 1차원 점화식 |
> | 2 | Climbing Stairs | [LeetCode #70](https://leetcode.com/problems/climbing-stairs/) | 🟢기초 | 경우의 수 |
> | 3 | Min Cost Climbing Stairs | [LeetCode #746](https://leetcode.com/problems/min-cost-climbing-stairs/) | 🟢기초 | 최소 비용 |
> | 4 | House Robber | [LeetCode #198](https://leetcode.com/problems/house-robber/) | 🟡중급 | 선택/건너뛰기 |
> | 5 | Maximum Subarray | [LeetCode #53](https://leetcode.com/problems/maximum-subarray/) | 🟡중급 | 최대 부분합(Kadane) |
> | 6 | Unique Paths | [LeetCode #62](https://leetcode.com/problems/unique-paths/) | 🟡중급 | 격자 경로 2D |
> | 7 | Coin Change | [LeetCode #322](https://leetcode.com/problems/coin-change/) | 🟡중급 | 배낭형(무한) |
> | 8 | Longest Increasing Subsequence | [LeetCode #300](https://leetcode.com/problems/longest-increasing-subsequence/) | 🔴심화 | LIS (O(n²)/O(n log n)) |
> | 9 | Longest Common Subsequence | [LeetCode #1143](https://leetcode.com/problems/longest-common-subsequence/) | 🔴심화 | 2차원 문자열 DP |
> | 10 | 정수 삼각형 ^triangle | [프로그래머스 #43105](https://school.programmers.co.kr/learn/courses/30/lessons/43105) | ⚫기출 | 격자 누적 DP |
> | 11 | N으로 표현 | [프로그래머스 #42895](https://school.programmers.co.kr/learn/courses/30/lessons/42895) | ⚫기출 | 집합 DP |
> | 12 | 등굣길 | [프로그래머스 #42898](https://school.programmers.co.kr/learn/courses/30/lessons/42898) | ⚫기출 | 격자 경로 + 모듈러 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근(순진 재귀 vs Top-Down 메모이제이션 vs Bottom-Up 타뷸레이션 vs 공간 최적화)과 복잡도 비교, 그리고 기출 "정수 삼각형·N으로 표현·등굣길"의 상태 정의·점화식 유도: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-30-review/concept|Day 30 — 개념 집중기 종합 복습 (Final Review)]] — 개념 집중기(Phase 0~3)를 마무리하고, 오늘부터 Phase 4 심화의 첫 주제 DP로 진입한다
- ➡️ **다음(next):** [[day-32-dp-knapsack/concept|Day 32 — 배낭 문제 (Knapsack DP)]] — 오늘의 "동전 교환"에서 맛본 아이템 선택 DP를 0/1 배낭·무한 배낭으로 일반화한다
- 🧭 **관련(related):**
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — DP는 "중복 부분 문제가 있는 재귀"에 저장을 얹은 것. Top-Down은 재귀 그대로, 분할정복과의 차이(중복 유무)가 핵심
  - [[day-21-greedy/concept|Day 21 — 그리디]] — 같은 최적화 문제라도 그리디가 실패하는 지점(동전 교환 반례)이 곧 DP가 필요한 신호. 둘의 경계를 이해한다
  - [[day-14-prefix-sum/concept|Day 14 — 누적 합]] — 누적 합은 "덧셈 점화식"을 미리 채워두는 가장 단순한 DP의 일종. dp 배열 채우기의 원형
  - [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — Top-Down DP는 상태 그래프 위의 DFS + 메모. 재귀 깊이 한계·setrecursionlimit이 그대로 적용된다
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — LIS를 O(n log n)으로 푸는 핵심 도구. DP와 이분탐색의 결합 패턴
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — "상태 수 × 전이 비용"으로 DP 복잡도를 계산하는 사고의 토대
  - [[day-32-dp-knapsack/concept|Day 32 — 배낭 문제 (Knapsack DP)]] — DP의 대표 응용. 오늘 배운 상태·점화식 설계를 2차원으로 확장
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]

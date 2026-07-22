---
day: 32
phase: 4-advanced
title: 배낭 문제 (Knapsack DP)
category: [DP, 배낭, 0/1 배낭, 무한 배낭, 부분집합 합]
difficulty: 중급
status: done
prev: "[[day-31-dp/concept|Day 31 — 동적 계획법 입문 (Dynamic Programming)]]"
next: "[[day-33-dp-lis-lcs/concept|Day 33 — 부분 수열 DP (LIS·LCS)]]"
related:
  - "[[day-31-dp/concept|Day 31 — 동적 계획법 입문]]"
  - "[[day-21-greedy/concept|Day 21 — 그리디]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-24-brute-force/concept|Day 24 — 완전 탐색]]"
  - "[[day-05-math/concept|Day 05 — 수학·진법·비트 기초]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-33-dp-lis-lcs/concept|Day 33 — 부분 수열 DP (LIS·LCS)]]"
sources:
  - https://leetcode.com/problems/coin-change/
  - https://leetcode.com/problems/coin-change-ii/
  - https://leetcode.com/problems/partition-equal-subset-sum/
  - https://leetcode.com/problems/target-sum/
  - https://leetcode.com/problems/ones-and-zeroes/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42897
  - https://docs.python.org/3/library/functools.html#functools.lru_cache
tags: [phase/4, topic/dp, topic/knapsack, topic/01-knapsack, topic/unbounded-knapsack, topic/subset-sum]
---

# Day 32 — 배낭 문제 (Knapsack DP)

> [!abstract] 한눈 요약 (TL;DR)
> **배낭 문제(Knapsack Problem)** 는 "**용량(무게)이 정해진 배낭에, 각자 무게와 가치가 있는 물건들을 골라 담아 가치의 합을 최대로**" 만드는 최적화 문제다. [[day-31-dp/concept|Day 31 DP]]에서 배운 "상태 → 점화식 → 초기값 → 순서" 설계를 **2차원으로 확장**하는 첫 관문이자, 코테 DP에서 가장 변형이 많고 자주 나오는 골격이다. 크게 두 종류로 나뉜다 — **① 0/1 배낭(0/1 Knapsack):** 각 물건을 **최대 1번만** 담는다(넣거나 안 넣거나). **② 무한 배낭(Unbounded Knapsack):** 각 물건을 **몇 번이든** 담는다(동전 교환이 대표). 핵심 상태는 **`dp[i][w]` = "i번째 물건까지 고려했고 남은/사용한 용량이 w일 때의 최대 가치"** 이고, 점화식은 **"이 물건을 안 담기 vs 담기 중 큰 값"** 이다. 실전에서는 **1차원 배열로 압축**하는데, 이때 **0/1은 용량을 큰 쪽→작은 쪽(역순)**, **무한은 작은 쪽→큰 쪽(정순)** 으로 도는 **루프 방향**이 정답과 오답을 가른다. "**고정된 예산/용량 안에서 아이템을 골라 최대·최소·개수·가능여부**"가 보이면 배낭을 의심하라 — 부분집합 합(Subset Sum), 동전 조합, 분할 가능 판정이 전부 배낭의 변형이다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **배낭 문제**는 도둑이 배낭 하나를 메고 보석 가게에 들어간 상황이다. 배낭이 버틸 수 있는 무게는 `W`로 정해져 있고, 진열장의 각 보석 `i`는 무게 `weight[i]`와 값어치 `value[i]`가 있다. **무게 한도를 넘지 않으면서 값어치 합을 최대로** 훔치려면 무엇을 담아야 하는가? 이게 배낭 문제다.
>
> **왜 그리디로 안 되나 (0/1의 경우).** "가성비(가치/무게)가 높은 것부터 담자"는 [[day-21-greedy/concept|그리디(Day 21)]]는 물건을 쪼갤 수 있는 **분할 배낭(Fractional Knapsack)** 에서만 최적이다. 물건을 **통째로만** 담아야 하는 **0/1 배낭**에서는 그리디가 틀린다 — 가성비 1등만 담으면 배낭에 애매한 빈 공간이 남아, 가성비는 낮아도 딱 맞는 조합을 놓칠 수 있다. "지금의 최선이 나중에 손해"인 전형적 상황이라 **DP가 필요**하다.
>
> **일상 비유 — 여행 가방 싸기.** 무게 제한 20kg 캐리어에 짐을 넣는다. 노트북(무겁지만 필수), 책 몇 권, 옷... 각 짐을 "넣을까 뺄까"를 모든 조합으로 따지면 물건이 30개만 돼도 2^30(약 10억) 경우다. 대신 **"몇 번째 짐까지 봤고, 남은 무게가 얼마"** 를 상태로 잡아 표에 적어두면, 같은 (짐 번호, 남은 무게) 상황을 딱 한 번만 계산한다. 이 표가 배낭 DP다.
>
> **0/1 vs 무한 — 진열장 vs 자판기.** **0/1 배낭**은 진열장의 보석처럼 각 물건이 **딱 하나**뿐이라 한 번 담으면 끝이다. **무한 배낭**은 자판기의 동전처럼 **같은 종류를 몇 번이든** 쓸 수 있다. [[day-31-dp/concept|Day 31]]의 동전 교환(Coin Change)이 바로 무한 배낭이었다. 이 "한 번만 vs 무제한"의 차이가 **1차원 압축 시 루프 방향**으로 그대로 드러난다(아래 동작 원리 참고).

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 0/1 배낭 — 2차원 표 (가장 직관적).**
> 상태 `dp[i][w]` = "물건 `1..i`까지만 고려하고, 배낭 용량이 `w`일 때 담을 수 있는 최대 가치".
> 물건 `i`(무게 `wt`, 가치 `val`)에 대해 두 선택이 있다:
> ```
> dp[i][w] = max(
>     dp[i-1][w],                    # (1) i를 안 담는다 -> 위 칸 그대로
>     dp[i-1][w-wt] + val   (w>=wt)  # (2) i를 담는다 -> wt만큼 비운 이전 상태 + val
> )
> ```
> 표를 물건 순서(i)로, 각 행에서 용량(w)순으로 채운다. 답은 `dp[N][W]`.
> ```
>        w=0  1   2   3   4   5      (예: W=5, 물건 {무게,가치}={(2,3),(3,4),(4,5),(5,6)})
>  i=0    0   0   0   0   0   0      <- 물건 0개: 전부 0 (초기값)
>  i=1    0   0   3   3   3   3      <- (2,3) 담으면 w>=2부터 3
>  i=2    0   0   3   4   4   7      <- (3,4) 추가: w=5 -> 3+4=7
>  i=3    0   0   3   4   5   7      <- (4,5) 추가
>  i=4    0   0   3   4   5   7      <- (5,6) 추가: 6<7 이라 갱신 안 됨 -> 답 7
> ```
>
> **(B) 0/1 배낭 — 1차원 압축 + 역순 루프 (실전형).**
> `dp[i]`는 `dp[i-1]`만 참조하므로 행 하나(`dp[w]`)로 줄인다. 단, **용량 w를 큰 쪽에서 작은 쪽으로(역순)** 돌아야 한다.
> ```
> dp = [0]*(W+1)
> for wt, val in items:
>     for w in range(W, wt-1, -1):       # 역순!  W, W-1, ..., wt
>         dp[w] = max(dp[w], dp[w-wt] + val)
> ```
> **왜 역순인가:** 정순으로 돌면 방금 갱신한 `dp[w-wt]`(같은 물건이 이미 들어간 값)를 다시 참조해 **같은 물건을 여러 번 담게 된다.** 역순이면 `dp[w-wt]`가 아직 "이전 물건까지의 값"이라 물건 `i`가 딱 한 번만 반영된다.
>
> **(C) 무한 배낭 — 1차원 + 정순 루프.**
> 같은 물건을 여러 번 담아야 하므로, 0/1과 정반대로 **용량을 작은 쪽에서 큰 쪽으로(정순)** 돈다.
> ```
> dp = [0]*(W+1)
> for wt, val in items:
>     for w in range(wt, W+1):           # 정순!  wt, wt+1, ..., W
>         dp[w] = max(dp[w], dp[w-wt] + val)
> ```
> 정순이면 방금 물건 `i`를 담아 갱신한 `dp[w-wt]`를 같은 물건 `i`가 또 참조 -> 자연스럽게 무제한 사용이 표현된다. **[[day-31-dp/concept|Day 31]]의 Coin Change가 이 구조**였다(가치 대신 개수).
>
> **(D) 부분집합 합 (Subset Sum) — 가치=무게인 0/1 배낭.**
> "어떤 부분집합의 합이 정확히 T가 되는가?"는 `value=weight`이고 `bool`을 채우는 0/1 배낭이다. LeetCode 'Partition Equal Subset Sum', 'Target Sum'이 이 변형.
> ```
> dp = [False]*(T+1); dp[0] = True
> for x in nums:
>     for s in range(T, x-1, -1):        # 0/1이므로 역순
>         dp[s] = dp[s] or dp[s-x]
> ```
>
> **(E) 설계 절차 요약 — 배낭 4문(問).**
> 1. **물건이 무엇, 용량 축이 무엇인가?** (짐/무게, 동전/금액, 숫자/합...)
> 2. **각 물건을 몇 번 쓰나?** 1번 -> 0/1(역순), 무제한 -> 무한(정순).
> 3. **무엇을 최적화하나?** 최대/최소 가치 -> `max`/`min`, 개수 -> `+= dp[w-wt]`, 가능여부 -> `or`.
> 4. **초기값:** 가치형 `dp[0]=0`(나머지 0 또는 -inf), 가능여부형 `dp[0]=True`, 개수형 `dp[0]=1`.
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> 배낭도 DP 공식 **`상태 개수 × 전이 비용`** 을 그대로 따른다. 상태가 `(물건 N개 × 용량 W)`이고 전이는 O(1)이므로 **시간 O(N×W)**.
>
> | 변형 | 상태 | 시간 | 공간 | 비고 |
> |---|---|---|---|---|
> | 0/1 배낭 (2D) | O(N×W) | O(N×W) | O(N×W) | 선택 복원 가능 |
> | 0/1 배낭 (1D 역순) | O(N×W) | O(N×W) | **O(W)** | 실전 표준 |
> | 무한 배낭 (1D 정순) | O(N×W) | O(N×W) | O(W) | 동전 교환류 |
> | 부분집합 합 | O(N×T) | O(N×T) | O(T) | bool/count |
> | 2D 배낭 (Ones&Zeroes) | O(L×M×N) | O(L×M×N) | O(M×N) | 제약 2개 |
>
> > **의사 다항 시간(pseudo-polynomial)에 주의.** O(N×W)는 "다항식처럼" 보이지만 **W(용량)는 입력의 값**이지 개수가 아니다. W가 10^9처럼 크면 N이 작아도 표가 터진다. 이런 문제는 배낭 DP가 아니라 다른 접근(그리디/수학/[[day-24-brute-force/concept|meet-in-the-middle]])을 써야 한다. **"용량·금액 범위"를 먼저 확인**하는 습관이 중요하다.
> >
> > **W가 커서 배열이 크면 메모리부터 본다.** 1D 압축(O(W))이 기본이고, 값이 커 오버플로가 걱정되면([[day-05-math/concept|Day 05]]) 파이썬은 안전하지만 다른 언어는 주의. "경우의 수" 카운팅형은 `% (10^9+7)`가 붙는 경우가 많다.
> >
> > **완전탐색과 비교.** 0/1 배낭을 [[day-24-brute-force/concept|완전 탐색]]으로 풀면 각 물건 넣/뺌의 O(2^N). N=40이면 약 10^12로 사실상 불가. 배낭 DP는 O(N×W)로 끌어내린다 — 단 W가 감당 가능할 때만.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **루프 방향이 전부다.** 0/1이면 용량 **역순**, 무한이면 **정순**. 이 한 줄을 외워두면 배낭 절반은 끝난다. 헷갈리면 "같은 물건을 또 쓰면 안 되니까(0/1) 아직 안 건드린 뒤쪽(역순)부터"라고 되뇌라.
>   - 참고: [Coin Change II (LeetCode, 무한 배낭 카운팅)](https://leetcode.com/problems/coin-change-ii/)
> - **"조합 vs 순열" 카운팅 함정.** 개수를 셀 때 **물건 루프를 바깥, 용량 루프를 안쪽**에 두면 **조합**(순서 무시, `{1,2}=={2,1}`)을 센다. 반대로 두면 **순열**(순서 구분)을 센다. Coin Change II(조합)와 Combination Sum IV(순열)의 차이가 정확히 이 루프 순서다.
> - **가치=무게로 두면 부분집합 합.** "합이 T가 되는 부분집합이 있나/몇 개인가"는 배낭의 특수형이다. Target Sum은 `+/-` 부호 문제를 `(총합+target)/2`짜리 부분집합 합으로 **변환**하는 게 정석이다.
> - **먼저 2D로 정확히 푼 뒤 1D로 압축하라.** 처음부터 1D 역순/정순을 외워 쓰면 실수하기 쉽다. Day 31처럼 "완전탐색 재귀 -> `@lru_cache` -> 2D 표 -> 1D 압축" 순으로 신뢰도를 쌓아라.
> - **선택 복원이 필요하면 표를 남겨라.** "무엇을 담았는지"까지 물으면 1D로 못 줄인다. 2D 표를 두고 `dp[i][w] != dp[i-1][w]`이면 i를 담은 것으로 역추적한다.
> - **`@lru_cache` Top-Down도 좋은 무기.** `knap(i, w)`를 인덱스와 남은 용량으로 재귀하면 점화식과 1:1이다. 단 [[day-31-dp/concept|Day 31]]처럼 인자는 불변(정수)이어야 하고 재귀 깊이·캐시 크기를 신경 쓴다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **0/1 = 역순, 무한 = 정순.** 1차원 배낭에서 이 방향을 바꾸면 "물건을 몇 번 쓰는가"가 뒤바뀌어 **조용히 틀린 답**이 나온다(에러가 안 나서 더 위험). 방향을 바꾸는 순간 문제 자체가 달라진다는 걸 기억하라.
> 2. **그리디로 0/1 배낭을 풀면 틀린다.** 가성비 정렬 그리디는 **분할 가능(fractional)** 배낭에서만 최적이다. 통째로만 담는 0/1은 반드시 DP. 이는 [[day-21-greedy/concept|그리디(Day 21)]]가 실패하는 대표 사례다.
> 3. **의사 다항(pseudo-polynomial) 함정.** O(N×W)의 W는 **값**이다. 용량·금액이 10^8~10^9이면 배열이 메모리를 초과하거나 시간 초과다. **"범위부터 확인"** — 큰 값이면 배낭 DP가 정답이 아니다.
> 4. **초기값이 목적에 따라 다르다.** 최대 가치형은 보통 `dp=[0]*(W+1)`(빈 배낭 가치 0). "정확히 용량 W를 꽉 채워야" 하면 `dp[0]=0, 나머지=-inf`로 두고 도달 불가를 구분해야 한다. 가능여부는 `dp[0]=True`, 개수는 `dp[0]=1`. **초기값을 잘못 두면 전 칸이 연쇄 오답.**
> 5. **카운팅은 조합/순열 루프 순서를 명시하라.** "몇 가지 방법"에서 순서를 구분하는지가 문제마다 다르다. Coin Change II(조합)는 동전 바깥·금액 안쪽. 순서를 뒤집으면 값이 달라진다 — 문제 정의를 다시 읽어라.
> 6. **모듈러 위치.** 경우의 수는 커지므로 `% (10^9+7)`가 요구되면 **누적 덧셈마다** 취한다. 파이썬은 큰 정수라 방심하기 쉽지만 문제가 요구하면 반드시 넣는다([[day-31-dp/concept|Day 31]] 등굣길 참고).
> 7. **부분집합 합 변환 실수.** Target Sum에서 `(sum+target)`이 **홀수이거나 음수**면 답은 0이다(정수 부분집합이 불가능). 변환 전에 이 예외를 반드시 처리하라 — 놓치면 잘못된 T로 배낭을 돌려 틀린다.
> 8. **다차원 제약은 차원을 늘린다.** 제약이 2개(0의 개수·1의 개수 등)면 `dp[m][n]`처럼 축을 추가한다. Ones and Zeroes가 대표. 각 물건마다 두 용량 축을 모두 역순으로 돌려야 0/1이 유지된다.
> 9. **도둑질(원형)은 배낭이 아니라 선택 DP지만 함정이 같다.** 원형 배열은 "첫 집 포함/제외"로 두 번 [[day-31-dp/concept|House Robber]]를 돌려 max를 취한다 — 경계 처리를 빼먹으면 인접 규칙이 깨진다.

> [!example]- 예제 코드 (Examples)
> ```python
> # (1) 0/1 배낭 - 2차원 표 (직관형)
> def knapsack_2d(weights, values, W):
>     n = len(weights)
>     dp = [[0]*(W+1) for _ in range(n+1)]
>     for i in range(1, n+1):
>         wt, val = weights[i-1], values[i-1]
>         for w in range(W+1):
>             dp[i][w] = dp[i-1][w]                      # 안 담기
>             if w >= wt:
>                 dp[i][w] = max(dp[i][w], dp[i-1][w-wt] + val)  # 담기
>     return dp[n][W]
>
> # (2) 0/1 배낭 - 1차원 역순 (실전형)
> def knapsack_01(weights, values, W):
>     dp = [0]*(W+1)
>     for wt, val in zip(weights, values):
>         for w in range(W, wt-1, -1):                   # 역순!
>             dp[w] = max(dp[w], dp[w-wt] + val)
>     return dp[W]
>
> # (3) 무한 배낭 - 1차원 정순
> def knapsack_unbounded(weights, values, W):
>     dp = [0]*(W+1)
>     for wt, val in zip(weights, values):
>         for w in range(wt, W+1):                       # 정순!
>             dp[w] = max(dp[w], dp[w-wt] + val)
>     return dp[W]
>
> # (4) 부분집합 합 - 합 T를 만들 수 있는가 (가치=무게, bool)
> def subset_sum(nums, T):
>     dp = [False]*(T+1); dp[0] = True
>     for x in nums:
>         for s in range(T, x-1, -1):                    # 0/1 역순
>             dp[s] = dp[s] or dp[s-x]
>     return dp[T]
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 무한 배낭(동전) -> 0/1 배낭(부분집합 합) -> 다차원 배낭 -> 기출(원형 선택 DP) 순으로, 배낭의 대표 변형을 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Coin Change | [LeetCode #322](https://leetcode.com/problems/coin-change/) | 🟢기초 | 무한 배낭(최소 개수) — Day 31 복습 |
> | 2 | Coin Change II | [LeetCode #518](https://leetcode.com/problems/coin-change-ii/) | 🟡중급 | 무한 배낭(조합 카운팅) |
> | 3 | Partition Equal Subset Sum | [LeetCode #416](https://leetcode.com/problems/partition-equal-subset-sum/) | 🟡중급 | 0/1 부분집합 합(가능여부) |
> | 4 | Target Sum | [LeetCode #494](https://leetcode.com/problems/target-sum/) | 🔴심화 | 0/1 부분집합 합(카운팅+변환) |
> | 5 | Ones and Zeroes | [LeetCode #474](https://leetcode.com/problems/ones-and-zeroes/) | 🔴심화 | 2차원 0/1 배낭(제약 2개) |
> | 6 | 도둑질 | [프로그래머스 #42897](https://school.programmers.co.kr/learn/courses/30/lessons/42897) | ⚫기출 | 원형 선택 DP(House Robber 응용) |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 배낭 유형 판별(0/1 vs 무한), 루프 방향, 부분집합 합 변환, 다차원 확장, 그리고 원형 배열 처리(도둑질)의 상태 정의·점화식: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-31-dp/concept|Day 31 — 동적 계획법 입문 (Dynamic Programming)]] — DP의 "상태 → 점화식 → 초기값 → 순서" 4단계와 동전 교환(무한 배낭 맛보기)을 오늘 2차원 배낭으로 일반화한다
- ➡️ **다음(next):** [[day-33-dp-lis-lcs/concept|Day 33 — 부분 수열 DP (LIS·LCS)]] — 배낭이 "어떤 아이템을 담나"라면, 다음은 "어떤 순서·부분 수열을 고르나"로 DP를 확장한다
- 🧭 **관련(related):**
  - [[day-31-dp/concept|Day 31 — 동적 계획법 입문]] — 배낭은 DP 설계 4단계를 2차원으로 확장한 대표 응용. 동전 교환이 바로 무한 배낭이었다
  - [[day-21-greedy/concept|Day 21 — 그리디]] — 분할 배낭은 그리디가 최적이지만 0/1 배낭은 그리디가 틀린다. 둘의 경계를 이해하는 핵심 사례
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — Top-Down 배낭 `knap(i, w)`는 재귀 + 메모. 완전탐색 재귀에서 출발해 DP로 다듬는 정석 루트
  - [[day-24-brute-force/concept|Day 24 — 완전 탐색]] — 배낭의 순진한 해법은 넣/뺌 2^N 완전탐색. DP가 이를 O(N×W)로 줄이는 대비를 이해한다
  - [[day-05-math/concept|Day 05 — 수학·진법·비트 기초]] — 아이템 부분집합은 비트마스크로도 표현 가능(작은 N). 카운팅 시 모듈러 연산의 토대
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — "상태 수 × 전이"로 O(N×W)를 계산하고, 의사 다항 시간(W=값)의 함정을 판별하는 사고의 토대
  - [[day-33-dp-lis-lcs/concept|Day 33 — 부분 수열 DP (LIS·LCS)]] — 배낭과 함께 코테 DP의 양대 골격. 2차원 문자열 DP로 이어진다
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]

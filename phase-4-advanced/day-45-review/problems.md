# Day 45 연습문제 — Phase 4 심화 종합 복습 (Advanced Review)

> 출처는 **프로그래머스 / LeetCode만** 사용합니다.
> 난이도: 🟢기초 · 🟡중급 · 🔴심화 · ⚫기출
> 정답 코드 → [solutions.py](solutions.py) · 개념 → [concept.md](concept.md)

## 이 세트를 푸는 방법 (중요)

오늘은 **기법을 훈련하는 날이 아니라 "판단"을 훈련하는 날**입니다. Day 31~44 전 범위를 섞었고,
**지난 14일 동안 한 번도 나오지 않은 문제들만** 골랐습니다 — 답을 기억하는 것이 아니라
**판단을 재현하는지**를 확인해야 하기 때문입니다.

**각 문제마다 코드를 쓰기 전에 아래 4줄을 먼저 적으세요.**

```
  1) 제약:        N 은 최대 몇인가? 질의 수 Q 는? 값의 범위는?
  2) 허용 복잡도:  그래서 O(?) 안에 끝내야 하는가?
  3) 도구 후보:    구조 신호(선후관계/연결성/접두사/구간질의...)로 무엇이 떠오르나?
  4) 전제 확인:    음수 간선? 갱신이 있나? 사이클이 있나? 재귀 깊이는?
```

**"복습 Day" 칸은 먼저 풀어 본 뒤에 확인하세요.** 미리 보면 판단 훈련이 되지 않습니다.

## 문제 목록

| # | 문제 | 출처 | 난이도 | 복습 Day |
|---|---|---|---|---|
| 1 | Coin Change | [LeetCode #322](https://leetcode.com/problems/coin-change/) | 🟢기초 | Day 31·32 (DP·무한 배낭) |
| 2 | Longest Common Subsequence | [LeetCode #1143](https://leetcode.com/problems/longest-common-subsequence/) | 🟢기초 | Day 33 (LCS) |
| 3 | Longest Increasing Subsequence | [LeetCode #300](https://leetcode.com/problems/longest-increasing-subsequence/) | 🟡중급 | Day 33·18 (LIS·이분) |
| 4 | 배달 | [프로그래머스 #12978](https://school.programmers.co.kr/learn/courses/30/lessons/12978) | 🟡중급 | Day 34 (다익스트라) |
| 5 | Network Delay Time | [LeetCode #743](https://leetcode.com/problems/network-delay-time/) | 🟡중급 | Day 34·35 (최단 경로 3형제) |
| 6 | Number of Provinces | [LeetCode #547](https://leetcode.com/problems/number-of-provinces/) | 🟢기초 | Day 36 (유니온파인드) |
| 7 | 섬 연결하기 | [프로그래머스 #42861](https://school.programmers.co.kr/learn/courses/30/lessons/42861) | 🟡중급 | Day 37 (MST) |
| 8 | Longest Increasing Path in a Matrix | [LeetCode #329](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | 🔴심화 | Day 38 (DAG·위상 정렬 DP) |
| 9 | Replace Words | [LeetCode #648](https://leetcode.com/problems/replace-words/) | 🟡중급 | Day 39 (트라이) |
| 10 | Create Sorted Array through Instructions | [LeetCode #1649](https://leetcode.com/problems/create-sorted-array-through-instructions/) | 🔴심화 | Day 40 (펜윅) |
| 11 | Smallest Sufficient Team | [LeetCode #1125](https://leetcode.com/problems/smallest-sufficient-team/) | 🔴심화 | Day 41 (비트마스크 DP) |
| 12 | Longest Happy Prefix | [LeetCode #1392](https://leetcode.com/problems/longest-happy-prefix/) | 🔴심화 | Day 42 (KMP 실패 함수) |
| 13 | Minimum Time to Collect All Apples in a Tree | [LeetCode #1443](https://leetcode.com/problems/minimum-time-to-collect-all-apples-in-a-tree/) | 🟡중급 | Day 43·44 (트리 DP) |

---

## 1. Coin Change 🟢

**출처:** [LeetCode #322](https://leetcode.com/problems/coin-change/)

서로 다른 액면가의 동전 배열 `coins`와 목표 금액 `amount`가 주어진다.
그 금액을 만드는 데 필요한 **동전의 최소 개수**를 반환하라. 만들 수 없으면 `-1`.

**각 동전은 무한히 많다고 가정한다.**

**예시:**
- `coins = [1,2,5], amount = 11` → **`3`** (`5 + 5 + 1`)
- `coins = [2], amount = 3` → `-1`
- `coins = [1], amount = 0` → `0`

**제약:** `1 <= coins.length <= 12`, `1 <= coins[i] <= 2^31 - 1`, `0 <= amount <= 10^4`.

**시그니처 (LeetCode):**
```python
class Solution:
    def coinChange(self, coins: 'List[int]', amount: int) -> int: ...
```

> [!tip]- 힌트 1 (제약을 먼저 읽어라)
> `coins.length <= 12`를 보면 **비트마스크(`2^12`)** 가 떠오를 수 있지만, 여기서는 **동전을 여러 번 쓸 수 있으므로 "어떤 동전을 골랐나"는 상태가 아니다.** 진짜 상태는 **"남은 금액"** 이고, 그 범위가 `amount <= 10^4`다.
> ```
>   상태 크기 = 10^4,  전이 = 동전 12개
>   -> O(amount * len(coins)) = 1.2 * 10^5   즉시 통과
> ```
> **`N`이 작다고 무조건 비트마스크가 아니다.** "무엇이 상태인가"를 먼저 물어라.

> [!tip]- 힌트 2 (이것은 무한 배낭이다)
> "각 동전을 무한히 쓸 수 있다" = **무한 배낭(unbounded knapsack)**. [[day-32-dp-knapsack/concept|Day 32]]의 규칙을 그대로 적용한다.
> ```
>   dp[x] = 금액 x 를 만드는 최소 동전 개수
>   dp[0] = 0,  나머지는 INF
>
>   for c in coins:
>       for x in range(c, amount+1):        <- 정순! (무한 배낭)
>           dp[x] = min(dp[x], dp[x-c] + 1)
>
>   0/1 배낭이었다면 역순(reversed) 이어야 했다. 방향 하나가 문제를 바꾼다.
> ```
> 답이 `INF`로 남아 있으면 `-1`을 반환한다.

> [!tip]- 힌트 3 (BFS 로도 풀린다)
> **"최소 개수"** 는 **간선 가중치가 전부 1인 최단 경로**와 같다. 금액을 정점으로 보고 동전을 간선으로 보면 **BFS 층 탐색**이 그대로 답이다([[day-26-bfs/concept|Day 26]]).
> ```
>   레벨 0: {amount}
>   레벨 1: {amount - c  for c in coins}
>   ...  0 에 처음 도달한 레벨이 답
> ```
> **DP와 BFS가 같은 답을 준다** — 교차 검증에 쓰기 좋다.

---

## 2. Longest Common Subsequence 🟢

**출처:** [LeetCode #1143](https://leetcode.com/problems/longest-common-subsequence/)

두 문자열 `text1`, `text2`가 주어진다. 둘의 **최장 공통 부분 수열(LCS)** 의 길이를 반환하라.
공통 부분 수열이 없으면 `0`.

**부분 수열(subsequence)** 은 원래 문자열에서 일부 문자를 지우되 **남은 문자들의 상대 순서는 유지**한 문자열이다.

**예시:**
- `text1 = "abcde", text2 = "ace"` → **`3`** (`"ace"`)
- `text1 = "abc", text2 = "abc"` → `3`
- `text1 = "abc", text2 = "def"` → `0`

**제약:** `1 <= text1.length, text2.length <= 1000`, 소문자 영문만.

**시그니처 (LeetCode):**
```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int: ...
```

> [!tip]- 힌트 1 (제약이 O(N*M) 을 허용한다)
> `1000 * 1000 = 10^6`. **2차원 DP가 정확히 들어맞는 크기**다. 제약이 `10^5`였다면 다른 접근을 찾아야 했다.

> [!tip]- 힌트 2 (상태와 전이)
> ```
>   dp[i][j] = text1[:i] 와 text2[:j] 의 LCS 길이
>
>   마지막 문자가 같으면:  dp[i][j] = dp[i-1][j-1] + 1
>                          (둘 다 쓰는 것이 항상 이득 - 증명 가능)
>   다르면:                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
>                          (둘 중 하나를 버린다)
> ```
> **부분 문자열(substring)이 아니라 부분 수열(subsequence)** 이라는 점을 놓치지 마라. 연속일 필요가 없어서 `dp[i-1][j]`, `dp[i][j-1]`을 함께 봐야 한다.

> [!tip]- 힌트 3 (공간을 O(min(N,M)) 로)
> `dp[i][j]`는 **바로 윗 행만** 참조한다. 두 행(`prev`, `cur`)만 유지하면 공간이 `O(M)`이 된다.
> 그리고 **짧은 쪽을 열(column)로 두면** `O(min(N,M))`이다. 면접에서 "공간을 줄여 보라"는 후속 질문의 표준 답이다.

---

## 3. Longest Increasing Subsequence 🟡

**출처:** [LeetCode #300](https://leetcode.com/problems/longest-increasing-subsequence/)

정수 배열 `nums`가 주어진다. **가장 긴 엄격 증가(strictly increasing) 부분 수열**의 길이를 반환하라.

**예시:**
- `nums = [10,9,2,5,3,7,101,18]` → **`4`** (`[2,3,7,101]`)
- `nums = [0,1,0,3,2,3]` → `4`
- `nums = [7,7,7,7,7,7,7]` → `1` (엄격 증가이므로 같은 값은 이어지지 않는다)

**제약:** `1 <= nums.length <= 2500`, `-10^4 <= nums[i] <= 10^4`.
**Follow-up:** `O(n log n)` 으로 풀 수 있는가?

**시그니처 (LeetCode):**
```python
class Solution:
    def lengthOfLIS(self, nums: 'List[int]') -> int: ...
```

> [!tip]- 힌트 1 (제약이 두 답을 모두 허용한다 - 그래서 좋은 복습 문제다)
> `N <= 2500`이면 `O(N^2) = 6.25 * 10^6`으로 **통과한다.** 그런데 follow-up이 `O(n log n)`을 요구한다.
> **같은 문제에 두 개의 답이 있고, 제약이 어느 쪽을 허용하는지 판단하는 훈련**이 오늘의 목적이다.
> 만약 `N <= 10^5`였다면 `O(N^2) = 10^10`으로 **즉사**했을 것이다.

> [!tip]- 힌트 2 (O(N^2) DP)
> ```
>   dp[i] = i 에서 "끝나는" LIS 의 길이
>   dp[i] = 1 + max( dp[j] for j < i if nums[j] < nums[i] )   (없으면 1)
>   답 = max(dp)
>
>   "i 에서 끝나는" 으로 정의하는 것이 핵심이다.
>   "i 까지의 최대" 로 정의하면 전이를 쓸 수 없다.
> ```
> 이 버전은 **역추적으로 실제 수열을 복원**하기 쉽다.

> [!tip]- 힌트 3 (O(N log N) - tails 배열)
> ```
>   tails[k] = "길이 k+1 인 증가 수열들" 중 마지막 값의 최솟값
>   tails 는 항상 정렬 상태를 유지한다 -> 이분 탐색이 가능하다
>
>   각 x 에 대해:
>     i = bisect_left(tails, x)     <- 엄격 증가면 left, 비감소면 right
>     i == len(tails) 면 append,  아니면 tails[i] = x
>
>   답 = len(tails)
> ```
> **⚠️ `tails` 배열 자체는 답이 되는 수열이 아니다.** 길이만 맞다.
> 실제 수열을 복원하려면 **각 원소가 들어간 위치 `i`를 기록**해 두고 뒤에서부터 역추적해야 한다.
> **면접에서 가장 자주 파고드는 지점**이다.

---

## 4. 배달 🟡

**출처:** [프로그래머스 #12978](https://school.programmers.co.kr/learn/courses/30/lessons/12978)

`N`개의 마을이 `1`번부터 `N`번까지 번호로 구분된다. 각 마을은 양방향 도로로 연결되어 있고
각 도로에는 이동에 걸리는 시간이 있다.

**1번 마을에 있는 음식점**에서 배달을 하는데, **`K` 시간 이하로 배달이 가능한 마을**에서만 주문을 받는다.
마을 개수 `N`, 도로 정보 `road`, 시간 `K`가 주어질 때 **주문을 받을 수 있는 마을의 개수**를 반환하라.

**예시:**
- `N = 5`, `road = [[1,2,1],[2,3,3],[5,2,2],[1,4,2],[5,3,1],[5,4,2]]`, `K = 3` → **`4`**
  (1번은 0, 2번은 1, 4번은 2, 5번은 3 → 4개. 3번은 4가 걸려 제외)

**제약:**
- 마을 개수 `N`은 `1` 이상 `50` 이하.
- `road`의 길이는 `1` 이상 `2,000` 이하.
- `road`의 각 원소는 `[a, b, c]` — a번과 b번 마을을 잇는 도로의 시간이 c.
- **두 마을을 잇는 도로가 여러 개일 수 있다.**
- `K`는 `1` 이상 `500,000` 이하.

**시그니처 (프로그래머스):**
```python
def solution(N, road, K):
    ...
```

> [!tip]- 힌트 1 (제약을 읽으면 도구가 두 개 보인다)
> ```
>   N <= 50 !!
>
>   -> 플로이드-워셜: O(N^3) = 125,000        코드가 가장 짧다
>   -> 다익스트라:    O(E log V) = 2000*6     역시 즉시
>
>   둘 다 통과한다. 이럴 때는 "짧고 틀리기 어려운" 쪽이 실전 정답이다.
> ```
> **`V <= 100` 정도면 플로이드-워셜이 거의 항상 이긴다** — 3중 루프 하나면 끝이고,
> 인접 리스트를 만들 필요도, 힙을 다룰 필요도 없다.

> [!tip]- 힌트 2 (중복 간선 함정)
> 제약에 **"두 마을을 잇는 도로가 여러 개일 수 있다"** 가 명시되어 있다.
> ```
>   인접 행렬을 쓴다면:  mat[a][b] = min(mat[a][b], c)      <- 반드시 min!
>                        그냥 대입하면 나중 것이 덮어써서 틀린다
>   인접 리스트를 쓴다면: 전부 넣어도 다익스트라가 알아서 최소를 고른다
> ```
> **이 한 줄이 이 문제의 진짜 함정**이다.

> [!tip]- 힌트 3 (1-based / 0-based)
> 프로그래머스는 마을 번호가 **1번부터**다. 배열을 `N+1` 크기로 잡거나 입력을 읽는 즉시 `-1`로 통일하라.
> **1-based와 0-based를 섞는 것이 프로그래머스 문제 최다 실수**다.

---

## 5. Network Delay Time 🟡

**출처:** [LeetCode #743](https://leetcode.com/problems/network-delay-time/)

`n`개의 노드가 `1`부터 `n`까지 번호로 주어진다. `times[i] = (u, v, w)`는
**노드 `u`에서 `v`로 신호가 가는 데 `w` 시간이 걸린다**는 뜻이다(**방향 간선**).

노드 `k`에서 신호를 보낼 때 **모든 노드가 신호를 받는 데 걸리는 최소 시간**을 반환하라.
모든 노드에 도달할 수 없으면 `-1`.

**예시:**
- `times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2` → **`2`**
- `times = [[1,2,1]], n = 2, k = 1` → `1`
- `times = [[1,2,1]], n = 2, k = 2` → `-1`

**제약:** `1 <= k <= n <= 100`, `1 <= times.length <= 6000`, `1 <= w <= 100`, **`w >= 1`(음수 없음)**.

**시그니처 (LeetCode):**
```python
class Solution:
    def networkDelayTime(self, times: 'List[List[int]]', n: int, k: int) -> int: ...
```

> [!tip]- 힌트 1 (답의 정체)
> "모든 노드가 받는 데 걸리는 시간" = **`k`에서 각 노드까지의 최단 거리 중 최댓값**이다.
> ```
>   dist = 최단 거리 배열
>   답 = max(dist)  단, INF 가 하나라도 있으면 -1
> ```
> **최댓값**이라는 점을 놓치고 합을 구하는 실수가 흔하다.

> [!tip]- 힌트 2 (세 가지 도구가 전부 통과한다 - 오늘의 핵심 연습)
> `n <= 100`, `E <= 6000`, **가중치는 모두 양수**.
> ```
>   다익스트라:     O(E log V) = 6000 * 7 = 4.2e4     가장 빠르다
>   벨만-포드:      O(V*E) = 100 * 6000 = 6e5         통과
>   플로이드-워셜:  O(V^3) = 10^6                      통과 (코드 최단)
>
>   -> 세 개를 전부 짜 보고 답이 같은지 대조하라.
>      이것이 오늘 이 문제를 고른 이유다.
> ```
> **실전이라면?** 가중치가 양수이고 출발점이 하나이므로 **다익스트라가 정답**이다.
> 플로이드는 `V=100`이라 통과하지만, `V`가 조금만 커져도 죽는다.

> [!tip]- 힌트 3 (도달 불가 처리)
> `dist`에 `INF`가 남아 있으면 `-1`. **`max(dist)`를 구한 뒤 `INF`인지 검사**하는 순서가 깔끔하다.
> 노드 번호가 **1-based**라는 것도 잊지 마라(배열은 `n+1` 크기).

---

## 6. Number of Provinces 🟢

**출처:** [LeetCode #547](https://leetcode.com/problems/number-of-provinces/)

`n`개의 도시가 있고, 일부는 서로 연결되어 있다.
**province(주)** 는 **직접 또는 간접적으로 연결된 도시들의 그룹**이며, 그룹 밖의 도시와는 연결되지 않는다.

`n x n` 행렬 `isConnected`가 주어진다. `isConnected[i][j] = 1`이면 `i`번과 `j`번 도시가 직접 연결된 것이다.
**province의 총 개수**를 반환하라.

**예시:**
- `isConnected = [[1,1,0],[1,1,0],[0,0,1]]` → **`2`** (`{0,1}`, `{2}`)
- `isConnected = [[1,0,0],[0,1,0],[0,0,1]]` → `3`

**제약:** `1 <= n <= 200`, `isConnected[i][i] == 1`, `isConnected[i][j] == isConnected[j][i]`.

**시그니처 (LeetCode):**
```python
class Solution:
    def findCircleNum(self, isConnected: 'List[List[int]]') -> int: ...
```

> [!tip]- 힌트 1 (위장 단어를 알아보라)
> **"직접 또는 간접적으로 연결된 그룹의 개수"** = **연결 요소(connected component)의 개수**다.
> 이 문장을 보면 즉시 두 도구가 떠올라야 한다:
> ```
>   [1] 유니온파인드:  간선을 전부 union 하고 남은 그룹 수를 센다   (Day 36)
>   [2] DFS/BFS:       방문 안 한 정점에서 탐색을 시작한 횟수        (Day 25/26)
> ```
> **둘 다 `O(N^2)`** (인접 행렬을 훑어야 하므로). `N <= 200`이면 `4 * 10^4`, 즉시 통과.

> [!tip]- 힌트 2 (유니온파인드로 세는 법)
> 그룹 개수를 **매번 `find`로 세지 마라.** DSU에 카운터를 두고 **union이 성공할 때마다 1씩 줄이는** 것이 정석이다.
> ```
>   count = n 으로 시작
>   union(a, b) 이 True 를 반환할 때만  count -= 1
>   (이미 같은 그룹이면 False -> 줄이지 않는다)
> ```
> 이 패턴은 **"간선을 추가하며 그룹 수를 추적"** 하는 모든 문제에 그대로 쓰인다.

> [!tip]- 힌트 3 (어느 쪽을 고를까)
> 이 문제만 놓고 보면 **DFS가 더 짧다.** 유니온파인드는 클래스를 써야 하니 코드가 길다.
> 하지만 **간선이 하나씩 추가되면서 그때그때 그룹 수를 물어보는 문제**(온라인 질의)라면
> **유니온파인드만 답이 된다** — DFS는 매번 전체를 다시 훑어야 하기 때문이다.
> **"동적으로 합쳐지는가"가 두 도구를 가르는 기준**이다.

---

## 7. 섬 연결하기 🟡

**출처:** [프로그래머스 #42861](https://school.programmers.co.kr/learn/courses/30/lessons/42861)

`n`개의 섬 사이에 다리를 건설하는 비용이 담긴 배열 `costs`가 주어진다.
**최소 비용으로 모든 섬이 서로 통행 가능하도록** 만들 때 필요한 **최소 비용**을 반환하라.

다리를 여러 번 건너서라도 이동 가능하면 "통행 가능"으로 본다.

**예시:**
- `n = 4`, `costs = [[0,1,1],[0,2,2],[1,2,5],[1,3,1],[2,3,8]]` → **`4`**
  (`0-1(1)`, `1-3(1)`, `0-2(2)` = 4)

**제약:**
- 섬의 개수 `n`은 `1` 이상 `100` 이하.
- `costs`의 길이는 `((n-1) * n) / 2` 이하.
- 임의의 `i`에 대해 `costs[i][0]`과 `costs[i][1]`에는 다리가 연결되는 두 섬의 번호가,
  `costs[i][2]`에는 다리를 건설할 때 드는 비용이 들어 있다.
- **모든 섬 사이의 통행은 가능하다고 가정한다**(연결 불가 케이스 없음).

**시그니처 (프로그래머스):**
```python
def solution(n, costs):
    ...
```

> [!tip]- 힌트 1 (위장 단어)
> **"모든 섬을 최소 비용으로 연결"** = **최소 신장 트리(MST)** 의 교과서적 정의다.
> ```
>   "전부 연결" + "최소 비용" + "사이클은 낭비"  ->  MST
>   Day 37 로 즉시 이동
> ```
> 이 문장 패턴("모든 도시를 잇는 최소 비용", "모든 컴퓨터를 연결하는 최소 케이블")을
> **위장 단어 사전에 넣어 두라.**

> [!tip]- 힌트 2 (크루스칼이 짧다)
> ```
>   1) 간선을 비용 오름차순으로 정렬한다
>   2) 앞에서부터 보며, 사이클을 만들지 않는 간선만 고른다
>      (= 유니온파인드로 find(a) != find(b) 인 간선만)
>   3) 간선 n-1 개를 고르면 종료
> ```
> **`find(a) == find(b)`면 이미 연결되어 있다는 뜻 = 이 간선은 사이클을 만든다.**
> [[day-36-union-find/concept|Day 36]]과 [[day-37-mst/concept|Day 37]]이 한 몸인 이유가 여기 있다.

> [!tip]- 힌트 3 (프림으로도 풀어 보라)
> ```
>   0번 섬에서 시작해, "지금까지 고른 집합에 붙는 가장 싼 간선"을 힙에서 계속 뽑는다.
>   이미 방문한 섬이 나오면 버린다.
> ```
> **두 방법이 같은 답을 주는지 대조하라.** MST의 총 비용은 유일하지만
> (간선 비용에 중복이 있으면) 고른 간선 집합은 다를 수 있다 — **비용만 비교**해야 한다.

> [!tip]- 힌트 4 (n = 1 엣지 케이스)
> 섬이 하나뿐이면 다리가 필요 없다 → 답은 `0`.
> `n-1 = 0`개의 간선을 고르면 되므로 대부분의 구현이 자연히 `0`을 반환하지만, **한 번 확인하라.**

---

## 8. Longest Increasing Path in a Matrix 🔴

**출처:** [LeetCode #329](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

`m x n` 정수 행렬 `matrix`가 주어진다. **가장 긴 증가 경로(longest increasing path)** 의 길이를 반환하라.

각 칸에서 **상하좌우 네 방향**으로 이동할 수 있고, **다음 칸의 값이 현재 칸보다 커야** 한다.
(대각선 이동 불가, 격자 밖으로 나갈 수 없음.)

**예시:**
```
  9 9 4        1 2 3
  6 6 8        6 4 5
  2 1 1        7 8 9
```
- 왼쪽 → **`4`** (`1 -> 2 -> 6 -> 9`)
- 오른쪽 → **`4`** (`3 -> 4 -> 5 -> 6`)

**제약:** `1 <= m, n <= 200`, `0 <= matrix[i][j] <= 2^31 - 1`.

**시그니처 (LeetCode):**
```python
class Solution:
    def longestIncreasingPath(self, matrix: 'List[List[int]]') -> int: ...
```

> [!tip]- 힌트 1 (격자를 그래프로 번역하라 - 오늘의 핵심 훈련)
> ```
>   각 칸 = 정점 (m*n <= 40,000 개)
>   "값이 커지는 방향"으로만 간선을 긋는다
>
>   -> 값이 항상 증가하므로 사이클이 있을 수 없다
>   -> 이 그래프는 DAG (방향 비순환 그래프) 다!
>
>   DAG 위의 최장 경로 = 위상 정렬 + DP  (Day 38)
> ```
> **"증가하는 방향으로만 간다"는 조건이 곧 "DAG다"라는 선언**이다. 이 번역이 이 문제의 전부다.

> [!tip]- 힌트 2 (접근 A - 메모이제이션 DFS)
> ```
>   dp[i][j] = (i,j) 에서 시작하는 최장 증가 경로 길이
>   dp[i][j] = 1 + max( dp[이웃] for 값이 더 큰 이웃 )    (없으면 1)
>
>   각 칸을 정확히 한 번만 계산한다 -> O(m*n)
>   방문 배열이 필요 없다! DAG 이므로 되돌아올 수 없기 때문이다.
> ```
> **⚠️ 재귀 깊이 주의.** 최악의 경우(값이 한 줄로 계속 증가하는 40,000칸) **`RecursionError`** 가 난다.
> `sys.setrecursionlimit`은 임시방편이다.

> [!tip]- 힌트 3 (접근 B - 위상 정렬, 재귀 0줄)
> 재귀가 불안하면 **Kahn 알고리즘의 층 벗기기**로 간다.
> ```
>   각 칸의 "진출 차수(더 큰 이웃의 수)"를 센다
>   차수가 0인 칸(= 주변에 더 큰 값이 없는 칸)부터 큐에 넣는다
>   층을 하나씩 벗기며 depth 를 세면, 총 층수가 답이다
>
>   이것은 Day 44 의 "잎에서부터 깎는다"와 같은 사고다
> ```
> **재귀 없이 `O(m*n)`.** 파이썬에서는 이쪽이 안전하다.

---

## 9. Replace Words 🟡

**출처:** [LeetCode #648](https://leetcode.com/problems/replace-words/)

영어에서 **어근(root)** 뒤에 다른 단어가 붙어 **파생어(derivative)** 가 만들어진다
(예: 어근 `"help"` + `"ful"` → `"helpful"`).

어근 목록 `dictionary`와 문장 `sentence`가 주어진다.
문장 안의 모든 파생어를 **그것을 이루는 어근**으로 바꿔라.
**여러 어근이 후보라면 가장 짧은 것**으로 바꾼다. 어떤 어근도 접두사가 아니면 원래 단어를 유지한다.

**예시:**
- `dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"`
  → **`"the cat was rat by the bat"`**
- `dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfafs"`
  → `"a a b c"`

**제약:** `1 <= dictionary.length <= 1000`, `1 <= dictionary[i].length <= 100`,
`1 <= sentence.length <= 10^6`, 소문자와 공백만.

**시그니처 (LeetCode):**
```python
class Solution:
    def replaceWords(self, dictionary: 'List[str]', sentence: str) -> str: ...
```

> [!tip]- 힌트 1 (위장 단어)
> **"접두사인 어근 중 가장 짧은 것"** — **접두사(prefix)** 라는 단어가 나오면 **트라이**를 먼저 의심하라([[day-39-trie/concept|Day 39]]).
> ```
>   sentence 길이가 10^6 이다!
>   나이브: 각 단어마다 사전 1000개를 전부 비교 -> 너무 느리다
>   트라이: 각 단어를 한 글자씩 따라가며 "끝 표시"를 만나면 즉시 종료
>           -> O(사전 총 길이 + 문장 총 길이)
> ```

> [!tip]- 힌트 2 (가장 짧은 어근 = 먼저 만나는 끝 표시)
> 트라이를 위에서부터 내려가면 **짧은 어근이 먼저 나온다.**
> ```
>   for i, ch in enumerate(word):
>       if ch not in node: return word          # 더 못 내려감 -> 원래 단어
>       node = node[ch]
>       if END in node: return word[:i+1]       # 첫 번째로 만난 끝 = 가장 짧은 어근
>   return word
> ```
> **`END` 표시를 만나자마자 반환**하는 것이 "가장 짧은"을 공짜로 만족시킨다.

> [!tip]- 힌트 3 (트라이 없이도 가능하다)
> 어근 길이가 **최대 100**이므로, 각 단어의 접두사를 짧은 것부터 최대 100개 잘라
> **`set`에 있는지 확인**해도 된다.
> ```
>   O(단어 수 * 100) - 제약 안에서 충분하다
> ```
> **문제를 두 방법으로 풀고 결과를 대조하라.** 트라이가 정석이지만 `set`이 더 짧다 —
> **실전에서는 "제약 안에서 가장 빨리 짤 수 있는 것"이 정답**이다.

---

## 10. Create Sorted Array through Instructions 🔴

**출처:** [LeetCode #1649](https://leetcode.com/problems/create-sorted-array-through-instructions/)

정수 배열 `instructions`가 주어진다. 빈 배열 `nums`에 `instructions`의 원소를 **왼쪽부터 하나씩** 넣어
**정렬된 배열**을 만든다.

`instructions[i]`를 넣을 때의 **비용**은 다음 둘 중 **작은 값**이다:
- 현재 `nums`에서 `instructions[i]`보다 **엄격히 작은** 원소의 개수
- 현재 `nums`에서 `instructions[i]`보다 **엄격히 큰** 원소의 개수

모든 원소를 넣는 데 드는 **총 비용**을 반환하라. 답이 클 수 있으므로 **`10^9 + 7`로 나눈 나머지**를 반환한다.

**예시:**
- `instructions = [1,5,6,2]` → **`1`**
  (1 넣기: 0, 5 넣기: 0, 6 넣기: 0, 2 넣기: `min(작은 것 1개, 큰 것 2개) = 1`)
- `instructions = [1,2,3,6,5,4]` → `3`
- `instructions = [1,3,3,3,2,4,2,1,2]` → `4`

**제약:** `1 <= instructions.length <= 10^5`, `1 <= instructions[i] <= 10^5`.

**시그니처 (LeetCode):**
```python
class Solution:
    def createSortedArray(self, instructions: 'List[int]') -> int: ...
```

> [!tip]- 힌트 1 (제약이 도구를 지목한다)
> ```
>   N = 10^5, 그리고 매 원소마다 "나보다 작은 것이 몇 개인가"를 물어야 한다
>
>   나이브: 매번 세기 -> O(N^2) = 10^10   즉사
>   필요:   질의당 O(log N) -> 전체 O(N log N) = 1.7e6   OK
>
>   "삽입하면서(갱신) 개수를 센다(질의)"  ->  펜윅 트리 (Day 40)
> ```
> **"갱신 + 구간 합 질의"** 조합이 보이면 펜윅이다. 값이 고정이면 누적 합으로 충분했을 것이다.

> [!tip]- 힌트 2 (값을 인덱스로 쓴다 - Phase 4 최고의 관용구)
> ```
>   BIT 를 "값의 개수를 담는 카운팅 배열"로 쓴다
>
>   x 보다 작은 것의 개수  = bit.query(x - 1)          # [1, x-1] 합
>   x 보다 큰 것의 개수    = 지금까지 넣은 개수 i - bit.query(x)
>                            (query(x) 는 x 이하의 개수이므로 x 자신도 포함)
>
>   비용 += min(작은 것, 큰 것)
>   그 다음 bit.add(x, 1)   <- 넣는 것은 세고 난 뒤에!
> ```
> **⚠️ "같은 값"의 처리가 함정이다.** `x`와 같은 값은 **작지도 크지도 않다.**
> `query(x-1)`과 `i - query(x)`로 정확히 갈라야 중복 값이 있는 테스트에서 맞는다.

> [!tip]- 힌트 3 (1-based 와 좌표 압축)
> `instructions[i] <= 10^5`이므로 **값을 그대로 인덱스로** 쓸 수 있다(크기 `10^5`의 BIT).
> 하지만 값이 `10^9`까지 갈 수 있는 문제라면 **좌표 압축**을 먼저 해야 한다.
> 그리고 **펜윅은 1-based 필수** — 값이 `0`부터 시작하는 문제라면 `+1`을 해서 넣어라
> (`i & -i`가 `0`에서 무한 루프에 빠진다).

> [!tip]- 힌트 4 (교차 검증)
> `bisect.insort`로 나이브하게 짜면 `O(N^2)`(리스트 삽입이 `O(N)`)이지만 **작은 입력에서는 정답**이다.
> **무작위 배열로 펜윅 버전과 대조**하면 "같은 값 처리"를 제대로 했는지 즉시 알 수 있다.

---

## 11. Smallest Sufficient Team 🔴

**출처:** [LeetCode #1125](https://leetcode.com/problems/smallest-sufficient-team/)

프로젝트에 필요한 기술 목록 `req_skills`와 사람들의 목록 `people`이 주어진다.
`people[i]`는 `i`번째 사람이 가진 기술들의 목록이다.

**충분한 팀(sufficient team)** 이란 `req_skills`의 **모든 기술을 최소 한 명은 가지고 있는** 사람들의 집합이다.
**크기가 가장 작은 충분한 팀**을 **사람의 인덱스 배열**로 반환하라. 답이 여러 개면 아무거나 반환해도 된다.

**답은 항상 존재한다고 보장된다.**

**예시:**
- `req_skills = ["java","nodejs","reactjs"]`,
  `people = [["java"],["nodejs"],["nodejs","reactjs"]]` → **`[0,2]`**
- `req_skills = ["algorithms","math","java","reactjs","csharp","aws"]`,
  `people = [["algorithms","math","java"],["algorithms","math","reactjs"],
  ["java","csharp","aws"],["reactjs","csharp"],["csharp","math"],["aws","java"]]` → `[1,2]`

**제약:** `1 <= req_skills.length <= 16`, `1 <= people.length <= 60`, 기술 이름은 서로 다르다.

**시그니처 (LeetCode):**
```python
class Solution:
    def smallestSufficientTeam(self, req_skills: 'List[str]',
                               people: 'List[List[str]]') -> 'List[int]': ...
```

> [!tip]- 힌트 1 (제약이 소리치고 있다)
> ```
>   req_skills.length <= 16      <-- 이것이 신호다!
>
>   2^16 = 65,536 개의 "기술 집합" 상태
>   사람 60명을 곱해도 60 * 65,536 = 3.9e6   즉시 통과
>
>   -> 비트마스크 DP (Day 41)
> ```
> **`<= 16`, `<= 20` 같은 작은 수를 보면 즉시 `2^N`을 의심하라.** 출제자가 대놓고 알려 주는 것이다.
> **사람이 60명인데 `2^60`을 시도하면 안 된다** — 상태로 삼을 것은 **기술 집합**이지 사람 집합이 아니다.

> [!tip]- 힌트 2 (기술을 비트로 압축)
> ```
>   skill_id = {"java": 0, "nodejs": 1, "reactjs": 2, ...}
>
>   각 사람의 기술을 하나의 정수로:
>     mask = 0
>     for s in person: mask |= 1 << skill_id[s]
>
>   목표: FULL = (1 << len(req_skills)) - 1  (모든 비트가 1)
> ```

> [!tip]- 힌트 3 (전이 - dp 를 dict 로 두면 짧다)
> ```
>   dp[mask] = 그 기술 집합을 달성하는 "최소 인원 팀"(인덱스 리스트)
>   dp = {0: []}
>
>   for i, pmask in enumerate(people_masks):
>       for cur, team in list(dp.items()):        # 스냅샷을 떠서 순회한다
>           nxt = cur | pmask
>           if nxt == cur:                        # 이 사람이 보태는 게 없다
>               continue
>           if nxt not in dp or len(dp[nxt]) > len(team) + 1:
>               dp[nxt] = team + [i]
>
>   답 = dp[FULL]
> ```
> **⚠️ `dp`를 순회하면서 동시에 수정하면 안 된다.** `list(dp.items())`로 **스냅샷**을 뜨는 것이
> "각 사람을 최대 한 번만 쓴다"를 보장한다(0/1 배낭에서 역순으로 도는 것과 같은 이유).

> [!tip]- 힌트 4 (불필요한 사람 제거 - 선택적 최적화)
> 어떤 사람의 기술이 다른 사람의 기술의 **부분집합**이면 그 사람은 절대 필요 없다.
> ```
>   a_mask & b_mask == a_mask  ->  a 는 b 에 완전히 흡수된다 -> a 를 버려도 된다
> ```
> 없어도 통과하지만, **비트 연산으로 포함 관계를 판정하는 감각**을 익히기 좋다.

---

## 12. Longest Happy Prefix 🔴

**출처:** [LeetCode #1392](https://leetcode.com/problems/longest-happy-prefix/)

문자열이 **happy prefix**라는 것은 그것이 **비어 있지 않은 접두사(prefix)이면서 동시에 접미사(suffix)** 라는 뜻이다
(**단, 문자열 자기 자신은 제외**).

문자열 `s`가 주어질 때 **가장 긴 happy prefix**를 반환하라. 없으면 빈 문자열 `""`.

**예시:**
- `s = "level"` → **`"l"`** (접두사이자 접미사인 것: `"l"`. `"le"`와 `"el"`은 다르다)
- `s = "ababab"` → **`"abab"`** (자기 자신 `"ababab"`은 제외)
- `s = "leetcodeleet"` → `"leet"`
- `s = "a"` → `""`

**제약:** `1 <= s.length <= 10^5`, 소문자 영문만.

**시그니처 (LeetCode):**
```python
class Solution:
    def longestPrefix(self, s: str) -> str: ...
```

> [!tip]- 힌트 1 (이것은 KMP 의 실패 함수 그 자체다)
> **"접두사이면서 접미사인 최장 길이"** — 이것이 바로 **KMP의 `pi` 배열(failure function)의 정의**다.
> ```
>   pi[i] = s[:i+1] 의 "자기 자신을 제외한, 접두사이자 접미사인" 최장 길이
>
>   답 = s[:pi[-1]]        <- 마지막 원소가 곧 답이다!
> ```
> **KMP를 "문자열 검색 알고리즘"으로만 외우면 이 유형을 통째로 놓친다.**
> [[day-42-string-matching/concept|Day 42]]에서 `pi` 배열을 구축하는 코드가 **이 문제의 전체 해답**이다.

> [!tip]- 힌트 2 (제약이 O(N^2) 를 막는다)
> ```
>   N = 10^5
>   나이브: 길이 k 를 N-1 부터 줄여 가며 s[:k] == s[-k:] 비교
>           -> 최악 O(N^2) = 10^10   즉사
>           ("aaaa...a" 같은 입력에서 실제로 터진다)
>
>   KMP:    O(N)   즉시
> ```

> [!tip]- 힌트 3 (pi 구축에서 while 을 잊지 마라)
> ```python
> pi = [0] * len(s)
> j = 0
> for i in range(1, len(s)):
>     while j and s[i] != s[j]:
>         j = pi[j - 1]        # <-- while! if 로 쓰면 조용히 틀린다
>     if s[i] == s[j]:
>         j += 1
>         pi[i] = j
> return s[:pi[-1]]
> ```
> **`if`로 한 번만 되감으면 특정 입력에서만 틀린다** — 예를 들어 `"aabaaacaa"`에서
> 올바른 `pi`는 `[0,1,0,1,2,2,0,1,2]`인데 `if` 버전은 `[0,1,0,1,2,2,0,2,2]`가 된다.
> **디버깅이 매우 어려운 종류의 버그**이니 손에 익혀 두라.
> (이 대조는 [examples.py](examples.py)의 "함정 확인" 절에서 실제로 실행해 볼 수 있다.)

> [!tip]- 힌트 4 (롤링 해시로도 풀린다)
> 접두사 해시와 접미사 해시를 굴리며 길이를 `N-1`부터 줄여 비교하면 `O(N)`이다.
> **다만 해시 충돌 검증이 필요**하고, KMP보다 상수가 크며 모듈러 선택에 신경 써야 한다.
> **KMP가 정석이고 롤링 해시는 교차 검증용**으로 쓰는 것이 좋다.

---

## 13. Minimum Time to Collect All Apples in a Tree 🟡

**출처:** [LeetCode #1443](https://leetcode.com/problems/minimum-time-to-collect-all-apples-in-a-tree/)

`n`개의 정점(`0` ~ `n-1`)으로 이루어진 **무향 트리**가 주어진다.
`edges[i] = [a, b]`는 `a`와 `b`를 잇는 간선이다.

일부 정점에는 사과가 있다 — `hasApple[i] == True`면 `i`번 정점에 사과가 있다.
**간선 하나를 지나는 데 1초**가 걸린다.

**정점 `0`에서 출발해 모든 사과를 모으고 다시 정점 `0`으로 돌아오는 최소 시간**을 반환하라.

**예시:**
- `n = 7`, `edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]]`,
  `hasApple = [false,false,true,false,true,true,false]` → **`8`**
- 같은 트리, `hasApple = [false,false,true,false,false,true,false]` → `6`
- 같은 트리, `hasApple`가 전부 `false` → `0`

**제약:** `1 <= n <= 10^5`, `edges.length == n - 1`, `hasApple.length == n`.

**시그니처 (LeetCode):**
```python
class Solution:
    def minTime(self, n: int, edges: 'List[List[int]]',
                hasApple: 'List[bool]') -> int: ...
```

> [!tip]- 힌트 1 (핵심 관찰 - 각 간선은 0번 아니면 2번 지난다)
> 출발지로 **되돌아와야** 하므로, 내려간 간선은 반드시 올라와야 한다.
> ```
>   간선 (부모 - 자식) 을 지나야 하는가?
>     자식의 서브트리 안에 사과가 하나라도 있으면   -> 지나야 한다 (내려갔다 올라옴 = 2초)
>     하나도 없으면                                 -> 갈 이유가 없다 (0초)
>
>   답 = 2 * (지나야 하는 간선의 수)
> ```
> **"어떤 순서로 도느냐"를 고민할 필요가 없다** — 필요한 간선의 집합이 결정되면 시간은 확정이다.
> 이것이 이 문제가 **탐색이 아니라 트리 DP**인 이유다([[day-44-tree-dp/concept|Day 44]]의 판별 훈련).

> [!tip]- 힌트 2 (상태와 전이)
> ```
>   need[v] = v 의 서브트리 안에 사과가 있는가 (bool)
>   need[v] = hasApple[v] or any(need[c] for c in children)
>
>   비용 = sum( 2 for v != root if need[v] )
>        = 각 정점 v(루트 제외)에 대해, need[v] 면 부모와의 간선 2초
> ```
> **루트(0번)는 제외**해야 한다 — 0번 위에는 부모가 없다.

> [!tip]- 힌트 3 (N = 10^5 - 재귀가 죽는다)
> ```
>   제약이 10^5 이고 "한 줄로 늘어진 트리" 테스트가 실제로 존재한다.
>   재귀 DFS -> RecursionError
>
>   정석: BFS 로 순서를 만들고 reversed(order) 로 후위 순회
>         (Day 44 의 관용구가 그대로 쓰인다)
> ```
> ```python
> parent, _, order = root_tree(adj, 0)     # BFS 로 부모/순서 생성
> need = list(hasApple)
> total = 0
> for v in reversed(order):                # 자식이 부모보다 먼저 처리된다
>     if v != 0 and need[v]:
>         need[parent[v]] = True
>         total += 2
> return total
> ```
> **`reversed(order)` 한 줄로 재귀 없이 끝난다.** 이 관용구를 손에 익히는 것이 Day 44~45의 목표다.

> [!tip]- 힌트 4 (무향 트리 - 부모를 제외하라)
> 인접 리스트가 무향이므로 `for w in adj[v]`를 그대로 돌면 **부모로 되돌아간다.**
> `if w == parent[v]: continue`가 필수다.
> 트리에는 사이클이 없으므로 **`visited` 대신 `parent` 비교만으로 충분**하다.

---

## 마무리 — 오늘 확인해야 할 것

13문제를 다 풀었다면 아래를 스스로 점검하세요. **막힌 지점이 곧 진짜 약점 목록**입니다.

```
  [ ] 문제를 읽고 30초 안에 "제약 -> 허용 복잡도"를 말할 수 있었나?
  [ ] 알고리즘 이름 없이 위장된 문장에서 구조를 알아봤나?
      (#7 "모든 섬 연결" -> MST,  #8 "증가 경로" -> DAG,  #12 "접두사이자 접미사" -> KMP)
  [ ] 전제를 확인했나? (#5 가중치 양수 확인,  #4 중복 간선,  #10 같은 값 처리)
  [ ] 재귀 깊이를 의식했나? (#8 40,000칸,  #13 N=10^5)
  [ ] 두 가지 방법으로 풀어 교차 검증했나?
  [ ] 1-based / 0-based 를 섞지 않았나? (#4, #5, #10)
```

**한 문제라도 "무슨 알고리즘인지 몰라서" 막혔다면** 해당 Day 노트로 돌아가되,
**개념을 다시 읽지 말고 그 Day의 problems.md를 다시 푸세요.** 복습은 읽기가 아니라 풀기입니다.

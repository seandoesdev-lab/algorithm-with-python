# Day 31 — 동적 계획법 입문 (Dynamic Programming) 연습문제

> 출처는 **프로그래머스 / LeetCode만** 사용합니다. 각 문제는 "상태 정의 → 점화식 → 초기값" 순으로 접근하세요.
> 정답 코드와 다중 접근(재귀/메모/타뷸/최적화) 비교는 [solutions.py](solutions.py) 참고.

## 난이도 범례
🟢 기초 · 🟡 중급 · 🔴 심화 · ⚫ 기출

---

## 1. Fibonacci Number 🟢
- **출처:** [LeetCode #509](https://leetcode.com/problems/fibonacci-number/)
- **요약:** `F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)`. `F(n)`을 구하라.
- **핵심:** DP의 "Hello World". 순진 재귀(O(2^n)) → 메모(O(n)) → 변수 2개 최적화(O(1) 공간)까지 손으로 변환해 보라.
- **상태/점화식:** `dp[i] = dp[i-1] + dp[i-2]`, 초기값 `dp[0]=0, dp[1]=1`.

## 2. Climbing Stairs 🟢
- **출처:** [LeetCode #70](https://leetcode.com/problems/climbing-stairs/)
- **요약:** n칸 계단을 한 번에 1칸 또는 2칸 오른다. 꼭대기까지 가는 경우의 수.
- **핵심:** "n칸 = (n-1칸에서 1칸) + (n-2칸에서 2칸)" → 피보나치와 완전히 같은 점화식.
- **함정:** `dp[1]=1, dp[2]=2`에서 시작. 초기값을 헷갈리면 전부 어긋난다.

## 3. Min Cost Climbing Stairs 🟢
- **출처:** [LeetCode #746](https://leetcode.com/problems/min-cost-climbing-stairs/)
- **요약:** 각 계단에 비용 `cost[i]`. 1칸 또는 2칸 오르며 꼭대기(len) 도달 최소 비용. 0 또는 1에서 시작 가능.
- **상태/점화식:** `dp[i] = min(dp[i-1]+cost[i-1], dp[i-2]+cost[i-2])`, `dp[0]=dp[1]=0`.
- **핵심:** "경우의 수"가 아니라 "최소 비용"으로 바뀌면 `+`가 `min`으로 바뀐다.

## 4. House Robber 🟡
- **출처:** [LeetCode #198](https://leetcode.com/problems/house-robber/)
- **요약:** 일렬 집에서 돈을 털되 **인접한 두 집은 동시에 못 턴다.** 최대 금액.
- **상태/점화식:** `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` (i를 건너뛰거나 / 털거나).
- **핵심:** "선택/건너뛰기" DP의 원형. 변수 2개(take/skip)로 O(1) 공간 가능.

## 5. Maximum Subarray 🟡
- **출처:** [LeetCode #53](https://leetcode.com/problems/maximum-subarray/)
- **요약:** 연속 부분 배열의 최대 합.
- **상태/점화식(Kadane):** `dp[i] = max(nums[i], dp[i-1] + nums[i])`, 답은 `max(dp)`.
- **함정:** `dp[i]`는 "i에서 **끝나는**" 최대합이다. "i까지의" 최대합으로 정의하면 점화식이 성립하지 않는다. 전부 음수인 경우도 처리(빈 배열 아님).

## 6. Unique Paths 🟡
- **출처:** [LeetCode #62](https://leetcode.com/problems/unique-paths/)
- **요약:** m×n 격자 좌상단→우하단, 오른쪽/아래로만 이동하는 경로 수.
- **상태/점화식:** `dp[r][c] = dp[r-1][c] + dp[r][c-1]`, 첫 행/열은 1.
- **핵심:** 2차원 격자 DP의 기본형. 한 행만 유지해 O(n) 공간으로 압축 가능.

## 7. Coin Change 🟡
- **출처:** [LeetCode #322](https://leetcode.com/problems/coin-change/)
- **요약:** 동전(무한 사용)으로 목표 금액을 만드는 **최소 동전 수**. 불가능하면 -1.
- **상태/점화식:** `dp[a] = min(dp[a], dp[a-c] + 1)` for each coin c.
- **함정:** **그리디로 풀면 틀린다**(예: 1,3,4로 6원). 도달 불가능 금액은 `INF`로 두고 마지막에 판별.

## 8. Longest Increasing Subsequence (LIS) 🔴
- **출처:** [LeetCode #300](https://leetcode.com/problems/longest-increasing-subsequence/)
- **요약:** 가장 긴 **증가하는** 부분 수열의 길이(연속일 필요 없음).
- **접근 A (O(n²)):** `dp[i] = 1 + max(dp[j] for j<i if nums[j]<nums[i])`.
- **접근 B (O(n log n)):** `tails[]`에 "길이 k인 증가 수열의 최소 끝값"을 유지, `bisect_left`로 위치를 찾아 교체([[day-18-binary-search/concept|이분 탐색]] 결합).

## 9. Longest Common Subsequence (LCS) 🔴
- **출처:** [LeetCode #1143](https://leetcode.com/problems/longest-common-subsequence/)
- **요약:** 두 문자열의 가장 긴 공통 부분 수열 길이.
- **상태/점화식:** `dp[i][j]` = text1[:i], text2[:j]의 LCS.
  - 같으면 `dp[i][j] = dp[i-1][j-1] + 1`
  - 다르면 `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`
- **핵심:** 2차원 문자열 DP의 대표. 배낭·편집거리로 이어지는 골격.

## 10. 정수 삼각형 ⚫ (기출)
- **출처:** [프로그래머스 #43105](https://school.programmers.co.kr/learn/courses/30/lessons/43105)
- **요약:** 삼각형 꼭대기에서 아래로 내려가며(바로 아래 또는 오른쪽 아래) 거치는 수의 합 최대.
- **상태/점화식:** `dp[r][c] += max(dp[r-1][c-1], dp[r-1][c])` (위 두 칸 중 큰 것). 양끝 경계 주의.
- **핵심:** 격자 누적 DP. 아래→위로 접어 올려도(bottom-up 역방향) 깔끔하게 풀린다.

## 11. N으로 표현 ⚫ (기출)
- **출처:** [프로그래머스 #42895](https://school.programmers.co.kr/learn/courses/30/lessons/42895)
- **요약:** 숫자 N을 사칙연산으로 이어 붙여(N, NN, NNN...) 목표 number를 만드는 **최소 N 사용 횟수**(8 초과면 -1).
- **상태/점화식:** `dp[k]` = "N을 k번 써서 만들 수 있는 값들의 **집합(set)**".
  - `dp[k]`는 `NN...N`(k개) 하나 + 모든 `dp[i] op dp[k-i]` (i=1..k-1, op는 +,-,*,/)의 합집합.
- **핵심:** dp의 값이 "집합"인 특이한 DP. 분할해 조합하는 구조가 핵심.

## 12. 등굣길 ⚫ (기출)
- **출처:** [프로그래머스 #42898](https://school.programmers.co.kr/learn/courses/30/lessons/42898)
- **요약:** m×n 격자에서 물에 잠긴 칸(puddle)을 피해 좌상→우하 최단 경로 수. `% 1000000007`.
- **상태/점화식:** `dp[r][c] = (dp[r-1][c] + dp[r][c-1]) % MOD`, 물웅덩이는 `dp=0`.
- **핵심:** Unique Paths + 장애물 + 모듈러. 매 덧셈마다 `% MOD`를 잊지 말 것.

---

## 추천 풀이 순서
1. **1 → 2 → 3** : 1차원 점화식 감 잡기(경우의 수 vs 최소 비용).
2. **4 → 5** : "선택/건너뛰기"와 "이어붙이기/새로 시작"의 상태 정의 차이.
3. **6 → 7** : 2차원 격자 / 배낭형 전이.
4. **8 → 9** : 심화(LIS 이분탐색, 2차원 문자열 DP).
5. **10 → 11 → 12** : 프로그래머스 기출로 실전 감각(누적·집합·모듈러).

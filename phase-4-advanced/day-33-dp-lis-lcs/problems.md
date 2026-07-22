# Day 33 — 부분 수열 DP (LIS·LCS) 연습문제

> 출처는 **프로그래머스 / LeetCode만** 사용합니다. 각 문제는 "연속인가? → 한 수열(LIS)인가 두 수열(LCS)인가 → 상태 정의 → 점화식" 순으로 접근하세요.
> 정답 코드와 다중 접근 비교는 [solutions.py](solutions.py) 참고.

## 난이도 범례
🟢 기초 · 🟡 중급 · 🔴 심화 · ⚫ 기출

---

## 1. Longest Increasing Subsequence 🟡
- **출처:** [LeetCode #300](https://leetcode.com/problems/longest-increasing-subsequence/)
- **요약:** 정수 배열에서 **강한 증가(strictly increasing) 부분 수열**의 최대 길이.
- **유형:** LIS 정석. 두 가지로 풀어보라.
  - **접근 A — O(N²) DP:** `dp[i]` = i로 끝나는 LIS 길이, `dp[i] = max(dp[j]+1)` (`j<i`, `nums[j]<nums[i]`). 답 `max(dp)`.
  - **접근 B — O(N log N):** `tails` + `bisect_left`. `tails` 길이가 답.
- **함정:** 답은 `dp[-1]`이 아니라 **`max(dp)`** (어디서 끝나든 최장). `tails`는 실제 수열이 아니다.

## 2. Longest Continuous Increasing Subsequence 🟢
- **출처:** [LeetCode #674](https://leetcode.com/problems/longest-continuous-increasing-subsequence/)
- **요약:** **연속(continuous)** 증가 부분 배열의 최대 길이.
- **유형:** 부분 배열(연속) — **DP가 아니다.** O(N) 한 번 훑기(현재 길이 누적, 끊기면 1로 리셋).
- **핵심:** #300(부분 수열)과 **딱 한 단어 차이**로 알고리즘이 완전히 달라진다는 것을 체득하는 문제. "연속인가?"를 먼저 묻는 습관.

## 3. Longest Common Subsequence 🟡
- **출처:** [LeetCode #1143](https://leetcode.com/problems/longest-common-subsequence/)
- **요약:** 두 문자열 `text1`, `text2`의 **최장 공통 부분 수열** 길이.
- **유형:** LCS 정석 2차원 DP.
- **상태/점화식:** `dp[i][j]` = `text1[:i]`와 `text2[:j]`의 LCS. 같으면 `dp[i-1][j-1]+1`, 다르면 `max(dp[i-1][j], dp[i][j-1])`.
- **함정:** 인덱스 오프셋 — `dp`는 `(m+1)×(n+1)`, 문자 접근은 `a[i-1]`, `b[j-1]`. 첫 행/열은 0.

## 4. Longest Palindromic Subsequence 🟡
- **출처:** [LeetCode #516](https://leetcode.com/problems/longest-palindromic-subsequence/)
- **요약:** 한 문자열에서 **가장 긴 팰린드롬 부분 수열**의 길이.
- **유형:** LCS 응용. **핵심 관찰: `LPS(s) = LCS(s, reverse(s))`.**
  - **접근 A:** `s`와 `s[::-1]`로 LCS를 돌린다(가장 외우기 쉬움).
  - **접근 B:** 구간 DP `dp[i][j]` = 구간 `s[i..j]`의 LPS. 양끝 같으면 `dp[i+1][j-1]+2`, 다르면 `max(dp[i+1][j], dp[i][j-1])`.
- **함정:** "부분 **수열**"이라 좌우로 건너뛸 수 있다. "부분 **문자열**(연속)"과 다르다(문제 6 참고).

## 5. Edit Distance 🔴
- **출처:** [LeetCode #72](https://leetcode.com/problems/edit-distance/)
- **요약:** `word1`을 `word2`로 바꾸는 최소 연산 수(삽입/삭제/교체).
- **유형:** LCS의 사촌. 2차원 DP.
- **상태/점화식:** `dp[i][j]` = `a[:i]`→`b[:j]` 최소 연산. 같으면 `dp[i-1][j-1]`, 다르면 `1 + min(삭제 dp[i-1][j], 삽입 dp[i][j-1], 교체 dp[i-1][j-1])`.
- **초기값:** `dp[i][0]=i`(전부 삭제), `dp[0][j]=j`(전부 삽입). **이 경계 초기화를 빼먹으면 전부 오답.**

## 6. 가장 긴 팰린드롬 ⚫ (기출)
- **출처:** [프로그래머스 #12904](https://school.programmers.co.kr/learn/courses/30/lessons/12904)
- **요약:** 문자열에서 **가장 긴 팰린드롬 부분 문자열(연속, substring)** 의 길이.
- **유형:** 문제 4와 **결정적으로 다르다** — 여기서는 **연속**이라 LCS 트릭이 안 통한다.
  - **접근 A — 중심 확장(center expansion) O(N²):** 각 위치를 중심으로 좌우로 같은 글자면 확장. 홀수 중심(한 글자)과 짝수 중심(두 글자) 모두 확인.
  - **접근 B — 구간 DP O(N²):** `dp[i][j]` = `s[i..j]`가 팰린드롬인가(bool). `s[i]==s[j] and dp[i+1][j-1]`.
- **함정:** 짝수 길이 팰린드롬(예: "abba")을 놓치기 쉽다. 중심 확장은 반드시 홀/짝 두 경우를 돌린다.

---

## 추천 풀이 순서
1. **1 → 2** : LIS(부분 수열)와 연속 증가(부분 배열)를 나란히 풀어 "연속?"의 위력을 체득.
2. **3** : LCS 2차원 DP의 표를 손으로 한 번 채워본다("같으면 ↖+1, 다르면 max(↑,←)").
3. **4 → 5** : LCS 응용 — 팰린드롬(뒤집어 LCS)과 편집 거리(min +1).
4. **6** : 기출 — "부분 문자열(연속)" 팰린드롬은 중심 확장/구간 DP로 4번과 대비.

## 셀프 체크리스트
- [ ] 이 문제는 **연속(부분 배열)** 인가 **건너뛰기(부분 수열)** 인가?
- [ ] LIS라면 N 범위를 보고 O(N²)/O(N log N)을 골랐는가? strict vs 비감소를 맞췄는가?
- [ ] LCS/편집 거리의 `dp` 크기 `(m+1)×(n+1)`과 인덱스 오프셋(`a[i-1]`)을 맞췄는가?
- [ ] 편집 거리 경계 초기값(`dp[i][0]=i`, `dp[0][j]=j`)을 넣었는가?
- [ ] 팰린드롬이 부분 **수열**인가 부분 **문자열(연속)**인가?

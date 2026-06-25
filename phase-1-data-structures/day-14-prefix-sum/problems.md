---
day: 14
phase: 1-data-structures
title: 누적 합 (Prefix Sum) — 연습문제
tags: [phase/1, topic/prefix-sum, problems]
---

# Day 14 — 연습문제 (Prefix Sum)

> 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 풀이 코드는 [solutions.py](solutions.py) 참고. **출처는 LeetCode·프로그래머스만.**

---

## 1. Running Sum of 1d Array 🟢

- **출처:** [LeetCode #1480](https://leetcode.com/problems/running-sum-of-1d-array/)
- **요약:** 배열 `nums`가 주어질 때, `result[i] = nums[0] + ... + nums[i]`인 "달리는 합(running sum)"을 반환하라.
- **예:** `nums=[1,2,3,4]` → `[1,3,6,10]`
- **힌트:** 누적합의 가장 순수한 정의. 앞 값에 현재 원소를 더하며 한 번 순회(O(n)). `itertools.accumulate`로 한 줄.

## 2. Range Sum Query - Immutable 🟢

- **출처:** [LeetCode #303](https://leetcode.com/problems/range-sum-query-immutable/)
- **요약:** 변하지 않는 배열에 대해 `sumRange(i, j)`(구간 `[i, j]` 합) 질의가 여러 번 들어온다. 효율적으로 답하라.
- **힌트:** 생성자에서 누적합 `P`(길이 n+1, `P[0]=0`)를 **한 번** 만들고, 질의는 `P[j+1] - P[i]`로 O(1). 질의가 많을수록 이득이 커지는 전형.

## 3. Find Pivot Index 🟢

- **출처:** [LeetCode #724](https://leetcode.com/problems/find-pivot-index/)
- **요약:** 왼쪽 원소들의 합 == 오른쪽 원소들의 합이 되는 가장 왼쪽 인덱스를 찾아라(없으면 -1).
- **예:** `nums=[1,7,3,6,5,6]` → `3` (왼쪽 1+7+3=11, 오른쪽 5+6=11)
- **힌트:** 전체 합 `total`을 먼저 구하고, 왼쪽 누적합 `left`를 키우며 `left == total - left - nums[i]`인지 검사. O(n), 추가 공간 O(1).

## 4. Subarray Sum Equals K 🟡

- **출처:** [LeetCode #560](https://leetcode.com/problems/subarray-sum-equals-k/)
- **요약:** 합이 정확히 `k`인 연속 부분 배열의 **개수**를 구하라(음수 포함 가능).
- **예:** `nums=[1,1,1], k=2` → `2`
- **힌트:** 모든 구간 O(n²) 대신 **누적합 + 해시맵**으로 O(n). `seen[prefix-k]`의 횟수를 더한다. `seen[0]=1` 초기화 필수. 음수가 있으므로 슬라이딩 윈도우는 불가.

## 5. Product of Array Except Self 🟡

- **출처:** [LeetCode #238](https://leetcode.com/problems/product-of-array-except-self/)
- **요약:** `answer[i]`가 `nums`에서 `i`번째를 **제외한** 모든 원소의 곱이 되도록 하라. 나눗셈 사용 금지, O(n).
- **예:** `nums=[1,2,3,4]` → `[24,12,8,6]`
- **힌트:** 누적합의 곱 버전. 왼쪽 누적 곱 한 번, 오른쪽 누적 곱 한 번을 곱해 합성. 0이 섞여도 나눗셈을 안 쓰므로 안전.

## 6. Count Number of Nice Subarrays 🟡

- **출처:** [LeetCode #1248](https://leetcode.com/problems/count-number-of-nice-subarrays/)
- **요약:** 홀수가 정확히 `k`개 들어 있는 연속 부분 배열의 개수를 구하라.
- **예:** `nums=[1,1,2,1,1], k=3` → `2`
- **힌트:** 각 원소를 "홀수면 1, 짝수면 0"으로 바꾸면 **합이 k인 부분 배열 개수**(#560과 동일 구조)가 된다. 누적합+해시맵 그대로.

## 7. Range Sum Query 2D - Immutable 🟡

- **출처:** [LeetCode #304](https://leetcode.com/problems/range-sum-query-2d-immutable/)
- **요약:** 변하지 않는 2D 행렬에서 직사각형 `(r1,c1)~(r2,c2)`의 합 질의에 효율적으로 답하라.
- **힌트:** 2D 누적합 `P[r+1][c+1]`을 만든 뒤, 포함-배제로 `P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`. 질의 O(1).

## 8. 우박수열 정적분 🟡 ⚫(프로그래머스)

- **출처:** [프로그래머스 #134239](https://school.programmers.co.kr/learn/courses/30/lessons/134239)
- **요약:** 콜라츠(우박) 수열을 꺾은선 그래프로 보고, 질의 `[a, b]`마다 구간 `[a, b]`의 사다리꼴 넓이(정적분 근사)를 구한다. `b=-1`이면 끝까지.
- **힌트:** 인접한 두 점의 사다리꼴 넓이 `(y_i + y_{i+1}) / 2`를 미리 배열로 만든 뒤 **그 배열의 누적합**을 둔다. 그러면 각 질의를 O(1)에 답한다. 누적합으로 "여러 구간 질의"를 가속하는 응용.

---

## 풀이 전략 요약

| 신호 | 떠올릴 도구 |
|---|---|
| "구간 합/평균"을 **여러 번** 묻는다 | 1D 누적합 (질의 O(1)) |
| "합이 K인 구간 **개수**" (음수 포함) | 누적합 + 해시맵 |
| "왼쪽 합 == 오른쪽 합" 균형점 | 좌우 누적합 |
| "자기 자신 제외 곱" | 좌우 누적 곱 |
| 2D 직사각형 합 | 2D 누적합 + 포함·배제 |
| "구간마다 +v" 갱신이 여러 번 후 조회 | 차분 배열 + 누적합 복원 |

> 관련 개념: [[concept]] · 해시 결합 패턴은 [[day-13-hashmap-patterns/concept|Day 13]] 참고.

# Day 18 — 이분 탐색 (Binary Search) 연습문제

> 출처는 **프로그래머스 / LeetCode** 만 사용합니다. 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 풀이 코드와 복잡도 비교는 [solutions.py](solutions.py) 참고.

이분 탐색은 두 갈래입니다. **값/경계 탐색**(1~5)은 "정렬된 배열"에서 위치를 찾고, **결정 문제형(parametric)**(6~8)은 "정답 자체"를 이분 탐색합니다. 실전 난이도의 핵심은 결정 문제형입니다 — "답 후보 x를 정했을 때 되는지 판별하는 함수 `pred(x)`가 단조로운가?"를 먼저 물으세요.

---

## 🟢 기초

### 1. Binary Search — [LeetCode #704](https://leetcode.com/problems/binary-search/)
정렬된 배열에서 `target`의 인덱스를 O(log n)으로 찾고, 없으면 -1.
- **핵심:** 표준 틀. `mid` 확인 후 왼/오 절반 중 하나를 버린다.
- **힌트:** 닫힌 구간 `[lo, hi]`, 조건 `lo <= hi`, 갱신 `lo=mid+1` / `hi=mid-1`.

### 2. Search Insert Position — [LeetCode #35](https://leetcode.com/problems/search-insert-position/)
정렬 배열에서 `target`이 있으면 그 위치, 없으면 삽입될 위치를 반환.
- **핵심:** 정확히 **lower_bound**(target 이상이 처음 나오는 위치) = `bisect_left`.
- **힌트:** 반열린 구간 `[lo, hi)`, `hi=len(nums)`로 시작.

### 3. First Bad Version — [LeetCode #278](https://leetcode.com/problems/first-bad-version/)
버전 1..n 중 어느 지점부터 전부 "불량"이다. `isBadVersion(v)` API 호출을 최소화하며 첫 불량 버전을 찾는다.
- **핵심:** `F,F,...,F,T,T,...,T`의 **경계(첫 True)** 찾기. `pred = isBadVersion`.
- **힌트:** True면 `hi=mid`(mid 후보 유지), False면 `lo=mid+1`. 끝나면 `lo==hi`.

---

## 🟡 중급

### 4. Find First and Last Position — [LeetCode #34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
정렬 배열에서 `target`의 시작·끝 인덱스를 O(log n)으로. 없으면 `[-1, -1]`.
- **핵심:** 시작 = `bisect_left`, 끝 = `bisect_right - 1`. 두 번의 경계 탐색.
- **힌트:** `bisect_left` 위치의 값이 target이 아니면 존재하지 않는 것.

### 5. Search in Rotated Sorted Array — [LeetCode #33](https://leetcode.com/problems/search-in-rotated-sorted-array/)
오름차순 정렬 후 한 지점에서 회전된 배열에서 `target`을 O(log n)으로.
- **핵심:** `mid` 기준으로 **한 쪽 절반은 항상 정렬**돼 있다. 정렬된 쪽에 target이 들어가면 그쪽, 아니면 반대쪽.
- **힌트:** `nums[lo] <= nums[mid]`면 왼쪽이 정렬. `nums[lo] <= target < nums[mid]` 판정.

### 6. Koko Eating Bananas — [LeetCode #875](https://leetcode.com/problems/koko-eating-bananas/)
바나나 더미 `piles`, `h`시간 안에 모두 먹을 수 있는 **최소 시간당 속도 k**를 구한다.
- **핵심(결정 문제형):** `pred(k)` = "속도 k면 `sum(ceil(p/k)) <= h`?". k가 커질수록 필요 시간은 줄어 단조 → 처음 True인 최소 k.
- **힌트:** 답 범위 `[1, max(piles)]`. `ceil(p/k)`는 `(p+k-1)//k`.

### 7. 입국심사 — [프로그래머스 #43238](https://school.programmers.co.kr/learn/courses/30/lessons/43238)
심사관별 소요 시간 `times`가 있을 때 `n`명을 심사하는 **최소 시간**을 구한다.
- **핵심(결정 문제형):** `pred(t)` = "시간 t 동안 처리 인원 `sum(t // time) >= n`?". t가 커질수록 처리 인원 증가 → 단조.
- **힌트:** 답 범위 `[1, min(times) * n]`. 처음 True인 최소 t.

---

## 🔴 심화

### 8. 징검다리 — [프로그래머스 #43236](https://school.programmers.co.kr/learn/courses/30/lessons/43236)
길이 `distance`의 강에 바위 위치 `rocks`. 바위 `n`개를 제거해 **"밟는 지점 사이 최소 거리"의 최댓값**을 구한다.
- **핵심(결정 문제형·최소 간격 최대화):** `pred(gap)` = "최소 간격을 gap 이상으로 만들 때 제거 바위 수 `<= n`?". gap이 커질수록 제거 수 증가 → 단조. 참인 **가장 큰 gap**.
- **힌트:** 바위를 정렬하고 도착점(distance)을 끝에 추가. 인접 간격이 gap 미만이면 그 바위를 제거(카운트).

---

## 학습 포인트 정리
- **먼저 "무엇을 이분 탐색하는가"를 정하라.** 값(인덱스)인가, 정답(값)인가.
- **경계 탐색 = `bisect`.** lower/upper bound를 직접 짜기 전에 `bisect_left`/`bisect_right`를 떠올려라.
- **결정 문제형의 3요소:** (1) 답 범위 `[lo, hi]` (2) 단조 판별식 `pred(x)` (3) "처음 True(또는 마지막 True)"를 찾는 표준 틀.
- **범위(hi)는 넉넉하고 안전하게.** 극단값(가장 느린/빠른 경우)을 hi로 잡아 정답 누락을 막는다.
- **무한 루프·off-by-one은 "닫힌 vs 반열린" 틀을 섞을 때** 생긴다. 한 가지 틀로 통일하라.

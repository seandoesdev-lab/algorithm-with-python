---
day: 23
phase: 2-core-algorithms
title: 알고리즘 기초 복습 (Core Algorithms Review) — 연습문제
tags: [phase/2, topic/review, topic/algorithm, problems]
---

# Day 23 — 연습문제 (알고리즘 기초 복습)

> 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 풀이 코드는 [solutions.py](solutions.py) 참고. **출처는 LeetCode·프로그래머스만.**
> 이 세트의 목적은 "푸는 것"보다 **문제 신호를 보고 어떤 기법(technique)을 꺼낼지 1초 만에 판단**하는 것이다.

---

## 1. Binary Search 🟢

- **출처:** [LeetCode #704](https://leetcode.com/problems/binary-search/)
- **기법:** 이분 탐색 (Binary Search)
- **요약:** 오름차순 정렬된 배열 `nums`와 `target`이 주어진다. `target`의 인덱스를 반환하고, 없으면 `-1`을 반환하라. O(log n) 요구.
- **예:** `nums=[-1,0,3,5,9,12], target=9` → `4`
- **신호:** "정렬돼 있다 + 값을 찾는다 + O(log n)". 이분 탐색의 원형. `lo <= hi` 경계와 `lo=mid+1`/`hi=mid-1` 갱신으로 무한 루프를 막는 것이 핵심.

## 2. Two Sum II — Input Array Is Sorted 🟢

- **출처:** [LeetCode #167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- **기법:** 투 포인터 (Two Pointers)
- **요약:** **정렬된** 1-indexed 배열에서 더해서 `target`이 되는 두 수의 인덱스(1부터)를 반환하라.
- **예:** `numbers=[2,7,11,15], target=9` → `[1,2]`
- **신호:** "정렬된 배열 + 두 수의 합". 양 끝 포인터로 시작해 합이 크면 오른쪽을 당기고, 작으면 왼쪽을 민다. O(n)/O(1). (해시로도 O(n)이지만 정렬 전제에선 투 포인터가 O(1) 공간.)

## 3. 체육복 🟢 ⚫(프로그래머스)

- **출처:** [프로그래머스 #42862](https://school.programmers.co.kr/learn/courses/30/lessons/42862)
- **기법:** 그리디 (Greedy)
- **요약:** 전체 학생 수 `n`, 체육복을 잃어버린 학생 `lost`, 여벌이 있는 학생 `reserve`가 주어진다. 여벌 있는 학생은 **바로 앞/뒤 번호**에게만 빌려줄 수 있다. 체육수업을 들을 수 있는 최대 학생 수를 구하라.
- **예:** `n=5, lost=[2,4], reserve=[1,3,5]` → `5`
- **신호:** "각자 앞/뒤에게만 빌려준다 + 최대 인원". 번호 순으로 훑으며 **앞 번호부터 먼저 빌려주는** 그리디가 최적. 함정: 여벌이 있는데 본인도 잃어버린 학생(교집합)은 빌려줄 수 없다 → 먼저 제거해야 한다.

## 4. Longest Substring Without Repeating Characters 🟡

- **출처:** [LeetCode #3](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
- **기법:** 슬라이딩 윈도우 (Sliding Window, 가변 크기)
- **요약:** 문자열 `s`에서 **중복 문자가 없는** 가장 긴 부분 문자열의 길이를 구하라.
- **예:** `"abcabcbb"` → `3`("abc"), `"pwwkew"` → `3`("wke")
- **신호:** "연속된 부분 문자열 + 조건(중복 없음)을 만족하는 최대 길이". 창의 오른쪽을 늘리다 중복을 만나면 왼쪽을 그 문자 다음으로 당긴다. `dict`로 각 문자의 마지막 위치를 O(1)에 관리. O(n).

## 5. Container With Most Water 🟡

- **출처:** [LeetCode #11](https://leetcode.com/problems/container-with-most-water/)
- **기법:** 투 포인터 (Two Pointers)
- **요약:** 높이 배열 `height`에서 두 선을 골라 물을 담을 때 담을 수 있는 최대 넓이를 구하라. 넓이 = `min(h[i], h[j]) * (j - i)`.
- **예:** `[1,8,6,2,5,4,8,3,7]` → `49`
- **신호:** "양 끝에서 좁혀가며 최대". 양 끝에서 시작해 **더 낮은 쪽 포인터를 안으로** 옮긴다(낮은 쪽을 옮겨야 높이가 커질 여지가 있음). 정렬 전제 없이 성립하는 투 포인터 그리디. O(n).

## 6. Merge Intervals 🟡

- **출처:** [LeetCode #56](https://leetcode.com/problems/merge-intervals/)
- **기법:** 정렬 + 그리디 (Sort + Greedy)
- **요약:** 구간 배열 `intervals`에서 겹치는 구간을 모두 병합해 반환하라.
- **예:** `[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`
- **신호:** "구간 + 병합/겹침". **시작점 기준 정렬**이 첫 수. 정렬 후 앞에서부터, 현재 구간의 시작이 직전 병합 구간의 끝 이하면 끝을 `max`로 확장, 아니면 새 구간으로 추가. O(n log n).

## 7. Jump Game 🟡

- **출처:** [LeetCode #55](https://leetcode.com/problems/jump-game/)
- **기법:** 그리디 (Greedy)
- **요약:** 각 칸의 값이 그 칸에서 점프할 수 있는 최대 거리인 배열이 주어진다. 0번 칸에서 시작해 마지막 칸에 도달할 수 있으면 `True`.
- **예:** `[2,3,1,1,4]` → `True`, `[3,2,1,0,4]` → `False`
- **신호:** "도달 가능 여부 + 각 칸의 최대 이동". **지금까지 닿을 수 있는 가장 먼 인덱스(farthest)**를 그리디로 갱신한다. 현재 인덱스가 farthest를 넘으면 실패. O(n)/O(1). DP로도 풀리지만 그리디가 압도적으로 간결.

## 8. Koko Eating Bananas 🟡

- **출처:** [LeetCode #875](https://leetcode.com/problems/koko-eating-bananas/)
- **기법:** 정답에 대한 이분 탐색 (Parametric Binary Search)
- **요약:** 바나나 더미 `piles`와 시간 `h`가 주어진다. 시간당 먹는 개수 `k`를 고를 때, `h`시간 안에 모두 먹을 수 있는 **최소 `k`**를 구하라(한 시간에 한 더미만, 더미보다 적게 남으면 그 시간엔 그만 먹음).
- **예:** `piles=[3,6,7,11], h=8` → `4`
- **신호:** "…할 수 있는 최소 K + K가 크면 쉬워지고 작으면 어려워진다". **답 자체가 단조**다(`k`가 크면 걸리는 시간이 준다). 값이 아니라 `k`의 범위 `[1, max(piles)]`를 이분 탐색하고, 각 `k`의 총 시간 `sum(ceil(p/k))`가 `h` 이하인지 판정. O(n log(max)).

## 9. 구명보트 🟡 ⚫(프로그래머스)

- **출처:** [프로그래머스 #42885](https://school.programmers.co.kr/learn/courses/30/lessons/42885)
- **기법:** 정렬 + 투 포인터 + 그리디 (Sort + Two Pointers + Greedy)
- **요약:** 사람들의 몸무게 `people`과 보트 한계 무게 `limit`이 주어진다. 보트 하나엔 **최대 2명**, 합이 `limit` 이하. 모두 구출하는 최소 보트 수를 구하라.
- **예:** `people=[70,50,80,50], limit=100` → `3`
- **신호:** "짝지어 최소 개수 + 무게 한계". **정렬 후 양 끝 투 포인터**: 가장 무거운 사람과 가장 가벼운 사람을 같이 태울 수 있으면 둘 다, 아니면 무거운 사람만. 가장 가벼운 사람을 짝으로 붙이는 그리디가 최적. O(n log n).

## 10. Sort List 🔴

- **출처:** [LeetCode #148](https://leetcode.com/problems/sort-list/)
- **기법:** 분할정복(병합 정렬) + 연결 리스트 (Divide & Conquer on Linked List)
- **요약:** 단일 연결 리스트를 오름차순으로 정렬해 반환하라. O(n log n) 시간, O(1)에 가까운 추가 공간(재귀 스택 제외)을 요구.
- **예:** `4->2->1->3` → `1->2->3->4`
- **신호:** "연결 리스트 + O(n log n) 정렬". 배열이 아니라 **연결 리스트**라 임의 접근이 안 되므로, **느린/빠른 포인터(slow/fast)**로 가운데를 찾아 반으로 끊고(divide), 각각 재귀 정렬(conquer), 두 정렬된 리스트를 병합(combine). Phase 1(연결 리스트) + Phase 2(분할정복)의 종합.

---

## 풀이 전략 요약 (신호 → 기법)

| 문제의 신호 | 떠올릴 기법 | 이 세트의 예 |
|---|---|---|
| "정렬됨 + 값 찾기 + O(log n)" | 이분 탐색 | #704 |
| "정렬됨 + 두 수의 합/짝" | 투 포인터 | #167 |
| "앞/뒤에게만 빌려주기, 최대 인원" | 그리디 | 체육복 |
| "연속 부분 문자열의 최대 길이" | 슬라이딩 윈도우 | #3 |
| "양 끝에서 좁혀 최대 넓이" | 투 포인터 | #11 |
| "구간 병합/겹침" | 정렬 + 그리디 | #56 |
| "도달 가능? 각 칸 최대 이동" | 그리디(farthest) | #55 |
| "…하는 최소/최대 K, 답이 단조" | 정답 이분 탐색 | #875 |
| "짝지어 최소 개수 + 무게 한계" | 정렬 + 투 포인터 | 구명보트 |
| "연결 리스트 O(n log n) 정렬" | 분할정복(병합) | #148 |

> 관련 개념: [[concept]] · 각 기법의 자세한 설명은 [[Phase-2 MOC]]의 Day 16~22 참고.

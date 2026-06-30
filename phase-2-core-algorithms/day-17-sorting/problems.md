# Day 17 — 정렬 (Sorting) 연습문제

> 출처는 **프로그래머스 / LeetCode** 만 사용합니다. 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 풀이 코드와 복잡도 비교는 [solutions.py](solutions.py) 참고.

핵심은 **"무엇을 key로 정렬할 것인가"** 를 설계하는 것입니다. 정렬은 거의 항상 *전처리*이고, 그 뒤의 탐색/그리디/병합이 본 풀이입니다.

---

## 🟢 기초

### 1. Merge Sorted Array — [LeetCode #88](https://leetcode.com/problems/merge-sorted-array/)
정렬된 두 배열 `nums1`(뒤쪽 여유 공간 포함), `nums2`를 `nums1` 안에 정렬 상태로 병합한다.
- **핵심:** 앞에서부터 채우면 덮어쓰기가 생기므로 **뒤에서부터(가장 큰 값부터)** 채운다. O(m+n).
- **힌트:** 세 포인터 — `nums1`의 끝, `nums2`의 끝, 채울 위치.

### 2. K번째수 — [프로그래머스 #42748](https://school.programmers.co.kr/learn/courses/30/lessons/42748)
배열을 `[i, j, k]` 명령마다 i~j 구간을 잘라 정렬한 뒤 k번째 수를 구한다.
- **핵심:** 슬라이싱 `array[i-1:j]` 후 `sorted(...)[k-1]`. 제약이 작아 단순 정렬로 충분.
- **힌트:** 1-based 인덱스 주의.

---

## 🟡 중급

### 3. Sort an Array — [LeetCode #912](https://leetcode.com/problems/sort-an-array/)
배열을 오름차순 정렬한다. **내장 정렬 없이 O(n log n)** 으로 풀어야 한다.
- **핵심:** 병합 정렬 또는 힙 정렬을 직접 구현. 퀵 정렬은 최악 O(n²)이라 같은 값/정렬된 입력에 주의(랜덤 pivot 또는 3-way).
- **힌트:** 병합 정렬이 구현 안정적. 재귀 깊이 log n.

### 4. Sort Colors — [LeetCode #75](https://leetcode.com/problems/sort-colors/)
0,1,2로만 이루어진 배열을 제자리 정렬(네덜란드 국기 문제).
- **핵심:** 값 범위가 3개뿐 → **계수 정렬** O(n) 또는 **3-way 분할(Dutch flag)** 로 한 번 순회 O(n)·O(1).
- **힌트:** `low/mid/high` 세 포인터로 0은 앞, 2는 뒤로 보낸다.

### 5. Merge Intervals — [LeetCode #56](https://leetcode.com/problems/merge-intervals/)
겹치는 구간들을 병합한다.
- **핵심:** **시작점 기준 정렬** 후 한 번 훑으며, 직전 구간의 끝과 현재 시작을 비교해 겹치면 끝을 확장.
- **힌트:** 정렬이 전처리, 병합이 본풀이. O(n log n).

### 6. 가장 큰 수 — [프로그래머스 #42746](https://school.programmers.co.kr/learn/courses/30/lessons/42746)
정수들을 이어붙여 만들 수 있는 가장 큰 수를 구한다.
- **핵심:** 두 수 a, b를 문자열로 보고 `a+b` vs `b+a` 로 비교(`functools.cmp_to_key`).
- **힌트:** 결과가 `"000"`처럼 0으로 시작하면 `"0"` 반환(`int` 변환으로 처리 가능).

### 7. H-Index — [프로그래머스 #42747](https://school.programmers.co.kr/learn/courses/30/lessons/42747)
인용 횟수 배열에서 H-Index(h번 이상 인용된 논문이 h편 이상)를 구한다.
- **핵심:** **내림차순 정렬** 후, `citations[i] >= i+1` 을 만족하는 가장 큰 i+1을 찾는다.
- **힌트:** 정렬 후 한 번 순회로 O(n log n).

---

## 🔴 심화 / 확장

### 8. Largest Number — [LeetCode #179](https://leetcode.com/problems/largest-number/)
"가장 큰 수"(프로그래머스 #42746)의 LeetCode 버전. 반환 타입이 문자열.
- **핵심:** 동일하게 `cmp_to_key`로 `x+y` vs `y+x` 비교. 전부 0이면 `"0"`.
- **확장:** 안정성·전이성(transitivity)이 성립하는 비교인지 따져보기.

---

## 학습 포인트 정리
- **정렬 = 전처리.** "막히면 정렬부터" 시도해 보라(구간 문제, 그리디, 투 포인터의 시작).
- **key 설계가 9할.** 다중 기준은 튜플 key, 이어붙이기/사용자 정의 순서는 `cmp_to_key`.
- **값 범위가 좁으면 계수 정렬** 로 O(n) (Sort Colors).
- **내장 정렬 금지 문제** 에선 병합/힙 정렬을 직접 구현(퀵의 최악 O(n²) 주의).

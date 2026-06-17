# Day 6 연습문제 — 배열과 동적 리스트 (Array & List)

> 난이도 표기: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출(대기업·빈출)
> 출처: 프로그래머스(programmers.co.kr), LeetCode(leetcode.com)
> 해설·여러 접근 비교는 `solutions.py` 참고.

---

## 🟢 문제 1. 배열의 평균값
- 출처: 프로그래머스 #120817 — https://school.programmers.co.kr/learn/courses/30/lessons/120817
- 카테고리: 배열 순회 / 기초
- 요약: 정수 배열 `numbers`의 원소 평균값을 반환한다.
- 💭 힌트: `sum(numbers) / len(numbers)`. 합과 길이를 한 번씩 훑으면 O(n).

## 🟢 문제 2. Running Sum of 1d Array (누적 합)
- 출처: LeetCode #1480 — https://leetcode.com/problems/running-sum-of-1d-array/
- 카테고리: 배열 / 누적 합 (Prefix Sum)
- 요약: `runningSum[i] = nums[0] + ... + nums[i]` 인 누적 합 배열을 반환한다.
- 💭 힌트: 직전 누적값에 현재 원소를 더해 가며 한 번만 훑으면 O(n).
  `itertools.accumulate`로 한 줄에도 가능. (제자리 갱신도 연습해 보자.)

## 🟡 문제 3. 배열 회전시키기
- 출처: 프로그래머스 #120844 — https://school.programmers.co.kr/learn/courses/30/lessons/120844
- 카테고리: 배열 / 슬라이싱·회전
- 요약: 배열 `numbers`를 `direction`("left"/"right") 방향으로 한 칸 회전한 배열을 반환한다.
- 💭 힌트: 오른쪽 회전은 `[마지막] + 나머지`, 왼쪽 회전은 `나머지 + [첫]`. 슬라이싱으로 한 줄,
  또는 `collections.deque`의 `rotate`로도 가능.

## 🟡 문제 4. 두 개 뽑아서 더하기
- 출처: 프로그래머스 #68644 — https://school.programmers.co.kr/learn/courses/30/lessons/68644
- 카테고리: 배열 / 조합 (Combination)
- 요약: 서로 다른 두 인덱스의 원소를 더해 만들 수 있는 모든 수를 **중복 없이 오름차순**으로 반환한다.
- 💭 힌트: 모든 (i<j) 쌍의 합을 `set`에 담아 중복 제거 후 `sorted`. 쌍의 수는 O(n^2).
  `itertools.combinations(numbers, 2)`로 간결하게.

## 🔴 문제 5. Rotate Array (배열을 k칸 회전, 제자리)
- 출처: LeetCode #189 — https://leetcode.com/problems/rotate-array/
- 카테고리: 배열 / 제자리(in-place) 처리
- 요약: 배열을 오른쪽으로 `k`칸 회전한다. 가능하면 **O(1) 추가 공간**으로 제자리에서.
- 💭 힌트: `k %= n`으로 정규화. 슬라이싱이면 한 줄(`nums[:] = nums[-k:] + nums[:-k]`)이지만
  O(n) 공간이다. **3번 뒤집기(reverse) 트릭**: 전체 뒤집고 -> 앞 k개 뒤집고 -> 나머지 뒤집기 = O(1) 공간.

## ⚫ 문제 6. Product of Array Except Self (빈출 - 나눗셈 없이)
- 출처: LeetCode #238 — https://leetcode.com/problems/product-of-array-except-self/
- 카테고리: 배열 / 누적 곱 (Prefix·Suffix Product) — 인터뷰 빈출
- 요약: `answer[i]` = 자기 자신을 뺀 나머지 모든 원소의 곱. **나눗셈 금지**, O(n) 시간.
- 💭 힌트: 왼쪽 누적 곱(prefix)과 오른쪽 누적 곱(suffix)을 곱한다. 출력 배열을 prefix로 채운 뒤,
  오른쪽에서 왼쪽으로 suffix를 곱해 가면 추가 공간 O(1)(출력 제외). 0이 섞여도 동작한다.

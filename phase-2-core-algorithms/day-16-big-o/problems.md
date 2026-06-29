# Day 16 — 연습문제 (Problems): 시간복잡도와 Big-O

> 오늘의 목표는 "정답"이 아니라 **목표 복잡도에 맞는 풀이를 고르는 감각**이다.
> 각 문제에서 먼저 "느린 풀이(brute force)"를 떠올린 뒤, 제한 조건을 보고 "더 빠른 풀이가 필요한가?"를 판단하라.
> 출처: 프로그래머스 / LeetCode. 해설 코드는 [solutions.py](solutions.py).

---

## 1. Contains Duplicate 🟢기초 — O(n) 해시
- **출처:** [LeetCode #217](https://leetcode.com/problems/contains-duplicate/)
- **요약:** 정수 배열에 중복된 값이 하나라도 있으면 `True`, 모두 다르면 `False`.
- **핵심 신호:** "존재하는가?" → 해시(set).
- **복잡도 사고:** 모든 쌍 비교는 O(n²). `set` 멤버십(O(1))으로 한 번 순회하면 O(n).
- **힌트:** 길이를 비교해도 된다 — `len(set(nums)) != len(nums)`.

## 2. Two Sum 🟢기초 — O(n) 해시
- **출처:** [LeetCode #1](https://leetcode.com/problems/two-sum/)
- **요약:** 두 원소의 합이 `target`이 되는 인덱스 쌍을 반환.
- **핵심 신호:** "합이 되는 짝" + "본 적 있는 값" → dict.
- **복잡도 사고:** 이중 루프 O(n²) → "필요한 짝(`target - x`)을 이미 봤는지" dict로 조회하면 O(n).
- **함정:** 같은 원소를 두 번 쓰면 안 된다. dict에 넣는 시점(조회 후 저장)으로 자연히 해결된다.

## 3. Binary Search 🟢기초 — O(log n)
- **출처:** [LeetCode #704](https://leetcode.com/problems/binary-search/)
- **요약:** **정렬된** 배열에서 `target`의 인덱스를 찾고, 없으면 -1.
- **핵심 신호:** "정렬되어 있다" + "찾기" → 이분 탐색.
- **복잡도 사고:** 선형 탐색 O(n) → 매 단계 절반을 버려 O(log n).
- **함정:** `mid = (lo + hi) // 2`, 경계는 `while lo <= hi`. off-by-one에 주의.

## 4. Best Time to Buy and Sell Stock 🟢기초 — O(n) 1회 순회
- **출처:** [LeetCode #121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
- **요약:** 하루에 한 번 사고 나중에 한 번 팔 때의 최대 이익(불가능하면 0).
- **핵심 신호:** "지금까지의 최소값"을 들고 가며 한 번 훑기.
- **복잡도 사고:** 모든 (사는 날, 파는 날) 쌍 O(n²) → 지금까지의 최저가를 갱신하며 O(n).
- **힌트:** `min_price`를 갱신하고, `price - min_price`로 이익 후보를 매번 갱신.

## 5. Maximum Subarray 🟡중급 — O(n) Kadane
- **출처:** [LeetCode #53](https://leetcode.com/problems/maximum-subarray/)
- **요약:** 연속 부분 배열의 합 중 최댓값(원소 1개 이상).
- **핵심 신호:** "연속 구간의 최대 합" → Kadane 알고리즘.
- **복잡도 사고:** 모든 구간 합 O(n²)(누적합 써도 O(n²)) → "직전 합을 이어갈지 새로 시작할지"만 O(n).
- **함정:** 전부 음수인 경우. `cur`와 `best`를 0이 아니라 `a[0]`으로 초기화.

## 6. 완주하지 못한 선수 🟢기초 — O(n) 해시
- **출처:** [프로그래머스 #42576](https://school.programmers.co.kr/learn/courses/30/lessons/42576)
- **요약:** `participant`(참가자)에서 `completion`(완주자)을 빼고 남은 한 명을 반환. **동명이인 가능.**
- **핵심 신호:** "몇 명?" + 동명이인 → `Counter`(빈도 해시).
- **복잡도 사고:** 참가자 최대 10만 명 → O(n²) 탈락. `Counter` 차집합으로 O(n).
- **함정:** 동명이인 때문에 단순 `set` 차집합은 틀린다. **개수**를 세야 한다.

## 7. 두 개 뽑아서 더하기 🟢기초 — O(n²)이 허용되는 작은 n
- **출처:** [프로그래머스 #68644](https://school.programmers.co.kr/learn/courses/30/lessons/68644)
- **요약:** 서로 다른 두 인덱스의 원소 합으로 만들 수 있는 모든 값을 오름차순·중복 제거하여 반환.
- **핵심 신호:** "모든 쌍" + n ≤ 100.
- **복잡도 사고:** n이 100 이하라 모든 쌍 O(n²)=1만 번이면 충분. **무리하게 최적화할 필요 없다** — Big-O는 "필요할 때만" 줄인다.
- **힌트:** `set`으로 중복 합을 모으고 마지막에 `sorted`.

---

### 복습 체크리스트
- [ ] 각 문제의 **제한 조건(n의 범위)** 을 먼저 확인했는가?
- [ ] "느린 풀이"의 복잡도를 말할 수 있는가? (예: 모든 쌍 → O(n²))
- [ ] 그 복잡도가 제한을 넘는지 판단했는가? (n=10만이면 O(n²) 탈락)
- [ ] 더 빠른 풀이의 복잡도와 **추가 메모리(공간복잡도)** 를 말할 수 있는가?
- [ ] 7번처럼 **굳이 최적화가 필요 없는** 경우를 구분했는가?

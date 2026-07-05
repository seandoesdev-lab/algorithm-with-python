# Day 20 — 슬라이딩 윈도우 (Sliding Window): 연습문제

> 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 출처는 **프로그래머스 / LeetCode만** 사용합니다. 풀이 코드는 [solutions.py](solutions.py) 참고.
> 학습 순서: 고정 창 → 가변 창(확장-수축) → 해시/문자 카운트 창 → 단조 덱.

---

## 1. Maximum Average Subarray I 🟢
- **출처:** [LeetCode #643](https://leetcode.com/problems/maximum-average-subarray-i/)
- **요약:** 정수 배열 `nums`와 정수 `k`가 주어질 때, 길이 `k`인 연속 부분 배열의 **최대 평균**을 구하라.
- **핵심:** 고정 크기 창. 앞 `k`개 합을 먼저 구하고, 창을 한 칸 밀 때 `합 += nums[right] - nums[right-k]`로 O(1) 갱신.
- **함정:** 매 구간을 다시 합산하면 O(n·k)로 느리다. 초기 창 한 번만 전체 합산할 것. 음수가 있어도 고정 창은 문제없다(수축이 없으므로).

## 2. Minimum Size Subarray Sum 🟡
- **출처:** [LeetCode #209](https://leetcode.com/problems/minimum-size-subarray-sum/)
- **요약:** 양의 정수 배열 `nums`와 `target`이 주어질 때, 합이 `target` **이상**이 되는 연속 부분 배열의 **최소 길이**를 구하라(없으면 0).
- **핵심:** 가변 창. 오른쪽으로 확장하다 `total >= target`이면 길이를 기록하고 왼쪽을 조인다.
- **함정:** 확장-수축 논리는 **원소가 모두 양수**여야 성립한다. 음수가 섞이면 [[day-14-prefix-sum/concept|누적 합]]+정렬/이분탐색 등 다른 접근이 필요하다.

## 3. Longest Substring Without Repeating Characters 🟡
- **출처:** [LeetCode #3](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
- **요약:** 문자열 `s`에서 **중복 문자가 없는 가장 긴 부분 문자열**의 길이를 구하라.
- **핵심:** 가변 창 + 해시맵(문자 → 마지막 인덱스). 중복을 만나면 `left = max(left, last[c] + 1)`로 왼쪽을 점프.
- **함정:** `max(...)`를 빼먹으면 `left`가 뒤로 후퇴해 답이 틀린다. 슬라이딩 윈도우 버그 1순위.

## 4. Find All Anagrams in a String 🟡
- **출처:** [LeetCode #438](https://leetcode.com/problems/find-all-anagrams-in-a-string/)
- **요약:** 문자열 `s`, `p`가 주어질 때, `s` 안에서 `p`의 **아나그램이 시작되는 모든 인덱스**를 반환하라.
- **핵심:** 길이 `len(p)`로 고정한 창의 문자 개수와 `p`의 문자 개수가 같은 순간을 찾는다.
- **함정:** 창이 아직 `len(p)`에 못 미쳤을 때 비교하면 오답. 창을 벗어나는 왼쪽 문자를 제때 제거해야 한다.

## 5. Permutation in String 🟡
- **출처:** [LeetCode #567](https://leetcode.com/problems/permutation-in-string/)
- **요약:** `s1`의 **어떤 순열이 `s2`의 부분 문자열로 존재**하는지 판별하라(True/False).
- **핵심:** #438과 사실상 동일 골격. 창 안 문자 카운트가 `s1` 카운트와 일치하면 True.
- **함정:** "순열 = 문자 개수만 같으면 됨"을 이용한다. 순서는 상관없다. `formed`(일치한 문자 종류 수)를 관리하면 매 창 O(1) 비교.

## 6. 보석 쇼핑 🟡
- **출처:** [프로그래머스 #67258](https://school.programmers.co.kr/learn/courses/30/lessons/67258)
- **요약:** 진열대 순서대로 보석 이름 배열 `gems`가 주어질 때, **모든 종류의 보석을 최소 한 개씩 포함**하는 가장 짧은 연속 구간 `[시작, 끝]`(1-indexed)을 구하라. 길이가 같으면 시작이 작은 것.
- **핵심:** 가변 창 + 해시맵(창 안 각 보석 개수). 전체 종류 수 = `len(set(gems))`. 창이 모든 종류를 포함하면 왼쪽을 조이며 최소 길이 갱신.
- **함정:** "모든 종류 포함"을 유지하면서 최소 구간을 찾아야 한다. 창 안 종류 수가 전체 종류 수와 같은 동안 수축.

## 7. Minimum Window Substring 🔴
- **출처:** [LeetCode #76](https://leetcode.com/problems/minimum-window-substring/)
- **요약:** 문자열 `s`, `t`가 주어질 때, `t`의 **모든 문자(중복 포함)를 담는 가장 짧은 부분 문자열**을 구하라(없으면 "").
- **핵심:** 가변 창 + `need`/`window` 딕셔너리 + `formed`(조건을 만족한 문자 종류 수). `formed == 필요한 종류 수`이면 수축.
- **함정:** 중복 문자 개수까지 맞춰야 한다("AABC"의 A는 2개 필요). 매번 딕셔너리 전체 비교는 느리니 `formed` 카운터로 O(1) 판정.

## 8. Sliding Window Maximum 🔴
- **출처:** [LeetCode #239](https://leetcode.com/problems/sliding-window-maximum/)
- **요약:** 배열 `nums`와 창 크기 `k`가 주어질 때, 창이 왼쪽에서 오른쪽으로 이동하며 **각 창의 최댓값**을 모두 반환하라.
- **핵심:** 단조 덱(monotonic deque). 덱에 **인덱스**를 값이 단조 감소하도록 유지하면 맨 앞이 항상 창 최댓값.
- **함정:** 매 창마다 `max()`를 부르면 O(n·k)로 TLE. 새 값보다 작은 뒤쪽 인덱스를 pop, 창을 벗어난 앞쪽 인덱스를 popleft 하는 것이 정석.

---

### 추천 풀이 순서
1. **#643** — 고정 창의 "초기 합 → 밀기" 감각을 잡는다.
2. **#209 → #3** — 가변 창의 확장-수축 골격(최소 길이 / 최장 길이 두 변형).
3. **#438 → #567** — 고정 창 + 문자 카운트(둘은 거의 같은 코드).
4. **#67258** — 가변 창 + "모든 종류 포함" 조건.
5. **#76** — `need`/`window`/`formed` 정석 패턴의 완성형.
6. **#239** — 단조 덱으로 [[day-08-queue-deque/concept|덱]]과 슬라이딩 윈도우를 잇는다.

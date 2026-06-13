# Day 02 연습문제 — 자료형과 컬렉션 (Types & Collections)

> 난이도 표기: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출(대기업)

---

## 🟢 문제 1. 두 수의 합 (Two Sum)

- 출처: LeetCode #1 — https://leetcode.com/problems/two-sum/
- 카테고리: dict, 해시(hash), 배열(array)
- 요약: 정수 배열 `nums`와 목표 값 `target`이 주어진다. 두 수를 더해 `target`이 되는 두 인덱스를 반환한다. 정확히 하나의 답이 존재하며, 같은 원소를 두 번 쓸 수 없다.
- 제한: 2 ≤ nums.length ≤ 10⁴ / 답은 유일
- 💭 힌트:
  - **접근 A — dict 한 번 순회(one-pass)**: 순회하면서 `target - nums[i]`가 이미 dict에 있으면 정답. 없으면 `{nums[i]: i}`를 기록 → 전체 O(N) 시간, O(N) 공간.
  - **접근 B — 이중 반복문(brute force)**: 모든 쌍을 확인 → O(N²). 정답은 나오지만 입력이 크면 느림.
  - 핵심 관찰: dict를 "지금까지 본 숫자 → 인덱스" 보조 테이블로 활용하면 O(N²) → O(N)으로 줄일 수 있다.

---

## 🟢 문제 2. 중복 원소 포함 여부 (Contains Duplicate)

- 출처: LeetCode #217 — https://leetcode.com/problems/contains-duplicate/
- 카테고리: set, 해시(hash), 배열(array)
- 요약: 정수 배열 `nums`가 주어질 때, 어떤 값이 두 번 이상 등장하면 `True`, 모든 원소가 서로 다르면 `False`를 반환한다.
- 제한: 1 ≤ nums.length ≤ 10⁵
- 💭 힌트:
  - **접근 A — set 변환**: `len(nums) != len(set(nums))` 한 줄 비교. set은 중복을 제거하므로 길이가 줄었다면 중복 존재 → O(N) 시간, O(N) 공간.
  - **접근 B — set 순회 조기 종료**: 순회 중 이미 seen에 있으면 바로 `True` 반환. 중복이 앞부분에 있으면 빠름 → 평균적으로 접근 A보다 실용적.
  - **접근 C — 정렬 후 인접 비교**: 정렬 후 `nums[i] == nums[i+1]` 비교 → O(N log N) 시간, O(1) 추가 공간. 공간 제약이 있을 때 유리.

---

## 🟡 문제 3. 전화번호 목록 (Phone Book)

- 출처: 프로그래머스 해시 Lv.2 — https://school.programmers.co.kr/learn/courses/30/lessons/42577
- 카테고리: dict, set, 문자열 해시(string hash)
- 요약: 전화번호부에 담긴 전화번호 중에서, 한 번호가 다른 번호의 접두어인 경우가 있으면 `False`, 그렇지 않으면 `True`를 반환한다.
- 제한: 1 ≤ 전화번호 수 ≤ 1,000,000 / 각 번호 길이 ≤ 20
- 💭 힌트:
  - **접근 A — set + 접두어 직접 확인**: 모든 번호를 set에 저장. 각 번호를 순회하며 길이 1부터 len-1까지 잘라낸 접두어가 set에 있으면 `False` → O(N × L²) 최악 (L=번호 최대 길이).
  - **접근 B — 정렬 후 인접 비교**: 번호를 정렬하면 접두어 관계인 번호들이 인접해 있다. `phone_list[i+1].startswith(phone_list[i])`만 확인하면 됨 → O(N log N) 시간.
  - 핵심 관찰: 번호 수가 최대 100만이므로, set을 이용해 접두어를 O(1)로 조회하거나 정렬로 비교 범위를 줄이는 것이 중요.

---

## ⚫ 문제 4. 완주하지 못한 선수 (Marathon — 카카오 출제 유형)

- 출처: 프로그래머스 해시 Lv.1 — https://school.programmers.co.kr/learn/courses/30/lessons/42576
- 카테고리: dict, Counter, 해시(hash)
- 요약: 마라톤 참가자 목록과 완주자 목록이 주어진다. 단 한 명이 완주하지 못했다. 그 선수의 이름을 반환한다. (동명이인 존재 가능)
- 제한: 참가자 수 ≤ 100,000 / 동명이인 가능
- 💭 힌트:
  - **접근 A — dict 빈도 카운팅**: 참가자 이름을 `dict`에 빈도 카운팅(+1). 완주자를 순회하며 빈도 차감(-1). 빈도가 1 이상인 이름이 정답.
  - **접근 B — collections.Counter**: `Counter(participant) - Counter(completion)` → 남은 원소가 미완주자. 한 줄 풀이 가능.
  - 핵심: 단순 set 사용 불가 — 동명이인이 있으므로 중복 카운팅 필요.
  - 정렬로도 풀 수 있음(O(n log n)): 두 리스트를 정렬 후 나란히 비교.

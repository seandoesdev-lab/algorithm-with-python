# Day 9 연습문제 — 해시: dict / set (Hashing)

> 난이도 표기: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출(대기업·빈출)
> 출처: 프로그래머스(programmers.co.kr), LeetCode(leetcode.com)
> 해설·여러 접근 비교는 `solutions.py` 참고.

---

## 🟢 문제 1. 완주하지 못한 선수
- 출처: 프로그래머스 #42576 — https://school.programmers.co.kr/learn/courses/30/lessons/42576
- 카테고리: 해시 / 개수 세기 (기초)
- 요약: 마라톤 참가자 명단 `participant`와 완주자 명단 `completion`이 주어진다(동명이인 가능).
  완주하지 **못한** 단 한 명의 이름을 반환한다.
- 💭 힌트: 동명이인 때문에 단순 `set` 차집합은 안 된다(개수까지 봐야 함). `Counter(participant)`에서
  `Counter(completion)`을 **빼면** 남는 한 명이 답이다(`Counter` 뺄셈은 개수 0 이하를 제거).

## 🟢 문제 2. 폰켓몬
- 출처: 프로그래머스 #1845 — https://school.programmers.co.kr/learn/courses/30/lessons/1845
- 카테고리: 해시 / 집합(set) (기초)
- 요약: 폰켓몬 종류 번호 배열 `nums`에서 **절반(N/2마리)**을 고를 때, 가질 수 있는 **서로 다른
  종류의 최대 개수**를 반환한다.
- 💭 힌트: 고를 수 있는 마리 수는 `N//2`로 고정. 서로 다른 종류 수는 `len(set(nums))`.
  둘 중 **작은 값**이 답이다(`min(N//2, len(set(nums)))`).

## 🟢 문제 3. Two Sum
- 출처: LeetCode #1 — https://leetcode.com/problems/two-sum/
- 카테고리: 해시 / 보수 찾기 (기초·빈출)
- 요약: 정수 배열 `nums`와 `target`이 주어질 때, 합이 `target`이 되는 두 원소의 **인덱스**를 반환한다.
- 💭 힌트: 이중 루프는 O(n^2). `값 -> 인덱스` dict를 만들며 한 번 순회하고, 매 원소에서
  `target - x`(보수)가 이미 dict에 있는지 평균 O(1)로 확인하면 **O(n)**.

## 🟡 문제 4. 전화번호 목록
- 출처: 프로그래머스 #42577 — https://school.programmers.co.kr/learn/courses/30/lessons/42577
- 카테고리: 해시 / 접두사(prefix) 검사 (중급)
- 요약: 전화번호 문자열 배열 `phone_book`에서 **어떤 번호가 다른 번호의 접두어**이면 `False`,
  아니면 `True`를 반환한다.
- 💭 힌트: 모든 쌍 비교는 O(n^2). 번호들을 `set`에 넣고, 각 번호의 **모든 접두사**(앞 1글자, 2글자, ...)가
  set에 있는지 확인하면 번호 길이에 비례 -> 빠르다. (정렬 후 인접만 비교하는 방법도 가능)

## 🟡 문제 5. 위장
- 출처: 프로그래머스 #42578 — https://school.programmers.co.kr/learn/courses/30/lessons/42578
- 카테고리: 해시 / 경우의 수(곱의 법칙) (중급)
- 요약: 의상 `[이름, 종류]` 목록 `clothes`가 주어진다. 종류별로 **안 입거나 1개 입는** 선택을
  조합해 만들 수 있는 **서로 다른 조합의 수**를 반환한다(최소 1개는 입어야 함).
- 💭 힌트: 종류별 개수를 `Counter`로 센다. 각 종류는 "그 종류 중 하나 입기 + 안 입기" = `(개수+1)`가지.
  모든 종류에 대해 곱한 뒤, **전부 안 입는 경우 1가지**를 뺀다: `prod(cnt+1) - 1`.

## 🟡 문제 6. Group Anagrams
- 출처: LeetCode #49 — https://leetcode.com/problems/group-anagrams/
- 카테고리: 해시 / 그룹화 (중급·빈출)
- 요약: 문자열 배열 `strs`를 **애너그램(구성 글자가 같음)끼리** 묶어 반환한다.
- 💭 힌트: 같은 애너그램은 **정렬하면 동일한 문자열**이 된다. `tuple(sorted(w))`(또는 정렬 문자열)을
  **키**로 `defaultdict(list)`에 모은다. 글자 개수 벡터(길이 26 tuple)를 키로 쓰면 정렬 없이 O(n*k).

## 🟡 문제 7. Top K Frequent Elements
- 출처: LeetCode #347 — https://leetcode.com/problems/top-k-frequent-elements/
- 카테고리: 해시 / 빈도 + 정렬·힙 (중급·빈출)
- 요약: 배열 `nums`에서 **가장 자주 등장하는 상위 k개** 원소를 반환한다.
- 💭 힌트: `Counter(nums)`로 빈도를 센 뒤 `most_common(k)`. 또는 빈도를 인덱스로 하는
  **버킷 정렬**로 O(n), 또는 힙(`heapq.nlargest`, Day 12 예고)으로 O(n log k).

## 🔴 문제 8. Longest Consecutive Sequence
- 출처: LeetCode #128 — https://leetcode.com/problems/longest-consecutive-sequence/
- 카테고리: 해시 / set 멤버십 (심화)
- 요약: 정렬되지 않은 배열에서 **연속된 정수**로 이루어진 가장 긴 수열의 길이를 **O(n)**에 구한다.
- 💭 힌트: 정렬하면 O(n log n)이지만 문제는 O(n)을 요구. 전부 `set`에 넣고, 각 수 `x`에 대해
  **`x-1`이 set에 없을 때만**(수열의 시작점) `x+1, x+2, ...`를 set 멤버십으로 이어 세어 길이를 잰다.
  각 수는 최대 한 번만 확장에 쓰이므로 전체 O(n).

## ⚫ 문제 9. 베스트앨범 (기출·빈출)
- 출처: 프로그래머스 #42579 — https://school.programmers.co.kr/learn/courses/30/lessons/42579
- 카테고리: 해시 / 그룹별 집계 + 정렬 (기업 코테 빈출)
- 요약: 노래의 장르 `genres`와 재생 횟수 `plays`가 주어진다. (1) **총 재생수가 많은 장르 먼저**,
  (2) 같은 장르 내에서는 **재생수 많은 곡 먼저**, 같으면 **고유번호(인덱스) 낮은 곡 먼저**로
  각 장르에서 최대 2곡을 골라 **수록 순서(인덱스)**를 반환한다.
- 💭 힌트: 두 개의 해시가 필요하다. ① 장르별 총 재생수 `defaultdict(int)`, ② 장르별 `(재생수, 인덱스)`
  목록 `defaultdict(list)`. 장르는 총합 내림차순 정렬, 각 장르 안에서는 `(-재생수, 인덱스)`로 정렬해
  앞 2곡의 인덱스를 모은다. 정렬 키 설계가 핵심.

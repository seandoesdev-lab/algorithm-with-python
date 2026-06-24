# Day 13 연습문제 — 해시맵 응용 (Hashmap Patterns)

> 난이도 표기: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출(대기업·빈출)
> 출처: 프로그래머스(programmers.co.kr), LeetCode(leetcode.com)
> 해설·여러 접근 비교는 [solutions.py](solutions.py) 참고 (각 문제 assert 자체 테스트).

---

## 🟡 문제 1. Subarray Sum Equals K
- 출처: LeetCode #560 — https://leetcode.com/problems/subarray-sum-equals-k/
- 카테고리: 누적합 + 해시맵 (중급·매우 빈출)
- 요약: 정수 배열 `nums`와 정수 `k`가 주어질 때, **합이 k인 연속 부분배열(subarray)의 개수**를 반환한다.
- 💭 힌트: 모든 구간을 보면 O(n²). 누적합 `prefix`를 만들며 `prefix - k`를 **과거에 몇 번 봤는지**를
  `defaultdict(int)`로 즉시 카운트하면 O(n). **`seen[0] = 1`**(빈 접두부)로 시작해 "맨 앞부터의 구간"을
  놓치지 않는다. 음수가 섞여 있어 슬라이딩 윈도우로는 못 푼다는 점이 핵심.

## 🟡 문제 2. Continuous Subarray Sum
- 출처: LeetCode #523 — https://leetcode.com/problems/continuous-subarray-sum/
- 카테고리: 누적합 모듈러 + 해시맵 (중급)
- 요약: 배열 `nums`에 **길이 2 이상**이고 원소 합이 **k의 배수**인 연속 부분배열이 있으면 `True`.
- 💭 힌트: 합이 k의 배수 ⟺ 두 누적합의 **나머지(`% k`)가 같다**. `{나머지: 처음 본 인덱스}`를 저장하고,
  같은 나머지를 다시 만났을 때 인덱스 차이가 2 이상인지 확인한다. 초기값 `{0: -1}`로 "처음부터의 구간"을 포함.

## 🟡 문제 3. 4Sum II
- 출처: LeetCode #454 — https://leetcode.com/problems/4sum-ii/
- 카테고리: 보수 찾기 + 분할 (중급)
- 요약: 길이 n인 네 배열 `nums1~4`에서 `a+b+c+d == 0`이 되는 인덱스 4튜플의 **개수**를 반환한다.
- 💭 힌트: 사중 루프는 O(n⁴). 네 배열을 **2+2로 쪼개** 앞 두 배열의 모든 합을 `Counter`에 담고(O(n²)),
  뒤 두 배열의 합 `(c+d)`에 대해 보수 `-(c+d)`의 개수를 더한다. 전체 **O(n²)**.

## 🟢 문제 4. Isomorphic Strings
- 출처: LeetCode #205 — https://leetcode.com/problems/isomorphic-strings/
- 카테고리: 양방향 매핑 (기초·빈출)
- 요약: 두 문자열 `s`, `t`가 **동형(isomorphic)**인지 판별. `s`의 각 글자를 일관되게 치환해 `t`가 되어야 한다.
- 💭 힌트: `s->t` dict 하나만으로는 부족하다("badc" vs "baba" 같은 위반을 놓침). `s->t`와 `t->s`
  **두 dict를 동시에** 검증해야 진짜 1:1 대응. `dict.setdefault(k, v)`가 기존 값과 다르면 즉시 `False`.

## 🟢 문제 5. Word Pattern
- 출처: LeetCode #290 — https://leetcode.com/problems/word-pattern/
- 카테고리: 양방향 매핑(토큰 단위) (기초)
- 요약: 패턴 문자열 `pattern`(예 "abba")과 문장 `s`(예 "dog cat cat dog")가 **같은 대응 구조**인지 판별.
- 💭 힌트: #205와 동일한 양방향 매핑인데 단위가 **글자 ↔ 단어**다. `s.split()`으로 토큰화 후 길이가
  패턴과 다르면 곧장 `False`. 패턴문자→단어, 단어→패턴문자 두 dict를 함께 검증.

## 🟡 문제 6. Insert Delete GetRandom O(1)
- 출처: LeetCode #380 — https://leetcode.com/problems/insert-delete-getrandom-o1/
- 카테고리: 설계 — dict + 리스트 (중급·빈출)
- 요약: 삽입·삭제·임의 원소 반환(`getRandom`)을 **모두 평균 O(1)**로 지원하는 `RandomizedSet` 설계.
- 💭 힌트: `getRandom`을 O(1)로 하려면 값이 **리스트**에 있어야 하고, 삭제를 O(1)로 하려면 값의 위치를
  `dict`로 알아야 한다. 삭제 시 **마지막 원소를 빈 자리로 옮기고 pop**(swap-and-pop)하면 리스트가
  연속을 유지한 채 O(1). 핵심은 "dict + 리스트를 함께 동기화"하는 설계.

## 🔴 문제 7. LRU Cache
- 출처: LeetCode #146 — https://leetcode.com/problems/lru-cache/
- 카테고리: 설계 — 해시맵 + 순서(LRU) (심화·면접 단골)
- 요약: 용량이 정해진 **LRU(Least Recently Used) 캐시**를 `get`/`put` 모두 O(1)로 설계. 용량 초과 시
  **가장 오래 사용 안 한 키**를 추방한다.
- 💭 힌트: "키→값 빠른 조회"(해시) + "사용 순서 유지"(연결 리스트)가 둘 다 필요하다. 파이썬은
  `OrderedDict`가 정확히 이 둘의 결합이라 `move_to_end(key)`(최근 사용 표시)와
  `popitem(last=False)`(가장 오래된 것 추방) 두 줄로 끝난다. 직접 이중 연결 리스트로도 구현해보면 좋다.

## ⚫ 문제 8. 오픈채팅방 (카카오 기출)
- 출처: 프로그래머스 #42888 — https://school.programmers.co.kr/learn/courses/30/lessons/42888
- 카테고리: 해시 — uid→닉네임 매핑 (2019 카카오 블라인드)
- 요약: `Enter uid 닉네임` / `Leave uid` / `Change uid 닉네임` 로그가 주어진다. 닉네임은 나중에 바뀔 수
  있으므로 **최종 닉네임 기준**으로 입장/퇴장 메시지를 출력한다.
- 💭 힌트: 닉네임이 도중에 변하니 **출력은 두 단계**로. ① 전체 로그를 훑어 `uid → 최종 닉네임` dict를
  확정한다. ② 다시 훑으며 Enter/Leave 이벤트만 모아, 최종 닉네임 dict로 메시지를 만든다. 순서 보존 주의.

## ⚫ 문제 9. 신고 결과 받기 (카카오 기출)
- 출처: 프로그래머스 #92334 — https://school.programmers.co.kr/learn/courses/30/lessons/92334
- 카테고리: 다중 해시 — 집합 + 카운터 (2022 카카오 블라인드)
- 요약: 유저별 신고 기록 `report`와 정지 기준 `k`가 주어진다. **k번 이상 신고당한** 유저는 정지되고,
  그 유저를 신고한 사람들은 메일을 받는다. 각 유저가 받을 **메일 수**를 `id_list` 순서로 반환.
- 💭 힌트: 같은 사람이 같은 사람을 여러 번 신고해도 1회 → **`set(report)`로 먼저 중복 제거**.
  `피신고자 → 신고자 집합`(`defaultdict(set)`)을 만들고, 집합 크기 ≥ k면 정지. 정지된 유저를 신고한
  사람마다 메일 수를 1씩 더한다.

## ⚫ 문제 10. 메뉴 리뉴얼 (카카오 기출)
- 출처: 프로그래머스 #72411 — https://school.programmers.co.kr/learn/courses/30/lessons/72411
- 카테고리: 조합 + Counter (2021 카카오 블라인드)
- 요약: 손님 주문 목록 `orders`와 코스 크기 목록 `course`가 주어진다. 각 코스 크기 c마다 **2명 이상이
  함께 주문한 메뉴 조합** 중 **가장 많이 주문된 것**을 모두 골라 사전순으로 반환한다.
- 💭 힌트: 각 주문 문자열을 `sorted` 후 `itertools.combinations(order, c)`로 모든 크기 c 조합을
  `Counter`에 센다. 코스별 최대 빈도를 구해 그 값이 **2 이상**일 때만, 최대 빈도와 같은 조합들을 채택.
  조합을 만들기 전 각 주문 글자를 정렬해 두면 같은 조합이 같은 키가 된다.

---

### 추천 풀이 순서
1) #205 → #290 (양방향 매핑 감 잡기 — 가장 쉬움)
2) #560 → #523 (누적합 + 해시맵 — 오늘의 핵심, mod 변형까지)
3) #454 (보수 + 분할로 차원 줄이기)
4) #380 → #146 (설계형: dict+리스트 → dict+순서/LRU)
5) 프로그래머스 #42888 → #92334 → #72411 (카카오 기출: 매핑 → 다중 해시 → 조합+Counter)

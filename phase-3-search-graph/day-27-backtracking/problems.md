# Day 27 — 백트래킹 연습문제 (Problems)

> 출처는 **프로그래머스 · LeetCode** 만 사용합니다. 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 각 문제의 코드 해설은 [solutions.py](solutions.py) 에 있습니다.

## 문제 목록

| 번호 | 문제 | 출처 | 난이도 | 형태 |
|---|---|---|---|---|
| 1 | Subsets | [LeetCode #78](https://leetcode.com/problems/subsets/) | 🟢기초 | 부분집합 생성 |
| 2 | Permutations | [LeetCode #46](https://leetcode.com/problems/permutations/) | 🟡중급 | 순열 생성(used) |
| 3 | Combinations | [LeetCode #77](https://leetcode.com/problems/combinations/) | 🟡중급 | 조합 생성(start) |
| 4 | Combination Sum | [LeetCode #39](https://leetcode.com/problems/combination-sum/) | 🟡중급 | 합 조건 + 가지치기 |
| 5 | Generate Parentheses | [LeetCode #22](https://leetcode.com/problems/generate-parentheses/) | 🟡중급 | 유효성 가지치기 |
| 6 | 소수 찾기 | [프로그래머스 #42839](https://school.programmers.co.kr/learn/courses/30/lessons/42839) | 🟡중급 | 자릿수 순열 + 소수 |
| 7 | 모음사전 | [프로그래머스 #84512](https://school.programmers.co.kr/learn/courses/30/lessons/84512) | 🟡중급 | 사전순 DFS 생성 |
| 8 | 피로도 | [프로그래머스 #87946](https://school.programmers.co.kr/learn/courses/30/lessons/87946) | 🟡중급 | 방문 순열 완전탐색 |
| 9 | Word Search | [LeetCode #79](https://leetcode.com/problems/word-search/) | 🟡중급 | 격자 백트래킹(visited 원복) |
| 10 | N-Queens | [LeetCode #51](https://leetcode.com/problems/n-queens/) | 🔴심화 | 제약 만족 + 대각선 가지치기 |

---

## 1. Subsets 🟢 — [LeetCode #78](https://leetcode.com/problems/subsets/)

서로 다른 정수 배열 `nums`의 **모든 부분집합(멱집합, power set)** 을 반환하라(순서 무관, 중복 없음).

- **핵심:** 백트래킹의 가장 기본형. 각 원소마다 "포함 / 불포함" 두 갈래로 분기하면 `2^n`개의 부분집합이 나온다. 또는 `start` 인덱스로 "지금까지 만든 것 + 뒤 원소 추가"를 반복해도 된다.
- **팁:** 리프에서만 기록하는 이진 결정 방식과, 모든 노드에서 기록하는 `start` 방식 둘 다 익혀 두면 조합 문제로 자연스럽게 확장된다.
- **복잡도:** O(2^n x n)(각 부분집합 복사 비용 포함).

## 2. Permutations 🟡 — [LeetCode #46](https://leetcode.com/problems/permutations/)

서로 다른 정수 배열 `nums`의 **모든 순열(permutation)** 을 반환하라.

- **핵심:** 매 자리마다 아직 안 쓴 원소를 하나씩 골라 `path`에 넣는다. `used[i]` 불리언 배열로 "이미 쓴 원소"를 가지치기한다.
- **함정:** 순열은 순서가 다르면 다른 답이다(조합과 반대). `start`가 아니라 매번 전체 인덱스를 훑되 `used`로 거른다.
- **복잡도:** O(n! x n).

## 3. Combinations 🟡 — [LeetCode #77](https://leetcode.com/problems/combinations/)

`1..n`에서 `k`개를 뽑는 **모든 조합**을 반환하라.

- **핵심:** `start` 인덱스로 "뒤로만 고르기"를 강제해 `(1,2)`와 `(2,1)`의 중복을 원천 차단한다. 순서가 무의미한 것이 조합.
- **팁(가지치기):** 남은 자리 `k - len(path)`개를 채울 원소가 부족한 `start`는 시도하지 않는다(`range` 상한을 `n - (k - len(path)) + 2`로). 큰 `n`에서 눈에 띄게 빨라진다.
- **복잡도:** O(nCk x k).

## 4. Combination Sum 🟡 — [LeetCode #39](https://leetcode.com/problems/combination-sum/)

서로 다른 양의 정수 `candidates`와 목표 `target`이 주어진다. **같은 수를 여러 번 써서** 합이 `target`이 되는 모든 조합을 반환하라(조합끼리 순서 무관, 중복 조합 없음).

- **핵심:** 같은 수 재사용을 허용하므로 재귀 시 인덱스를 `i`로 유지한다(`dfs(i, ...)`). 정렬 후 "남은 목표보다 큰 후보가 나오면 `break`"로 강하게 가지친다.
- **함정:** 중복 조합을 피하려면 `start`부터만 고른다(뒤로만). 다음 후보로 넘어갈 때는 `i+1`이 아니라 현재 `i`를 넘겨 재사용을 허용.
- **복잡도:** 지수(해의 수에 비례). 가지치기가 실전 성능을 좌우.

## 5. Generate Parentheses 🟡 — [LeetCode #22](https://leetcode.com/problems/generate-parentheses/)

`n`쌍의 괄호로 만들 수 있는 **모든 유효한 괄호 문자열**을 반환하라.

- **핵심:** 유효성으로 가지치기하는 백트래킹의 정석. "열린 괄호 수 `open < n`이면 `(` 추가 가능", "`close < open`이면 `)` 추가 가능"이라는 두 조건만으로 유효한 문자열만 생성한다(무효 조합은 애초에 만들지 않음).
- **팁:** 모든 `2^(2n)` 문자열을 만든 뒤 검사하는 완전 탐색보다, 만들며 거르는 이 방식이 훨씬 빠르다. 답 개수는 카탈란 수(Catalan number).
- **복잡도:** O(4^n / sqrt(n))(카탈란 수 규모).

## 6. 소수 찾기 🟡 — [프로그래머스 #42839](https://school.programmers.co.kr/learn/courses/30/lessons/42839)

숫자가 적힌 종이 조각(문자열 `numbers`)에서 조각들을 **이어 붙여 만들 수 있는 모든 수** 중 **서로 다른 소수의 개수**를 구하라.

- **핵심:** 자릿수들의 **순열**로 가능한 모든 수를 만든다(길이 1..len 모두). 만든 수를 집합에 모아 중복을 제거하고, 각 수가 소수인지 판별해 센다.
- **함정:** `"011"`처럼 앞자리 0이 붙은 조각도 `int()`로 변환하면 자연히 정규화된다. 소수 판별은 `2..sqrt(x)`까지만, `0`과 `1`은 소수가 아니다.
- **팁:** `itertools.permutations`로 순열을 뽑으면 코드가 짧다. 직접 백트래킹으로도 동일하게 구현 가능(둘 다 해설에 수록).
- **복잡도:** 자릿수 L이 작아(<=7) 순열 수가 제한적. 실전 무리 없음.

## 7. 모음사전 🟡 — [프로그래머스 #84512](https://school.programmers.co.kr/learn/courses/30/lessons/84512)

모음 `A, E, I, O, U`만으로 만든 길이 5 이하의 모든 단어를 사전순으로 나열했을 때, 주어진 단어 `word`가 **몇 번째**인지 구하라.

- **핵심:** `A, E, I, O, U` 순서로 DFS를 돌리면 생성 순서가 곧 사전순이다. 빈 문자열부터 시작해 각 단계에서 5개 모음을 순서대로 붙이며(길이 5까지) 카운트를 세다가 `word`를 만나면 그 카운트를 반환한다.
- **팁:** 굳이 전부 만들지 않고 자릿값(각 자리가 기여하는 개수 = 등비수열 합)으로 O(L)에 계산하는 수학적 풀이도 있다. 둘 다 해설에 수록.
- **복잡도:** DFS 생성 방식 O(5^5) 규모, 수학 방식 O(L).

## 8. 피로도 🟡 — [프로그래머스 #87946](https://school.programmers.co.kr/learn/courses/30/lessons/87946)

현재 피로도 `k`와 던전 목록(각 던전 `[최소 필요 피로도, 소모 피로도]`)이 주어진다. 던전을 **탐험하는 순서를 자유롭게 정할 때** 최대 몇 개의 던전을 탐험할 수 있는지 구하라.

- **핵심:** 던전 수가 8 이하로 작다. **모든 방문 순서(순열)** 를 백트래킹으로 시도하며, "현재 피로도 >= 최소 필요 피로도"를 만족할 때만 그 던전에 들어가고(가지치기), 최댓값을 갱신한다.
- **함정:** 순서에 따라 결과가 달라지므로 조합이 아니라 순열이다. `used` 배열로 방문 던전을 관리하고 재귀 후 되돌린다.
- **복잡도:** O(n! x n), n<=8이라 충분히 빠름.

## 9. Word Search 🟡 — [LeetCode #79](https://leetcode.com/problems/word-search/)

문자 격자 `board`에서 인접(상하좌우) 칸을 이어 `word`를 만들 수 있는지 판별하라. 같은 칸은 한 번만 쓸 수 있다.

- **핵심:** 격자 위의 백트래킹. 각 시작 칸에서 DFS로 글자를 맞춰 나가되, 방문한 칸을 임시로 표시(예: `#`로 덮기)하고 **재귀에서 돌아오면 원래 글자로 복원**한다. 이 "표시→복원"이 백트래킹의 undo다.
- **함정:** visited를 복원하지 않으면 한 칸을 다시 못 써서 다른 경로 탐색이 막힌다. 경계·글자 불일치는 즉시 가지치기.
- **복잡도:** O(R x C x 4^L)(L=단어 길이). 첫 글자 불일치 조기 컷이 실전 속도.

## 10. N-Queens 🔴 — [LeetCode #51](https://leetcode.com/problems/n-queens/)

`n x n` 체스판에 `n`개의 퀸을 서로 공격할 수 없도록 놓는 **모든 배치**를 반환하라(같은 행·열·대각선에 두 퀸이 없어야 함).

- **핵심:** 백트래킹 + 가지치기의 교과서. 행마다 퀸을 하나씩 놓고, **열·↘대각선(r-c)·↙대각선(r+c)** 을 집합으로 관리해 충돌을 O(1)에 검사한다. 충돌하면 즉시 접는다.
- **팁:** 대각선을 `r-c`(왼위-오른아래)와 `r+c`(오른위-왼아래) 두 값으로 인덱싱하는 것이 정석. 배치를 기록할 때는 각 행의 퀸 열 위치만 저장하면 충분.
- **복잡도:** 최악 상한은 크지만 가지치기로 실제 방문 노드가 급감. 대표적인 "가지치기가 통과를 만드는" 문제.

---

## 학습 순서 제안

1. **전수 생성 3형제:** Subsets(#78) -> Permutations(#46) -> Combinations(#77) — 포함/불포함, used, start 세 패턴을 몸에 익힌다
2. **조건·가지치기 추가:** Combination Sum(#39) -> Generate Parentheses(#22) — "만들며 거르기"의 위력을 체감
3. **프로그래머스 응용:** 소수 찾기(#42839, 순열+소수) -> 모음사전(#84512, 사전순 생성) -> 피로도(#87946, 방문 순열)
4. **제약 만족 심화:** Word Search(#79, 격자 visited 원복) -> N-Queens(#51, 대각선 가지치기)

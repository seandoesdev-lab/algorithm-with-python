---
day: 24
phase: 3-search-graph
title: 완전 탐색 (Brute Force / Exhaustive Search)
category: [탐색, 완전탐색]
difficulty: 중급
status: done
prev: "[[day-23-review/concept|Day 23 — 알고리즘 기초 복습]]"
next: "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
related:
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-27-backtracking/concept|Day 27 — 백트래킹]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-21-greedy/concept|Day 21 — 그리디]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/parts/12230
  - https://school.programmers.co.kr/learn/courses/30/lessons/42840
  - https://school.programmers.co.kr/learn/courses/30/lessons/42839
  - https://school.programmers.co.kr/learn/courses/30/lessons/42842
  - https://leetcode.com/problems/two-sum/
  - https://leetcode.com/problems/subsets/
  - https://leetcode.com/problems/permutations/
  - https://leetcode.com/problems/combinations/
  - https://leetcode.com/problems/letter-combinations-of-a-phone-number/
  - https://leetcode.com/problems/combination-sum/
  - https://docs.python.org/3/library/itertools.html
tags: [phase/3, topic/brute-force, topic/search]
---

# Day 24 — 완전 탐색 (Brute Force / Exhaustive Search)

> [!abstract] 한눈 요약 (TL;DR)
> **완전 탐색(brute force / exhaustive search)** 은 "가능한 모든 경우를 빠짐없이 만들어 하나씩 확인"하는 가장 정직한 문제 해결 전략이다. 똑똑한 공식이 없어도, *경우의 수를 셀 수만 있으면* 반드시 정답을 찾는다. 그래서 완전 탐색은 Phase 3(탐색·그래프)의 **출발점이자 모든 탐색 알고리즘의 어머니**다 — DFS·BFS·백트래킹은 전부 "완전 탐색을 더 똑똑하게 가지치기(pruning)한 형태"에 지나지 않는다. 코테에서 완전 탐색이 중요한 이유는 두 가지다. ① **입력이 작으면(대략 요소 20개 이하, 경우의 수 100만~1000만 이하) 완전 탐색이 정답이자 가장 안전한 풀이**다. 굳이 어려운 최적화를 고민하다 틀리느니 전수조사로 확실히 맞히는 게 낫다. ② 더 빠른 알고리즘(그리디·DP)을 설계할 때, **완전 탐색이 "정답의 기준선(baseline)"** 이 된다. 오늘은 완전 탐색의 4대 형태 — **순열(permutation)·조합(combination)·부분집합(subset)·중첩 반복(nested loop)** 을 재귀와 `itertools`로 구현하고, "언제 완전 탐색을 꺼내도 되는가"를 입력 크기와 경우의 수로 판정하는 감각을 훈련한다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **완전 탐색이란 "답이 될 수 있는 모든 후보(candidate)를 하나도 빼놓지 않고 생성한 뒤, 조건에 맞는지 전부 검사"하는 방법**이다. 영어로 brute force(무차별 대입) 또는 exhaustive search(전수 탐색)라 부른다. 핵심 단어는 *빠짐없이(exhaustive)* 다 — 하나라도 빠뜨리면 완전 탐색이 아니다.
>
> **일상 비유 — 자물쇠 번호 맞히기.** 3자리 다이얼 자물쇠의 비밀번호를 잊었다. 똑똑한 방법이 없다면? `000, 001, 002, ..., 999`를 순서대로 전부 돌려본다. 최대 1000번이면 반드시 열린다. 이것이 완전 탐색이다. "최대 몇 번 시도해야 하나?"(=경우의 수)가 감당 가능하면 이 무식한 방법이 가장 확실하다. 만약 자릿수가 10자리라면 100억 번이 되어 불가능해진다 — 그래서 **완전 탐색의 가능 여부는 경우의 수가 결정**한다.
>
> **완전 탐색의 사고 순서:**
> 1. **후보의 구조를 정의한다.** 답이 "n개 중 순서 있는 나열"인가(순열), "순서 없는 선택"인가(조합), "각 원소를 넣거나 빼는가"(부분집합), "여러 축을 각각 훑는가"(중첩 반복)?
> 2. **경우의 수를 센다.** 그 수가 시간 제한 안(대략 1000만 연산 이하)이면 완전 탐색 확정.
> 3. **모든 후보를 생성한다.** 재귀 또는 `itertools`로 하나도 빠짐없이.
> 4. **각 후보를 검사·집계한다.** 조건 만족 여부, 최댓값/최솟값/개수 갱신.
>
> 즉 완전 탐색은 *"세어보고(count) → 만들고(generate) → 확인한다(check)"* 의 3박자다.

> [!gear]- 2. 동작 원리 (How It Works) — 완전 탐색 4대 형태
> 완전 탐색의 "후보 생성"은 대부분 아래 네 가지 틀 중 하나로 떨어진다. 각 형태의 경우의 수를 외워두면 입력 크기만 보고 즉시 완전 탐색 가능 여부를 판단할 수 있다.
> ```
> 형태             후보의 의미                       경우의 수        대표 도구
> --------------------------------------------------------------------------------
> 중첩 반복        축 여러 개를 각각 훑기            곱(예: n*m)      for 중첩
> 부분집합         각 원소를 넣거나(1) 빼거나(0)     2^n             재귀 / bitmask
> 순열             n개를 순서 있게 나열             n! (일부 nPr)    itertools.permutations
> 조합             n개 중 r개를 순서 없이 선택      nCr             itertools.combinations
> ```
>
> **(A) 중첩 반복 (nested loop) - 가장 단순한 완전 탐색.**
> ```
> for i in range(n):
>     for j in range(m):
>         check(i, j)          # 모든 (i, j) 쌍을 검사
> ```
> Two Sum을 O(n^2)로 푸는 것, 카펫 문제에서 가로 후보를 전부 돌리는 것이 여기 해당한다.
>
> **(B) 부분집합 (subset) - "각 원소를 포함할까 말까".**
> ```
> 원소 [a, b, c] 에 대해 각각 O/X -> 2^3 = 8가지
>   {} {a} {b} {c} {a,b} {a,c} {b,c} {a,b,c}
> 재귀 골격:
>   go(i, chosen):
>       if i == n: 후보 chosen 확정; return
>       go(i+1, chosen)          # i번째를 빼고
>       go(i+1, chosen + [a[i]]) # i번째를 넣고
> ```
> 비트마스크로도 표현한다: `0`부터 `2^n - 1`까지 정수의 각 비트가 원소 포함 여부.
>
> **(C) 순열 (permutation) - "순서가 의미 있는 나열".**
> ```
> [1,2,3]의 순열 -> 3! = 6가지
>   (1,2,3) (1,3,2) (2,1,3) (2,3,1) (3,1,2) (3,2,1)
> 재귀 골격: 아직 안 쓴 원소를 하나씩 골라 자리에 놓고, 다음 자리로 재귀.
> ```
> "소수 찾기"에서 숫자 카드로 만들 수 있는 모든 수, 외판원 순회 경로가 순열이다.
>
> **(D) 조합 (combination) - "순서 없는 선택".**
> ```
> [1,2,3,4] 중 2개 선택 -> 4C2 = 6가지
>   (1,2) (1,3) (1,4) (2,3) (2,4) (3,4)
> 재귀 골격: 시작 인덱스 start부터 하나 고르고, 그 다음 인덱스부터 재귀(중복/역순 방지).
> ```
>
> **재귀가 공통 엔진이다.** (B)(C)(D)는 모두 [[day-22-recursion/concept|Day 22 재귀]]의 "선택 → 재귀 → 되돌리기" 골격으로 통일된다. 이 골격에 "가망 없는 가지를 미리 자르는" 로직을 더하면 [[day-27-backtracking/concept|Day 27 백트래킹]]이 되고, 그래프 위에서 하면 [[day-25-dfs/concept|Day 25 DFS]]가 된다. 완전 탐색은 탐색 계열 전체의 뿌리다.

> [!chart]- 3. 복잡도 (Time / Space Complexity) — 경우의 수가 곧 복잡도
> 완전 탐색의 시간복잡도는 **"후보의 개수 x 후보 1개 검사 비용"** 이다. 후보 개수가 지배하므로 아래 표를 외워라. (n = 원소 수)
>
> | 형태 | 경우의 수 | 시간복잡도 | n이 이 정도까지 현실적 |
> |---|---|---|---|
> | 중첩 반복(2중) | n^2 | O(n^2) | n <= 수천 |
> | 중첩 반복(3중) | n^3 | O(n^3) | n <= 수백 |
> | 부분집합 | 2^n | O(2^n) | n <= 20~25 |
> | 순열 | n! | O(n! x n) | n <= 10~11 |
> | 조합 nCr | nCr | O(nCr x r) | 조합 수가 관건 |
>
> > **판정 공식 — "경우의 수 x 검사비용 <= 약 10^7~10^8 이면 GO".** 대략 1초에 파이썬은 1000만(10^7) 안팎의 연산을 처리한다(언어·연산 종류에 따라 편차 큼). 그래서 완전 탐색을 결정하기 전 **경우의 수를 먼저 계산**하라. `2^20 ~= 100만`(OK), `2^30 ~= 10억`(위험), `10! ~= 363만`(OK), `13! ~= 62억`(불가), `15! ~= 1.3조`(불가). 시간복잡도 판정은 [[day-16-big-o/concept|Day 16 Big-O]]의 직접 응용이다.
>
> > **공간복잡도.** 재귀 방식은 호출 스택 깊이 O(n), 결과를 전부 저장하면 후보 개수만큼의 공간이 든다. `itertools`는 **제너레이터(generator)** 라 후보를 하나씩 흘려보내 메모리를 아낀다 — `for p in permutations(...)` 는 모든 순열을 한꺼번에 리스트로 만들지 않는다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"입력이 작다"는 강력한 신호다.** 문제에서 `n <= 8`, `배열 길이 <= 20`, `1 <= 숫자의 개수 <= 7` 처럼 **범위가 유난히 작으면** 출제자가 완전 탐색을 기대한다는 뜻이다. 큰 입력이면 애초에 완전 탐색으로 못 풀게 막았을 것이다.
>   - 참고: [프로그래머스 완전탐색 문제집](https://school.programmers.co.kr/learn/courses/30/parts/12230)
> - **손으로 짜기 전에 `itertools`부터 떠올려라.** `permutations`(순열) · `combinations`(조합) · `product`(중첩 반복/곱집합) · `combinations_with_replacement`(중복 조합)가 표준 라이브러리에 있다. off-by-one 버그 없이 한 줄로 후보를 생성한다.
>   - 참고: [itertools (Python 공식 문서)](https://docs.python.org/3/library/itertools.html)
> - **부분집합은 비트마스크(bitmask)로 우아하게.** `for mask in range(1 << n)` 로 0..2^n-1을 돌며, `if mask & (1 << i)` 로 i번째 원소 포함 여부를 검사한다. 재귀 없이 반복문만으로 모든 부분집합을 만든다([[day-05-math/concept|Day 05 비트 연산]] 응용).
> - **완전 탐색 후 최적화가 정석 순서다.** 실전 팁: 먼저 완전 탐색으로 "맞는 답"을 만든 뒤, 시간 초과가 나면 그때 그리디/DP/가지치기로 개선한다. 완전 탐색 버전이 **작은 입력용 정답 검증기(oracle)** 역할을 하므로 최적화 코드의 버그를 잡아준다.
> - **경우의 수는 반드시 곱셈으로 미리 계산.** "각 축의 선택지를 곱한다"가 경우의 수의 본질이다. 3자리 각 10개면 10x10x10=1000. 계산해서 10^8을 넘으면 완전 탐색을 포기하고 다른 전략으로 전환하라.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **완전 탐색은 "정확성은 100%, 효율은 최악"의 트레이드오프.** 반드시 정답을 찾지만 느리다. 그래서 **"입력이 작을 때"** 와 **"정답 기준선이 필요할 때"** 두 상황에서만 최선의 선택이다. 큰 입력에 무턱대고 완전 탐색을 쓰면 시간 초과(TLE)의 지름길이다.
> 2. **완전 탐색 여부는 코드 짜기 전에 경우의 수로 판정한다.** 이것이 초보와 숙련자를 가르는 지점이다. 순열이면 n!, 부분집합이면 2^n을 즉시 계산해 시간 제한과 비교하라. 계산 없이 "일단 짜보자"가 가장 흔한 실패 패턴.
> 3. **순열 n!의 폭발성.** `10! = 3,628,800`(약 360만, OK)이지만 `13! = 62억`, `20! = 약 2.4x10^18`이다. 순열 완전 탐색은 사실상 n <= 10~11에서만 가능하다. n이 그보다 크면 순열 완전 탐색은 답이 아니다.
> 4. **부분집합 2^n의 경계.** `2^20 ~= 100만`(빠름), `2^25 ~= 3300만`(빠듯), `2^30 ~= 10억`(불가). 부분집합/비트마스크 완전 탐색은 n <= 20~25가 실전 한계다.
> 5. **중복 처리에 주의.** 입력에 같은 값이 있으면 순열·조합·부분집합에서 **중복된 후보**가 생긴다(예: `[1,1,2]`의 순열). 정렬 후 "직전 값과 같으면 건너뛰기" 또는 `set`으로 결과를 유일화해야 한다. LeetCode Subsets II / Permutations II의 핵심 함정이다.
> 6. **완전 탐색 != 백트래킹.** 완전 탐색은 "모든 후보를 다 만든다", 백트래킹은 "만들다가 **가망 없으면 도중에 포기(pruning)**"한다. 백트래킹은 완전 탐색의 최적화 버전이다([[day-27-backtracking/concept|Day 27]]). 완전 탐색을 확실히 이해해야 백트래킹의 "무엇을 쳐내는지"가 보인다.
> 7. **`itertools`는 제너레이터라 메모리 안전, 하지만 시간은 그대로.** `permutations`가 리스트를 미리 안 만들어 메모리는 아끼지만, 순회하는 총 개수(n!)는 변하지 않는다. "메모리 초과는 피해도 시간 초과는 여전히 위험"임을 기억하라.
> 8. **재귀 완전 탐색의 상태 되돌리기(undo).** 리스트에 `append` 하고 재귀했으면 돌아와서 `pop` 해야 한다(백트래킹 골격). 안 하면 이전 선택이 다음 가지에 오염된다 — 완전 탐색/백트래킹 최다 버그.
> 9. **완전 탐색은 그리디의 반례 검증기.** 그리디가 맞는지 의심스러울 때, 작은 입력에 대해 완전 탐색 결과와 그리디 결과를 비교하면 반례를 찾을 수 있다([[day-21-greedy/concept|Day 21 그리디]]). "정답이 보장된 느린 방법"의 가장 실용적인 쓰임새 중 하나다.

> [!example]- 예제 코드 (Examples)
> ```python
> from itertools import permutations, combinations, product
>
> # 1) 중첩 반복 완전 탐색: 두 수의 합이 target인 쌍 (Two Sum, O(n^2))
> def two_sum_brute(nums, target):
>     n = len(nums)
>     for i in range(n):
>         for j in range(i + 1, n):        # 모든 쌍 (i<j)
>             if nums[i] + nums[j] == target:
>                 return [i, j]
>     return []
>
> # 2) 부분집합: 재귀로 모든 부분집합 생성 (2^n)
> def all_subsets(nums):
>     res = []
>     def go(i, chosen):
>         if i == len(nums):
>             res.append(chosen[:])        # 현재 후보 확정(복사)
>             return
>         go(i + 1, chosen)                # i번째 빼고
>         chosen.append(nums[i])
>         go(i + 1, chosen)                # i번째 넣고
>         chosen.pop()                     # 되돌리기(undo)
>     go(0, [])
>     return res
>
> # 3) 부분집합: 비트마스크로 (재귀 없이)
> def all_subsets_bitmask(nums):
>     n = len(nums)
>     res = []
>     for mask in range(1 << n):           # 0 .. 2^n - 1
>         subset = [nums[i] for i in range(n) if mask & (1 << i)]
>         res.append(subset)
>     return res
>
> # 4) 순열: itertools로 모든 순서 나열 (n!)
> def all_permutations(nums):
>     return [list(p) for p in permutations(nums)]
>
> # 5) 조합: n개 중 r개 선택 (nCr)
> def all_combinations(nums, r):
>     return [list(c) for c in combinations(nums, r)]
>
> # 6) product: 중첩 반복을 곱집합으로 (자물쇠 000..999 같은 전수)
> def all_codes(digits, length):
>     return ["".join(p) for p in product(digits, repeat=length)]
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 완전 탐색의 4대 형태(중첩 반복·부분집합·순열·조합)를 골고루 담았다. 각 문제 옆에 "어떤 형태의 완전 탐색인지" 표시했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | 번호 | 문제 | 출처 | 난이도 | 형태 |
> |---|---|---|---|---|
> | 1 | 모의고사 | [프로그래머스 #42840](https://school.programmers.co.kr/learn/courses/30/lessons/42840) | 🟢기초 | 중첩 반복(전수 비교) |
> | 2 | Two Sum | [LeetCode #1](https://leetcode.com/problems/two-sum/) | 🟢기초 | 중첩 반복(O(n^2)) |
> | 3 | Subsets | [LeetCode #78](https://leetcode.com/problems/subsets/) | 🟡중급 | 부분집합(2^n) |
> | 4 | 소수 찾기 | [프로그래머스 #42839](https://school.programmers.co.kr/learn/courses/30/lessons/42839) | 🟡중급 | 순열 + 소수 판정 |
> | 5 | Permutations | [LeetCode #46](https://leetcode.com/problems/permutations/) | 🟡중급 | 순열(n!) |
> | 6 | 카펫 | [프로그래머스 #42842](https://school.programmers.co.kr/learn/courses/30/lessons/42842) | 🟡중급 | 약수 완전 탐색 |
> | 7 | Combinations | [LeetCode #77](https://leetcode.com/problems/combinations/) | 🟡중급 | 조합(nCr) |
> | 8 | Letter Combinations of a Phone Number | [LeetCode #17](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | 🔴심화 | 곱집합(product) |
> | 9 | Combination Sum | [LeetCode #39](https://leetcode.com/problems/combination-sum/) | 🔴심화 | 조합 + 재귀(중복 허용) |
> | 10 | Subsets II | [LeetCode #90](https://leetcode.com/problems/subsets-ii/) | 🔴심화 | 부분집합 + 중복 처리 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근 방식(재귀 vs itertools vs 비트마스크) 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-23-review/concept|Day 23 — 알고리즘 기초 복습]] — Phase 2 기법 정리를 마치고, 기법이 없을 때의 기본기인 완전 탐색으로 Phase 3를 연다
- ➡️ **다음(next):** [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — 완전 탐색을 그래프/트리 위에서 재귀로 수행하는 대표 방법
- 🧭 **관련(related):**
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 부분집합·순열·조합 완전 탐색의 공통 엔진이 재귀다
  - [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — 완전 탐색을 상태 공간 그래프에서 깊이 우선으로 전개
  - [[day-27-backtracking/concept|Day 27 — 백트래킹]] — 완전 탐색에 가지치기(pruning)를 더해 불필요한 후보를 조기 포기
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — 경우의 수(2^n·n!)로 완전 탐색 가능 여부를 판정
  - [[day-21-greedy/concept|Day 21 — 그리디]] — 완전 탐색은 그리디 정당성 검증의 기준선(baseline) 역할
- 🗺️ **지도(MOC):** [[Phase-3 MOC]] · [[00 Algorithm MOC]]

---
day: 21
phase: 2-core-algorithms
title: 그리디 (Greedy)
category: [알고리즘, 최적화]
difficulty: 중급
status: done
prev: "[[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]]"
next: "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
related:
  - "[[day-17-sorting/concept|Day 17 — 정렬]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]]"
sources:
  - https://leetcode.com/problems/assign-cookies/
  - https://leetcode.com/problems/jump-game/
  - https://leetcode.com/problems/jump-game-ii/
  - https://leetcode.com/problems/gas-station/
  - https://leetcode.com/problems/non-overlapping-intervals/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42862
  - https://school.programmers.co.kr/learn/courses/30/lessons/42883
  - https://school.programmers.co.kr/learn/courses/30/lessons/42885
  - https://school.programmers.co.kr/learn/courses/30/lessons/42884
  - https://school.programmers.co.kr/learn/courses/30/lessons/42860
tags: [phase/2, topic/greedy, topic/algorithm]
---

# Day 21 — 그리디 (Greedy)

> [!abstract] 한눈 요약 (TL;DR)
> **그리디(greedy, 탐욕법)는 매 단계에서 "지금 이 순간 가장 좋아 보이는 선택(국소 최적, local optimum)"을 하나씩 확정해 나가면, 그 선택들이 모여 전체 최적해(global optimum)가 되기를 기대하는 전략**이다. 뒤를 되돌아보지 않고(no backtracking), 앞으로의 모든 경우를 계산하지도 않는다(no exhaustive search). 그래서 보통 **정렬 한 번 + 한 번의 선형 스캔**으로 끝나 O(n log n)~O(n)으로 매우 빠르다. 하지만 **그리디가 항상 맞는 것은 아니다.** "지금 최선"이 "전체 최선"으로 이어진다는 **정당성(greedy choice property + optimal substructure)** 이 증명되는 문제에서만 옳다. 그렇지 않으면 [[day-22-recursion/concept|완전 탐색]]이나 DP로 가야 한다. 코테에서 그리디는 (1) **무엇을 기준으로 정렬할지 정하고**, (2) **그 순서로 하나씩 확정하는** 두 단계로 요약된다. "동전 거스름돈", "회의실 배정(구간 스케줄링)", "가장 큰/작은 수 만들기", "보트에 사람 태우기"처럼 **정렬 기준을 잘 잡으면 즉시 풀리는** 유형이 시그널이다. 정렬이 핵심이라 [[day-17-sorting/concept|정렬]]과, "가장 급한 것 먼저"를 반복하는 형태라 [[day-12-heap/concept|힙(우선순위 큐)]]과 자주 짝을 이룬다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **그리디 알고리즘(greedy algorithm)** 은 여러 선택지 중에서 **매 순간 국소적으로 가장 이득인 것을 고르는 규칙**을 반복해 최종 해를 만드는 방법이다. 한 번 고른 선택은 나중에 번복하지 않는다. 그래서 "탐욕(greedy)"이라는 이름이 붙었다 — 눈앞의 이익을 그때그때 최대한 챙긴다.
>
> **일상 비유 — 거스름돈 동전 세기.** 850원을 500·100·50·10원 동전으로 거슬러 줄 때, 우리는 자연스럽게 "가능한 한 큰 동전부터" 고른다. 500원 1개 → 남은 350원, 100원 3개 → 50원, 50원 1개 → 0원. 매 단계에서 "지금 쓸 수 있는 가장 큰 동전"이라는 국소 최적을 골랐을 뿐인데 동전 개수 최소(전체 최적)가 나왔다. 이것이 그리디의 직관이다. (단, 이 최적성은 동전 체계가 특정 조건을 만족할 때만 성립한다 — 아래 필수 상식 참고.)
>
> **왜 빠른가.** 완전 탐색은 "모든 선택의 조합"을 보므로 지수적으로 폭발한다. DP는 "겹치는 부분 문제"를 표에 저장해 다항식으로 줄인다. 그리디는 한 발 더 나아가 **각 단계에서 후보를 단 하나로 좁혀** 버린다. 그래서 대개 정렬(O(n log n)) 후 한 번 훑으면(O(n)) 끝난다. 대신 "그 하나로 좁혀도 정말 최적인가?"를 반드시 정당화해야 한다.
>
> **그리디 vs DP — 한 문장 구분.** DP는 "이번 선택이 나중 선택에 영향을 주므로 모든 상태를 고려"하고, 그리디는 "이번 국소 최적이 미래를 해치지 않음이 보장"된다. 보장되면 그리디(빠름), 안 되면 DP나 [[day-22-recursion/concept|완전 탐색]](느리지만 정확).

> [!gear]- 2. 동작 원리 (How It Works)
> **그리디의 표준 골격은 "정렬 → 순차 확정"이다.**
> ```
> 1) 선택의 우선순위를 정하는 "정렬 기준"을 찾는다 (핵심!)
> 2) 그 순서대로 원소를 하나씩 본다
> 3) 각 원소를 "지금 규칙상 최선"이면 답에 확정, 아니면 버린다
> 4) 되돌아가지 않는다
> ```
>
> **예시 A — 구간 스케줄링 (Activity Selection / 회의실 최대 개수).** "겹치지 않게 최대한 많은 회의를 배정"하려면 **끝나는 시간(end)이 이른 순**으로 정렬하고, 앞에서부터 "직전에 고른 회의의 끝 시간 이후에 시작하는" 회의를 계속 고른다.
> ```
> 회의 (start, end): (1,3) (2,4) (3,5) (0,6) (5,7) (8,9)
>  end 기준 정렬:      (1,3) (2,4) (3,5) (0,6) (5,7) (8,9)
>  고른다: (1,3)                     last_end=3
>  (2,4) start2 < 3  버림
>  (3,5) start3 >= 3  고른다        last_end=5
>  (0,6) start0 < 5  버림
>  (5,7) start5 >= 5  고른다        last_end=7
>  (8,9) start8 >= 7  고른다        last_end=9
>  => 최대 4개
> ```
> "끝이 이른 것부터"가 정답 기준인 이유: 가장 빨리 끝나는 회의를 고르면 **남는 시간이 최대로 확보**되어 이후 더 많은 회의를 담을 여지가 생긴다(교환 논증, exchange argument).
>
> **예시 B — 가장 큰 수 만들기 (Remove k digits의 반대꼴).** 자릿수를 지워 가장 큰 수를 만들 때는 **단조 스택(monotonic stack)** 으로 "앞에서부터 보다가, 뒤에 더 큰 수가 오면 앞의 작은 수를 버린다". 이것도 "지금 이 자리를 크게 유지"하는 국소 최적 반복이다.
>
> **예시 C — 보트 태우기 (Two Pointer + Greedy).** 무게 제한 안에서 보트 수를 최소화하려면 정렬 후 **"가장 무거운 사람과 가장 가벼운 사람을 짝지어" 태운다**. 둘이 함께 못 타면 무거운 사람만 태운다. 정렬 + 양끝 [[day-20-sliding-window/concept|투 포인터]] 그리디.
>
> **정당성 증명의 두 기둥.**
> - **탐욕 선택 속성(greedy choice property):** 국소 최적 선택이 어떤 전체 최적해에 반드시 포함될 수 있다.
> - **최적 부분 구조(optimal substructure):** 그 선택을 확정한 뒤 남은 문제도 같은 방식으로 최적이 된다.
> 이 둘이 성립하면 그리디가 옳다. 보통 "교환 논증(exchange argument)" — 최적해가 그리디 선택과 다르다고 가정하고, 바꿔치기해도 손해가 없음을 보여 모순을 이끈다 — 으로 증명한다.

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> | 유형 | 시간복잡도 | 공간 | 설명 |
> |---|---|---|---|
> | 정렬 기반 그리디 | O(n log n) | O(1)~O(n) | 정렬이 지배항, 이후 스캔은 O(n) |
> | 스캔만 하는 그리디 | O(n) | O(1) | 이미 정렬됐거나 순서 무관(예: Jump Game) |
> | 힙 기반 그리디 | O(n log n) | O(n) | 매 단계 최댓/최솟값을 [[day-12-heap/concept\|힙]]에서 꺼냄 |
> | 단조 스택 그리디 | O(n) | O(n) | 각 원소 push/pop 1회씩(분할 상환) |
> | (비교) 완전 탐색 | O(2^n)~O(n!) | - | 그리디로 줄이는 대상 |
> | (비교) DP | O(n·상태) | O(상태) | 그리디가 안 될 때의 대안 |
>
> - **거의 항상 정렬이 병목.** 그리디 자체 로직은 O(n)이라, 전체는 정렬 O(n log n)로 수렴하는 경우가 많다.
> - **"정렬 필요 없는" 그리디도 있다.** Jump Game처럼 "지금까지 도달 가능한 최대 위치(reach)"만 갱신하면 O(n), O(1)로 끝난다.
> - **힙 그리디는 O(n log n).** "가장 급한 것 먼저"를 n번 꺼내는데 각 pop이 O(log n)이라 그렇다(예: 회의실 개수(방 개수), 작업 스케줄러).

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"정렬 기준"이 곧 문제의 절반.** 그리디 문제의 난이도는 "무엇을 기준으로 정렬/선택하느냐"에 거의 다 들어 있다. 구간 문제면 대개 **끝점 기준**, 짝짓기 문제면 **양끝(최대·최소) 기준**, 자릿수 문제면 **자리별 크기** 를 먼저 의심하라. ([Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/))
> - **작은 반례로 검증부터.** 그리디가 떠올랐다면 코드보다 먼저 **손으로 2~3개 반례**를 돌려 국소 최적이 깨지지 않는지 확인하라. "동전 [1,3,4]로 6원" 같은 반례에서 그리디(4+1+1=3개)가 DP(3+3=2개)에 지는 걸 눈으로 보면 감이 생긴다.
> - **정렬 방향을 헷갈리지 말 것.** "가장 큰 수"는 내림차순 느낌이지만 실제 구현은 단조 스택이고, 구간 문제는 start가 아니라 **end로 정렬**해야 하는 경우가 많다. ([구명보트 풀이 관점](https://school.programmers.co.kr/learn/courses/30/lessons/42885))
> - **그리디가 안 되면 즉시 DP를 떠올려라.** "국소 최적이 미래를 해칠 수 있다"는 낌새(예: 배낭 문제에서 무게 대비 가치 순으로 넣으면 틀리는 0/1 knapsack)면 DP로 전환. 그리디와 DP는 같은 문제의 두 얼굴이다.
> - **면접에선 "왜 이 그리디가 맞는가"를 말로.** 교환 논증("최적해가 내 선택과 다르면 바꿔치기해도 손해 없음")을 한두 문장으로 설명할 수 있으면 강한 인상을 준다. ([위키피디아 Greedy algorithm](https://en.wikipedia.org/wiki/Greedy_algorithm))

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **그리디는 "항상" 옳지 않다 — 정당성이 전부다.** 그리디의 최대 함정은 "빠르고 그럴듯해서" 정당성 확인 없이 제출하는 것이다. 반드시 **탐욕 선택 속성**과 **최적 부분 구조**가 성립하는지(또는 최소한 반례가 없는지) 따져라. 안 되면 DP·완전 탐색으로.
> 2. **거스름돈 그리디는 동전 체계에 의존.** "큰 동전부터"가 최소 개수를 보장하는 건 동전이 **정준 체계(canonical, 예: 1·5·10·50·100·500)** 일 때다. [1, 3, 4]로 6을 만들면 그리디는 4+1+1(3개), 최적은 3+3(2개)로 **그리디가 틀린다.** "동전 문제 = 무조건 그리디"는 위험한 착각.
> 3. **0/1 배낭(knapsack)은 그리디 불가, 분수 배낭은 가능.** 쪼갤 수 있는 **분수 배낭(fractional knapsack)** 은 "가치/무게 비율" 그리디가 최적이지만, 쪼갤 수 없는 **0/1 배낭**은 그리디가 틀리고 DP가 필요하다. "쪼갤 수 있나?"를 먼저 확인하라.
> 4. **구간 스케줄링은 "끝 시간" 기준.** 최대 개수 회의 배정은 **start가 아니라 end 오름차순** 정렬이 정답이다. 시작이 이른 순으로 고르면 긴 회의 하나가 여러 회의를 잡아먹어 틀린다. 흔한 실수 1순위.
> 5. **정렬 안정성·2차 기준.** 여러 원소의 정렬 키가 같을 때 2차 기준(tie-breaker)을 잘못 잡으면 답이 갈린다. 예: 구간을 end로 정렬하되 end가 같으면 start로 등. 문제마다 tie 처리를 명시하라.
> 6. **그리디 + 자료구조 결합이 흔하다.** "가장 급한 것 먼저"는 [[day-12-heap/concept|힙]], "직전보다 크/작은 것 유지"는 [[day-07-stack/concept|단조 스택]], "양끝 짝짓기"는 [[day-20-sliding-window/concept|투 포인터]]와 결합한다. 그리디 로직 자체보다 **어떤 자료구조로 최선을 O(log n)/O(1)에 뽑느냐**가 관건일 때가 많다.
> 7. **부동소수·오버플로 주의.** 분수 배낭의 비율 비교, 가스 스테이션의 누적합 등에서 실수/정수 처리를 조심하라. 파이썬은 정수 오버플로가 없어 유리하지만, 비율 비교는 `a/b < c/d` 대신 `a*d < c*b`(교차 곱)로 정밀도를 지키는 습관이 좋다.
> 8. **"greedy가 통하면 왜 통하는지"가 면접 단골.** 단순히 "정렬하고 골랐다"가 아니라 "이 기준으로 고르면 남은 문제에서 손해가 없다(exchange argument)"를 설명하라. 반대로 "왜 여기선 DP인가"도 함께 준비.

> [!example]- 예제 코드 (Examples)
> ```python
> # 1) 구간 스케줄링 - 겹치지 않는 최대 개수 (end 기준 정렬)
> def max_non_overlapping(intervals):
>     intervals.sort(key=lambda x: x[1])   # 끝 시간 오름차순
>     count = 0
>     last_end = float("-inf")
>     for start, end in intervals:
>         if start >= last_end:            # 직전 회의 이후 시작
>             count += 1
>             last_end = end
>     return count
>
> # 2) 보트 태우기 - 정렬 + 투 포인터 그리디
> def num_rescue_boats(people, limit):
>     people.sort()
>     lo, hi = 0, len(people) - 1
>     boats = 0
>     while lo <= hi:
>         if people[lo] + people[hi] <= limit:
>             lo += 1                      # 가벼운 사람도 함께
>         hi -= 1                          # 무거운 사람은 무조건 태움
>         boats += 1
>     return boats
>
> # 3) Jump Game - 정렬 없이 도달 가능 최대 위치만 갱신 (O(n))
> def can_jump(nums):
>     reach = 0
>     for i, step in enumerate(nums):
>         if i > reach:                    # 여기 못 오면 실패
>             return False
>         reach = max(reach, i + step)
>     return True
>
> # 4) 거스름돈 - "큰 동전부터" (정준 체계에서만 최적)
> def coin_change_greedy(amount, coins=(500, 100, 50, 10)):
>     count = 0
>     for c in coins:
>         count += amount // c
>         amount %= c
>     return count if amount == 0 else -1
> ```
>
> 전체 실행 가능한 예제(구간 스케줄링·보트·점프·거스름돈 반례 포함): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 앞쪽은 **정렬 기준이 명확한 기초 그리디**, 중간은 **점프·누적합형**, 뒤로 갈수록 **구간 스케줄링·문자열 그리디**로 어려워진다.
>
> | 번호 | 문제 | 출처 | 난이도 | 핵심 |
> |---|---|---|---|---|
> | 1 | Assign Cookies | [LeetCode #455](https://leetcode.com/problems/assign-cookies/) | 🟢기초 | 양쪽 정렬 후 매칭 |
> | 2 | 체육복 | [프로그래머스 #42862](https://school.programmers.co.kr/learn/courses/30/lessons/42862) | 🟢기초 | 앞→뒤 순서로 빌려주기 |
> | 3 | 큰 수 만들기 | [프로그래머스 #42883](https://school.programmers.co.kr/learn/courses/30/lessons/42883) | 🟡중급 | 단조 스택 그리디 |
> | 4 | Jump Game | [LeetCode #55](https://leetcode.com/problems/jump-game/) | 🟡중급 | 도달 가능 최대 위치 |
> | 5 | Jump Game II | [LeetCode #45](https://leetcode.com/problems/jump-game-ii/) | 🟡중급 | 구간별 최소 점프 |
> | 6 | 구명보트 | [프로그래머스 #42885](https://school.programmers.co.kr/learn/courses/30/lessons/42885) | 🟡중급 | 정렬 + 투 포인터 |
> | 7 | Gas Station | [LeetCode #134](https://leetcode.com/problems/gas-station/) | 🟡중급 | 누적합 + 시작점 갱신 |
> | 8 | Non-overlapping Intervals | [LeetCode #435](https://leetcode.com/problems/non-overlapping-intervals/) | 🔴심화 | 구간 스케줄링(end 정렬) |
> | 9 | 단속카메라 | [프로그래머스 #42884](https://school.programmers.co.kr/learn/courses/30/lessons/42884) | 🔴심화 | 구간 스케줄링 응용 |
> | 10 | 조이스틱 | [프로그래머스 #42860](https://school.programmers.co.kr/learn/courses/30/lessons/42860) | 🔴심화 | 좌우 이동 최적화 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 정렬 기준·정당성 + 여러 접근(그리디 vs DP/완전 탐색)과 복잡도 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]] — "창을 최대한 늘리거나 조이는" 국소 최적 선택의 사고가 그리디로 이어진다
- ➡️ **다음(next):** [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 그리디로 안 되는 문제는 모든 경우를 나눠 푸는 재귀·분할정복(그리고 DP)으로 간다
- 🧭 **관련(related):**
  - [[day-17-sorting/concept|Day 17 — 정렬]] — 그리디의 첫 단계는 거의 항상 "올바른 기준으로 정렬"
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — "가장 급한 것 먼저"를 O(log n)에 꺼내는 그리디의 단짝
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 그리디가 정당화되지 않을 때의 대안(완전 탐색·DP)
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — 그리디가 완전 탐색을 왜 크게 줄이는지의 근거
  - [[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]] — 양끝 투 포인터 그리디(보트 태우기)로 직접 연결
- 🗺️ **지도(MOC):** [[Phase-2 MOC]] · [[00 Algorithm MOC]]

---
day: 20
phase: 2-core-algorithms
title: 슬라이딩 윈도우 (Sliding Window)
category: [알고리즘, 탐색]
difficulty: 중급
status: done
prev: "[[day-19-two-pointers/concept|Day 19 — 투 포인터]]"
next: "[[day-21-greedy/concept|Day 21 — 그리디]]"
related:
  - "[[day-19-two-pointers/concept|Day 19 — 투 포인터]]"
  - "[[day-14-prefix-sum/concept|Day 14 — 누적 합]]"
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
sources:
  - https://leetcode.com/problems/maximum-average-subarray-i/
  - https://leetcode.com/problems/minimum-size-subarray-sum/
  - https://leetcode.com/problems/longest-substring-without-repeating-characters/
  - https://leetcode.com/problems/find-all-anagrams-in-a-string/
  - https://leetcode.com/problems/permutation-in-string/
  - https://leetcode.com/problems/minimum-window-substring/
  - https://leetcode.com/problems/sliding-window-maximum/
  - https://school.programmers.co.kr/learn/courses/30/lessons/67258
tags: [phase/2, topic/sliding-window, topic/algorithm]
---

# Day 20 — 슬라이딩 윈도우 (Sliding Window)

> [!abstract] 한눈 요약 (TL;DR)
> **슬라이딩 윈도우(sliding window)는 배열·문자열에서 "연속된 구간(부분 배열/부분 문자열)"을 다룰 때, 창(window)의 양 끝을 나타내는 두 포인터를 같은 방향으로 밀어 O(n²) 완전 탐색을 O(n)으로 줄이는 기법**이다. 핵심 아이디어는 **"이미 계산한 구간 값을 버리지 않고 재사용"** 하는 것이다. 창을 한 칸 옮길 때 새로 들어온 원소만 더하고 빠져나간 원소만 빼면, 매번 구간 전체를 다시 합산할 필요가 없다. 창은 두 종류다. (1) **고정 크기 창(fixed window)** — 길이 k가 정해져 있어 "들어오는 원소 추가 / 나가는 원소 제거"를 짝지어 한 칸씩 민다(길이 k 부분 배열의 최대 평균). (2) **가변 크기 창(variable window)** — 오른쪽 끝을 계속 확장(expand)하다가 조건을 어기면 왼쪽 끝을 줄여(shrink) 유효하게 만든다(합이 target 이상인 최소 길이, 중복 없는 최장 부분 문자열). 이는 [[day-19-two-pointers/concept|투 포인터]]의 "같은 방향" 특수형이며, "부분 배열/부분 문자열의 합·개수·길이 조건"이라는 신호가 보이면 가장 먼저 떠올려야 하는 도구다. 구간 합을 미리 만드는 [[day-14-prefix-sum/concept|누적 합]]과, 창 안의 문자 개수를 세는 [[day-09-hashing/concept|해시맵]]과 자주 짝을 이룬다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **슬라이딩 윈도우**는 배열/문자열 위에 **연속된 구간을 나타내는 "창(window)"** 을 두고, 그 창을 왼쪽에서 오른쪽으로 밀면서 매 위치의 답(합·길이·개수 등)을 구하는 기법이다. 창은 보통 두 인덱스 `left`, `right`로 표현하며, `right`가 창의 오른쪽 끝, `left`가 왼쪽 끝이다. **두 인덱스 모두 되돌아가지 않고 오른쪽으로만 움직이므로** 전체 이동 횟수가 O(n)에 묶인다.
>
> **일상 비유 — 달리는 기차 창밖 풍경.** 기차 창문(고정 크기)으로 밖을 본다고 하자. 기차가 앞으로 가면 창 오른쪽으로 새 풍경이 들어오고 왼쪽으로 옛 풍경이 사라진다. "지금 창에 보이는 풍경"을 매번 처음부터 다시 그리지 않고, **새로 들어온 것만 더하고 사라진 것만 지우면** 된다. 이것이 슬라이딩 윈도우의 재활용(reuse) 정신이다.
>
> **왜 완전 탐색보다 빠른가 — 재계산 제거.** 길이 k인 모든 부분 배열의 합을 구할 때, 각 구간을 처음부터 더하면 구간마다 O(k)라 전체 O(n·k)다. 하지만 창을 한 칸 밀면 합의 변화는 `+새원소 - 옛원소` 딱 두 번의 연산뿐이다. 그래서 O(n)에 끝난다. **"겹치는 계산을 버리지 않는다"** 가 핵심이다.
>
> **[[day-19-two-pointers/concept|투 포인터]]와의 관계.** 슬라이딩 윈도우는 투 포인터의 부분집합이다. 투 포인터가 "양끝에서 서로를 향해(opposite)" 또는 "같은 방향(same direction)"으로 움직이는 일반형이라면, 슬라이딩 윈도우는 **두 포인터가 같은 방향으로 움직이며 그 사이 구간을 하나의 의미 단위(창)로 유지**하는 특수형이다. "쌍(pair)"을 찾으면 투 포인터, "구간(subarray/substring)"을 다루면 슬라이딩 윈도우로 감을 잡으면 된다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 고정 크기 창 — 길이 k 부분 배열의 최대 합/평균 (Maximum Average Subarray)**
> ```
> 배열: [1, 12, -5, -6, 50, 3]   k = 4
>  1단계: 첫 창 [1,12,-5,-6] 합 = 2                (초기 k개를 한 번 더함)
>  2단계: 오른쪽으로 한 칸  +50 -1  -> 합 = 2+50-1 = 51   창 [12,-5,-6,50]
>  3단계: 한 칸 더          +3  -12 -> 합 = 51+3-12 = 42  창 [-5,-6,50,3]
>  최대 합 = 51  => 최대 평균 = 51/4 = 12.75
> ```
> 규칙: 먼저 앞 k개 합 `s`를 구한다. 이후 `right`를 k부터 끝까지 밀며 `s += a[right] - a[right-k]`(새 원소 추가, k칸 전 원소 제거)로 창 합을 O(1)에 갱신한다.
>
> **(B) 가변 크기 창 — 합이 target 이상인 최소 길이 (Minimum Size Subarray Sum)**
> ```
> 배열: [2, 3, 1, 2, 4, 3]   target = 7   (양수 배열)
>  right 확장:                             창합  동작
>   [2]                                     2    < 7  확장
>   [2,3]                                   5    < 7  확장
>   [2,3,1]                                 6    < 7  확장
>   [2,3,1,2]                               8   >= 7  길이4 기록, left 줄임
>   [3,1,2]                                 6    < 7  확장
>   [3,1,2,4]                               10  >= 7  길이4, left 줄임
>   [1,2,4]                                 7   >= 7  길이3 기록, left 줄임
>   [2,4]                                   6    < 7  확장
>   [2,4,3]                                 9   >= 7  길이3, left 줄임
>   [4,3]                                   7   >= 7  길이2 기록! (최소)
>  정답: 최소 길이 2
> ```
> 규칙(확장-수축 골격): `for right in range(n): 창에 a[right] 추가; while 조건 만족: 답 갱신 후 a[left] 제거하고 left+=1`. **오른쪽으로 넓히고, 유효해지면 왼쪽을 최대한 조인다.**
>
> **(C) 가변 크기 창 + 해시 — 중복 없는 최장 부분 문자열 (Longest Substring Without Repeating)**
> ```
> 문자열: "abcabcbb"    last = {문자: 마지막 등장 인덱스}
>  right가 문자를 하나씩 읽는다. 같은 문자가 창 안(left 이상)에 이미 있으면
>  left를 "그 문자의 직전 위치 +1"로 점프시켜 중복을 창 밖으로 밀어낸다.
>   a(0) b(1) c(2) -> 창 "abc" 길이3
>   a(3): 이전 a는 0, left=0 -> left=1, 창 "bca" 길이3
>   b(4): 이전 b는 1, left=1 -> left=2, 창 "cab" 길이3 ...
>  최대 길이 = 3
> ```
> 규칙: [[day-09-hashing/concept|해시맵]]으로 각 문자의 마지막 위치를 기억하고, 중복을 만나면 `left = max(left, last[c] + 1)`로 왼쪽을 점프시킨다. `max(...)`가 핵심 — left는 절대 뒤로 가면 안 된다.
>
> **왜 O(n)인가.** 세 형태 모두 `right`는 0->n-1로 정확히 n번 전진하고, `left`도 전체를 통틀어 최대 n번만 전진한다(각 원소는 창에 딱 한 번 들어오고 한 번 나간다). 포인터 이동 총합이 2n 이하라 O(n). while 안쪽 루프가 있어 "이중 반복문처럼 보여도" 실제로는 분할 상환(amortized) O(n)이다.

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> | 상황 | 시간복잡도 | 공간 | 설명 |
> |---|---|---|---|
> | 고정 창 (합/평균) | O(n) | O(1) | 창을 한 칸 밀 때 +새 -옛 두 연산 |
> | 가변 창 (최소/최장 길이) | O(n) | O(1) | left·right 각각 최대 n번 전진 |
> | 가변 창 + 해시(문자 카운트) | O(n) | O(k) | k = 문자 종류 수(알파벳이면 O(1)) |
> | 창 최댓값 (Sliding Window Maximum) | O(n) | O(k) | 단조 덱(monotonic deque) 사용 |
> | 완전 탐색(모든 구간)과 비교 | O(n²)~O(n·k) → O(n) | - | 재계산 제거로 한 차수 감소 |
>
> - **핵심은 amortized O(n).** `while`이 안에 있어도 `left`가 되돌아가지 않으므로 총 이동은 O(n). "겉보기 O(n²), 실제 O(n)"을 설명할 수 있어야 한다.
> - **고정 창은 공간 O(1).** 창 합 하나만 들고 다니면 된다. 반면 문자/원소 종류를 세야 하면 [[day-09-hashing/concept|해시맵]] 크기만큼 O(k) 공간이 붙는다.
> - **창 최댓값은 덱이 정답.** 매 창마다 max를 다시 구하면 O(n·k)다. [[day-08-queue-deque/concept|덱(deque)]] 기반 단조 자료구조로 O(n)에 처리하는 것이 표준 기법.
> - **[[day-14-prefix-sum/concept|누적 합]]과의 갈림길.** "고정/양수 구간"은 슬라이딩 윈도우가 O(1) 공간으로 우세, "임의 구간 합을 여러 번 질의"하거나 "음수 포함 target 구간"이면 누적 합(+해시)이 맞다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **신호어로 패턴 잡기.** "연속된 부분 배열/부분 문자열", "길이 k인 구간", "합이 ~ 이상/이하", "중복 없는 최장", "조건을 만족하는 최소/최대 길이" → 슬라이딩 윈도우를 먼저 의심하라. ([LeetCode 슬라이딩 윈도우 정리](https://leetcode.com/problems/minimum-size-subarray-sum/))
> - **"고정이냐 가변이냐" 먼저 결정.** 창 길이가 문제에 **숫자로 주어지면** 고정 창(초기 합 → 밀기). "조건을 만족하는 가장 길거나 짧은"이면 가변 창(확장-수축).
> - **가변 창의 만능 골격을 외워라.** `for right: add(a[right]); while invalid: remove(a[left]); left+=1; update_answer()`. 최소 길이는 "유효할 때 답 갱신 후 수축", 최장 길이는 "무효일 때만 수축, 유효 구간에서 답 갱신"으로 갱신 위치가 살짝 다르다.
> - **양수 전제를 확인하라.** [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)의 확장-수축 논리는 **원소가 모두 양수**여야 성립한다(수축하면 합이 반드시 준다). 음수가 섞이면 단조성이 깨져 [[day-14-prefix-sum/concept|누적 합]]+해시 등 다른 도구가 필요하다.
> - **문자 문제는 카운트 배열/딕셔너리.** [Find All Anagrams](https://leetcode.com/problems/find-all-anagrams-in-a-string/), [Permutation in String](https://leetcode.com/problems/permutation-in-string/), [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)은 모두 "창 안 문자 개수 = 목표 개수"인지 비교한다. `need`(필요 개수)와 `window`(현재 개수) 딕셔너리 + 만족한 문자 종류 수 `formed`를 함께 관리하는 패턴이 정석.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **`left`는 절대 되돌아가지 않는다.** 중복 없는 최장 부분 문자열에서 `left = last[c] + 1`이 아니라 `left = max(left, last[c] + 1)`을 써야 한다. 이 `max`를 빼먹으면 이미 지나간 위치로 `left`가 후퇴해 창이 오히려 늘어나고 답이 틀린다. 슬라이딩 윈도우 버그 1순위.
> 2. **확장-수축의 골격을 지켜라.** 가변 창은 "밖 for로 right 확장 → 안 while로 left 수축"이 정석이다. 두 포인터를 임의로 움직이면 O(n) 보장이 깨지거나 구간을 빠뜨린다.
> 3. **초기 창을 한 번 세팅한다(고정 창).** 고정 창은 앞 k개 합을 먼저 구한 뒤 k번째 인덱스부터 밀어야 한다. 처음부터 밀면 창이 아직 k개가 아니라 결과가 어긋난다. 경계 `right - k` 인덱스가 음수가 되지 않는지 확인하라.
> 4. **양수 가정 위에서만 "수축=감소".** 최소 길이/최소 합류의 while 수축은 원소가 양수라 "왼쪽을 빼면 합이 준다"가 보장될 때만 옳다. 음수·0이 섞이면 이 단조성이 무너진다. 문제 제약(1 ≤ nums[i])을 반드시 확인하라.
> 5. **창 최댓값은 max 재계산을 피하라.** 매 창마다 `max(window)`를 부르면 O(n·k)로 TLE 위험. [[day-08-queue-deque/concept|덱]]에 **인덱스를 단조 감소로 유지**(새 값보다 작은 뒤쪽을 pop)하고, 창을 벗어난 앞쪽 인덱스를 popleft 하는 단조 덱이 표준. 덱 맨 앞이 항상 현재 창의 최댓값이다.
> 6. **부분 배열(subarray)은 연속, 부분 수열(subsequence)은 불연속.** 슬라이딩 윈도우는 **연속 구간에만** 쓴다. "순서만 유지하고 건너뛰어도 되는" 부분 수열 문제(예: 최장 증가 부분 수열)는 윈도우가 아니라 [[day-16-big-o/concept|DP]] 등 다른 접근이다. 문제의 "연속(contiguous)" 여부를 먼저 확인하라.
> 7. **문자 카운트 비교는 "만족 종류 수"로.** 매번 두 딕셔너리 전체를 비교하면 창마다 O(알파벳)이라 느려진다. `formed`(조건을 만족한 문자 종류 수)를 증감으로 관리해 O(1) 비교로 만드는 것이 Minimum Window Substring 정석 풀이다.
> 8. **면접 단골 — "왜 O(n)인가".** "right와 left가 각각 최대 n번만 전진하고 되돌아가지 않으므로 총 이동이 2n 이하 → amortized O(n)"을 말로 설명할 수 있어야 한다. 안쪽 while만 보고 O(n²)이라 답하면 감점.

> [!example]- 예제 코드 (Examples)
> ```python
> # 1) 고정 크기 창 - 길이 k 부분 배열의 최대 합
> def max_sum_fixed(a, k):
>     s = sum(a[:k])            # 초기 창 한 번만 합산
>     best = s
>     for right in range(k, len(a)):
>         s += a[right] - a[right - k]   # 새 원소 추가, 옛 원소 제거
>         best = max(best, s)
>     return best
>
> # 2) 가변 창 - 합이 target 이상인 최소 길이 (양수 배열)
> def min_subarray_len(target, nums):
>     left = 0
>     total = 0
>     best = len(nums) + 1
>     for right in range(len(nums)):
>         total += nums[right]              # 오른쪽 확장
>         while total >= target:            # 유효하면 왼쪽 수축
>             best = min(best, right - left + 1)
>             total -= nums[left]
>             left += 1
>     return best if best <= len(nums) else 0
>
> # 3) 가변 창 + 해시 - 중복 없는 최장 부분 문자열 길이
> def longest_unique(s):
>     last = {}                 # 문자 -> 마지막 등장 인덱스
>     left = 0
>     best = 0
>     for right, c in enumerate(s):
>         if c in last and last[c] >= left:
>             left = last[c] + 1            # left는 되돌아가지 않는다
>         last[c] = right
>         best = max(best, right - left + 1)
>     return best
> ```
>
> 전체 실행 가능한 예제(고정/가변/해시 창 + 아나그램 탐색): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 앞쪽은 **고정 창 기초**, 중간은 **가변 창(확장-수축)·해시 창**, 뒤로 갈수록 **문자 카운트 창·단조 덱**으로 어려워진다.
>
> | 번호 | 문제 | 출처 | 난이도 | 핵심 |
> |---|---|---|---|---|
> | 1 | Maximum Average Subarray I | [LeetCode #643](https://leetcode.com/problems/maximum-average-subarray-i/) | 🟢기초 | 고정 창 합 밀기 |
> | 2 | Minimum Size Subarray Sum | [LeetCode #209](https://leetcode.com/problems/minimum-size-subarray-sum/) | 🟡중급 | 가변 창 최소 길이 |
> | 3 | Longest Substring Without Repeating Characters | [LeetCode #3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | 🟡중급 | 해시 창 최장 길이 |
> | 4 | Find All Anagrams in a String | [LeetCode #438](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | 🟡중급 | 고정 창 문자 카운트 |
> | 5 | Permutation in String | [LeetCode #567](https://leetcode.com/problems/permutation-in-string/) | 🟡중급 | 고정 창 카운트 일치 |
> | 6 | 보석 쇼핑 | [프로그래머스 #67258](https://school.programmers.co.kr/learn/courses/30/lessons/67258) | 🟡중급 | 가변 창 모든 종류 포함 |
> | 7 | Minimum Window Substring | [LeetCode #76](https://leetcode.com/problems/minimum-window-substring/) | 🔴심화 | 가변 창 + formed 카운트 |
> | 8 | Sliding Window Maximum | [LeetCode #239](https://leetcode.com/problems/sliding-window-maximum/) | 🔴심화 | 단조 덱 O(n) |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 핵심 아이디어 + 여러 접근(완전 탐색 vs 슬라이딩 윈도우, 해시 카운트 vs 단조 덱 등)과 복잡도 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-19-two-pointers/concept|Day 19 — 투 포인터]] — 슬라이딩 윈도우는 두 포인터가 "같은 방향으로 움직이며 그 사이 구간을 유지"하는 투 포인터의 특수형
- ➡️ **다음(next):** [[day-21-greedy/concept|Day 21 — 그리디]] — 창을 최대한 늘리거나 조이는 "국소 최적 선택"의 사고는 그리디와 맞닿아 있다
- 🧭 **관련(related):**
  - [[day-19-two-pointers/concept|Day 19 — 투 포인터]] — 슬라이딩 윈도우의 상위 개념(같은 방향 두 포인터)
  - [[day-14-prefix-sum/concept|Day 14 — 누적 합]] — 구간 합 문제에서 윈도우와 상호 보완(음수·다중 질의는 누적 합)
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — 창 안 문자·원소 개수를 세는 데 필수
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — 창 최댓값을 O(n)에 구하는 단조 덱의 토대
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — 겉보기 O(n²)를 amortized O(n)로 증명하는 근거
- 🗺️ **지도(MOC):** [[Phase-2 MOC]] · [[00 Algorithm MOC]]

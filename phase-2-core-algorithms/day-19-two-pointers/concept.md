---
day: 19
phase: 2-core-algorithms
title: 투 포인터 (Two Pointers)
category: [알고리즘, 탐색]
difficulty: 중급
status: done
prev: "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
next: "[[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]]"
related:
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]]"
  - "[[day-17-sorting/concept|Day 17 — 정렬]]"
  - "[[day-14-prefix-sum/concept|Day 14 — 누적 합]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
sources:
  - https://leetcode.com/problems/valid-palindrome/
  - https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
  - https://leetcode.com/problems/remove-duplicates-from-sorted-array/
  - https://leetcode.com/problems/squares-of-a-sorted-array/
  - https://leetcode.com/problems/container-with-most-water/
  - https://leetcode.com/problems/3sum/
  - https://leetcode.com/problems/trapping-rain-water/
  - https://school.programmers.co.kr/learn/courses/30/lessons/12924
tags: [phase/2, topic/two-pointers, topic/algorithm]
---

# Day 19 — 투 포인터 (Two Pointers)

> [!abstract] 한눈 요약 (TL;DR)
> **투 포인터(two pointers)는 배열·문자열 위에 두 개의 인덱스를 두고, 조건에 따라 둘을 움직여 O(n²) 완전 탐색을 O(n)으로 줄이는 기법**이다. 이중 for문으로 "모든 쌍"을 보던 문제를, 포인터가 되돌아가지 않게(단조 이동) 설계해 한 번의 스캔으로 푼다. 대표 형태는 세 가지다. (1) **양끝 수렴형(opposite ends)** — 정렬된 배열의 양 끝에서 시작해 합·거리 조건에 맞춰 안쪽으로 좁힌다(Two Sum II, 회문 검사, Container With Most Water). (2) **같은 방향 빠름/느림(fast & slow)** — 느린 포인터는 "채울 자리", 빠른 포인터는 "읽는 자리"로 두고 제자리에서 원소를 걸러낸다(중복 제거). (3) **두 배열 병합형** — 정렬된 두 수열을 각자의 포인터로 훑으며 합친다(정렬된 배열의 제곱). 성립의 대전제는 **단조성**이다. "한 포인터를 움직이면 조건이 한 방향으로만 변한다"가 보장돼야 포인터를 되돌리지 않아도 답을 놓치지 않는다. 그래서 대부분 [[day-17-sorting/concept|정렬]]이 선행되며, 창(window) 크기가 가변인 특수형이 바로 다음 [[day-20-sliding-window/concept|슬라이딩 윈도우]]다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **투 포인터**는 하나의 배열(또는 문자열)에 **두 개의 위치 인덱스**를 놓고, 문제의 조건을 보면서 두 포인터를 각각 앞뒤로 이동시켜 답을 찾는 기법이다. 핵심은 **두 포인터가 전체를 합쳐 O(n)번만 움직인다**는 점이다. 이중 반복문이 "왼쪽을 고정하고 오른쪽을 처음부터 다시 훑는"(되돌아가는) O(n²)이라면, 투 포인터는 "이미 확인한 구간은 다시 보지 않는다"로 O(n)을 만든다.
>
> **일상 비유 — 책장에서 두 손으로 책 찾기.** 정렬된 책장에서 "두께 합이 딱 30cm인 두 권"을 찾는다고 하자. 왼손은 가장 얇은 책(맨 왼쪽), 오른손은 가장 두꺼운 책(맨 오른쪽)에 둔다. 합이 30보다 크면 오른손을 한 칸 왼쪽(더 얇게)으로, 작으면 왼손을 한 칸 오른쪽(더 두껍게)으로 옮긴다. 두 손이 만날 때까지 각 손은 **한 방향으로만** 움직이므로 책장을 한 번만 훑으면 된다.
>
> **결정적 전제 — 단조성(monotonicity).** 위 비유가 성립하는 이유는 배열이 정렬돼 있어 "오른손을 왼쪽으로 옮기면 합이 반드시 줄어든다"가 보장되기 때문이다. 이 단조 관계가 없으면(정렬 안 됨) 포인터를 움직여 버린 구간에 답이 숨어 있을 수 있어 틀린다. 그래서 투 포인터 문제의 절반은 사실 "**어떻게 정렬/전처리해서 단조성을 만들 것인가**"의 문제다.
>
> **[[day-18-binary-search/concept|이분 탐색]]과의 대비.** 이분 탐색이 "탐색 공간을 매번 절반으로 접기"라면, 투 포인터는 "양쪽(또는 한쪽)에서 한 칸씩 좁히기"다. 둘 다 정렬을 전제로 O(n log n)/O(n)을 노리지만, 이분 탐색은 "특정 값/경계 하나"를, 투 포인터는 "쌍·구간·필터링"을 겨냥한다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 양끝 수렴형 — 정렬 배열에서 합이 target인 쌍 (Two Sum II)**
> ```
> 배열: [2, 7, 11, 15]   target = 18
>  lo=0 ......... hi=3   2+15=17 < 18  => 합을 키우려 lo++  (lo=1)
>       lo=1 .... hi=3   7+15=22 > 18  => 합을 줄이려 hi--  (hi=2)
>       lo=1  hi=2        7+11=18 == 18 => 발견! (index 1, 2)
> ```
> 규칙: `s = a[lo] + a[hi]`. `s < target`이면 `lo += 1`(합을 키움), `s > target`이면 `hi -= 1`(합을 줄임), 같으면 정답. `lo < hi`인 동안 반복. 정렬돼 있으므로 버리는 쪽에 정답이 없음이 보장된다.
>
> **(B) 같은 방향 빠름/느림 — 정렬 배열 중복 제거 (Remove Duplicates)**
> ```
> [1, 1, 2, 2, 3]   slow=쓸 자리, fast=읽는 자리
>  slow=0  fast=1  a[1]==a[0](1==1) -> 건너뜀
>  slow=0  fast=2  a[2]!=a[0](2!=1) -> slow++; a[1]=2
>  slow=1  fast=3  a[3]==a[1](2==2) -> 건너뜀
>  slow=1  fast=4  a[4]!=a[1](3!=2) -> slow++; a[2]=3
>  결과: 앞 3칸 [1,2,3], 길이 slow+1 = 3
> ```
> 규칙: `fast`가 앞에서 원소를 읽어보고 "새로운 값"일 때만 `slow`를 전진시켜 그 자리에 값을 덮어쓴다. 추가 배열 없이 O(1) 공간에 in-place로 거른다.
>
> **(C) 두 배열 병합형 — 정렬된 배열의 제곱 (Squares of a Sorted Array)**
> ```
> 정렬 배열: [-4, -1, 0, 3, 10]  (음수는 제곱하면 커진다!)
>  양끝에서 제곱을 비교해 "큰 것부터" 결과 배열 뒤에서 채운다.
>  lo=-4^2=16, hi=10^2=100 -> 100 뒤에 채움, hi--
>  lo=16,      hi=3^2=9    -> 16  채움, lo++  ...
>  => [0, 1, 9, 16, 100]  전체 O(n)
> ```
> 규칙: 양 끝의 절댓값이 가장 큰 쪽을 골라 결과의 **뒤에서부터** 채운다. 정렬을 다시 하면 O(n log n)이지만 투 포인터로 O(n)에 끝난다.
>
> **왜 O(n)인가.** 세 형태 모두 각 포인터는 시작점에서 끝점까지 **한 방향으로만** 이동하고 되돌아가지 않는다. 포인터 이동 총합이 최대 n이므로 전체 O(n). 이것이 이중 for문 O(n²)을 이기는 핵심이다.

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> | 상황 | 시간복잡도 | 공간 | 설명 |
> |---|---|---|---|
> | 정렬된 입력 + 투 포인터 | O(n) | O(1) | 한 번의 스캔, 포인터만 사용 |
> | 정렬 필요 + 투 포인터 | O(n log n) | O(1)~O(n) | 정렬이 지배항, 스캔은 O(n) |
> | 3Sum (정렬 + 고정 1개 + 투 포인터) | O(n²) | O(1) | 바깥 루프 n번 × 안쪽 투 포인터 n |
> | 완전 탐색(이중 for)과 비교 | O(n²) → O(n) | - | 되돌아감 제거로 한 차수 감소 |
>
> - **핵심은 "되돌아가지 않음".** 두 포인터가 각각 최대 n칸 이동 → 합쳐서 O(n). 이중 for문은 안쪽이 매번 처음부터라 O(n²).
> - **정렬 비용을 항상 세라.** 입력이 정렬돼 있지 않으면 O(n log n)이 먼저 붙는다. 그래도 O(n²)보다 낫다.
> - **3Sum류는 O(n²)가 최선급.** "한 원소 고정 → 나머지 투 포인터"라 한 차수만 줄어든다. n²이 한계라고 낙담 말 것(브루트포스 O(n³)를 이긴 것).
> - **공간 O(1)이 큰 장점.** in-place 필터링(중복 제거)은 [[day-14-prefix-sum/concept|누적 합]]처럼 별도 배열 없이 처리 가능.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **신호어로 패턴 잡기.** "정렬된 배열에서 …", "두 수의 합/차", "회문(palindrome)", "가장 큰/작은 넓이·거리", "중복 제거", "합쳐서 정렬" → 투 포인터를 먼저 의심하라. ([LeetCode Two Pointers 패턴 정리](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/))
> - **"양끝이냐 같은 방향이냐" 먼저 결정.** 합·넓이·회문처럼 **양쪽 조건**이면 `lo, hi` 양끝 수렴형. 필터링·중복 제거처럼 **읽기/쓰기 분리**면 `slow, fast` 같은 방향형.
> - **정렬이 인덱스를 망가뜨리는지 확인.** [Two Sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)는 이미 정렬돼 투 포인터가 되지만, 원본 인덱스를 답으로 요구하는 [Two Sum I](https://leetcode.com/problems/two-sum/)은 정렬하면 인덱스가 어긋나 [[day-09-hashing/concept|해시맵]]이 더 낫다. **"정렬해도 되는 문제인가"를 항상 자문하라.**
> - **중복 건너뛰기(dedup) 관용구.** [3Sum](https://leetcode.com/problems/3sum/)처럼 "유일한 조합"을 요구하면 `while lo < hi and a[lo] == a[lo-1]: lo += 1`로 같은 값을 건너뛴다. 이 한 줄을 빠뜨리면 중복 답이 쏟아진다.
> - **문자열 회문은 `isalnum()` + `lower()`.** [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)은 영숫자만 비교하고 대소문자를 무시한다. 양끝 포인터가 영숫자가 아닌 문자를 만나면 건너뛴다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **정렬 안 된 배열엔 양끝 수렴형이 틀린다.** 투 포인터의 대전제는 단조성이다. 합/거리 조건으로 좁히는 형태는 반드시 [[day-17-sorting/concept|정렬]]을 먼저 하거나, 입력이 이미 정렬임을 확인하라. 정렬이 불가능/무의미하면(원본 순서·인덱스 필요) 투 포인터가 아니라 [[day-09-hashing/concept|해시]]를 써라.
> 2. **`lo < hi` vs `lo <= hi` 경계.** 서로 다른 두 원소의 쌍을 찾을 땐 `lo < hi`(자기 자신과 짝짓지 않음). 회문 검사도 `lo < hi`면 가운데 글자는 자동으로 통과. 무엇을 세는지에 따라 등호 포함 여부가 갈린다.
> 3. **포인터를 실제로 전진시켜라(무한 루프 방지).** 조건 분기 안에서 `lo`/`hi` 중 하나는 반드시 움직여야 한다. 같은 값 건너뛰기 루프(`while a[lo]==...`)를 쓸 땐 범위 밖으로 나가지 않도록 `lo < hi` 조건을 함께 검사하라.
> 4. **중복 제거는 "정렬돼 있어야" O(n).** 빠름/느림 in-place 중복 제거는 **정렬된 배열** 전제다. 정렬 안 된 배열의 중복 제거는 [[day-09-hashing/concept|set]]으로 O(n) 공간을 쓰는 게 맞다.
> 5. **3Sum은 "정렬 → 고정 → 투 포인터".** 정렬 없이 투 포인터를 쓰면 틀린다. 바깥 원소를 고정하고 남은 구간에서 두 수의 합을 O(n)에 찾는 구조이며, 세 위치(고정·lo·hi) 모두에서 중복 스킵이 필요하다.
> 6. **투 포인터 ⊃ 슬라이딩 윈도우.** [[day-20-sliding-window/concept|슬라이딩 윈도우]]는 "두 포인터가 같은 방향으로 움직이며 그 사이 구간(window)을 유지"하는 투 포인터의 특수형이다. "부분 배열/부분 문자열의 합·길이 조건"이면 윈도우, "쌍/양끝 조건"이면 일반 투 포인터로 구분하면 편하다.
> 7. **면접 단골 — 왜 O(n)인가 설명하기.** "두 포인터의 이동 총합이 n을 넘지 않으므로"가 정답. 이 amortized(분할 상환) 논리를 말로 설명할 수 있어야 한다.
> 8. **Container With Most Water의 이동 규칙.** 넓이 = `min(h[lo], h[hi]) * (hi - lo)`. **더 낮은 쪽**을 안으로 옮긴다(높은 쪽을 옮기면 폭만 줄고 높이는 그대로라 결코 나아지지 않음). 이 "낮은 쪽 이동"의 정당성이 자주 물어보는 포인트다.

> [!example]- 예제 코드 (Examples)
> ```python
> # 1) 양끝 수렴형 - 정렬 배열에서 합이 target인 두 수 (1-indexed)
> def two_sum_sorted(a, target):
>     lo, hi = 0, len(a) - 1
>     while lo < hi:
>         s = a[lo] + a[hi]
>         if s == target:
>             return [lo + 1, hi + 1]
>         if s < target:
>             lo += 1          # 합을 키운다
>         else:
>             hi -= 1          # 합을 줄인다
>     return []
>
> # 2) 양끝 수렴형 - 회문(palindrome) 검사 (영숫자만, 대소문자 무시)
> def is_palindrome(s):
>     lo, hi = 0, len(s) - 1
>     while lo < hi:
>         while lo < hi and not s[lo].isalnum():
>             lo += 1
>         while lo < hi and not s[hi].isalnum():
>             hi -= 1
>         if s[lo].lower() != s[hi].lower():
>             return False
>         lo += 1
>         hi -= 1
>     return True
>
> # 3) 빠름/느림 - 정렬 배열 중복 제거 (in-place, O(1) 공간)
> def remove_duplicates(a):
>     if not a:
>         return 0
>     slow = 0
>     for fast in range(1, len(a)):
>         if a[fast] != a[slow]:
>             slow += 1
>             a[slow] = a[fast]
>     return slow + 1          # 유일 원소 개수
>
> # 4) 병합형 - 정렬 배열의 제곱을 정렬 상태로 (O(n))
> def sorted_squares(a):
>     n = len(a)
>     res = [0] * n
>     lo, hi, pos = 0, n - 1, n - 1
>     while lo <= hi:
>         if abs(a[lo]) > abs(a[hi]):
>             res[pos] = a[lo] * a[lo]
>             lo += 1
>         else:
>             res[pos] = a[hi] * a[hi]
>             hi -= 1
>         pos -= 1
>     return res
> ```
>
> 전체 실행 가능한 예제(양끝/빠름·느림/병합 3형 + Container 넓이): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 앞쪽은 **양끝 수렴형·빠름/느림 기초**, 뒤로 갈수록 **정렬 후 고정+투 포인터(3Sum)·투 포인터 응용(빗물)** 로 어려워진다.
>
> | 번호 | 문제 | 출처 | 난이도 | 핵심 |
> |---|---|---|---|---|
> | 1 | Valid Palindrome | [LeetCode #125](https://leetcode.com/problems/valid-palindrome/) | 🟢기초 | 양끝 회문 검사 |
> | 2 | Two Sum II - Input Array Is Sorted | [LeetCode #167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | 🟢기초 | 양끝 합 맞추기 |
> | 3 | Remove Duplicates from Sorted Array | [LeetCode #26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) | 🟢기초 | 빠름/느림 in-place |
> | 4 | Squares of a Sorted Array | [LeetCode #977](https://leetcode.com/problems/squares-of-a-sorted-array/) | 🟡중급 | 양끝 병합 |
> | 5 | Container With Most Water | [LeetCode #11](https://leetcode.com/problems/container-with-most-water/) | 🟡중급 | 낮은 쪽 이동 |
> | 6 | 숫자의 표현 | [프로그래머스 #12924](https://school.programmers.co.kr/learn/courses/30/lessons/12924) | 🟡중급 | 연속합 투 포인터 |
> | 7 | 3Sum | [LeetCode #15](https://leetcode.com/problems/3sum/) | 🟡중급 | 정렬+고정+투 포인터 |
> | 8 | Trapping Rain Water | [LeetCode #42](https://leetcode.com/problems/trapping-rain-water/) | 🔴심화 | 양끝 최대높이 추적 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 핵심 아이디어 + 여러 접근(브루트포스 vs 투 포인터, 정렬 후 투 포인터 등)과 복잡도 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — 정렬 배열을 "절반씩 접어" 탐색하는 기법. 투 포인터는 같은 정렬 전제 위에서 "양쪽/한쪽으로 좁혀" 훑는 사촌 기법이다
- ➡️ **다음(next):** [[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]] — 두 포인터가 같은 방향으로 움직이며 그 사이 "구간(window)"을 유지하는 투 포인터의 특수형
- 🧭 **관련(related):**
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — 정렬을 전제로 한 또 다른 O(log n)/O(n) 탐색 축
  - [[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]] — 투 포인터로 가변 구간을 다루는 직접적 확장
  - [[day-17-sorting/concept|Day 17 — 정렬]] — 투 포인터의 단조성을 만들어 주는 필수 전처리
  - [[day-14-prefix-sum/concept|Day 14 — 누적 합]] — 구간 합 문제에서 투 포인터/윈도우와 자주 함께 쓰인다
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — O(n²)→O(n) 감소를 amortized로 설명하는 근거
- 🗺️ **지도(MOC):** [[Phase-2 MOC]] · [[00 Algorithm MOC]]

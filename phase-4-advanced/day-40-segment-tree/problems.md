# Day 40 연습문제 — 세그먼트 트리·펜윅 트리 (Segment Tree & Fenwick/BIT)

> 출처는 **프로그래머스 / LeetCode만** 사용합니다.
> 난이도: 🟢기초 · 🟡중급 · 🔴심화 · ⚫기출
> 정답 코드 → [solutions.py](solutions.py) · 개념 → [concept.md](concept.md)

## 문제 목록

| # | 문제 | 출처 | 난이도 | 핵심 유형 |
|---|---|---|---|---|
| 1 | Range Sum Query - Immutable | [LeetCode #303](https://leetcode.com/problems/range-sum-query-immutable/) | 🟢기초 | 누적 합 (갱신 없음) |
| 2 | Range Sum Query - Mutable | [LeetCode #307](https://leetcode.com/problems/range-sum-query-mutable/) | 🟡중급 | 세그먼트 트리 / BIT |
| 3 | Count of Smaller Numbers After Self | [LeetCode #315](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | 🔴심화 | 값의 축 + 좌표 압축 + BIT |
| 4 | 징검다리 건너기 | [프로그래머스 #64062](https://school.programmers.co.kr/learn/courses/30/lessons/64062) | ⚫기출 | 구간 최댓값 / 덱 / 이분 탐색 |
| 5 | Reverse Pairs | [LeetCode #493](https://leetcode.com/problems/reverse-pairs/) | 🔴심화 | 역순 쌍 세기 (BIT / 머지 소트) |
| 6 | My Calendar III | [LeetCode #732](https://leetcode.com/problems/my-calendar-iii/) | 🔴심화 | 구간 갱신 (지연 전파 / 스위핑) |

---

## 1. Range Sum Query - Immutable 🟢

**출처:** [LeetCode #303](https://leetcode.com/problems/range-sum-query-immutable/)

정수 배열 `nums`로 객체를 만들고, `sumRange(left, right)`가 `nums[left..right]`(양끝 포함)의 합을 반환하도록 구현하라. `sumRange`는 여러 번 호출된다.

**제약:** `1 <= nums.length <= 10^4`, `-10^5 <= nums[i] <= 10^5`, 호출 최대 `10^4`회.

**시그니처 (LeetCode):**
```python
class NumArray:
    def __init__(self, nums: List[int]): ...
    def sumRange(self, left: int, right: int) -> int: ...
```

> [!tip]- 힌트 1
> 이 문제에는 **갱신이 없다**. 배열이 절대 변하지 않는다.
> 그러면 세그먼트 트리는 **필요 없다** — 더 단순하고 더 빠른 도구가 있다.

> [!tip]- 힌트 2
> `pref[i+1] = pref[i] + nums[i]`로 누적 합을 한 번 만들어 두면
> `sumRange(l, r) = pref[r+1] - pref[l]`이다. 전처리 O(N), 질의 **O(1)**.

> [!tip]- 힌트 3
> `pref`를 크기 `N+1`로 잡고 `pref[0] = 0`으로 두는 것이 정석이다.
> `l = 0`일 때 `pref[-1]` 같은 예외 처리를 없애준다.

> [!warning]- 이 문제를 먼저 푸는 이유
> 다음 문제 #307은 완전히 같은 질의에 **갱신 하나만 추가**된 것이다.
> 두 문제를 나란히 풀고 나면 **"갱신 유무가 자료구조를 결정한다"** 는
> 판단 기준이 몸에 남는다. 세그먼트 트리를 배웠다고 여기에도 쓰면
> 코드만 길어지고 질의는 O(1)에서 O(log N)으로 **느려진다**.

**복잡도 목표:** 전처리 O(N), 질의 O(1), 공간 O(N).

---

## 2. Range Sum Query - Mutable 🟡

**출처:** [LeetCode #307](https://leetcode.com/problems/range-sum-query-mutable/)

정수 배열 `nums`에 대해 두 연산을 지원하라.
- `update(index, val)` — `nums[index]`를 `val`로 바꾼다.
- `sumRange(left, right)` — `nums[left..right]`의 합을 반환한다.

**제약:** `1 <= nums.length <= 3·10^4`, `-100 <= nums[i] <= 100`, 호출 최대 `3·10^4`회.

**시그니처 (LeetCode):**
```python
class NumArray:
    def __init__(self, nums: List[int]): ...
    def update(self, index: int, val: int) -> None: ...
    def sumRange(self, left: int, right: int) -> int: ...
```

> [!tip]- 힌트 1
> #303의 누적 합을 그대로 쓰면 `update` 한 번마다 뒤쪽 전체를 다시 만들어야 해
> **O(N)** 이다. 호출이 3만 번이면 `3·10^4 × 3·10^4 = 9·10^8` → TLE.
> **갱신과 질의를 모두 O(log N)** 으로 만들어야 한다.

> [!tip]- 힌트 2
> 두 가지 정답이 있다.
> - **세그먼트 트리**: 잎을 `tree[n..2n-1]`에 깔고 `tree[i] = tree[2i] + tree[2i+1]`.
> - **BIT**: `i & -i`로 점프. 코드가 1/3이고 더 빠르다.
>
> 합 문제이므로 **BIT가 더 적합**하다. 둘 다 구현해 비교해보라.

> [!tip]- 힌트 3 (BIT의 함정)
> BIT의 `add(i, delta)`는 **증분(delta)** 을 받는다. 그런데 문제의 `update`는
> **값 지정(assign)** 이다. 현재 값을 따로 배열에 들고 있다가
> `add(index+1, val - cur[index])`로 환산하고 `cur[index] = val`을 해야 한다.
> 이걸 빼먹으면 값이 계속 누적되어 틀린다.

> [!tip]- 힌트 4 (인덱스 규약)
> 문제는 닫힌 구간 `[left, right]`, BIT는 1-based, 반복형 세그먼트 트리는
> 반열린 `[l, r)`이다. **입구에서 한 번만 변환**하라.
> - BIT: `range_sum(left+1, right+1)`
> - 반복형 세그트리: `query(left, right+1)`

**복잡도 목표:** 구축 O(N), `update`/`sumRange` 각각 O(log N).

---

## 3. Count of Smaller Numbers After Self 🔴

**출처:** [LeetCode #315](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)

정수 배열 `nums`가 주어진다. `counts[i]` = **`nums[i]`의 오른쪽에 있으면서 `nums[i]`보다 작은 원소의 개수**인 배열 `counts`를 반환하라.

**예시:** `nums = [5,2,6,1]` → `[2,1,1,0]`
(5의 오른쪽에 5보다 작은 것은 2와 1 → 2개, 2의 오른쪽에는 1 → 1개, …)

**제약:** `1 <= nums.length <= 10^5`, `-10^4 <= nums[i] <= 10^4`.

**시그니처 (LeetCode):**
```python
class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]: ...
```

> [!tip]- 힌트 1
> 브루트포스는 O(N²)이고 N=10⁵이면 10¹⁰ → TLE. **O(N log N)** 이 필요하다.

> [!tip]- 힌트 2 (핵심 발상 전환)
> 지금까지 세그먼트 트리/BIT를 **인덱스(위치)** 위에 세웠다.
> 이 문제에서는 **값** 위에 세운다. 각 칸이 "그 값이 지금까지 몇 번 나왔나"다.
> 그러면 `prefix(x-1)` = **"본 것 중 x보다 작은 것의 개수"** 가 된다.

> [!tip]- 힌트 3 (순회 방향)
> "**오른쪽에** 있는" 조건이므로 배열을 **오른쪽에서 왼쪽으로** 훑는다.
> `i`를 볼 때 BIT에 들어 있는 것이 정확히 "i보다 오른쪽에 있는 원소들"이다.
> ```
> for i in range(n-1, -1, -1):
>     answer[i] = bit.prefix(rank(nums[i]) - 1)   # 먼저 센다
>     bit.add(rank(nums[i]), 1)                   # 그다음 나를 등록
> ```
> **순서가 중요하다** — 나를 먼저 등록하면 나 자신을 셀 위험이 있고,
> 같은 값이 여러 개일 때 `<` 조건이 `<=`로 오염된다.

> [!tip]- 힌트 4 (좌표 압축)
> 값이 `-10^4..10^4`이므로 그냥 `+10001` 오프셋을 줘도 되지만,
> **일반해는 좌표 압축**이다. 값 범위가 10⁹이 되어도 그대로 통한다.
> ```python
> comp = sorted(set(nums))
> rank = bisect_left(comp, x) + 1        # 1-based (BIT 필수)
> ```
> `+1`을 빼먹으면 `x`가 최솟값일 때 `rank=0`이 되어 `add(0, 1)`이
> **무한 루프**에 빠진다.

> [!tip]- 힌트 5 (다른 정석: 머지 소트)
> 머지 소트로 병합하면서 "오른쪽 배열에서 먼저 빠져나간 원소 수"를 세는
> 방법도 O(N log N)이다. 인덱스를 함께 들고 정렬해야 해서 구현이 조금 더 길다.
> **BIT 쪽이 짧고 실수가 적다.**

**복잡도 목표:** O(N log N) 시간, O(N) 공간.

---

## 4. 징검다리 건너기 ⚫ (2019 카카오 겨울 인턴십)

**출처:** [프로그래머스 #64062](https://school.programmers.co.kr/learn/courses/30/lessons/64062)

디딤돌이 일렬로 놓여 있고 각 디딤돌에는 숫자가 적혀 있다. 친구들이 한 명씩 건너는데, **밟은 디딤돌의 숫자는 1 감소**한다. 숫자가 0이 된 디딤돌은 밟을 수 없어 **다음으로 밟을 수 있는 가장 가까운 디딤돌로 뛰어야** 하며, **한 번에 최대 `k`칸까지** 건너뛸 수 있다.

`stones`(디딤돌 숫자 배열)와 `k`가 주어질 때, **최대 몇 명이 건널 수 있는지** 반환하라.

**예시:** `stones = [2,4,5,3,2,1,4,2,5,1]`, `k = 3` → `3`

**제약:** `1 <= len(stones) <= 200,000`, `1 <= stones[i] <= 200,000,000`, `1 <= k <= len(stones)`.

**시그니처 (프로그래머스):**
```python
def solution(stones, k):
    return answer
```

> [!tip]- 힌트 1 (문제 변환이 전부다)
> "x명이 건널 수 있는가?"를 생각해보라. x명이 지나가면 각 디딤돌은
> 최대 x번 밟히므로, **`stones[i] < x`인 디딤돌은 x번째 사람 이전에 0이 된다**.
> 즉 x명이 건너지 **못하는** 조건은 **`stones[i] < x`인 디딤돌이 연속 k개**
> 나타나는 것이다(k칸을 넘어 뛸 수 없으므로).

> [!tip]- 힌트 2 (결론 — 방향을 헷갈리기 쉽다)
> 힌트 1의 "연속 k개가 **모두** `x`보다 작다"를 한 번 더 번역하라.
> **"모두 x보다 작다" = "그 구간의 최댓값 < x"** 이다(최솟값이 아니다!).
> 따라서 x가 실패하는 조건은 `min(윈도우 최댓값들) < x`이고, 답은
> **"길이 k인 모든 연속 구간의 최댓값 중 최솟값"** 이다.
> ```
> answer = min( max(stones[i : i+k]) for i in range(len(stones)-k+1) )
> ```
> 예시 검증: `[2,4,5,3,2,1,4,2,5,1]`, k=3의 윈도우 **최댓값**들은
> `5,5,5,3,4,4,5,5` → 그중 최솟값 **3** (문제의 기대 답과 일치)

> [!warning]- 이 문제 최대의 함정 (반드시 읽어라)
> 공식 예제에서는 **"최솟값들의 최댓값"도 우연히 3**이 나온다
> (윈도우 최솟값들 `2,3,2,1,1,1,2,1` → 최댓값 3).
> 그래서 **식을 거꾸로 세워도 예제는 통과**한다.
> 반례: `stones = [13,2,18,3,9,14,2,13,7,15,11,13,13,2,19]`, `k = 15`
> - 올바른 식(최댓값의 최솟값): 윈도우가 하나뿐이므로 `max(전체) = 19`
> - 잘못된 식(최솟값의 최댓값): `min(전체) = 2`
>
> **예제만 맞춰보고 제출하지 말고, 무작위 입력으로 브루트포스와 교차 검증하라.**
> 이분 탐색 풀이(힌트 3의 3번)와 답을 대조해 보면 즉시 드러난다.

> [!tip]- 힌트 3 (세 가지 구현)
> 1. **세그먼트 트리 구간 최댓값** — `SegTree(stones, max, -inf)`로 만들고
>    `query(i, i+k)`를 N번 구한 뒤 그중 최솟값. **O(N log N)**.
>    오늘 배운 도구의 직접 적용.
> 2. **덱 슬라이딩 윈도우** — 값이 증가하는 인덱스 덱을 유지. **O(N)**.
>    이게 **최적해**다([[day-20-sliding-window/concept|Day 20 슬라이딩 윈도우]] 참고).
> 3. **이분 탐색(파라메트릭 서치)** — "x명이 가능한가?"를 O(N)에 판정하고
>    x를 이분 탐색. **O(N log(max))**.
>
> **세 가지를 다 구현해 보는 것이 이 문제의 학습 가치**다. 오늘의 교훈은
> "세그먼트 트리는 만능이지만 최적은 아니다".

> [!warning]- 흔한 실수
> - `k`가 `len(stones)`와 같을 수 있다 → 윈도우가 딱 하나. 인덱스 범위 주의.
> - `stones[i]`가 최대 2억이므로 이분 탐색 상한을 `max(stones)`로 잡아라.
> - 세그먼트 트리 **최댓값** 항등원은 `-inf`다. 습관적으로 `0`을 쓰면
>   음수가 없는 이 문제에서는 우연히 통과하지만, 일반적으로는 오답이 된다.
> - 덱 풀이도 **최댓값용**이어야 한다(값이 **감소**하는 덱, `<=`로 pop).
>   최솟값용 덱을 그대로 쓰면 힌트 2의 함정에 그대로 빠진다.

**복잡도 목표:** 덱 O(N) / 세그먼트 트리 O(N log N) 둘 다 통과.

---

## 5. Reverse Pairs 🔴

**출처:** [LeetCode #493](https://leetcode.com/problems/reverse-pairs/)

배열 `nums`에서 **역순 쌍(reverse pair)** 의 개수를 반환하라. 역순 쌍은 `0 <= i < j < nums.length`이면서 **`nums[i] > 2 * nums[j]`** 인 쌍 `(i, j)`다.

**예시:** `nums = [1,3,2,3,1]` → `2` (쌍 `(1,4)`: 3 > 2·1, 쌍 `(3,4)`: 3 > 2·1)

**제약:** `1 <= nums.length <= 5·10^4`, `-2^31 <= nums[i] <= 2^31 - 1`.

**시그니처 (LeetCode):**
```python
class Solution:
    def reversePairs(self, nums: List[int]) -> int: ...
```

> [!tip]- 힌트 1
> #315와 **골격이 같다**. 조건이 `nums[j] < nums[i]`에서
> `2 * nums[j] < nums[i]`로 바뀐 것뿐이다. 오른쪽에서 왼쪽으로 훑으며
> "이미 본 것 중 `2*v < nums[i]`인 v의 개수"를 BIT로 센다.

> [!tip]- 힌트 2 (부등식을 경계로 옮기기 — 여기가 진짜 함정)
> `nums[i] > 2 * nums[j]`를 `nums[j]`에 대해 풀면 `nums[j] < nums[i] / 2`다.
> **정수 나눗셈 `x // 2`로 뭉개면 음수에서 틀린다.**
> 가장 안전한 방법은 **정수만으로 경계를 이분 탐색**하는 것이다.
> ```python
> comp    = sorted(set(nums))
> doubled = [2 * v for v in comp]          # 정렬 순서 유지 (단조 증가)
> cut = bisect_left(doubled, x)            # doubled[cut] >= x
> # -> rank 1..cut 에 해당하는 값들은 모두 2*v < x
> count = bit.prefix(cut)
> ```
> `doubled`가 정렬을 유지하는 이유: `v`가 증가하면 `2v`도 증가한다(단조).
> 부동소수(`x / 2`)를 쓰지 않으므로 큰 값·음수에서도 정확하다.

> [!tip]- 힌트 3 (경계 확인)
> `bisect_left`는 "`doubled[i] >= x`인 첫 i"를 준다. 따라서 `cut` 앞의 것들은
> 정확히 `2*v < x`를 만족한다 — 등호(`2*v == x`)는 **포함되지 않아야** 하고
> `bisect_left`가 바로 그렇게 동작한다. `bisect_right`를 쓰면
> `2*v == x`인 경우를 잘못 포함해 **답이 커진다**.

> [!tip]- 힌트 4 (다른 정석: 머지 소트)
> 병합 단계에서 왼쪽 절반의 각 `x`에 대해 오른쪽 절반에서 `2*y < x`인 `y`를
> 투 포인터로 세면 O(N log N)이다. 두 절반이 이미 정렬되어 있어
> 포인터가 되돌아가지 않는다는 것이 핵심.
> **BIT 풀이와 답이 일치하는지 서로 교차 검증**해 보라.

**복잡도 목표:** O(N log N) 시간, O(N) 공간.

---

## 6. My Calendar III 🔴

**출처:** [LeetCode #732](https://leetcode.com/problems/my-calendar-iii/)

`book(startTime, endTime)`으로 반열린 구간 `[startTime, endTime)` 일정을 추가한다. **k-booking**은 서로 겹치는(교집합이 비지 않는) 일정이 k개 있는 상태다. 각 `book` 호출 후 **현재 존재하는 최대 k**를 반환하라.

**예시:** `book(10,20)`→1, `book(50,60)`→1, `book(10,40)`→2, `book(5,15)`→3, `book(5,10)`→3, `book(25,55)`→3

**제약:** `0 <= startTime < endTime <= 10^9`, `book` 호출 최대 `400`회.

**시그니처 (LeetCode):**
```python
class MyCalendarThree:
    def __init__(self): ...
    def book(self, startTime: int, endTime: int) -> int: ...
```

> [!tip]- 힌트 1 (문제를 구간 갱신으로 번역)
> "`[start, end)`에 있는 모든 시점의 겹침 수를 +1하고, **전체 최댓값**을 답하라."
> → **구간 갱신(range add) + 전체 최댓값 질의**. 이게 지연 전파의 교과서 형태다.

> [!tip]- 힌트 2 (좌표 문제)
> 시간이 `0..10^9`이므로 배열을 그대로 잡을 수 없다. 두 가지 해법:
> - **좌표 압축**: 호출이 400번이니 서로 다른 경계는 최대 800개.
>   압축한 좌표축 위에 지연 전파 세그먼트 트리를 세운다.
>   단, 압축은 **모든 경계를 미리 알아야** 해서 온라인 질의에는 매번
>   재구축이 필요하다(호출 400번이면 그래도 충분하다).
> - **동적 세그먼트 트리(dynamic/implicit)**: 필요한 노드만 dict로 만든다.
>   압축 없이 `0..10^9` 좌표축을 그대로 쓸 수 있어 온라인 처리에 적합하다.

> [!tip]- 힌트 3 (지연 전파에서 최댓값 트리의 lazy)
> 합 트리와 다르다. **최댓값 트리에서는 구간 길이를 곱하지 않는다.**
> ```
> 합 트리   : tree[node] += add * (hi - lo)
> 최댓값 트리: tree[node] += add            # 길이 무관!
> ```
> 이 차이를 놓치는 것이 lazy 구현 최다 오답이다.

> [!tip]- 힌트 4 (제약을 보면 더 쉬운 답이 있다)
> **호출이 400번뿐이다.** 세그먼트 트리를 쓸 필요조차 없다.
> **차분(difference) + 스위핑**으로 끝난다.
> ```python
> # delta: dict[시각] = 증감량  (표준 라이브러리만 사용)
> delta[start] = delta.get(start, 0) + 1
> delta[end]   = delta.get(end, 0) - 1
> # 매 호출마다 시각 순으로 누적하며 최댓값 추적
> #   -> 호출당 O(N log N), 전체 O(N^2 log N). N=400 이면 넉넉히 통과
> ```
> **제약이 작으면 단순한 답이 정답이다.** 오늘의 교훈("세그먼트 트리가 항상
> 최적은 아니다")을 다시 확인하는 문제다. 단, **학습을 위해 지연 전파 버전도
> 반드시 구현해 보라** — 호출이 10만 번으로 늘면 그쪽만 살아남는다.

> [!warning]- 흔한 실수
> - 구간이 **반열린 `[start, end)`** 다. `end`를 포함시키면
>   `book(5,10)` 뒤 `book(10,20)`이 겹친 것으로 계산되어 틀린다.
> - `delta[end] -= 1`을 `delta[end-1]`로 바꾸면 경계가 어긋난다.
>   **경계를 그대로 쓰는 것이 안전**하다.
> - 지연 전파에서 **질의에도 `push_down`** 을 호출해야 한다.

**복잡도 목표:** 압축+지연 전파 O(N log N), 또는 차분 스위핑 O(N² log N)(N=400이면 충분).

---

## 학습 순서 제안

1. **#303 → #307을 연달아 풀어라.** 같은 질의에 갱신만 추가되었을 때
   자료구조가 어떻게 바뀌는지가 오늘의 핵심이다. #307은 **BIT와
   세그먼트 트리 두 버전**을 다 써보고 코드 길이를 비교하라.
2. **#315로 "값의 축" 발상을 익혀라.** 이게 안 넘어가면 #493도 못 푼다.
   좌표 압축 + 1-based rank를 손에 익힌다.
3. **#64062(징검다리)로 문제 변환을 연습하라.** 원래 문제가 "윈도우 최댓값의
   최솟값"이라는 걸 알아내는 것이 90%이고, **방향(min/max)을 뒤집지 않는 것**이
   나머지 10%다. 그리고 **덱이 세그먼트 트리보다 빠르다**는 것을 실측으로
   확인하라.
4. **#493은 #315의 변형**이다. 부등식을 BIT 질의 경계로 옮기는 계산에서
   **음수 처리**를 반드시 검증하라(`x // 2` 금지).
5. **#732로 지연 전파를 구현하라.** 그리고 제약이 작을 때는
   차분 스위핑이 낫다는 것도 함께 확인하라.

## 오늘의 판단 기준 (다시)

| 상황 | 도구 |
|---|---|
| 갱신 없음 | 누적 합 (질의 O(1)) |
| 질의가 마지막에만 | 차분 배열 (갱신 O(1)) |
| 갱신+질의 섞임, **합/개수** | **BIT** (코드 최단, 가장 빠름) |
| 갱신+질의 섞임, **min/max/gcd** | **세그먼트 트리** (항등원 주의) |
| **구간 전체** 갱신 | **지연 전파** (query에도 push) |
| 고정 길이 윈도우 min/max (#64062) | **덱** O(N) |
| 순서/역순 쌍 세기 | **값의 축 + 좌표 압축 + BIT** |

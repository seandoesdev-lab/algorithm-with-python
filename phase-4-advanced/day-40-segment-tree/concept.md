---
day: 40
phase: 4-advanced
title: 세그먼트 트리·펜윅 트리 (Segment Tree & Fenwick/BIT)
category: [자료구조, 세그먼트 트리, Segment Tree, 펜윅 트리, Fenwick Tree, BIT, 구간 질의, Range Query, 지연 전파, Lazy Propagation, 좌표 압축]
difficulty: 심화
status: done
prev: "[[day-39-trie/concept|Day 39 — 트라이 (Trie / Prefix Tree)]]"
next: "[[day-41-bitmask/concept|Day 41 — 비트마스킹 (Bitmasking)]]"
related:
  - "[[day-39-trie/concept|Day 39 — 트라이 (Trie / Prefix Tree)]]"
  - "[[day-14-prefix-sum/concept|Day 14 — 구간 자료구조 입문 (Prefix Sum)]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]]"
  - "[[day-17-sorting/concept|Day 17 — 정렬 (Sorting)]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-05-math/concept|Day 05 — 수학·진법·비트 기초]]"
sources:
  - https://leetcode.com/problems/range-sum-query-immutable/
  - https://leetcode.com/problems/range-sum-query-mutable/
  - https://leetcode.com/problems/count-of-smaller-numbers-after-self/
  - https://school.programmers.co.kr/learn/courses/30/lessons/64062
  - https://leetcode.com/problems/reverse-pairs/
  - https://leetcode.com/problems/my-calendar-iii/
  - https://en.wikipedia.org/wiki/Segment_tree
  - https://en.wikipedia.org/wiki/Fenwick_tree
tags: [phase/4, topic/segment-tree, topic/fenwick-tree, topic/bit, topic/range-query, topic/lazy-propagation, topic/prefix-sum, topic/coordinate-compression, topic/divide-conquer]
---

# Day 40 — 세그먼트 트리·펜윅 트리 (Segment Tree & Fenwick/BIT)

> [!abstract] 한눈 요약 (TL;DR)
> **세그먼트 트리(segment tree)** 는 배열의 **구간(segment)마다 미리 계산한 요약값을 트리로 쌓아둔 자료구조**다. 뿌리는 `[0, N)` 전체를, 두 자식은 왼쪽 절반과 오른쪽 절반을, 잎은 원소 하나를 담당한다. 이 한 가지 구조로 **"구간 질의(range query)"와 "원소 갱신(point update)"을 둘 다 O(log N)** 에 처리한다. 이게 왜 특별한가? [[day-14-prefix-sum/concept|누적 합(Day 14)]]은 구간 합 질의를 O(1)에 하지만 **원소 하나를 바꾸면 뒤쪽 누적 합 전체를 O(N)에 다시 만들어야** 한다. 반대로 원본 배열은 갱신이 O(1)이지만 질의가 O(N)이다. **세그먼트 트리는 이 둘을 O(log N)/O(log N)으로 타협**한다 — 질의 Q번, 갱신 U번이면 O(N + (Q+U) log N)이고, 누적 합의 O(N + Q + U·N)이나 브루트포스의 O(Q·N)이 시간 초과로 죽는 자리에서 살아남는다. 핵심 발상은 **"임의의 구간은 트리 위의 O(log N)개 노드로 정확히 쪼개진다"** 는 것이다(구간 분해, canonical decomposition). 합만 되는 게 아니다 — **결합법칙(associativity)** 만 성립하면 최솟값·최댓값·GCD·행렬곱·개수 무엇이든 얹을 수 있다(구간 최솟값 질의 = **RMQ**). 여기에 두 가지 확장이 코테 단골이다: **펜윅 트리(Fenwick tree / BIT, Binary Indexed Tree)** 는 세그먼트 트리에서 "합"만 특화해 코드 10줄·메모리 N칸으로 줄인 형태이고(`i & -i` 한 줄이 전부), **지연 전파(lazy propagation)** 는 "구간 전체에 +5" 같은 **구간 갱신(range update)** 까지 O(log N)으로 만든다. 그리고 세그먼트 트리/BIT의 진짜 무기는 합 질의가 아니라 **"정렬·순서 세기 문제를 값의 축 위에서 카운팅으로 바꾸는 것"** 이다 — 역순 쌍(inversion) 세기, 내 오른쪽에 나보다 작은 수 세기가 모두 O(N log N)으로 떨어진다(LeetCode #315, #493). 핵심 한 줄: **"구간을 미리 요약해 트리로 쌓으면, 임의 구간은 log개 조각으로 답이 나오고 갱신은 뿌리까지 log칸만 고친다."**

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **정의.** 길이 N인 배열 `A`에 대한 세그먼트 트리는 각 노드가 **구간 `[lo, hi)`** 를 담당하는 **이진 트리**이며, 노드에는 그 구간에 대한 **집계값(aggregate)** `f(A[lo..hi-1])`을 저장한다. 뿌리는 `[0, N)`, 어떤 노드가 `[lo, hi)`이면 `mid = (lo+hi)//2`로 잘라 왼쪽 자식이 `[lo, mid)`, 오른쪽 자식이 `[mid, hi)`를 맡는다. 잎은 길이 1 구간, 즉 원소 하나다. **`f`는 결합법칙을 만족하는 이항 연산**이어야 한다 — `f(f(a,b),c) = f(a,f(b,c))`. 합, 최솟값, 최댓값, GCD, XOR, 행렬곱이 모두 해당한다. (교환법칙은 필요 없다. 그래서 행렬곱도 얹힌다.)
>
> **핵심은 "부분 답을 미리 접어둔다"는 것.** 원본 배열은 원소만 안다. 누적 합은 "앞에서부터 여기까지"라는 **한 종류의 접기**만 미리 해둔다 — 그래서 질의는 빠르지만 앞쪽 원소 하나가 바뀌면 뒤쪽 전체가 무효가 된다. 세그먼트 트리는 **계층적으로, 여러 해상도로 접어둔다**. 원소 하나가 바뀌면 그 원소를 포함하는 구간은 **뿌리까지 이어지는 하나의 경로, 즉 log N개뿐**이다. 나머지 구간의 요약값은 전혀 영향받지 않는다. **"국소적 변화가 국소적 재계산으로 끝난다"** — 이것이 트리 구조가 주는 이득의 정체다.
>
> **일상 비유 — 회사의 매출 결산 보고 체계.** 팀장은 팀 매출 합계를, 부장은 팀 합계들의 합을, 사장은 전체를 들고 있다. "3팀부터 7팀까지 합계"를 물으면 사원 전부에게 묻지 않는다 — 이미 집계된 **팀·부 단위 보고서 몇 장을 골라 더하면** 된다. 사원 한 명의 실적이 수정되면? 사원 전체를 다시 세지 않고, **그 사람의 팀장 → 부장 → 사장 보고서만 갱신**한다. 딱 조직도의 높이만큼, 즉 log N번이다. 세그먼트 트리는 이 결산 체계를 자료구조로 굳힌 것이다.
>
> **또 다른 비유 — 지도의 축척(zoom level).** 세계 지도, 대륙 지도, 국가 지도, 도시 지도가 함께 있다고 하자. "서울에서 부산까지"를 표현할 때는 국가 지도 한 장이면 되고, "이 골목에서 저 골목"은 도시 지도를 본다. **질의 구간의 크기에 맞는 축척을 골라 쓰는 것** — 세그먼트 트리 질의가 하는 일이 정확히 이것이다. 큰 구간은 큰 노드 몇 개로, 양 끝의 자잘한 부분만 작은 노드로 채운다.
>
> **왜 O(log N)개 노드로 충분한가 (직관).** 질의 구간 `[l, r)`을 뿌리에서부터 내려가며 처리하면, 각 깊이에서 **"완전히 포함되어 즉시 답이 되는 노드"** 와 **"걸쳐 있어 더 내려가야 하는 노드"** 로 나뉜다. 그런데 **걸쳐 있는 노드는 각 깊이에 최대 2개** — 왼쪽 경계 `l`이 지나가는 노드와 오른쪽 경계 `r`이 지나가는 노드뿐이다(구간은 연속이므로 가운데는 통째로 포함된다). 깊이가 log N이니 방문 노드는 O(log N)이다. **경계 두 개만 쪼개진다**는 이 사실이 복잡도의 전부다.
>
> **경쟁 자료구조와의 역할 분담이 정확한 이해다.**
>
> | | 구축 | 구간 질의 | 원소 갱신 | 구간 갱신 | 메모리 | 비고 |
> |---|---|---|---|---|---|---|
> | 원본 배열 | O(N) | **O(N)** ❌ | O(1) ✅ | O(N) | N | 갱신만 잦으면 이게 정답 |
> | [[day-14-prefix-sum/concept\|누적 합(Day 14)]] | O(N) | **O(1)** ✅ | **O(N)** ❌ | O(N) | N | **갱신이 없으면 무조건 이것** |
> | 차분 배열(difference array) | O(N) | O(N) | O(N) | **O(1)** ✅ | N | 갱신 다 끝난 뒤 한 번 확정할 때 |
> | **펜윅 트리 (BIT)** | O(N) | **O(log N)** | **O(log N)** | O(log N)＊ | **N** ✅ | 합·역원 있는 연산만. **코드 최단** |
> | **세그먼트 트리** | O(N) | **O(log N)** | **O(log N)** | O(N)† | 2N~4N | **min/max/gcd 등 아무거나** ✅ |
> | **세그트리 + 지연 전파** | O(N) | **O(log N)** | O(log N) | **O(log N)** ✅ | 4N×2 | 구간 갱신까지 필요할 때 |
> | 스파스 테이블(sparse table) | O(N log N) | **O(1)** ✅ | 불가 ❌ | 불가 | N log N | **불변 배열 RMQ 최강** |
>
> ＊BIT는 두 개를 겹치면(range-update range-query BIT) 구간 갱신도 O(log N)에 된다. †지연 전파 없는 세그먼트 트리로 구간 갱신을 하면 원소마다 갱신해야 해서 O(N log N)이다.
>
> 결론은 단순하다. **갱신이 아예 없으면 누적 합/스파스 테이블이 옳다**(더 짧고 더 빠르다). **"갱신과 질의가 섞여서 번갈아 온다"** 는 신호가 보이는 순간 세그먼트 트리/BIT를 꺼낸다. 그리고 **합만 필요하면 BIT**(코드가 1/3), **최솟값·최댓값·GCD가 필요하면 세그먼트 트리**다. LeetCode #303(불변) vs #307(가변)이 정확히 이 갈림길에 나란히 서 있는 문제 쌍이다.
>
> **세그먼트 트리를 "값의 축" 위에 세우면 카운팅 도구가 된다.** 지금까지는 트리를 **인덱스(위치)** 위에 세웠다. 그런데 **값** 위에 세우고 "이 값이 지금까지 몇 번 나왔나"를 저장하면, `query(0, x)` = **"지금까지 나온 수 중 x보다 작은 것의 개수"** 가 된다. 배열을 오른쪽에서 왼쪽으로 훑으며 이걸 물으면 LeetCode #315 "내 오른쪽에 나보다 작은 수의 개수"가 O(N log N)에 풀린다. **이 발상 전환(위치 축 → 값 축)이 세그먼트 트리 문제의 진짜 난이도**이고, [[day-17-sorting/concept|정렬(Day 17)]]·역순 쌍 세기와 직결된다. 값의 범위가 크면 **좌표 압축(coordinate compression)** 으로 순위(rank)로 바꿔 넣는다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 구조 — 배열 하나로 트리를 표현한다 (1-based heap 인덱싱).**
> `A = [5, 3, 7, 1, 4, 2]` (N=6), 연산 = 합. [[day-12-heap/concept|힙(Day 12)]]과 같은 규칙 — 노드 `i`의 자식은 `2i`, `2i+1`, 부모는 `i//2`.
> ```
>                        [0,6) 22          <- tree[1] (root)
>                     /            \
>            [0,3) 15                [3,6) 7
>            /      \                /      \
>     [0,2) 8      [2,3) 7    [3,5) 5      [5,6) 2
>     /     \                  /     \
> [0,1)5  [1,2)3          [3,4)1  [4,5)4
>
>   잎 = 원소 하나, 내부 노드 = 두 자식의 합
>   tree[i] = f(tree[2i], tree[2i+1])       <- 이 한 줄이 불변식(invariant)
> ```
> **불변식 하나만 지키면 세그먼트 트리다.** 모든 내부 노드가 "두 자식을 `f`로 합친 값"이라는 것. 구축·갱신·질의 세 연산은 전부 이 불변식을 유지하거나 이용하는 일이다.
>
> **(B) 구축 (build) — 아래에서 위로, O(N).**
> ```
> 잎에 원본을 깔고, 뒤에서 앞으로 내부 노드를 채운다
>
>   tree[N + i] = A[i]                      for i in 0..N-1     (잎)
>   tree[i]     = f(tree[2i], tree[2i+1])   for i in N-1..1     (내부, 역순)
>
>   역순으로 도는 이유: tree[i] 를 계산할 때 자식 2i, 2i+1 은
>                       i 보다 크므로 이미 채워져 있다
>
>   비용: 노드 수 = 2N -> O(N).  (재귀로 나눠 내려가도 O(N))
> ```
> **잎을 `tree[N..2N-1]`에 두는 "반복(iterative) 방식"** 은 크기가 정확히 `2N`이면 되고 재귀가 없어 빠르다. 반면 **재귀(recursive) 방식**은 `mid`로 나누며 내려가고 배열 크기를 **`4N`** 으로 잡는다(N이 2의 거듭제곱이 아닐 때 인덱스가 `2N`을 넘을 수 있어서 넉넉히 잡는 관행). 코테에서는 **합/최솟값처럼 단순하면 반복형, 지연 전파가 필요하면 재귀형**을 쓴다.
>
> **(C) 원소 갱신 (point update) — 잎에서 뿌리까지 한 줄만 고친다, O(log N).**
> ```
> A[4] = 4 -> 9 로 바꾼다 (위 그림, 잎 인덱스 N+4)
>
>   1) 잎을 새 값으로 덮는다
>   2) 부모로 올라가며 tree[i] = f(tree[2i], tree[2i+1]) 를 다시 계산
>   3) 뿌리에 도달하면 끝
>
>            [0,6) 22 -> 27          <- 갱신
>          /          \
>   [0,3) 15        [3,6) 7 -> 12    <- 갱신
>                   /      \
>            [3,5) 5->10   [5,6) 2   <- 갱신 / 무관
>            /     \
>       [3,4)1   [4,5)4->9           <- 갱신(잎)
>
>   고쳐지는 노드는 경로 하나 = 트리 높이 = log N 개.
>   형제 서브트리는 건드리지 않는다 -> 이게 누적 합 대비 승리 지점.
> ```
>
> **(D) 구간 질의 (range query) — 걸치는 노드는 층마다 2개뿐, O(log N).**
> 재귀형이 이해하기 쉽다. 현재 노드 구간 `[lo,hi)`와 질의 구간 `[l,r)`의 관계는 **세 가지뿐**이다.
> ```
> query(node, lo, hi, l, r):
>     if r <= lo or hi <= l:          # (1) 완전히 벗어남 -> 항등원 반환
>         return IDENTITY             #     (합=0, 최솟값=+inf, 최댓값=-inf, gcd=0)
>     if l <= lo and hi <= r:         # (2) 완전히 포함 -> 저장값 즉시 사용 (더 안 내려간다!)
>         return tree[node]
>     mid = (lo + hi) // 2            # (3) 걸침 -> 반으로 쪼개 양쪽에 물어본다
>     return f(query(2*node,   lo, mid, l, r),
>              query(2*node+1, mid, hi, l, r))
> ```
> ```
> 위 그림에서 query([1,5)) = A[1]+A[2]+A[3]+A[4] = 3+7+1+4 = 15
>
>   [0,6) 걸침    -> 내려간다
>     [0,3) 걸침  -> 내려간다
>       [0,2) 걸침  -> 내려간다
>         [0,1) 벗어남 -> 0
>         [1,2) 포함  -> 3        (*)
>       [2,3) 포함  -> 7          (*)
>     [3,6) 걸침  -> 내려간다
>       [3,5) 포함  -> 5          (*)
>       [5,6) 벗어남 -> 0
>
>   답 = 3 + 7 + 5 = 15.  (*) 표시된 3개 노드가 구간의 "정규 분해"
>   방문 노드 총 9개 (N=6). N 이 커져도 층마다 걸치는 노드는 최대 2개.
> ```
> **조건 (2) "완전히 포함이면 즉시 반환"이 성능의 심장이다.** 이걸 빼먹고 잎까지 내려가면 O(N)이 된다. 세그먼트 트리를 처음 구현할 때 가장 흔한 성능 버그가 바로 이것이다.
>
> **(E) 반복형 질의 — 양쪽에서 좁혀 올라간다 (코테 최속 형태).**
> ```
> query(l, r):                  # 반열린 구간 [l, r)
>     resL = resR = IDENTITY
>     l += N;  r += N           # 잎 위치로 이동
>     while l < r:
>         if l & 1:             # l 이 오른쪽 자식 -> 이 노드는 부모에 포함 안 됨
>             resL = f(resL, tree[l]);  l += 1
>         if r & 1:             # r 이 오른쪽 자식 -> r-1 노드를 취한다
>             r -= 1;  resR = f(tree[r], resR)
>         l >>= 1;  r >>= 1     # 한 층 올라간다
>     return f(resL, resR)
>
>   왼쪽 결과와 오른쪽 결과를 따로 모으는 이유:
>     교환법칙이 없는 연산(행렬곱, 문자열 이어붙이기)에서도 순서를 지키려고.
>     합/최솟값만 쓸 거면 res 하나로 합쳐도 된다.
> ```
> 재귀 호출이 없어 파이썬에서 체감 속도가 크게 좋다. **`[l, r)` 반열린 구간 규약**을 쓰는 이유는 `r`을 그대로 올려 쓸 수 있어 off-by-one 버그가 줄기 때문이다.
>
> **(F) 펜윅 트리 (Fenwick / BIT) — "합"만 특화해 극단적으로 줄인 세그먼트 트리.**
> ```
> 아이디어: tree[i] 가 "i 에서 끝나고 길이가 (i & -i) 인 구간의 합"을 담는다
>          i & -i = i 의 최하위 1비트 (lowest set bit), 예: 12=1100 -> 4
>
>   i :  1    2    3    4    5    6    7    8
>  i&-i: 1    2    1    4    1    2    1    8
>  담당: [1] [1,2] [3] [1..4] [5] [5,6] [7] [1..8]
>
>        8 ------------------------------.
>        4 --------.                     |
>        2 --.     |          6 --.      |
>        1   |  3  |  5       |  7|      |
>        +---+--+--+--+-------+---+------+
>          1  2  3  4  5  6  7  8
>
> prefix_sum(i):  i 에서 최하위 비트를 계속 떼며 왼쪽으로 점프
>     s = 0
>     while i > 0:  s += tree[i];  i -= i & -i
>     예) prefix_sum(7) = tree[7] + tree[6] + tree[4]
>                       = [7] + [5,6] + [1..4]  =  [1..7]  OK
>
> add(i, delta):  i 를 포함하는 구간들로 오른쪽으로 점프
>     while i <= N:  tree[i] += delta;  i += i & -i
>     예) add(3) -> tree[3], tree[4], tree[8], ...
>
> range_sum(l, r) = prefix_sum(r) - prefix_sum(l-1)      <- 뺄셈이 필요!
> ```
> ```
> BIT 는 반드시 1-based 인덱스로 쓴다 (i & -i 가 0 에서 무한 루프이므로 i=0 금지).
>
> 세그먼트 트리 대비:  코드 10줄(vs 40줄), 메모리 N+1(vs 2N~4N), 상수도 더 작다.
> 대가:  "역원(inverse)이 있는 연산"만 된다.
>        합/XOR/개수 -> OK (뺄셈/XOR 로 구간을 만들 수 있다)
>        최솟값/최댓값 -> 일반 구간에는 NO (prefix_min 만 가능. max(a,b) 의 역원이 없다)
> ```
> **"합·개수 세기 = BIT, min/max/gcd = 세그먼트 트리"** — 이 한 줄이 실전 선택 기준이다. 그리고 **역순 쌍 세기 계열 문제는 거의 전부 BIT가 정답**이다(개수는 합이므로).
>
> **(G) 값의 축 위에 세우기 + 좌표 압축 — #315/#493의 열쇠.**
> ```
> 문제: nums[i] 의 오른쪽에 있는, nums[i] 보다 작은 수의 개수 (LeetCode #315)
>
> 관찰: 오른쪽에서 왼쪽으로 훑으며 "이미 본 수"를 값의 축에 표시해 두면
>       답 = "이미 본 수 중 nums[i] 보다 작은 것의 개수" = prefix_sum(rank-1)
>
>   nums = [5, 2, 6, 1]
>   정렬·중복제거 -> [1,2,5,6],  rank: 1->1, 2->2, 5->3, 6->4   (1-based)
>
>   i=3: x=1(rank1)  prefix_sum(0)=0  -> 0   ; add(1)
>   i=2: x=6(rank4)  prefix_sum(3)=1  -> 1   ; add(4)   (본 것: {1})
>   i=1: x=2(rank2)  prefix_sum(1)=1  -> 1   ; add(2)   (본 것: {1,6})
>   i=0: x=5(rank3)  prefix_sum(2)=2  -> 2   ; add(3)   (본 것: {1,6,2})
>
>   답 = [2,1,1,0]   OK    총 O(N log N)
>
> 좌표 압축이 필요한 이유: 값이 -10^4..10^4 이든 10^9 이든
>   BIT 크기는 "서로 다른 값의 개수"면 충분하다.
>   rank = bisect_left(sorted_unique, x) + 1
> ```
> **"오른쪽에서 왼쪽으로 + 값의 축 + 누적 개수"** 3콤보는 그대로 외워둘 패턴이다. LeetCode #493 "역순 쌍"은 조건이 `nums[i] > 2*nums[j]`로 바뀔 뿐 골격이 같다.
>
> **(H) 지연 전파 (lazy propagation) — 구간 갱신도 O(log N)으로.**
> ```
> 문제: "[l, r) 전체에 +5" 를 해야 한다. 원소마다 갱신하면 O(N log N).
>
> 아이디어: 노드에 "내 서브트리 전체에 아직 안 내려보낸 +5 가 있다"를 적어두고(lazy)
>          실제로 그 아래를 볼 일이 생겼을 때 자식에게 밀어준다(push down).
>
>   update(node, lo, hi, l, r, add):
>       if 완전히 벗어남:  return
>       if 완전히 포함:                        # 여기서 멈춘다! 아래로 안 내려감
>           tree[node] += add * (hi - lo)      # 합이면 구간 길이만큼
>           lazy[node] += add                  # 빚을 적어둔다
>           return
>       push_down(node, lo, hi)                # 자식 볼 일이 생겼으니 빚부터 청산
>       mid = (lo+hi)//2
>       update(왼쪽); update(오른쪽)
>       tree[node] = tree[2n] + tree[2n+1]     # 올라오며 재계산
>
>   push_down(node, lo, hi):
>       if lazy[node] == 0: return
>       mid = (lo+hi)//2
>       왼자식.tree += lazy * (mid-lo);  왼자식.lazy += lazy
>       우자식.tree += lazy * (hi-mid);  우자식.lazy += lazy
>       lazy[node] = 0
>
>   query 도 내려갈 때마다 push_down 을 먼저 호출해야 한다 (안 하면 옛 값을 읽는다).
> ```
> ```
> 지연 전파의 정신: "게으르게, 필요할 때만 일한다"
>   -> 구간 갱신이 O(log N) 노드에서 멈추므로 갱신도 질의와 같은 비용
>
> 주의: "구간 +add" 와 "구간 = set" 은 lazy 합성 규칙이 다르다.
>   +add 는 누적(lazy += add), set 은 덮어쓰기(lazy = v, 기존 +add 무효화).
>   둘이 섞이면 lazy 를 (배수, 덧셈량) 쌍으로 들거나 태그 종류를 구분해야 한다.
> ```
>
> **(I) 그 밖에 알아둘 변형.**
> ```
> - 차분 배열(difference array): 갱신이 전부 끝난 뒤 한 번만 확정하면 되면
>   구간 갱신 O(1) + 마지막에 누적 합 O(N). 세그먼트 트리가 필요 없다!
>   -> "질의가 마지막에 몰려 있는가?" 를 먼저 확인하라.
>
> - 스파스 테이블(sparse table): 갱신이 전혀 없는 RMQ 는 O(N log N) 전처리 후
>   질의 O(1). min/max/gcd 처럼 겹쳐도 되는(idempotent) 연산만.
>
> - 세그먼트 트리 이분 탐색(descent): "누적 합이 처음 k 를 넘는 위치"를
>   뿌리에서 내려가며 O(log N) 에 찾는다. (이분탐색 x 질의 = O(log^2 N) 보다 빠름)
>
> - 머지 소트 트리 / 좌표 압축 2D: 노드에 정렬된 리스트를 들고 있는 변형.
>
> - 2D 세그먼트 트리 / 2D BIT: 격자 구간 합. O(log^2 N).
> ```
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> [[day-16-big-o/concept|Big-O(Day 16)]] 기준. **N** = 원소 수, **Q** = 질의 수, **U** = 갱신 수.
>
> | 자료구조 / 연산 | 시간복잡도 | 공간 | 설명 |
> |---|---|---|---|
> | **세그먼트 트리 구축 (build)** | **O(N)** | O(2N)~O(4N) | 노드 수가 2N 내외. 잎 채우고 역순 1패스 |
> | **세그먼트 트리 구간 질의** | **O(log N)** | O(1) 반복 / O(log N) 재귀 | 층마다 걸치는 노드 최대 2개 |
> | **세그먼트 트리 원소 갱신** | **O(log N)** | O(1) | 잎→뿌리 경로 하나만 재계산 |
> | 세그먼트 트리 구간 갱신 (lazy 없이) | O(K log N) | O(1) | 원소 K개를 하나씩 → 느리다 |
> | **지연 전파 구간 갱신/질의** | **O(log N)** | O(4N)×2 (tree+lazy) | 포함되는 노드에서 멈춘다 |
> | **BIT 구축** | O(N log N) 순차 / **O(N)** 직접 | **O(N)** ✅ | `tree[i+(i&-i)] += tree[i]` 로 O(N) 구축 가능 |
> | **BIT prefix 합 / 갱신** | **O(log N)** | O(1) | 최하위 비트만큼 점프 = 세운 비트 수 ≤ log N |
> | BIT 구간 합 `[l,r]` | O(log N) | O(1) | `sum(r) - sum(l-1)`. **뺄셈 필요** |
> | BIT 구간 최솟값 (일반 구간) | **불가** ❌ | — | max/min에 역원이 없다. prefix_min만 가능 |
> | 누적 합 질의 / 갱신 | O(1) / **O(N)** | O(N) | **갱신 없으면 최강** |
> | 차분 배열 구간 갱신 / 질의 | **O(1)** / O(N) | O(N) | **질의가 마지막에 몰리면 최강** |
> | 스파스 테이블 RMQ | O(N log N) 전처리 / **O(1)** 질의 | O(N log N) | **갱신 불가**. 불변 배열 전용 |
> | 브루트포스 구간 질의 | O(N) | O(1) | Q·N — 보통 여기서 TLE 난다 |
> | 역순 쌍 세기 (BIT + 좌표 압축) | **O(N log N)** | O(N) | 브루트포스 O(N²) 대체 (#315, #493) |
> | 2D BIT / 2D 세그먼트 트리 | O(log² N) | O(N·M) | 격자 구간 합 |
>
> > **전체 시나리오 비용 비교가 판단 기준이다.** N=10⁵, Q=U=10⁵일 때(합 질의 + 원소 갱신이 섞임):
> >
> > | 방법 | 총 비용 | 대략 연산 수 |
> > |---|---|---|
> > | 브루트포스 | O(Q·N) | 10¹⁰ ❌ TLE |
> > | 누적 합 재구축 | O(U·N + Q) | 10¹⁰ ❌ TLE |
> > | **세그먼트 트리 / BIT** | O(N + (Q+U) log N) | **약 3.4×10⁶** ✅ |
> >
> > 3천 배 차이다. **"갱신과 질의가 번갈아 10만 번"** 이라는 제약을 보면 반사적으로 세그먼트 트리를 떠올려야 한다.
> >
> > **`log N`이 붙는 진짜 이유는 트리의 높이다.** N=10⁵면 높이 ≈ 17, N=10⁶이면 20. **N이 100배 늘어도 비용은 1.2배 남짓** 늘 뿐이다. 이 완만함이 세그먼트 트리를 "일단 이걸 쓰면 대체로 통과하는" 도구로 만든다.
> >
> > **BIT의 O(log N)은 "세워진 비트 수"다.** `i -= i & -i`는 매번 최하위 1비트를 지우므로, 반복 횟수는 `i`의 **popcount** ≤ log N이다. 상수가 매우 작아(비트 연산 한 번 + 배열 접근 한 번) 실전에서 세그먼트 트리보다 **2~3배 빠르다**. 합 문제라면 BIT를 먼저 고려하라.
> >
> > **공간이 왜 4N인가.** 재귀형에서 N이 2의 거듭제곱이 아니면 인덱스가 `2N`을 넘어갈 수 있다(예: N=5면 최대 인덱스 13 > 10). 정확한 상한은 `2·2^⌈log₂N⌉ ≤ 4N`이라 **관행적으로 4N을 잡는다**. 반복형(잎을 `tree[N..2N-1]`에)은 정확히 `2N`이면 된다. 파이썬은 리스트 원소당 8바이트 포인터 + 정수 객체라 N=10⁶에서 4N 리스트는 수십 MB로 튈 수 있으니 **반복형을 선호**하라.
> >
> > **파이썬 상수 비용을 무시하지 마라.** 같은 O(log N)이라도 재귀 세그먼트 트리는 함수 호출 오버헤드로 반복형보다 **3~5배 느리다**. N=2×10⁵, Q=2×10⁵ 급에서 재귀형이 TLE, 반복형이 통과하는 일이 실제로 있다. **BIT ＜ 반복형 세그트리 ＜ 재귀형 세그트리** 순으로 빠르다(왼쪽이 더 빠름).
> >
> > **지연 전파는 공간·상수 모두 2배다.** `tree`와 `lazy` 두 배열, 그리고 질의마다 `push_down` 호출이 추가된다. **구간 갱신이 정말 필요한지** 먼저 확인하라 — 원소 갱신만 있으면 lazy는 순수한 낭비다.
> >
> > **좌표 압축의 비용은 정렬이다.** BIT 자체는 O(N log N)이지만 압축을 위한 `sorted(set(nums))`도 O(N log N)이다. 전체는 여전히 O(N log N)이고, `bisect`로 rank를 찾는 것이 O(log N)임을 잊지 말자([[day-18-binary-search/concept|이분 탐색 Day 18]]).
>
> 파이썬 재귀 깊이: 세그먼트 트리 재귀는 깊이 log N(≈20)이라 안전하다. 그래서 **세그먼트 트리 때문에 `sys.setrecursionlimit`을 건드릴 일은 없다** — 깊은 재귀가 걱정되는 것은 DFS 계열이다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **암기 문장.** **"임의의 구간은 트리 위 log개 노드로 정확히 쪼개진다."** 여기서 전부 따라 나온다 — 질의가 O(log N), 갱신은 경로 하나뿐, 그리고 결합법칙만 있으면 어떤 연산이든 얹힌다. ([Segment tree 위키](https://en.wikipedia.org/wiki/Segment_tree))
> - **판단 순서를 고정하라.** ① **갱신이 있는가?** 없으면 [[day-14-prefix-sum/concept|누적 합(Day 14)]]/스파스 테이블로 끝. ② 있으면 **질의가 중간중간 섞이는가?** 마지막에 몰려 있으면 차분 배열. ③ 섞인다면 **연산이 합/개수인가?** 그러면 **BIT**. ④ min/max/gcd면 **세그먼트 트리**. ⑤ **구간 전체를 갱신**해야 하면 **지연 전파**. 이 5단계 결정 트리가 실전 선택의 전부다.
> - **BIT 골격은 3줄이니 손에 익혀라.** `while i <= n: tree[i] += d; i += i & -i` / `while i: s += tree[i]; i -= i & -i`. **`i & -i`가 최하위 1비트**라는 것만 알면 된다([[day-05-math/concept|비트 Day 05]]). 그리고 **BIT는 반드시 1-based** — `i=0`이면 `i & -i == 0`이라 무한 루프다.
> - **반열린 구간 `[l, r)` 규약으로 통일하라.** 파이썬 슬라이스와 같아 헷갈리지 않고, 반복형 질의에서 `r`을 그대로 쓸 수 있다. LeetCode는 보통 닫힌 구간 `[left, right]`로 주므로 **입구에서 `r+1`로 한 번만 변환**하고 내부는 전부 반열린으로 다루는 것이 버그를 줄인다.
> - **항등원(identity)을 연산에 맞게 바꿔라.** 합 → `0`, 곱 → `1`, 최솟값 → `float('inf')`, 최댓값 → `float('-inf')`, GCD → `0`(`gcd(0,x)=x`), XOR → `0`, AND → `-1`(모든 비트 1). **최솟값 트리에 항등원 0을 쓰는 것**이 대표적 오답 원인이다.
> - **"완전히 포함이면 즉시 반환"을 빼먹지 마라.** 이 한 줄이 없으면 잎까지 내려가 O(N)이 된다. 구현 후 **"큰 입력에서 이상하게 느리다"** 면 십중팔구 이 조건이다.
> - **`i & -i`가 왜 최하위 1비트인가.** 2의 보수에서 `-i = ~i + 1`이다. `~i`는 모든 비트를 뒤집고 `+1`은 최하위 0비트들을 타고 올라가 **최하위 1비트 위치에서 멈춘다** → `i`와 `-i`가 그 비트에서만 함께 1이다. 예: `12=1100`, `-12=...10100`, `AND = 100 = 4`. ([Fenwick tree 위키](https://en.wikipedia.org/wiki/Fenwick_tree))
> - **"오른쪽에서 왼쪽 + 값의 축 + 누적 개수"를 패턴으로 외워라.** [Count of Smaller Numbers After Self(LeetCode #315)](https://leetcode.com/problems/count-of-smaller-numbers-after-self/), [Reverse Pairs(#493)](https://leetcode.com/problems/reverse-pairs/)가 같은 골격이다. **인덱스가 아니라 값을 인덱스로 쓴다**는 발상 전환이 이 유형의 유일한 난관이다.
> - **좌표 압축은 `sorted(set(...))` + `bisect_left` 두 줄이다.** `rank = bisect_left(comp, x) + 1`. BIT 크기는 `len(comp)`면 충분하다. 값이 10⁹까지여도 서로 다른 값이 10⁵개면 배열은 10⁵칸이다.
> - **구간 질의 문제는 세그먼트 트리 말고 다른 답이 먼저일 수 있다.** [징검다리 건너기(프로그래머스 #64062)](https://school.programmers.co.kr/learn/courses/30/lessons/64062)는 **"길이 k 윈도우의 최댓값들 중 최솟값"** 이라 [[day-20-sliding-window/concept|슬라이딩 윈도우(Day 20)]] + 덱으로 **O(N)** 에 풀린다(세그먼트 트리는 O(N log N)). **세그먼트 트리는 만능이지만 최적은 아니다** — 답을 낸 뒤 더 단순한 풀이가 있는지 되돌아보는 습관이 실력 차이를 만든다.
> - **문제 변환의 방향을 끝까지 검산하라 — "최솟값의 최댓값"과 "최댓값의 최솟값"은 다르다.** 위 문제에서 "x명이 실패한다 = 연속 k개가 **모두** x 미만"인데, "모두 x 미만"은 **그 구간의 최댓값 < x**라는 뜻이다(최솟값이 아니다). 그래서 답은 `min(윈도우 최댓값들)`이다. 공교롭게도 **공식 예제에서는 두 식이 모두 3**이라 예제만 맞춰보면 통과한 것처럼 보인다. **무작위 입력으로 브루트포스와 교차 검증**해야 잡히는 종류의 오류다.
> - **`log²`를 피하는 트릭: 세그먼트 트리 하강(descent).** "누적 합이 처음 k 이상이 되는 위치"는 이분 탐색 + 질의(O(log²N))가 아니라 **뿌리에서 왼자식 값과 k를 비교하며 내려가면 O(log N)** 이다. BIT에서도 최상위 비트부터 내려가는 같은 기법이 있다.
> - **파이썬에서는 반복형을 기본으로.** 재귀 세그먼트 트리는 예쁘지만 느리다. 지연 전파가 필요할 때만 재귀로 가고, 그 외에는 `tree[N+i]` 반복형을 쓰라. 그리고 합 문제라면 애초에 BIT가 더 짧고 더 빠르다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **결합법칙이 없는 연산은 세그먼트 트리에 얹을 수 없다.** `f(f(a,b),c) = f(a,f(b,c))`가 성립해야 구간을 쪼개 합칠 수 있다. 합·min·max·gcd·XOR·행렬곱은 OK. **"구간의 최빈값", "구간의 중앙값", "구간에서 서로 다른 값의 개수"는 단순 집계로 결합되지 않는다** — 이런 문제는 머지 소트 트리, 오프라인 처리(Mo's algorithm), 혹은 다른 접근이 필요하다. 문제를 보고 **"두 구간의 답을 합쳐 큰 구간의 답이 나오는가?"** 를 먼저 자문하라.
> 2. **교환법칙은 필요 없지만, 순서는 지켜야 한다.** 행렬곱처럼 `f(a,b) ≠ f(b,a)`인 연산에서는 반복형 질의에서 **왼쪽 결과와 오른쪽 결과를 따로 모아 마지막에 `f(resL, resR)`** 로 합쳐야 한다. 하나의 변수에 마구 누적하면 순서가 뒤섞여 조용히 틀린다.
> 3. **BIT로는 일반 구간의 최솟값/최댓값을 구할 수 없다.** `range_sum(l,r) = sum(r) - sum(l-1)`이 성립하는 것은 **덧셈에 역원(뺄셈)이 있기 때문**이다. `max`에는 역원이 없다 — `max([1..r])`와 `max([1..l-1])`을 알아도 `max([l..r])`을 복원할 방법이 없다. **prefix_min/prefix_max(항상 1부터 시작)** 만 가능하다. 일반 구간 min/max는 세그먼트 트리를 쓰라. 이건 면접 단골 질문이다.
> 4. **BIT는 1-based 인덱스가 강제다.** `i = 0`이면 `i & -i == 0`이라 `i += 0`으로 **무한 루프**에 빠진다. 문제의 0-based 인덱스를 받으면 **입구에서 `+1`** 하고, 배열 크기도 `n+1`로 잡는다. 좌표 압축 rank도 `bisect_left(...) + 1`로 1부터 시작시켜라.
> 5. **최솟값 세그먼트 트리의 항등원은 0이 아니라 `inf`다.** "완전히 벗어난 구간"이 반환하는 값이 연산의 항등원이어야 한다. 합 트리에서 습관적으로 쓴 `0`을 최솟값 트리에 그대로 두면 **모든 답이 0으로 오염**된다. 최댓값은 `-inf`, GCD는 `0`, AND는 `-1`(파이썬 정수는 무한 비트라 `-1`이 "모든 비트 1")이다.
> 6. **재귀형 세그먼트 트리 배열은 `4N`을 잡아라.** `2N`으로 잡으면 N이 2의 거듭제곱이 아닐 때 인덱스 초과(IndexError) 또는 조용한 덮어쓰기가 난다. 반복형(잎을 `tree[N..2N-1]`)은 `2N`이 정확히 맞다. **두 방식의 인덱싱을 섞어 쓰지 마라** — 가장 찾기 어려운 버그가 된다.
> 7. **구간 갱신을 지연 전파 없이 하면 O(N log N)이다.** "구간에 +5"를 원소마다 point update로 처리하면 구간 길이가 N일 때 O(N log N)이고, 갱신이 10만 번이면 즉시 TLE다. **구간 갱신이 있으면 lazy를, 질의가 마지막에만 있으면 차분 배열을** 쓰라.
> 8. **지연 전파에서 `push_down`을 질의에도 호출해야 한다.** 갱신에서만 밀어주고 질의에서 빼먹으면 **자식이 옛 값을 들고 있어 틀린 답**이 나온다. 그리고 갱신 후 올라오며 `tree[node] = f(자식들)`을 재계산하는 것도 잊지 마라. 이 두 줄이 lazy 구현 오답의 90%다.
> 9. **lazy 태그의 합성 규칙은 연산마다 다르다.** "구간 +add"는 누적(`lazy += add`)이지만 "구간 = v로 덮어쓰기"는 **기존 lazy를 무효화**해야 한다(`lazy = v`, add 태그 제거). 둘이 섞이는 문제에서는 lazy를 `(곱, 더함)` 쌍이나 태그 종류로 들고 **합성 순서를 명시**해야 한다. 여기서 틀리면 디버깅이 지옥이다.
> 10. **"합 트리에 구간 +add"에서 구간 길이를 곱하는 것을 잊지 마라.** `tree[node] += add * (hi - lo)`다. 최솟값 트리라면 `tree[node] += add`(길이 무관), 최댓값도 마찬가지다. **연산 종류에 따라 lazy 적용식이 다르다.**
> 11. **인덱스 규약(닫힌 vs 반열린)을 코드 전체에서 하나로 통일하라.** `[l, r]`과 `[l, r)`을 섞으면 off-by-one이 나고, 그 버그는 경계 테스트에서만 드러나 발견이 늦다. **입구에서 한 번 변환하고 내부는 한 규약만** 쓰는 것이 정석이다.
> 12. **좌표 압축을 잊으면 MLE/IndexError다.** 값이 `-10⁹..10⁹`인데 BIT를 값 크기로 잡으면 배열이 20억 칸이다. **서로 다른 값의 개수만큼**만 필요하다. 그리고 음수 값을 압축하지 않고 그냥 인덱스로 쓰면 파이썬에서는 **에러 없이 리스트 뒤에서부터 접근**하는 최악의 조용한 버그가 난다.
> 13. **세그먼트 트리가 정답이 아닐 수 있음을 늘 의심하라.** ① 갱신이 없다 → 누적 합/스파스 테이블. ② 질의가 마지막에 몰림 → 차분 배열. ③ 고정 길이 윈도우의 min/max → [[day-20-sliding-window/concept|덱(Day 20)]]으로 O(N). ④ "k번째 큰 값" 스트림 → [[day-12-heap/concept|힙(Day 12)]]. **세그먼트 트리는 강력한 대신 코드가 길고 상수가 크다** — 더 단순한 도구로 되는지 30초만 먼저 생각하라.
> 14. **파이썬 성능 순서를 기억하라: BIT가 가장 빠르고, 반복형 세그트리, 재귀형 세그트리 순이다.** 같은 O(log N)이라도 실측 차이가 몇 배다. N, Q가 2×10⁵ 이상인 문제에서 재귀형이 TLE 나면 **알고리즘이 틀린 게 아니라 구현 형태를 바꿔야** 한다. 입출력도 `sys.stdin`을 쓰는 등 상수 관리가 함께 필요하다([[day-01-fast-io/concept|Day 01]]).
> 15. **실무에서 이 자료구조가 쓰이는 곳.** DB의 **구간 인덱스·집계 뷰**, 시계열 모니터링 시스템의 **다중 해상도 롤업(rollup)** — 초/분/시/일 단위 집계를 계층으로 들고 있는 구조가 정확히 세그먼트 트리다. 게임 서버의 **랭킹 보드**(내 점수보다 높은 사람 수 = BIT prefix count), 컴퓨터 그래픽스의 **구간 겹침 판정**, 텍스트 에디터의 **줄 오프셋 관리(rope 자료구조)**. **"부분 집계를 계층으로 쌓아 국소 갱신을 싸게 만든다"** 는 발상은 알고리즘 문제를 넘어 시스템 설계의 기본 패턴이다.
> 16. **면접 단골 비교: 세그먼트 트리 vs BIT vs 누적 합.** 정답 요지: "**누적 합은 질의 O(1)·갱신 O(N)**, **세그먼트 트리는 둘 다 O(log N)**, **BIT는 세그먼트 트리에서 합만 특화해 코드와 메모리를 줄인 것**이다. BIT는 역원이 있는 연산만 되고 일반 구간 min/max는 불가하다. 구간 갱신까지 필요하면 지연 전파를 얹는다."

> [!example]- 예제 코드 (Examples)
> ```python
> # ---- (1) 반복형 세그먼트 트리: 임의 결합 연산 (코테 최속 형태) ----
> class SegTree:
>     """반열린 구간 [l, r) 규약. 잎은 tree[n..2n-1] 에 배치."""
>     def __init__(self, data, func=lambda a, b: a + b, identity=0):
>         self.n = len(data)
>         self.f = func
>         self.e = identity                      # 항등원: 합0 / min inf / max -inf
>         self.tree = [identity] * (2 * self.n)
>         self.tree[self.n:] = data              # 잎을 깐다
>         for i in range(self.n - 1, 0, -1):     # 역순으로 내부 노드 채우기 -> O(N)
>             self.tree[i] = self.f(self.tree[2 * i], self.tree[2 * i + 1])
>
>     def update(self, i, value):                # A[i] = value,  O(log N)
>         i += self.n
>         self.tree[i] = value
>         i >>= 1
>         while i:                               # 잎 -> 뿌리 경로만 재계산
>             self.tree[i] = self.f(self.tree[2 * i], self.tree[2 * i + 1])
>             i >>= 1
>
>     def query(self, l, r):                     # f(A[l..r-1]),  O(log N)
>         resL = resR = self.e                   # 좌/우 분리 -> 비가환 연산도 안전
>         l += self.n
>         r += self.n
>         while l < r:
>             if l & 1:                          # l 이 오른쪽 자식 -> 지금 취한다
>                 resL = self.f(resL, self.tree[l]); l += 1
>             if r & 1:                          # r 이 오른쪽 자식 -> r-1 을 취한다
>                 r -= 1; resR = self.f(self.tree[r], resR)
>             l >>= 1; r >>= 1                   # 한 층 올라간다
>         return self.f(resL, resR)
>
> # 합 트리 / 최솟값 트리 — 항등원만 바꾸면 끝
> seg_sum = SegTree([5, 3, 7, 1, 4, 2])
> seg_min = SegTree([5, 3, 7, 1, 4, 2], min, float('inf'))
>
>
> # ---- (2) 펜윅 트리 (BIT): 합 전용, 코드 10줄 ----
> class BIT:
>     """1-based 인덱스 강제 (i=0 이면 i & -i == 0 -> 무한 루프)."""
>     def __init__(self, n):
>         self.n = n
>         self.tree = [0] * (n + 1)
>
>     def add(self, i, delta):                   # A[i] += delta,  O(log N)
>         while i <= self.n:
>             self.tree[i] += delta
>             i += i & -i                        # 나를 포함하는 상위 구간으로
>
>     def prefix(self, i):                       # A[1..i] 의 합,  O(log N)
>         s = 0
>         while i > 0:
>             s += self.tree[i]
>             i -= i & -i                        # 최하위 1비트를 떼며 왼쪽으로
>         return s
>
>     def range_sum(self, l, r):                 # A[l..r] (닫힌 구간)
>         return self.prefix(r) - self.prefix(l - 1)   # 뺄셈 = 역원 필요!
>
>
> # ---- (3) 값의 축 + 좌표 압축: 오른쪽의 더 작은 수 개수 (LeetCode #315) ----
> from bisect import bisect_left
>
> def count_smaller(nums):
>     comp = sorted(set(nums))                   # 좌표 압축
>     bit = BIT(len(comp))
>     out = [0] * len(nums)
>     for i in range(len(nums) - 1, -1, -1):     # 오른쪽 -> 왼쪽
>         rank = bisect_left(comp, nums[i]) + 1  # 1-based rank
>         out[i] = bit.prefix(rank - 1)          # 나보다 작은 것의 개수
>         bit.add(rank, 1)                       # 나를 등록
>     return out
>
>
> # ---- (4) 지연 전파: 구간 +add / 구간 합 (재귀형, 4N) ----
> class LazySeg:
>     def __init__(self, data):
>         self.n = len(data)
>         self.tree = [0] * (4 * self.n)
>         self.lazy = [0] * (4 * self.n)
>         self._build(data, 1, 0, self.n)
>
>     def _build(self, a, node, lo, hi):
>         if hi - lo == 1:
>             self.tree[node] = a[lo]; return
>         mid = (lo + hi) // 2
>         self._build(a, 2 * node, lo, mid)
>         self._build(a, 2 * node + 1, mid, hi)
>         self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
>
>     def _push(self, node, lo, hi):
>         if self.lazy[node] == 0:
>             return
>         mid = (lo + hi) // 2
>         v = self.lazy[node]
>         for ch, ln in ((2 * node, mid - lo), (2 * node + 1, hi - mid)):
>             self.tree[ch] += v * ln            # 합 트리 -> 구간 길이를 곱한다
>             self.lazy[ch] += v                 # 빚을 물려준다
>         self.lazy[node] = 0
>
>     def add_range(self, l, r, v, node=1, lo=0, hi=None):
>         if hi is None:
>             hi = self.n
>         if r <= lo or hi <= l:
>             return
>         if l <= lo and hi <= r:                # 완전 포함 -> 여기서 멈춘다
>             self.tree[node] += v * (hi - lo)
>             self.lazy[node] += v
>             return
>         self._push(node, lo, hi)               # 자식 볼 일 생김 -> 빚 청산
>         mid = (lo + hi) // 2
>         self.add_range(l, r, v, 2 * node, lo, mid)
>         self.add_range(l, r, v, 2 * node + 1, mid, hi)
>         self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]
>
>     def sum_range(self, l, r, node=1, lo=0, hi=None):
>         if hi is None:
>             hi = self.n
>         if r <= lo or hi <= l:
>             return 0                           # 항등원
>         if l <= lo and hi <= r:
>             return self.tree[node]
>         self._push(node, lo, hi)               # 질의에서도 push 필수!
>         mid = (lo + hi) // 2
>         return (self.sum_range(l, r, 2 * node, lo, mid)
>                 + self.sum_range(l, r, 2 * node + 1, mid, hi))
>
>
> # ---- (5) 세그먼트 트리 하강: 누적 합이 처음 k 이상이 되는 위치, O(log N) ----
> def find_kth(seg, k):
>     """합 세그먼트 트리(반복형, n 이 2의 거듭제곱)에서 누적 합 >= k 인 최소 인덱스."""
>     node = 1
>     while node < seg.n:                        # 잎에 도달할 때까지
>         left = 2 * node
>         if seg.tree[left] >= k:
>             node = left                        # 왼쪽에 답이 있다
>         else:
>             k -= seg.tree[left]                # 왼쪽을 다 쓰고 오른쪽으로
>             node = left + 1
>     return node - seg.n
> ```
>
> 전체 실행 가능한 예제(브루트포스와의 무작위 교차 검증, 누적 합·BIT·세그먼트 트리 성능 비교, min/max/gcd 트리, 지연 전파 검증, 슬라이딩 윈도우 최솟값과 RMQ 비교 포함): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> **불변 구간 합 → 가변 구간 합 → 값의 축 카운팅 → RMQ 기출 → 역순 쌍 → 구간 갱신** 순으로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Range Sum Query - Immutable | [LeetCode #303](https://leetcode.com/problems/range-sum-query-immutable/) | 🟢기초 | 누적 합. **갱신이 없으면 세그먼트 트리가 필요 없다**는 기준선 |
> | 2 | Range Sum Query - Mutable | [LeetCode #307](https://leetcode.com/problems/range-sum-query-mutable/) | 🟡중급 | 세그먼트 트리/BIT 핵심. #303과의 대비가 학습 포인트 |
> | 3 | Count of Smaller Numbers After Self | [LeetCode #315](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | 🔴심화 | 값의 축 + 좌표 압축 + BIT. 위치→값 발상 전환 |
> | 4 | 징검다리 건너기 | [프로그래머스 #64062](https://school.programmers.co.kr/learn/courses/30/lessons/64062) | ⚫기출 | 2019 카카오 겨울 인턴십. 길이 k 윈도우 **최댓값의 최솟값** = 구간 최댓값 vs 덱 vs 이분 탐색 |
> | 5 | Reverse Pairs | [LeetCode #493](https://leetcode.com/problems/reverse-pairs/) | 🔴심화 | 역순 쌍(inversion) 세기. BIT vs 머지 소트 두 정석 |
> | 6 | My Calendar III | [LeetCode #732](https://leetcode.com/problems/my-calendar-iii/) | 🔴심화 | 구간 겹침 최대 개수 = 구간 갱신(지연 전파) vs 차분/스위핑 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> #303과 #307을 나란히 놓고 "갱신 유무가 자료구조를 결정한다"를 확인하는 법, 반복형 세그먼트 트리와 BIT를 같은 문제에 둘 다 구현해 코드 길이·속도를 비교하는 법, #315에서 좌표 압축 rank를 1-based로 만드는 이유와 오른쪽→왼쪽 순회의 근거, 징검다리 건너기의 문제 변환을 "연속 k개가 모두 x 미만 = 그 구간의 최댓값 < x"까지 정확히 밀어붙여 답이 **`min(윈도우 최댓값들)`** 임을 유도하고(공식 예제만으로는 "최솟값의 최댓값"과 구별되지 않는 함정), 이를 **① 세그먼트 트리 구간 최댓값 O(N log N) ② 덱 슬라이딩 윈도우 O(N) ③ 이분 탐색 + 판정 O(N log max)** 세 가지로 풀고 왜 ②가 최적인지, #493의 `nums[i] > 2*nums[j]` 조건을 BIT 질의 경계로 옮기는 계산과 머지 소트 풀이와의 비교, #732를 지연 전파 세그먼트 트리와 정렬 딕셔너리 스위핑으로 각각 푸는 법, 그리고 모든 구현을 브루트포스와 무작위 교차 검증하는 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-39-trie/concept|Day 39 — 트라이 (Trie / Prefix Tree)]] — 트라이가 **문자열 집합**을 트리로 조직해 접두사 질의를 O(L)로 만들었다면, 세그먼트 트리는 **구간(range)** 을 트리로 조직해 구간 질의를 O(log N)로 만든다. 둘 다 "미리 계층으로 접어두면 질의가 싸진다"는 같은 사상의 다른 적용이다
- ➡️ **다음(next):** [[day-41-bitmask/concept|Day 41 — 비트마스킹 (Bitmasking)]] — Phase 4 심화 개념의 마지막 축. BIT의 `i & -i`, 세그먼트 트리의 `i >> 1`/`i & 1`에서 이미 비트 연산을 도구로 썼는데, 비트마스킹은 그 비트 자체를 **상태(state)** 로 쓰는 기법이다(부분집합 순회, 비트 DP)
- 🧭 **관련(related):**
  - [[day-14-prefix-sum/concept|Day 14 — 구간 자료구조 입문 (Prefix Sum)]] — 세그먼트 트리의 직접적인 전신이자 최대 경쟁자. **갱신이 없으면 누적 합이 정답**이고, 갱신이 끼는 순간 세그먼트 트리로 넘어온다. 차분 배열까지 함께 비교해야 선택 기준이 완성된다
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — 배열 하나를 `2i`/`2i+1`로 이진 트리처럼 쓰는 **암묵적 트리(implicit tree)** 인덱싱이 완전히 같다. 힙 인덱싱을 손에 익혔다면 세그먼트 트리 배열 표현은 새로 배울 게 없다
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 노드·자식·높이·완전 이진 트리 개념이 전제. "높이가 log N"이 모든 복잡도의 출처다
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 구간을 `mid`로 반씩 쪼개 부분 답을 합치는 것이 정확히 분할정복이다. 세그먼트 트리는 **분할정복의 결과를 캐싱해 재사용하는 자료구조**로 볼 수 있다
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — 좌표 압축의 `bisect_left`, 세그먼트 트리 하강(descent)으로 "누적 합이 처음 k 이상인 위치"를 O(log N)에 찾는 기법, 징검다리 건너기의 파라메트릭 서치 풀이가 모두 여기서 온다
  - [[day-20-sliding-window/concept|Day 20 — 슬라이딩 윈도우]] — 고정 길이 윈도우의 min/max는 덱으로 **O(N)** 이고 세그먼트 트리 O(N log N)보다 빠르다. 징검다리 건너기에서 "세그먼트 트리가 만능이지만 최적은 아니다"를 배우는 지점
  - [[day-17-sorting/concept|Day 17 — 정렬 (Sorting)]] — 역순 쌍(inversion) 개수는 "정렬에 필요한 인접 교환 횟수"이고, 머지 소트로 세는 것과 BIT로 세는 것이 같은 답을 낸다. #315/#493이 이 연결의 교과서적 예
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — "Q·N이 10¹⁰이라 죽고, (Q+U)·log N이 3×10⁶이라 산다"는 계산이 세그먼트 트리를 꺼낼지 판단하는 유일한 근거다
  - [[day-05-math/concept|Day 05 — 수학·진법·비트 기초]] — `i & -i`가 최하위 1비트인 이유(2의 보수), `i >> 1`로 부모 찾기, popcount가 BIT 반복 횟수인 이유가 모두 비트 연산의 기초 위에 있다
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]

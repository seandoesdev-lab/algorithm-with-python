# Day 12 — 힙·우선순위 큐 (Heap & Priority Queue) 연습문제

> 출처는 **LeetCode**와 **프로그래머스**만 사용한다.
> 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 풀이 코드는 [solutions.py](solutions.py) 참고 (각 문제 다중 접근 + assert 자체 테스트).

---

## 1. Last Stone Weight 🟢기초
- **출처:** [LeetCode #1046](https://leetcode.com/problems/last-stone-weight/)
- **요약:** 돌 무게 배열에서 매 턴 **가장 무거운 두 돌**을 부딪쳐, 같으면 둘 다 사라지고 다르면 차이만큼 남긴다. 마지막에 남는 돌 무게(없으면 0)를 반환.
- **핵심 아이디어:** 최대 힙. 파이썬은 최소 힙뿐이므로 **부호를 뒤집어**(-x) 넣고 꺼낼 때 복원한다.
- **힌트:** 두 개를 pop → 차이를 다시 push. 힙 크기가 1 이하가 될 때까지 반복.

## 2. Kth Largest Element in an Array 🟡중급
- **출처:** [LeetCode #215](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- **요약:** 배열에서 **k번째로 큰 값**을 반환(정렬 순서 기준, 중복 포함).
- **핵심 아이디어:** **크기 k짜리 최소 힙**을 유지하면 힙의 바닥(`heap[0]`)이 곧 답. 작은 값이 들어오면 버린다.
- **힌트:** 정렬은 O(n log n), 크기 k 힙은 O(n log k). `heapq.nlargest(k, nums)[-1]` 한 줄도 가능. (면접 심화: 평균 O(n) Quickselect)

## 3. Kth Largest Element in a Stream 🟢기초
- **출처:** [LeetCode #703](https://leetcode.com/problems/kth-largest-element-in-a-stream/)
- **요약:** 값이 **스트림으로 계속 들어올 때**마다 현재까지의 k번째 큰 값을 반환하는 클래스 설계.
- **핵심 아이디어:** 크기 k 최소 힙을 멤버로 들고, `add` 마다 push 후 k 초과면 pop. 항상 `heap[0]`이 답.
- **힌트:** "최댓값 k개만 살아남기면 그 중 최솟값이 k번째 큰 값"을 떠올린다.

## 4. Top K Frequent Elements 🟡중급
- **출처:** [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/)
- **요약:** 가장 **자주 등장하는 원소 k개**를 반환(순서 무관).
- **핵심 아이디어:** `Counter`로 빈도를 세고, 빈도를 key로 `heapq.nlargest(k, ...)`.
- **힌트:** O(n log k). (버킷 정렬로 O(n)도 가능하지만 힙이 가장 짧고 안전.)

## 5. K Closest Points to Origin 🟡중급
- **출처:** [LeetCode #973](https://leetcode.com/problems/k-closest-points-to-origin/)
- **요약:** 평면 점들 중 **원점에서 가장 가까운 k개**를 반환.
- **핵심 아이디어:** 거리 제곱(`x²+y²`, sqrt 불필요)을 기준으로 **크기 k 최대 힙**을 유지해 먼 점을 버린다.
- **힌트:** 가까운 k개를 "남긴다" → 최대 힙으로 가장 먼 것을 쫓아낸다. O(n log k).

## 6. Merge k Sorted Lists 🔴심화
- **출처:** [LeetCode #23](https://leetcode.com/problems/merge-k-sorted-lists/)
- **요약:** **정렬된 k개의 연결 리스트**를 하나의 정렬된 리스트로 병합.
- **핵심 아이디어:** 각 리스트의 **머리 노드만** 힙에 넣고 최솟값을 뽑아 이어붙인 뒤, 그 노드의 다음 노드를 다시 push. 힙 크기 = k → O(N log k).
- **힌트:** 튜플에 `(val, 인덱스, node)`처럼 **고유 인덱스를 끼워** 동점일 때 노드끼리 비교(TypeError)를 막는다. 연결 리스트는 [[day-10-linked-list/concept|Day 10]] 참고.

## 7. Find Median from Data Stream 🔴심화
- **출처:** [LeetCode #295](https://leetcode.com/problems/find-median-from-data-stream/)
- **요약:** 값이 스트림으로 들어올 때마다 **지금까지의 중앙값**을 O(log n)에 구하는 클래스.
- **핵심 아이디어:** **두 개의 힙.** 아래 절반은 최대 힙(`small`), 위 절반은 최소 힙(`large`). 두 꼭대기로 중앙값을 즉시 계산.
- **힌트:** 불변식 = `max(small) <= min(large)` 이고 크기 차이는 1 이하. 넣을 때마다 한쪽에 넣고 균형을 맞춘다. "두 힙으로 중앙값"은 매우 유명한 패턴.

## 8. 더 맵게 🟡중급
- **출처:** [프로그래머스 #42626](https://school.programmers.co.kr/learn/courses/30/lessons/42626)
- **요약:** 모든 음식의 스코빌이 K 이상이 되도록 **가장 안 매운 두 음식**을 `최소 + 두번째*2`로 섞는다. 필요한 최소 횟수(불가능하면 -1)를 반환.
- **핵심 아이디어:** 최소 힙. `heap[0] < K`인 동안 두 개를 꺼내 섞어 다시 넣고 카운트.
- **힌트:** 종료 후 `heap[0] >= K`인지 확인. 원소가 1개만 남았는데 K 미만이면 -1.

## 9. 디스크 컨트롤러 🔴심화
- **출처:** [프로그래머스 #42627](https://school.programmers.co.kr/learn/courses/30/lessons/42627)
- **요약:** `[요청시각, 소요시간]` 작업들의 **평균 대기시간(요청→완료)을 최소화**하는 스케줄을 짜고 그 평균(소수점 버림)을 반환.
- **핵심 아이디어:** **SJF(Shortest Job First).** 현재 시각까지 도착한 작업을 모두 힙에 넣고, **소요시간이 가장 짧은 작업**부터 처리한다.
- **힌트:** 요청 시각으로 먼저 정렬. 대기열이 비면 다음 작업 도착 시각으로 시간을 점프. 힙 키 = `(소요시간, 요청시각)`.

## 10. 이중우선순위큐 🟡중급
- **출처:** [프로그래머스 #42628](https://school.programmers.co.kr/learn/courses/30/lessons/42628)
- **요약:** `I n`(삽입), `D 1`(최댓값 삭제), `D -1`(최솟값 삭제) 명령을 처리한 뒤 **[최댓값, 최솟값]**(비었으면 [0,0])을 반환.
- **핵심 아이디어:** **최소 힙 + 최대 힙**을 동시에 유지하고, 한쪽에서 지운 값은 다른 힙에 남아 있으므로 **게으른 삭제(lazy deletion)**로 꼭대기를 정리한다.
- **힌트:** 값별 "살아있는 개수" 딕셔너리로 유효성 추적. (정렬 리스트나 균형 트리가 없는 파이썬에서 흔한 우회.)

---

### 추천 풀이 순서
1) #1046 → #703 → #215 (최대/최소 힙, 크기 k 힙 감 잡기)
2) #347 → #973 (빈도·거리 기준 Top-K)
3) #23 → #295 (k-way 병합 / 두 힙 중앙값 — 힙의 꽃)
4) 프로그래머스 #42626 → #42628 → #42627 (기출: 기본 힙 → 게으른 삭제 → SJF 스케줄링)

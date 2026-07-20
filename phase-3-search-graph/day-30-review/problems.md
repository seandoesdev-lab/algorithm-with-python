# Day 30 — 연습문제: 개념 집중기 종합 복습 (Final Review)

> 개념 집중기(Phase 0~3) 전 범위를 섞은 **종합 세트**입니다.
> 각 문제에서 먼저 **"세 개의 질문"** 을 던지세요:
> ① 무엇을 저장·조회하나(자료구조)? ② 이미 정렬/단조인가(기법)? ③ 상태 공간을 어떻게 훑나(탐색)?
> 정답 코드는 [solutions.py](solutions.py) 참고. 출처는 **프로그래머스 / LeetCode**만 사용합니다.

| # | 문제 | 출처 | 난이도 | 무기(신호) |
|---|---|---|---|---|
| 1 | Valid Anagram | [LeetCode #242](https://leetcode.com/problems/valid-anagram/) | 🟢기초 | 해시/Counter |
| 2 | Two Sum | [LeetCode #1](https://leetcode.com/problems/two-sum/) | 🟢기초 | 해시 O(1) 조회 |
| 3 | Valid Parentheses | [LeetCode #20](https://leetcode.com/problems/valid-parentheses/) | 🟢기초 | 스택 |
| 4 | Binary Search | [LeetCode #704](https://leetcode.com/problems/binary-search/) | 🟢기초 | 이분 탐색 |
| 5 | Number of Islands | [LeetCode #200](https://leetcode.com/problems/number-of-islands/) | 🟡중급 | 완전탐색+DFS/BFS |
| 6 | Merge Intervals | [LeetCode #56](https://leetcode.com/problems/merge-intervals/) | 🟡중급 | 정렬+그리디 |
| 7 | Top K Frequent Elements | [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/) | 🟡중급 | 해시+힙 |
| 8 | Course Schedule | [LeetCode #207](https://leetcode.com/problems/course-schedule/) | 🟡중급 | 그래프 사이클(DFS/BFS) |
| 9 | 타겟 넘버 | [프로그래머스 #43165](https://school.programmers.co.kr/learn/courses/30/lessons/43165) | ⚫기출 | 완전탐색/DFS |
| 10 | 네트워크 | [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162) | ⚫기출 | 그래프 연결요소(DFS/BFS) |

---

## 1. Valid Anagram 🟢 — 해시/Counter

- **링크:** [LeetCode #242](https://leetcode.com/problems/valid-anagram/)
- **요약:** 두 문자열 `s`, `t`가 서로 애너그램(anagram, 같은 글자를 재배열한 것)인지 판별한다.
- **입력/출력:** `s = "anagram"`, `t = "nagaram"` → `True` / `s = "rat"`, `t = "car"` → `False`
- **무기 판단:** ① 저장·조회 = "각 글자의 개수" → `Counter`/`dict`. 정렬(O(n log n))로도 되지만 해시 집계가 O(n)로 더 빠르다.
- **힌트:** 길이가 다르면 즉시 `False`. `Counter(s) == Counter(t)` 한 줄.
- **복잡도:** 해시 O(n) / 정렬 O(n log n).

## 2. Two Sum 🟢 — 해시 O(1) 조회

- **링크:** [LeetCode #1](https://leetcode.com/problems/two-sum/)
- **요약:** 배열에서 합이 `target`이 되는 두 원소의 인덱스를 반환한다(정답은 유일, 같은 원소 재사용 불가).
- **입력/출력:** `nums = [2,7,11,15]`, `target = 9` → `[0,1]`
- **무기 판단:** ② 정렬 안 됨 → 브루트포스는 O(n^2). ① "이미 본 값을 O(1)에 조회"하고 싶다 → 해시. 이 문제가 "해시로 O(n^2)를 O(n)으로"의 대표 예.
- **힌트:** 순회하며 `target - x`가 `seen`에 있는지 확인 후, 없으면 `seen[x] = i` 저장.
- **복잡도:** O(n) 시간 / O(n) 공간.

## 3. Valid Parentheses 🟢 — 스택

- **링크:** [LeetCode #20](https://leetcode.com/problems/valid-parentheses/)
- **요약:** `()[]{}` 로 이루어진 문자열이 올바르게 짝지어지고 중첩됐는지 판별한다.
- **입력/출력:** `"()[]{}"` → `True` / `"(]"` → `False` / `"([)]"` → `False`
- **무기 판단:** ① "가장 최근에 열린 괄호가 가장 먼저 닫혀야" = **후입선출(LIFO)** → 스택.
- **힌트:** 여는 괄호는 push, 닫는 괄호는 top과 짝이 맞으면 pop. 끝에 스택이 비어야 유효.
- **복잡도:** O(n) 시간 / O(n) 공간.

## 4. Binary Search 🟢 — 이분 탐색

- **링크:** [LeetCode #704](https://leetcode.com/problems/binary-search/)
- **요약:** **오름차순 정렬된** 배열에서 `target`의 인덱스를 반환(없으면 -1). O(log n)으로.
- **입력/출력:** `nums = [-1,0,3,5,9,12]`, `target = 9` → `4`
- **무기 판단:** ② "정렬돼 있다 + 값 찾기" → 이분 탐색의 교과서.
- **힌트:** `lo <= hi` 루프, `mid = (lo+hi)//2`, 크면 `hi=mid-1` 작으면 `lo=mid+1`. `bisect`로도 가능.
- **복잡도:** O(log n) 시간 / O(1) 공간.

## 5. Number of Islands 🟡 — 완전탐색 + DFS/BFS

- **링크:** [LeetCode #200](https://leetcode.com/problems/number-of-islands/)
- **요약:** `'1'`(땅)과 `'0'`(물)로 된 그리드에서 상하좌우로 연결된 땅 덩어리(섬)의 개수를 센다.
- **입력/출력:** 아래 그리드 → `3`
  ```
  1 1 0 0 0
  1 1 0 0 0
  0 0 1 0 0
  0 0 0 1 1
  ```
- **무기 판단:** ③ 그리드 전체를 **완전 탐색**하다가 방문 안 한 땅을 만나면 그 섬 전체를 **DFS/BFS**로 지운다(방문 처리). 격자 그래프의 연결 요소 세기.
- **힌트:** 방문한 `'1'`을 `'0'`으로 덮어쓰면 별도 visited 없이 처리 가능. 깊은 그리드는 BFS(큐)로 재귀 한계 회피.
- **복잡도:** O(R*C) 시간 / O(R*C) 공간(최악).

## 6. Merge Intervals 🟡 — 정렬 + 그리디

- **링크:** [LeetCode #56](https://leetcode.com/problems/merge-intervals/)
- **요약:** 구간 목록에서 겹치는 구간을 모두 병합한다.
- **입력/출력:** `[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`
- **무기 판단:** ② "구간 문제의 90%는 정렬부터" → 시작점 정렬 후 앞에서부터 그리디로 겹치면 확장.
- **힌트:** 정렬 후 `현재.start <= 직전.end`면 `직전.end = max(직전.end, 현재.end)`.
- **복잡도:** O(n log n) 시간(정렬 지배) / O(n) 공간.

## 7. Top K Frequent Elements 🟡 — 해시 + 힙

- **링크:** [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/)
- **요약:** 배열에서 가장 자주 등장한 상위 `k`개 원소를 반환한다.
- **입력/출력:** `nums = [1,1,1,2,2,3]`, `k = 2` → `[1,2]`
- **무기 판단:** ① "빈도수" → `Counter`(해시 집계, O(n)). "상위 K 추출" → 힙(`nlargest`, O(n log k)) 또는 버킷 정렬(O(n)).
- **힌트:** `heapq.nlargest(k, freq, key=freq.get)`. 빈도를 인덱스로 쓰는 버킷 정렬이면 O(n).
- **복잡도:** 해시+힙 O(n log k) / 버킷 정렬 O(n).

## 8. Course Schedule 🟡 — 그래프 사이클 판정(DFS/BFS)

- **링크:** [LeetCode #207](https://leetcode.com/problems/course-schedule/)
- **요약:** 선수과목 관계 `prerequisites`가 주어질 때 모든 과목을 수강할 수 있는지(= 유향 그래프에 사이클이 없는지) 판별한다.
- **입력/출력:** `numCourses = 2`, `[[1,0]]` → `True` / `[[1,0],[0,1]]` → `False`(순환)
- **무기 판단:** ③ 정점-간선 관계 → 그래프. "모두 처리 가능?" = **사이클 없음(DAG)?** → 위상 정렬(BFS, 진입차수) 또는 DFS 3색 판정.
- **힌트:** 진입차수 0인 노드부터 큐로 제거(Kahn). 제거한 노드 수 == 전체면 사이클 없음. Phase 4의 위상 정렬 맛보기.
- **복잡도:** O(V+E) 시간 / O(V+E) 공간.

## 9. 타겟 넘버 ⚫기출 — 완전탐색/DFS

- **링크:** [프로그래머스 #43165](https://school.programmers.co.kr/learn/courses/30/lessons/43165)
- **요약:** 음이 아닌 정수 배열 `numbers`의 각 수 앞에 `+` 또는 `-`를 붙여 순서대로 더해 `target`을 만드는 방법의 수를 구한다.
- **입력/출력:** `numbers = [1,1,1,1,1]`, `target = 3` → `5`
- **무기 판단:** ③ 각 수마다 두 갈래(+/-) → `2^n` 조합 **완전 탐색**을 **DFS**로. 제약이 `n <= 20`이라 `2^20 ~ 10^6`으로 허용된다(제약이 곧 힌트).
- **힌트:** `dfs(i, total)` — 마지막 인덱스에서 `total == target`이면 1을 반환. `itertools.product([+1,-1], repeat=n)`로도 가능.
- **복잡도:** O(2^n) 시간 / O(n) 재귀 깊이.

## 10. 네트워크 ⚫기출 — 그래프 연결 요소(DFS/BFS)

- **링크:** [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162)
- **요약:** 컴퓨터 수 `n`과 연결 정보 `computers`(인접 행렬)가 주어질 때, 네트워크(연결 요소, connected component)의 개수를 구한다.
- **입력/출력:** `n = 3`, `[[1,1,0],[1,1,0],[0,0,1]]` → `2`
- **무기 판단:** ③ 관계 = 그래프. "몇 개의 덩어리?" = **연결 요소 개수**. 방문 안 한 노드에서 DFS/BFS를 시작할 때마다 카운트를 +1.
- **힌트:** `visited` 배열로 방문 표시. `for i in range(n): if not visited[i]: count += 1; dfs(i)`. Union-Find로도 풀린다(대표원소 개수).
- **복잡도:** O(n^2) 시간(인접 행렬) / O(n) 공간.

---

## 학습 포인트 (개념 집중기 마무리)

- **문제를 읽는 즉시 "세 개의 질문"을 던지는 습관**을 몸에 붙인다: 자료구조 → 기법 → 탐색, 그리고 항상 **Big-O 검산**.
- **제약(constraints)이 알고리즘을 결정한다.** N의 상한을 먼저 보고 허용 복잡도를 역산하라(타겟 넘버가 대표 예).
- **결합이 실전이다.** 섬의 개수(완전탐색+DFS), Top K(해시+힙), 구간 병합(정렬+그리디)처럼 무기는 섞여 나온다.
- **막히면 완전 탐색으로 내려가** baseline을 잡고, 거기서 해시·정렬·가지치기·메모이제이션으로 최적화한다.
- 내일(Day 31)부터는 **문제 풀이기**: 이 판단 근육으로 유형별 기출을 반복 훈련한다.

---
day: 11
phase: 1-data-structures
title: 트리 기본 (Tree Basics)
category: [자료구조, 트리]
difficulty: 기초
status: done
prev: "[[day-10-linked-list/concept|Day 10 — 연결 리스트]]"
next: "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
related:
  - "[[day-10-linked-list/concept|Day 10 — 연결 리스트]]"
  - "[[day-07-stack/concept|Day 07 — 스택]]"
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-25-dfs/concept|Day 25 — DFS]]"
  - "[[day-26-bfs/concept|Day 26 — BFS]]"
  - "[[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]]"
sources:
  - https://leetcode.com/problems/maximum-depth-of-binary-tree/
  - https://leetcode.com/problems/invert-binary-tree/
  - https://leetcode.com/problems/same-tree/
  - https://leetcode.com/problems/binary-tree-inorder-traversal/
  - https://leetcode.com/problems/symmetric-tree/
  - https://leetcode.com/problems/balanced-binary-tree/
  - https://leetcode.com/problems/diameter-of-binary-tree/
  - https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/
  - https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42892
tags: [phase/1, topic/tree]
---

# Day 11 — 트리 기본 (Tree Basics)

> [!abstract] 한눈 요약 (TL;DR)
> **트리(tree)**는 데이터를 **계층(hierarchy)** 구조로 담는 자료구조다. 연결 리스트가 노드를 "한 줄"로 이었다면, 트리는 한 노드가 **여러 자식(child)**을 가리키며 "가지처럼" 뻗어나간다. 사이클이 없고 노드가 N개면 간선(edge)은 항상 N-1개인 **연결된 그래프**다. 코테에서는 특히 자식이 최대 둘인 **이진 트리(binary tree)**와, 왼쪽<부모<오른쪽 규칙을 지키는 **이진 탐색 트리(BST)**가 핵심이다. 트리 문제의 90%는 **재귀(recursion)** 로 풀린다 — "현재 노드를 처리하고 왼쪽·오른쪽 자식에게 같은 일을 시킨다"는 한 줄 사고가 전부다. DFS(스택/재귀)·BFS(큐)로 순회하며, 깊이·높이·경로·대칭 등을 묻는 문제가 LeetCode·카카오 단골이다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **트리**는 **루트(root)** 라는 하나의 꼭대기 노드에서 시작해, 각 노드가 아래로 **자식 노드(child)** 들을 가지는 계층적 자료구조다. 위아래가 거꾸로인 "나무"라고 보면 된다 — 뿌리(root)가 맨 위, 잎(leaf)이 맨 아래.
>
> 가장 친숙한 비유는 **회사 조직도**나 **컴퓨터 폴더 구조**다. 최상위 폴더(root) 아래에 하위 폴더(자식)가 있고, 그 안에 또 하위 폴더가 있으며, 더 이상 하위가 없는 파일(leaf)에서 끝난다. 어떤 폴더로 가는 경로는 항상 **유일**하고, 위로 거슬러 올라가면 반드시 하나의 루트로 모인다.
>
> ```
>            [1]  <- 루트(root), 깊이 0
>           /   \
>        [2]     [3]   <- 깊이 1
>       /   \       \
>     [4]   [5]     [6]  <- 깊이 2, 자식 없으면 잎(leaf)
> ```
>
> **꼭 외워야 하는 용어 (Terminology)**
>
> | 용어 | 영어 | 뜻 |
> |---|---|---|
> | 루트 | root | 부모가 없는 최상위 노드(딱 하나) |
> | 부모 | parent | 어떤 노드의 바로 위 노드 |
> | 자식 | child | 어떤 노드의 바로 아래 노드 |
> | 형제 | sibling | 같은 부모를 둔 노드들 |
> | 잎/단말 | leaf | 자식이 없는 노드 |
> | 내부 노드 | internal node | 자식이 하나 이상 있는 노드 |
> | 조상/자손 | ancestor / descendant | 위쪽 경로의 모든 노드 / 아래쪽 모든 노드 |
> | 간선 | edge | 부모-자식을 잇는 연결선 (노드 N개 → 간선 N-1개) |
> | 깊이 | depth | 루트에서 그 노드까지의 간선 수 (루트=0) |
> | 높이 | height | 그 노드에서 가장 먼 잎까지의 간선 수 (잎=0) |
> | 레벨 | level | 보통 깊이+1 (루트=레벨 1) |
> | 서브트리 | subtree | 어떤 노드와 그 모든 자손이 이루는 작은 트리 |
>
> **트리의 핵심 성질**
> 1. 노드가 N개면 간선은 **정확히 N-1개**.
> 2. **사이클(cycle)이 없다** (한 번 내려가면 다시 위로 못 돌아옴).
> 3. 임의의 두 노드 사이 경로는 **유일**하다.
> 4. 어떤 노드든 자기 자신을 루트로 보면 다시 **하나의 트리(서브트리)** 다 → 그래서 **재귀**가 자연스럽다.
>
> **트리의 종류**
>
> - **이진 트리(binary tree):** 모든 노드의 자식이 **최대 2개**(왼쪽/오른쪽). 코테의 주력.
> - **완전 이진 트리(complete binary tree):** 마지막 레벨을 뺀 모든 레벨이 꽉 차 있고, 마지막 레벨은 왼쪽부터 채워짐. → **배열로 저장하기 좋다**(힙의 기반, [[day-12-heap/concept|Day 12]]).
> - **포화 이진 트리(perfect/full):** 모든 잎이 같은 깊이, 모든 내부 노드가 자식 2개.
> - **이진 탐색 트리(BST, Binary Search Tree):** **왼쪽 서브트리 < 부모 < 오른쪽 서브트리**. 정렬된 상태를 유지해 탐색·삽입·삭제가 평균 O(log n).
> - **균형 트리(balanced):** 좌우 높이 차가 항상 작게 유지됨(AVL, Red-Black). 최악에도 O(log n) 보장.

> [!gear]- 2. 동작 원리 (How It Works)
> **(1) 노드 정의** — 연결 리스트의 `next` 하나가, 트리에서는 `left`·`right` 둘로 늘어난 것뿐이다.
>
> ```python
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val
>         self.left = left
>         self.right = right
> ```
>
> **(2) 재귀의 본질 — "나 + 왼쪽 + 오른쪽"**
> 트리 문제의 표준 틀은 항상 같다. 현재 노드에서 할 일을 정하고, 왼쪽/오른쪽 **서브트리에게 똑같은 함수를 위임**한 뒤 결과를 합친다.
>
> ```python
> def solve(node):
>     if node is None:        # 1) 기저 조건(base case): 빈 트리
>         return ...          #    보통 0, None, True 등 "중립값"
>     left  = solve(node.left)    # 2) 왼쪽 서브트리 결과
>     right = solve(node.right)   # 3) 오른쪽 서브트리 결과
>     return combine(node.val, left, right)   # 4) 합치기
> ```
>
> 예) **최대 깊이**는 `1 + max(왼쪽 깊이, 오른쪽 깊이)`, **노드 개수**는 `1 + 왼쪽 개수 + 오른쪽 개수`. 틀은 똑같고 `combine`만 바뀐다.
>
> **(3) 순회(Traversal) — 트리를 "한 줄"로 펴서 방문하기**
> 노드를 방문하는 순서에 따라 4가지가 있다. (자세한 응용은 [[day-29-tree-traversal/concept|Day 29]])
>
> ```
>            [1]
>           /   \
>        [2]     [3]
>       /   \
>     [4]   [5]
> ```
>
> | 순회 | 방문 순서 규칙 | 위 트리 결과 |
> |---|---|---|
> | **전위(preorder)** | **부모** → 왼쪽 → 오른쪽 | 1 2 4 5 3 |
> | **중위(inorder)** | 왼쪽 → **부모** → 오른쪽 | 4 2 5 1 3 |
> | **후위(postorder)** | 왼쪽 → 오른쪽 → **부모** | 4 5 2 3 1 |
> | **레벨(level-order)** | 위→아래, 같은 레벨은 왼→오 (BFS) | 1 2 3 4 5 |
>
> > **암기 포인트:** "전/중/후"는 **부모를 언제 방문하느냐**다(앞·가운데·뒤). **BST를 중위 순회하면 값이 오름차순으로 정렬**되어 나온다 — 매우 자주 쓰는 성질.
>
> 재귀 전위 순회:
> ```python
> def preorder(node, out):
>     if not node:
>         return
>     out.append(node.val)   # 부모 먼저
>     preorder(node.left, out)
>     preorder(node.right, out)
> ```
>
> **(4) DFS vs BFS로 보는 순회**
> - **DFS(깊이 우선):** 한 가지를 끝까지 내려간 뒤 되돌아옴. **재귀** 또는 **스택**([[day-07-stack/concept|Day 07]])으로 구현. 전/중/후위가 모두 DFS.
> - **BFS(너비 우선):** 레벨 단위로 가까운 것부터. **큐**([[day-08-queue-deque/concept|Day 08]])로 구현. 레벨 순회가 BFS.
>
> ```python
> from collections import deque
> def level_order(root):
>     if not root:
>         return []
>     out, q = [], deque([root])
>     while q:
>         node = q.popleft()
>         out.append(node.val)
>         if node.left:  q.append(node.left)
>         if node.right: q.append(node.right)
>     return out
> ```
>
> **(5) 완전 이진 트리의 배열 표현**
> 노드를 레벨 순서대로 배열에 넣으면 포인터 없이 인덱스 계산만으로 부모-자식을 오갈 수 있다. 힙([[day-12-heap/concept|Day 12]])이 이 방식을 쓴다.
> - 0-기반: 노드 `i`의 왼쪽 자식 `2i+1`, 오른쪽 자식 `2i+2`, 부모 `(i-1)//2`.
> - 1-기반: 왼쪽 `2i`, 오른쪽 `2i+1`, 부모 `i//2`.

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> **일반 이진 트리 (노드 N개, 높이 h)**
>
> | 연산 | 시간복잡도 | 설명 |
> |---|---|---|
> | 순회(전·중·후·레벨) | O(N) | 모든 노드를 한 번씩 방문 |
> | 높이/깊이 계산 | O(N) | 모든 노드 재귀 방문 |
> | 특정 값 탐색(일반 트리) | O(N) | 정렬 규칙이 없으면 전부 확인 |
> | 재귀 호출 스택(공간) | O(h) | h는 높이. 치우치면 O(N), 균형이면 O(log N) |
>
> **이진 탐색 트리 (BST)**
>
> | 연산 | 평균 | 최악(편향 트리) | 설명 |
> |---|---|---|---|
> | 탐색(search) | **O(log N)** | O(N) | 매 단계 절반씩 버림 |
> | 삽입(insert) | **O(log N)** | O(N) | 내려갈 위치를 탐색 후 연결 |
> | 삭제(delete) | **O(log N)** | O(N) | 후속자(successor)로 대체 |
>
> > **핵심:** BST의 O(log N)은 **트리가 균형 잡혀 있을 때만** 성립한다. 정렬된 데이터를 그냥 순서대로 삽입하면 한쪽으로 쭉 늘어진 **편향 트리(skewed tree)** 가 되어 사실상 연결 리스트(O(N))가 된다. 이 문제를 자동으로 막는 것이 AVL·Red-Black 같은 **균형 트리**다(파이썬 표준엔 없음 → 실전에선 정렬 리스트+`bisect`나 `dict`로 우회).
>
> **공간:** 어떤 트리든 노드 저장에 O(N), 재귀 깊이에 O(h) 추가.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"트리 문제 = 재귀"를 먼저 의심하라.** 빈 노드(`None`)를 기저 조건으로 두고 "왼쪽 결과 + 오른쪽 결과 + 나"로 합치는 틀에 90%가 들어맞는다. 깊이·개수·합·대칭 판정이 전부 이 한 틀.
>   - 참고: [Maximum Depth of Binary Tree (LeetCode #104)](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
>
> - **깊이(depth)와 높이(height)를 혼동하지 말 것.** 깊이는 "루트에서 나까지"(위에서 잼), 높이는 "나에서 가장 먼 잎까지"(아래에서 잼). 루트의 높이 = 트리의 높이. 면접에서 단골로 묻는 구분이다.
>   - 참고: [Tree (data structure) — Wikipedia](https://en.wikipedia.org/wiki/Tree_(data_structure))
>
> - **BST면 "중위 순회 = 정렬"을 떠올려라.** "BST에서 k번째 작은 값", "두 노드 사이 값들" 같은 문제는 중위 순회로 즉시 풀린다. 또 BST 탐색은 값 비교로 좌/우 한쪽만 내려가므로 절반씩 줄어든다.
>   - 참고: [Validate Binary Search Tree (LeetCode #98)](https://leetcode.com/problems/validate-binary-search-tree/)
>
> - **레벨별 처리(level-order)는 BFS + `for _ in range(len(q))`.** 큐에서 "현재 레벨 크기만큼" 끊어 처리하면 레벨 단위 작업(레벨 평균, 우측에서 본 모습 등)을 깔끔히 구현한다.
>   - 참고: [Binary Tree Level Order Traversal (LeetCode #102)](https://leetcode.com/problems/binary-tree-level-order-traversal/)
>
> - **그림으로 3~4개 노드만 그려 손으로 순회하라.** 전/중/후위 결과를 직접 적어보면 "부모를 언제 찍는지"가 몸에 익는다. 머릿속 추적은 반드시 헷갈린다(연결 리스트와 같은 교훈).
>   - 참고: [Binary Tree Traversals (GeeksforGeeks)](https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/)

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **기저 조건(빈 노드)을 먼저 처리하라.** `if node is None: return 중립값`을 빼먹으면 `None.left`에서 `AttributeError`가 난다. 빈 트리(root=None)와 노드 1개짜리는 항상 따로 테스트할 경계 케이스.
>
> 2. **깊은/편향 트리는 재귀 깊이 폭발.** 파이썬 기본 재귀 한계는 약 1000. 노드가 한쪽으로 쭉 늘어선 트리에서 재귀 DFS는 `RecursionError`를 낼 수 있다. 깊이가 크면 **명시적 스택(반복문)** 으로 바꾸거나 `sys.setrecursionlimit`를 올린다.
>
> 3. **BST의 O(log n)은 균형이 깨지면 O(n)이 된다.** 정렬된 입력을 순서대로 삽입하면 편향 트리가 된다. "BST는 항상 빠르다"는 착각. 균형 보장은 AVL/Red-Black의 몫이고, 파이썬 표준 라이브러리엔 균형 BST가 없다.
>
> 4. **이진 트리 ≠ 이진 탐색 트리(BST).** 이진 트리는 "자식이 최대 2개"라는 모양 제약만, BST는 거기에 "왼<부모<오른"이라는 **값 순서** 제약이 추가된 것. BST 가정을 일반 이진 트리에 쓰면 틀린다.
>
> 5. **순회 순서 정의를 정확히.** 전위=부모먼저, 중위=가운데, 후위=마지막. **후위 순회는 "자식부터 처리"** 라서 노드 삭제·서브트리 합 계산처럼 "아래를 끝낸 뒤 부모"가 필요한 일에 쓴다.
>
> 6. **트리는 사이클 없는 연결 그래프다.** 그래서 방문 체크(`visited`) 없이 순회할 수 있다(왔던 길로 안 돌아감). 단, 부모 포인터가 있거나 그래프로 표현된 트리를 순회할 땐 부모로 되돌아가지 않도록 주의.
>
> 7. **노드 수 N ↔ 간선 수 N-1.** 트리인지 판별하는 기본 조건. 간선이 N개 이상이면 사이클이 있어 트리가 아니다. (그래프 단원 [[day-28-graph/concept|Day 28]]에서 다시 등장.)
>
> 8. **DFS=스택/재귀, BFS=큐.** 트리 순회 도구의 매핑을 외워라. DFS는 재귀 또는 `list`/`deque`를 스택처럼, BFS는 `deque`를 큐(`popleft`)로 쓴다. `deque`를 큐로 쓸 때 `pop(0)`(리스트) 대신 `popleft()`를 써야 O(1)이다.

> [!example]- 예제 코드 (Examples)
> ```python
> from collections import deque
>
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val
>         self.left = left
>         self.right = right
>
> # 리스트(레벨 순서, None 포함) -> 트리 (테스트용)
> # 노드를 꺼낼 때마다 다음 두 칸을 왼쪽/오른쪽 자식으로 소비한다.
> def build(values):
>     if not values:
>         return None
>     root = TreeNode(values[0])
>     q = deque([root])
>     i, n = 1, len(values)
>     while q and i < n:
>         node = q.popleft()
>         if i < n:
>             if values[i] is not None:
>                 node.left = TreeNode(values[i]); q.append(node.left)
>             i += 1
>         if i < n:
>             if values[i] is not None:
>                 node.right = TreeNode(values[i]); q.append(node.right)
>             i += 1
>     return root
>
> # 1) 최대 깊이: 1 + max(왼, 오)
> def max_depth(node):
>     if not node:
>         return 0
>     return 1 + max(max_depth(node.left), max_depth(node.right))
>
> # 2) 노드 개수: 1 + 왼 + 오
> def count(node):
>     if not node:
>         return 0
>     return 1 + count(node.left) + count(node.right)
>
> # 3) 전/중/후위 순회 (DFS)
> def preorder(node, out):
>     if not node: return
>     out.append(node.val); preorder(node.left, out); preorder(node.right, out)
>
> def inorder(node, out):
>     if not node: return
>     inorder(node.left, out); out.append(node.val); inorder(node.right, out)
>
> def postorder(node, out):
>     if not node: return
>     postorder(node.left, out); postorder(node.right, out); out.append(node.val)
>
> # 4) 레벨 순회 (BFS) - 레벨별로 묶기
> def level_order(root):
>     if not root: return []
>     out, q = [], deque([root])
>     while q:
>         level = []
>         for _ in range(len(q)):       # 현재 레벨 크기만큼만
>             node = q.popleft()
>             level.append(node.val)
>             if node.left:  q.append(node.left)
>             if node.right: q.append(node.right)
>         out.append(level)
>     return out
>
> # 5) BST 탐색 (값 비교로 한쪽만 내려감, 평균 O(log n))
> def bst_search(root, target):
>     cur = root
>     while cur:
>         if target == cur.val:
>             return True
>         cur = cur.left if target < cur.val else cur.right
>     return False
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> | 번호 | 문제 | 출처 | 난이도 | 카테고리 |
> |---|---|---|---|---|
> | 1 | Maximum Depth of Binary Tree | [LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 🟢기초 | 재귀·깊이 |
> | 2 | Invert Binary Tree | [LeetCode #226](https://leetcode.com/problems/invert-binary-tree/) | 🟢기초 | 재귀·스왑 |
> | 3 | Same Tree | [LeetCode #100](https://leetcode.com/problems/same-tree/) | 🟢기초 | 동시 순회 |
> | 4 | Binary Tree Inorder Traversal | [LeetCode #94](https://leetcode.com/problems/binary-tree-inorder-traversal/) | 🟢기초 | 중위 순회 |
> | 5 | Symmetric Tree | [LeetCode #101](https://leetcode.com/problems/symmetric-tree/) | 🟡중급 | 대칭·미러 |
> | 6 | Balanced Binary Tree | [LeetCode #110](https://leetcode.com/problems/balanced-binary-tree/) | 🟡중급 | 높이·균형 |
> | 7 | Diameter of Binary Tree | [LeetCode #543](https://leetcode.com/problems/diameter-of-binary-tree/) | 🟡중급 | 높이·경로 |
> | 8 | Convert Sorted Array to BST | [LeetCode #108](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) | 🟡중급 | BST·분할 |
> | 9 | Lowest Common Ancestor of a BST | [LeetCode #235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 🔴심화 | BST 성질 |
> | 10 | 길 찾기 게임 | [프로그래머스 #42892](https://school.programmers.co.kr/learn/courses/30/lessons/42892) | ⚫기출 | 트리 구성·순회(카카오 2019) |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-10-linked-list/concept|Day 10 — 연결 리스트]] — 노드+포인터(`next`)를 자식 방향(`left`/`right`)으로 확장한 것이 트리
- ➡️ **다음(next):** [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — 완전 이진 트리를 배열로 구현한 대표 자료구조
- 🧭 **관련(related):**
  - [[day-10-linked-list/concept|Day 10 — 연결 리스트]] — 포인터 연결 사고의 확장(1개 → 2개 자식)
  - [[day-07-stack/concept|Day 07 — 스택]] — DFS(전·중·후위 순회)의 구현 도구
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — BFS(레벨 순회)의 구현 도구
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — 완전 이진 트리의 배열 표현
  - [[day-25-dfs/concept|Day 25 — DFS]] — 트리 DFS의 일반화(그래프)
  - [[day-26-bfs/concept|Day 26 — BFS]] — 트리 BFS의 일반화(그래프)
  - [[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]] — 순회의 심화·기출 응용
- 🗺️ **지도(MOC):** [[Phase-1 MOC]] · [[00 Algorithm MOC]]

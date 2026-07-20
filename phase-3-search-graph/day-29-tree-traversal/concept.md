---
day: 29
phase: 3-search-graph
title: 트리 순회·응용 (Tree Traversal)
category: [트리, 순회, DFS, BFS, 이진트리, BST]
difficulty: 중급
status: done
prev: "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회 (Graph Representation)]]"
next: "[[day-30-review/concept|Day 30 — 개념 집중기 종합 복습 (Final Review)]]"
related:
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회 (Graph Representation)]]"
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
  - "[[day-07-stack/concept|Day 07 — 스택]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-30-review/concept|Day 30 — 개념 집중기 종합 복습 (Final Review)]]"
sources:
  - https://leetcode.com/problems/binary-tree-inorder-traversal/
  - https://leetcode.com/problems/maximum-depth-of-binary-tree/
  - https://leetcode.com/problems/invert-binary-tree/
  - https://leetcode.com/problems/same-tree/
  - https://leetcode.com/problems/symmetric-tree/
  - https://leetcode.com/problems/binary-tree-level-order-traversal/
  - https://leetcode.com/problems/path-sum/
  - https://leetcode.com/problems/validate-binary-search-tree/
  - https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42892
  - https://docs.python.org/3/library/collections.html#collections.deque
  - https://docs.python.org/3/library/sys.html#sys.setrecursionlimit
tags: [phase/3, topic/tree, topic/traversal, topic/binary-tree, topic/bst, topic/dfs, topic/bfs]
---

# Day 29 — 트리 순회·응용 (Tree Traversal)

> [!abstract] 한눈 요약 (TL;DR)
> **트리 순회(tree traversal)** 는 트리의 모든 노드를 빠짐없이·중복 없이 한 번씩 방문하는 것이다. 어제 배운 [[day-28-graph/concept|그래프 순회(Day 28)]]가 트리에 특화된 형태로, **트리는 사이클이 없는 특수 그래프**라서 `visited` 배열 없이 **부모만 회피**하면 무한 루프가 나지 않는다. 순회는 크게 두 갈래다. **깊이 우선(DFS)** 계열의 세 순회 — **전위(preorder: 루트→왼쪽→오른쪽)**, **중위(inorder: 왼쪽→루트→오른쪽)**, **후위(postorder: 왼쪽→오른쪽→루트)** — 는 사실상 **"루트를 언제 기록하느냐"** 딱 한 줄만 다르다. **너비 우선(BFS)** 계열의 **레벨 순회(level-order)** 는 큐로 층(level)별로 훑는다. 이 네 순회는 각각 특기가 있다: **전위**는 트리 복사·직렬화, **중위**는 **BST(이진 탐색 트리)에서 정렬된 순서**를 뽑을 때, **후위**는 자식 정보를 모아 부모를 계산할 때(삭제·크기·높이·LCA), **레벨 순회**는 "각 층/최단 깊이" 문제에 쓴다. 코테에서 트리 문제의 90%는 **"어떤 순회를 고르고, 노드에서 무엇을 계산해 위/아래로 넘길까"** 로 귀결된다. **"최대 깊이 / 대칭 / 경로 합 / BST 검증 / 공통 조상"** 이 보이면 곧바로 순회를 떠올려라.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **트리(tree)는 "사이클 없이 연결된 그래프"** 다. 정점 V개면 간선은 정확히 V-1개, 임의의 두 노드 사이 경로는 유일하다. 그중 **이진 트리(binary tree)** 는 각 노드가 자식을 **최대 둘**(왼쪽·오른쪽) 갖는 트리로, 코테 트리 문제의 대부분을 차지한다. **순회(traversal)** 란 이 트리의 모든 노드를 한 번씩 "방문"(값을 읽거나 처리)하는 절차다.
>
> **일상 비유 — 회사 조직도 읽기.** CEO(루트) 아래로 임원, 팀장, 팀원이 가지처럼 뻗은 조직도가 트리다. 이 조직도를 "종이에 적어 보고"하는 방법이 여러 가지다.
> - **전위(preorder):** "나를 먼저 쓰고, 그 다음 부하 조직을 쓴다." → 상사부터 훑는 하향식 보고서(목차 출력, 트리 복사).
> - **후위(postorder):** "부하 조직을 다 정리한 뒤 마지막에 나를 쓴다." → 팀 예산을 모두 합산한 뒤 부서 총합을 내는 상향식 집계(폴더 용량 계산, 노드 삭제).
> - **중위(inorder):** 이진 트리에서만 자연스러운 "왼쪽 다 보고 → 나 → 오른쪽". **BST라면 이 순서가 곧 오름차순**이다.
> - **레벨 순회(level-order):** "직급(층)별로 한 줄씩 읽는다." → 조직을 계층별로 나열(가장 가까운 층부터).
>
> **핵심 직관 — 세 DFS 순회의 차이는 "루트를 찍는 타이밍" 하나다.** 세 순회 모두 "왼쪽 서브트리를 먼저, 오른쪽 서브트리를 나중"에 재귀한다. 다른 것은 오직 **루트 값을 언제 리스트에 넣느냐**다: 재귀 전(전위) / 두 재귀 사이(중위) / 재귀 후(후위). 이 한 줄의 위치가 순회의 성격 전체를 바꾼다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 이진 트리 노드와 세 DFS 순회 — 재귀.** 차이는 `order.append(root.val)`의 위치뿐이다.
> ```
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val, self.left, self.right = val, left, right
>
> def preorder(root):    # 루트 -> 왼 -> 오
>     if not root: return []
>     return [root.val] + preorder(root.left) + preorder(root.right)
>
> def inorder(root):     # 왼 -> 루트 -> 오   (BST면 오름차순!)
>     if not root: return []
>     return inorder(root.left) + [root.val] + inorder(root.right)
>
> def postorder(root):   # 왼 -> 오 -> 루트   (자식 먼저)
>     if not root: return []
>     return postorder(root.left) + postorder(root.right) + [root.val]
> ```
>
> **(B) 세 순회를 그림으로.** 아래 트리에서:
> ```
>         1
>        / \
>       2   3
>      / \   \
>     4   5   6
>
>  전위(pre) : 1 2 4 5 3 6     (루트를 만나자마자 기록)
>  중위(in)  : 4 2 5 1 3 6     (왼쪽을 다 본 뒤 루트, 그 다음 오른쪽)
>  후위(post): 4 5 2 6 3 1     (자식을 다 본 뒤 루트 -> 루트가 마지막)
>  레벨(bfs) : 1 2 3 4 5 6     (층별로: [1] [2 3] [4 5 6])
> ```
> **전위는 루트가 맨 앞, 후위는 루트가 맨 뒤**에 온다는 점을 기억하면 헷갈리지 않는다.
>
> **(C) 전위 순회 — 반복(명시적 스택).** 재귀 깊이 한계를 피하려면 스택으로. **오른쪽을 먼저 push**해야 왼쪽이 먼저 pop된다.
> ```
> def preorder_iter(root):
>     if not root: return []
>     order, stack = [], [root]
>     while stack:
>         node = stack.pop()
>         order.append(node.val)
>         if node.right: stack.append(node.right)   # 오른쪽 먼저!
>         if node.left:  stack.append(node.left)
>     return order
> ```
>
> **(D) 중위 순회 — 반복(스택).** 왼쪽 끝까지 내려가며 쌓고, 꺼내 기록한 뒤 오른쪽으로.
> ```
> def inorder_iter(root):
>     order, stack, cur = [], [], root
>     while cur or stack:
>         while cur:                    # 왼쪽 체인을 전부 스택에
>             stack.append(cur); cur = cur.left
>         cur = stack.pop()             # 가장 왼쪽부터 기록
>         order.append(cur.val)
>         cur = cur.right               # 오른쪽 서브트리로 전환
>     return order
> ```
>
> **(E) 레벨 순회(BFS) — 큐.** `for _ in range(len(q))`로 **현재 층 크기만큼만** 꺼내면 층이 자동으로 나뉜다.
> ```
> from collections import deque
> def level_order(root):
>     if not root: return []
>     res, q = [], deque([root])
>     while q:
>         level = []
>         for _ in range(len(q)):       # 이 층에 있는 노드 수만큼
>             node = q.popleft()
>             level.append(node.val)
>             if node.left:  q.append(node.left)
>             if node.right: q.append(node.right)
>         res.append(level)             # [[1],[2,3],[4,5,6]]
>     return res
> ```
>
> **(F) 순회를 "계산"에 얹기 — 응용의 본질.** 순회는 방문만 하는 게 아니라, 각 노드에서 값을 계산해 **부모에게 올려 보내거나(후위형)** **자식에게 내려 보낸다(전위형)**.
> ```
> def max_depth(root):                  # 후위형: 자식 깊이를 받아 +1
>     if not root: return 0
>     return 1 + max(max_depth(root.left), max_depth(root.right))
>
> def has_path_sum(root, t):            # 전위형: 남은 합을 자식에게 내려보냄
>     if not root: return False
>     if not root.left and not root.right:   # 리프에서 판정
>         return root.val == t
>     rest = t - root.val
>     return has_path_sum(root.left, rest) or has_path_sum(root.right, rest)
> ```
>
> **(G) 일반 트리(그래프 형태) 순회 — visited 대신 부모 회피.** 트리가 인접 리스트로 주어지면(간선 목록), 사이클이 없으므로 **방문한 부모만 건너뛰면** `visited` 배열이 필요 없다.
> ```
> def tree_dfs(adj, node, parent):
>     order = [node]
>     for nxt in adj[node]:
>         if nxt != parent:             # 이 한 줄이 visited를 대신한다
>             order += tree_dfs(adj, nxt, node)
>     return order
> ```
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> 모든 순회는 **각 노드를 정확히 한 번** 방문하므로 시간은 **O(N)**(N=노드 수)이다. 공간은 "무엇을 쌓느냐"에 따라 갈린다 — 재귀/스택은 **트리의 높이 H**, 레벨 순회 큐는 **가장 넓은 층의 폭 W** 에 비례한다.
>
> | 순회 | 시간 | 공간(보조) | 설명 |
> |---|---|---|---|
> | 전위/중위/후위 (재귀) | O(N) | O(H) | 재귀 호출 스택 = 트리 높이 |
> | 전위/중위/후위 (반복) | O(N) | O(H) | 명시적 스택 최대 깊이 = 높이 |
> | 레벨 순회 (BFS) | O(N) | O(W) | 큐에 한 층이 통째로 들어감 |
> | 깊이·경로 합·BST 검증·LCA | O(N) | O(H) | 순회 1회로 해결 |
>
> > **높이 H의 두 얼굴.** 균형 잡힌 트리(balanced)면 H ~ log N이라 공간이 매우 작다. 하지만 **한쪽으로 치우친(skewed) 트리**(사실상 연결 리스트)면 H = N이 되어 **재귀 순회가 O(N) 스택**을 쓴다 — 노드가 수만 개면 `RecursionError`. 이때는 반복 순회(스택/큐)로 바꾸거나 `sys.setrecursionlimit()`을 올려야 한다([[day-25-dfs/concept|Day 25]] 재귀 한계 참고).
> >
> > **DFS vs BFS 공간 트레이드오프.** 넓고 얕은 트리(폭 W가 큼)에서는 BFS 큐가 O(W)로 커지고 DFS 스택 O(H)가 작다. 깊고 좁은 트리에서는 반대. **"가장 가까운/최소 깊이"** 를 찾을 땐 BFS가 답을 조기에 만나 유리하고([[day-26-bfs/concept|Day 26]]), 전체를 훑거나 부모-자식 계산이 필요하면 DFS가 간결하다.
> >
> > **왜 O(N)이 최선인가.** 모든 노드를 최소 한 번은 봐야 답을 낼 수 있으니 O(N)보다 빠를 수 없다. 순회는 이 하한을 정확히 달성하는 최적 절차다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **세 순회 암기법: "루트 위치 = pre/in/post".** Pre(전, 앞)=루트 먼저, In(중, 사이)=루트 가운데, Post(후, 뒤)=루트 마지막. 영어 접두사가 곧 루트를 찍는 순서다. **전위 결과의 첫 원소는 항상 루트, 후위 결과의 마지막 원소는 항상 루트.**
>   - 참고: [LeetCode Binary Tree Inorder Traversal](https://leetcode.com/problems/binary-tree-inorder-traversal/)
> - **BST + "정렬" 냄새가 나면 무조건 중위 순회.** BST의 중위 순회는 오름차순이다. "k번째 작은 값", "BST가 유효한가", "두 노드 값의 차 최소" 같은 문제는 중위 순회 한 줄로 정렬 배열을 얻어 푼다.
> - **"부모가 자식 정보를 필요로 하면" 후위 순회.** 서브트리 크기·높이·합·최대 경로·LCA는 전부 "자식 먼저 계산 후 부모"라서 후위형 재귀(`return`으로 값 올려보내기)가 자연스럽다.
> - **"층/깊이/가장 가까운"이면 레벨 순회(BFS).** 최소 깊이, 각 층의 최댓값, 우측면도, 지그재그는 모두 `for _ in range(len(q))` 층 분리 골격의 변형이다.
> - **트리엔 visited가 필요 없다(부모만 피하면 됨).** 사이클이 없기 때문. 다만 트리가 **무방향 인접 리스트**로 오면 자식→부모 역방향 간선이 있으니 `parent`를 넘겨 되돌아가지 않게 한다. 이게 [[day-28-graph/concept|그래프]]와 트리의 실전 차이.
> - **깊은/치우친 트리는 반복 순회로.** 파이썬 기본 재귀 한도는 1000. 스큐 트리에서 재귀 순회는 터진다. `sys.setrecursionlimit(10**6)`으로 올리거나 스택 기반 반복으로 바꿔라.
>   - 참고: [sys.setrecursionlimit (Python 공식 문서)](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit)

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **트리 = 사이클 없는 연결 그래프(V-1 간선).** 이 정의에서 순회의 모든 성질이 나온다. 두 노드 사이 경로는 유일하고, 순회에 `visited`가 불필요하며(부모만 회피), 어떤 노드에서 시작해도 전체를 훑을 수 있다. [[day-11-tree-basics/concept|Day 11 트리 기본]]과 [[day-28-graph/concept|Day 28 그래프]]를 이 한 줄로 잇는다.
> 2. **세 DFS 순회의 차이는 "루트 기록 시점" 한 줄뿐.** 코드를 통째로 외우지 말고 `append(root)`의 위치(재귀 전/중간/후)만 기억하라. 세 순회를 자유자재로 변환할 수 있어야 한다.
> 3. **중위 순회 = BST의 오름차순.** 이것이 BST 문제의 만능열쇠다. 반대로 "중위가 정렬돼 있지 않다"는 BST 위반의 정의다. 단, **중복 값 처리**(<= vs <)를 문제 조건에 맞춰야 한다.
> 4. **레벨 순회는 "층 크기 고정" 후 꺼내라.** 루프 안에서 큐에 새 노드를 넣기 전에 `size = len(q)`를 먼저 잡아야 층이 정확히 나뉜다. 잡지 않고 `while q`만 돌면 층 구분이 사라진다.
> 5. **리프(leaf)의 정의는 "자식이 둘 다 없음".** 경로 합·최소 깊이에서 한쪽 자식만 없는 노드를 리프로 착각하면 오답. `if not node.left and not node.right`로 정확히 판정하라.
> 6. **재귀 깊이 한계는 트리 높이에 걸린다.** 균형 트리(H~logN)는 안전하지만 치우친 트리(H=N)는 `RecursionError`. 노드 수가 수만이면 반복 순회 또는 `setrecursionlimit`이 필수다. (오늘의 [[#^gilchatgi|길 찾기 게임]] 기출이 정확히 이 함정.)
> 7. **BST 검증은 "부모와만" 비교하면 틀린다.** 각 노드는 **모든 조상**이 만든 `(low, high)` 구간을 만족해야 한다. 부모만 보면 `[5,1,4,null,null,3,6]`의 3을 놓친다. 경계 전파 재귀 또는 중위 단조증가로 풀어라.
> 8. **후위 순회 LCA는 "양쪽에서 하나씩 찾으면 갈림점".** 좌·우 재귀가 둘 다 non-None을 반환하면 현재 노드가 최소 공통 조상. 한쪽만 있으면 그것을 위로 전달. 이 패턴은 트리의 대표 난이도 문제다.
> 9. **레벨 순서 리스트(직렬화)에서 트리 복원 시 None 자리를 지켜라.** `[1,None,2,3]` 같은 입력은 None을 "자식 없음"으로 소비해야 구조가 맞다. 인덱스 규칙(부모 i의 자식 2i+1, 2i+2)은 **완전 트리에서만** 성립하니 일반 트리엔 큐 기반 복원을 써라.
>   - 참고: [collections.deque (Python 공식 문서)](https://docs.python.org/3/library/collections.html#collections.deque)

> [!example]- 예제 코드 (Examples)
> ```python
> from collections import deque
>
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val, self.left, self.right = val, left, right
>
> # 세 DFS 순회 - 차이는 append(root) 위치 한 줄
> def preorder(root):
>     if not root: return []
>     return [root.val] + preorder(root.left) + preorder(root.right)
>
> def inorder(root):
>     if not root: return []
>     return inorder(root.left) + [root.val] + inorder(root.right)
>
> def postorder(root):
>     if not root: return []
>     return postorder(root.left) + postorder(root.right) + [root.val]
>
> # 중위 순회 - 반복(스택): 재귀 깊이 한계 회피
> def inorder_iter(root):
>     order, stack, cur = [], [], root
>     while cur or stack:
>         while cur:
>             stack.append(cur); cur = cur.left
>         cur = stack.pop()
>         order.append(cur.val)
>         cur = cur.right
>     return order
>
> # 레벨 순회(BFS) - 층별로 묶기
> def level_order(root):
>     if not root: return []
>     res, q = [], deque([root])
>     while q:
>         level = []
>         for _ in range(len(q)):
>             node = q.popleft()
>             level.append(node.val)
>             if node.left:  q.append(node.left)
>             if node.right: q.append(node.right)
>         res.append(level)
>     return res
>
> # 응용: 최대 깊이(후위형) / 경로 합(전위형)
> def max_depth(root):
>     if not root: return 0
>     return 1 + max(max_depth(root.left), max_depth(root.right))
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 세 DFS 순회와 레벨 순회를 익히고, 순회를 얹은 응용(깊이·대칭·경로 합·BST 검증·LCA·트리 재구성)까지 기초→기출로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Binary Tree Inorder Traversal | [LeetCode #94](https://leetcode.com/problems/binary-tree-inorder-traversal/) | 🟢기초 | 중위 순회 |
> | 2 | Maximum Depth of Binary Tree | [LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 🟢기초 | 깊이 DFS/BFS |
> | 3 | Invert Binary Tree | [LeetCode #226](https://leetcode.com/problems/invert-binary-tree/) | 🟢기초 | 좌우 교환 |
> | 4 | Same Tree | [LeetCode #100](https://leetcode.com/problems/same-tree/) | 🟢기초 | 동시 순회 |
> | 5 | Symmetric Tree | [LeetCode #101](https://leetcode.com/problems/symmetric-tree/) | 🟡중급 | 거울 대칭 |
> | 6 | Binary Tree Level Order Traversal | [LeetCode #102](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 🟡중급 | 레벨 순회 |
> | 7 | Path Sum | [LeetCode #112](https://leetcode.com/problems/path-sum/) | 🟡중급 | 경로 합 |
> | 8 | Validate Binary Search Tree | [LeetCode #98](https://leetcode.com/problems/validate-binary-search-tree/) | 🟡중급 | BST 검증 |
> | 9 | Lowest Common Ancestor | [LeetCode #236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | 🔴심화 | 후위 LCA |
> | 10 | 길 찾기 게임 ^gilchatgi | [프로그래머스 #42892](https://school.programmers.co.kr/learn/courses/30/lessons/42892) | ⚫기출 | 트리 재구성 + 전위·후위 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근(재귀 vs 반복, DFS vs BFS, 중위 순회 vs 경계 전파)과 복잡도 비교, 그리고 기출 "길 찾기 게임"의 트리 재구성 + 반복 순회 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-28-graph/concept|Day 28 — 그래프 표현과 순회 (Graph Representation)]] — 사이클 있는 일반 그래프를 `visited`로 순회했다면, 오늘은 사이클 없는 특수 그래프(트리)를 부모 회피로 순회하고 전위/중위/후위로 특화한다
- ➡️ **다음(next):** [[day-30-review/concept|Day 30 — 개념 집중기 종합 복습 (Final Review)]] — 완전탐색·DFS·BFS·백트래킹·그래프·트리 순회를 한자리에서 통합 정리하며 개념 집중기를 마무리한다
- 🧭 **관련(related):**
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 트리 노드·용어(루트·리프·높이·서브트리)의 기초. 오늘은 그 위를 "어떻게 훑을까"로 확장한다
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회 (Graph Representation)]] — 트리는 그래프의 특수 사례. `visited`를 부모 회피로 대신할 수 있는 이유를 사이클 개념으로 이해
  - [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — 전위·중위·후위는 모두 DFS. 재귀 깊이 한계·스택 변환이 그대로 적용된다
  - [[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]] — 레벨 순회가 곧 트리 위의 BFS. "층 크기 고정" 골격을 공유한다
  - [[day-07-stack/concept|Day 07 — 스택]] — 반복 순회(전위·중위·후위)의 엔진. 재귀 호출 스택을 명시적 스택으로 바꾸는 원리
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — 힙은 배열로 구현한 완전 이진 트리. 부모/자식 인덱스 규칙이 오늘의 트리 구조와 이어진다
  - [[day-30-review/concept|Day 30 — 개념 집중기 종합 복습 (Final Review)]] — 트리 순회를 포함한 Phase 3 전체를 복습·통합
- 🗺️ **지도(MOC):** [[Phase-3 MOC]] · [[00 Algorithm MOC]]

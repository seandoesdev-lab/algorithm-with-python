---
day: 6
phase: 1-data-structures
title: 배열과 동적 리스트 (Array & List)
category: [자료구조]
difficulty: 기초
status: done
prev: "[[day-05-math/concept|Day 05 — 수학·진법·비트 기초]]"
next: "[[day-07-stack/concept|Day 07 — 스택]]"
related:
  - "[[day-02-collections/concept|Day 02 — 자료형과 컬렉션]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/lessons/120817
  - https://leetcode.com/problems/running-sum-of-1d-array/
  - https://school.programmers.co.kr/learn/courses/30/lessons/120844
  - https://school.programmers.co.kr/learn/courses/30/lessons/68644
  - https://leetcode.com/problems/rotate-array/
  - https://leetcode.com/problems/product-of-array-except-self/
tags: [phase/1, topic/array]
---

# Day 06 — 배열과 동적 리스트 (Array & List)

> [!abstract] 한눈 요약 (TL;DR)
> 파이썬 `list`는 **동적 배열(dynamic array)**이다. 인덱싱은 O(1)이지만 중간 삽입/삭제는 O(n). `append`는 **초과 할당(over-allocation)** 덕분에 분할 상환 O(1). 2차원 리스트는 반드시 `[[0]*n for _ in range(m)]` 컴프리헨션으로 — `[[0]*n]*m`은 앨리어싱 버그. `pop(0)·insert(0)`는 O(n)이므로 양끝 작업에는 `deque`를 쓴다.

> [!note]- 1. 정의와 직관
> ### 배열이란 무엇인가 (What Is an Array)
>
> **배열(array)**은 같은 종류의 데이터를 **메모리에 연속(contiguous)으로 나란히** 저장한 자료구조다.
> 주소가 일렬로 붙어 있기 때문에, `시작주소 + 인덱스 * 원소크기`라는 단순 계산만으로 임의 위치를
> **상수 시간 O(1)**에 바로 읽을 수 있다(임의 접근, random access).
>
> ```
> 인덱스:   0     1     2     3     4
>         +-----+-----+-----+-----+-----+
> 값:     | 10  | 20  | 30  | 40  | 50  |
>         +-----+-----+-----+-----+-----+
> 주소:   1000  1008  1016  1024  1032   (원소 8바이트 가정)
>         arr[3] 주소 = 1000 + 3*8 = 1024  -> 계산 한 번에 접근
> ```
>
> 전통적인 배열(C의 `int arr[5]`)은 **크기가 고정(fixed-size)**이다. 한 번 잡으면 늘리거나 줄일 수 없다.
>
> ### 동적 배열과 파이썬 list (Dynamic Array)
>
> 파이썬 `list`는 고정 배열이 아니라 **동적 배열(dynamic array)**이다. 크기가 가변적이라 `append`로
> 원소를 계속 추가할 수 있다. 내부적으로는 **포인터들의 연속 배열**(C 레벨 `PyObject*` 배열)을 들고
> 있고, 꽉 차면 더 큰 메모리를 새로 잡아 내용을 옮긴다.
>
> 핵심은 **초과 할당(over-allocation)**이다. CPython은 리스트가 가득 차면 필요한 만큼만 1칸 늘리는 게
> 아니라 **여유 공간을 미리 더 크게** 잡는다(대략 1.125배 + 상수). 그래서 매번 재할당(reallocation)이
> 일어나지 않고, append 비용이 **평균적으로 O(1)**이 된다. 이를 **분할 상환 O(1)**이라 부른다.
>
> 용어 정리: 파이썬엔 진짜 "배열"도 있다. `array` 모듈(`array.array`)은 같은 타입 숫자만 담는
> 진짜 연속 배열이고, `numpy.ndarray`도 마찬가지다. 하지만 코딩 테스트에서는 거의 항상 `list`를 쓴다.
>
> ### 슬라이싱과 음수 인덱스 (Slicing & Negative Index)
>
> ```python
> a = [0, 1, 2, 3, 4, 5]
> a[1:4]      # [1, 2, 3]      (start 포함, stop 미포함)
> a[:3]       # [0, 1, 2]      (앞에서 3개)
> a[3:]       # [3, 4, 5]      (인덱스 3부터 끝까지)
> a[::2]      # [0, 2, 4]      (스텝 2)
> a[::-1]     # [5,4,3,2,1,0]  (역순 복사 - 단골 관용구)
> a[-1]       # 5              (마지막)
> a[-2]       # 4              (뒤에서 두 번째)
> a[-3:]      # [3, 4, 5]      (뒤에서 3개)
> ```
>
> 슬라이싱은 **항상 새 리스트를 만든다(복사)**. 따라서 `b = a[:]`는 a의 **얕은 복사본**이다.
> 슬라이스 대입도 가능하다: `a[1:3] = [9, 9, 9]`처럼 길이가 달라도 된다.
>
> ### 얕은 복사 vs 깊은 복사 (Shallow vs Deep Copy)
>
> ```python
> import copy
> a = [[1, 2], [3, 4]]
>
> b = a[:]              # 얕은 복사 (또는 a.copy(), list(a))
> b[0][0] = 99          # a[0][0] 도 99! (안쪽 리스트는 공유)
>
> c = copy.deepcopy(a)  # 깊은 복사: 안쪽까지 전부 새로 만듦
> c[0][0] = 0           # a 는 영향 없음
> ```
>
> `a[:]`, `list(a)`, `a.copy()`는 모두 **얕은 복사**다. 바깥 리스트만 새로 만들고 안쪽 원소는
> 참조를 공유한다. 안쪽까지 독립시키려면 `copy.deepcopy`를 써야 한다.

> [!gear]- 2. 동작 원리
> ### 분할 상환 O(1)의 직관 (Amortized Analysis)
>
> append가 "평균 O(1)"인데 어떻게 가끔은 O(n)(재할당+복사)이 일어나는데도 평균이 상수일까?
>
> 용량을 2배씩 늘린다고 단순화하면, n개를 추가하는 동안 복사가 일어나는 총 횟수는
> `1 + 2 + 4 + ... + n ≈ 2n` 이다. 즉 **n번의 append에 든 총 비용이 O(n)**이므로, 한 번당 평균은
> `O(n)/n = O(1)`이다. 가끔 비싼 연산이 있어도 **전체를 나눠 보면(amortized) 상수**라는 뜻이다.
>
> ```
> append 13번 -> 용량이 1,2,4,8,16... 로 커지며 복사는 가끔만 발생
> [||] -> [||  ] -> [|||| ] -> ...   대부분의 append는 빈칸에 그냥 채움(O(1))
> ```
>
> ### 2차원 리스트와 함정 (2D List Pitfall)
>
> 격자(grid)·행렬(matrix)은 "리스트의 리스트"로 표현한다.
>
> ```python
> # 올바른 생성: 행마다 독립된 리스트
> grid = [[0] * cols for _ in range(rows)]
>
> # 위험한 생성 (절대 금지): 같은 안쪽 리스트를 rows번 "참조"만 복사
> bad = [[0] * cols] * rows
> bad[0][0] = 1
> # -> bad == [[1,...], [1,...], [1,...]]  모든 행이 같이 바뀐다! (aliasing)
> ```
>
> `[x] * n`은 **x를 n번 복제하는 게 아니라, 같은 객체를 가리키는 참조를 n개** 만든다. 안쪽이
> 가변 객체(리스트)면 한 곳을 바꿔도 전부 바뀌는 **앨리어싱(aliasing)** 버그가 난다. 그래서 2차원은
> **반드시 컴프리헨션**으로 만든다.
>
> 행 r, 열 c 접근은 `grid[r][c]`. 전치(transpose)는 `list(zip(*grid))`로 한 줄에 된다.
>
> ### 언제 쓰는가 (When to Use / Avoid)
>
> - 적합: 순서가 있는 데이터, 인덱스로 빠르게 접근, 맨 뒤에 쌓고 빼는 작업(스택처럼), 정렬·순회, 격자/행렬 표현, 누적 합 같은 인덱스 기반 알고리즘
> - 적합: 크기가 자주 바뀌는 시퀀스(동적 배열이라 append가 싸다)
> - 부적합: 맨 앞에서 자주 넣고 빼는 큐 작업 -> `collections.deque`
> - 부적합: "포함 여부"를 매우 자주 물어보는 경우 -> `set`/`dict`(O(1) 조회)
> - 부적합: 중간 삽입/삭제가 잦은 경우(O(n)). 자료 특성에 따라 다른 구조(힙, 트리 등) 고려
>
> ### 파이썬 관용구 (Pythonic Usage)
>
> ```python
> from itertools import accumulate
>
> # 1) 1차원 초기화
> zeros = [0] * n                       # [0, 0, ..., 0]
> squares = [i * i for i in range(n)]   # 컴프리헨션
>
> # 2) 2차원 초기화 (반드시 컴프리헨션)
> grid = [[0] * cols for _ in range(rows)]
>
> # 3) 역순
> rev = a[::-1]                         # 복사본 역순
> a.reverse()                           # 제자리 역순 (반환 None)
>
> # 4) 누적 합 (prefix sum)
> ps = list(accumulate([1, 2, 3, 4]))   # [1, 3, 6, 10]
>
> # 5) 평탄화 (2D -> 1D)
> flat = [x for row in grid for x in row]
>
> # 6) 전치 (transpose)
> t = [list(r) for r in zip(*grid)]
>
> # 7) 필터링
> evens = [x for x in a if x % 2 == 0]
>
> # 8) 인덱스와 값 동시에
> for i, v in enumerate(a):
>     ...
>
> # 9) 두 리스트 묶기
> for x, y in zip(a, b):
>     ...
>
> # 10) 안전한 얕은/깊은 복사
> shallow = a.copy()
> import copy
> deep = copy.deepcopy(grid)
> ```

> [!chart]- 3. 복잡도 (시간/공간)
>
> | 연산 | 시간복잡도 | 비고 |
> |---|---|---|
> | `a[i]` 접근/수정 | O(1) | 임의 접근 |
> | `a.append(x)` | O(1) 분할상환 | 초과 할당 |
> | `a.pop()` (끝) | O(1) | |
> | `a.pop(0)` / `a.insert(0, x)` | **O(n)** | 앞쪽은 비쌈 -> deque 고려 |
> | `x in a` | O(n) | 멤버십 빠르게 하려면 set (Day 9) |
> | `a[i:j]` 슬라이싱 | O(k) | k=구간 길이, 새 리스트 |
> | `a.sort()` / `sorted(a)` | O(n log n) | Timsort, 안정 정렬 |
> | `a + b` / `a.extend(b)` | O(len(b)) | |
> | `a.reverse()` / `a[::-1]` | O(n) | 후자는 복사본 |
> | `len(a)` | O(1) | |

> [!tip]- 💡 이해를 돕는 팁
> - **append는 O(1), insert(0)·pop(0)은 O(n)**: 리스트의 "뒤"는 싸고 "앞"은 비싸다. 큐처럼 앞에서 빼야 하면 `collections.deque`를 쓰자(양끝 O(1)).
>   - 참고: [Python TimeComplexity (공식 위키)](https://wiki.python.org/moin/TimeComplexity)
>
> - **`[[0]*n]*m` 금지**: 2차원 리스트는 컴프리헨션 `[[0]*n for _ in range(m)]`으로. `*` 곱은 안쪽 리스트의 참조를 복제해 앨리어싱 버그를 낸다. 코테에서 "왜 다 같이 바뀌지?" 1순위 원인.
>   - 참고: [2차원 리스트 초기화 함정 (위키독스)](https://wikidocs.net/7290)
>
> - **초과 할당(over-allocation)**: CPython 리스트는 가득 차면 약 1.125배 + 상수만큼 미리 더 잡아 재할당을 줄인다. 그래서 append가 분할 상환 O(1)이다.
>   - 참고: [Python list 구현 내부 (Laurent Luce)](https://www.laurentluce.com/posts/python-list-implementation/)
>
> - **슬라이싱은 복사**: `a[:]`는 얕은 복사본을 만든다. 큰 리스트를 자주 슬라이싱하면 O(k) 비용과 메모리를 쓴다는 걸 기억하자. 인덱스 범위만 필요하면 슬라이스 대신 인덱스를 직접 다루는 게 빠르다.
>   - 참고: [정수 배열 / 슬라이싱 (점프 투 파이썬)](https://wikidocs.net/14)
>
> - **누적 합(prefix sum)**: 구간 합을 여러 번 물으면 `itertools.accumulate`로 누적 합을 한 번 만들어 `ps[j] - ps[i]`로 O(1) 조회한다(Day 14에서 본격적으로 다룸).
>   - 참고: [누적 합(Prefix Sum) 개념 (안경잡이개발자)](https://blog.naver.com/ndb796/221237111516)

> [!warning]- ⚠️ 개발자 필수 상식
> 1. **파이썬 `list`는 동적 배열이지 연결 리스트가 아니다**. 임의 접근 O(1), 중간 삽입/삭제 O(n). 이름은 list지만 동작은 배열(array)에 가깝다.
>
> 2. **앞에서 빼지 마라**: `pop(0)`, `insert(0, x)`는 O(n). 누적되면 O(n^2) 함정. 양끝 작업은 `deque`.
>
> 3. **2차원은 컴프리헨션으로**: `[[0]*n]*m`은 앨리어싱 버그. 반드시 `[[0]*n for _ in range(m)]`.
>
> 4. **`in` 연산은 O(n)**: 리스트 멤버십 검사는 선형. 반복적으로 "있나?"를 물으면 `set`/`dict`로 바꿔 O(1)로 만들자(Day 9).
>
> 5. **슬라이싱은 새 객체**: `b = a[:]`는 복사본. 단, 안쪽이 가변 객체면 얕은 복사라 공유된다.
>
> 6. **리스트 메서드는 대부분 제자리(in-place)에서 None 반환**: `a.sort()`, `a.reverse()`, `a.append()`는 `None`을 반환한다. `b = a.sort()`라 쓰면 b는 None! 정렬된 사본은 `sorted(a)`.
>
> 7. **리스트를 순회하며 수정하지 마라**: `for x in a: a.remove(x)`처럼 순회 중 크기를 바꾸면 원소를 건너뛰는 버그가 난다. 새 리스트를 만들거나(`[x for x in a if ...]`) 인덱스를 거꾸로 돌자.
>
> 8. **`a * 3`은 원소 반복**: `[1,2] * 3 == [1,2,1,2,1,2]`. 가변 객체를 담으면 참조가 반복됨에 주의.
>
> 9. **음수 인덱스/슬라이스**: `a[-1]`은 마지막, `a[::-1]`은 역순 복사. 경계 밖 인덱스는 `IndexError`지만, 슬라이스는 범위를 벗어나도 에러 없이 잘린다(`a[:100]` 안전).
>
> 10. **얕은 복사 vs 깊은 복사**: 중첩 리스트를 진짜로 독립시키려면 `copy.deepcopy`. `a.copy()`로는 안쪽이 공유된다.

> [!example]- 예제 코드
> ```python
> from itertools import accumulate
> import copy
>
> # 기본 초기화
> a = [10, 20, 30, 40, 50]
>
> # 슬라이싱
> a[1:4]      # [20, 30, 40]
> a[::-1]     # [50, 40, 30, 20, 10]  (역순)
>
> # 2차원 리스트 (올바른 방법)
> grid = [[0] * 3 for _ in range(3)]
> grid[0][0] = 1   # 첫 행 첫 열만 변경됨
>
> # 누적 합
> ps = list(accumulate([1, 2, 3, 4]))   # [1, 3, 6, 10]
>
> # 전치
> matrix = [[1, 2], [3, 4], [5, 6]]
> t = [list(r) for r in zip(*matrix)]   # [[1,3,5],[2,4,6]]
>
> # 깊은 복사
> original = [[1, 2], [3, 4]]
> deep = copy.deepcopy(original)
> deep[0][0] = 99   # original 영향 없음
> ```
>
> 전체 실행 예제: [examples.py](examples.py)

> [!question]- 연습문제
> | 난이도 | 문제 | 출처 | 핵심 개념 |
> |---|---|---|---|
> | 🟢 | [배열의 평균값 (120817)](https://school.programmers.co.kr/learn/courses/30/lessons/120817) | 프로그래머스 | 배열 순회, sum/len |
> | 🟢 | [Running Sum of 1d Array (LC 1480)](https://leetcode.com/problems/running-sum-of-1d-array/) | LeetCode Easy | 누적 합(prefix sum) |
> | 🟡 | [배열 회전시키기 (120844)](https://school.programmers.co.kr/learn/courses/30/lessons/120844) | 프로그래머스 | 슬라이싱, 회전 |
> | 🟡 | [두 개 뽑아서 더하기 (68644)](https://school.programmers.co.kr/learn/courses/30/lessons/68644) | 프로그래머스 | 조합, set 중복 제거 |
> | 🔴 | [Rotate Array (LC 189)](https://leetcode.com/problems/rotate-array/) | LeetCode Medium | 제자리 회전, 3번 뒤집기 |
> | ⚫ | [Product of Array Except Self (LC 238)](https://leetcode.com/problems/product-of-array-except-self/) | LeetCode Medium | 누적 곱 (prefix·suffix) |
>
> 전체 문제 목록 및 힌트: [problems.md](problems.md)

> [!check]- 해설
> 각 문제의 해설 및 다중 접근 방식 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ 이전: [[day-05-math/concept|Day 05 — 수학·진법·비트 기초]]
- ➡️ 다음: [[day-07-stack/concept|Day 07 — 스택]]
- 🧭 관련:
  - [[day-02-collections/concept|Day 02 — 자료형과 컬렉션]] — list 기본 동작·복잡도의 기반이 되며, 자료형 선택 기준(list vs set vs dict)을 이해하는 데 필요하다 (list 기본 동작·복잡도)
- 🗺️ 지도: [[Phase-1 MOC]] · [[00 Algorithm MOC]]

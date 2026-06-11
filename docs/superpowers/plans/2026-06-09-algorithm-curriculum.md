# 파이썬 알고리즘 학습 커리큘럼 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 파이썬 알고리즘·자료구조를 기초부터 대기업 코테 기출까지 매일 한 단계씩 학습하는 콘텐츠 시스템의 뼈대와 Day 1~3 콘텐츠를 만들고, 매일 아침 8시 자동 생성 스케줄을 등록한다.

**Architecture:** 마크다운(개념) + 파이썬(코드) 파일로 하루 = `concept.md`/`examples.py`/`problems.md`/`solutions.py` 4종 세트. `curriculum.md`가 진도의 단일 출처(single source of truth)이며, 매일 8시 스케줄 루틴이 다음 미완료 Day를 읽어 템플릿대로 콘텐츠를 생성하고 진도를 갱신한다.

**Tech Stack:** Python 3 (표준 라이브러리만), Markdown, Claude 스케줄(routine).

**참고:** 이 디렉토리는 git 저장소가 아니다. 각 Task의 검증(verification)은 파일 존재 확인 및 `.py` 실행으로 수행하고, git commit 단계는 생략한다.

---

## File Structure

| 파일 | 책임 |
|---|---|
| `README.md` | 프로젝트 소개, 학습법 안내, 전체 Day 진도 체크리스트 |
| `curriculum.md` | 전체 Day 인덱스 (Day번호·Phase·주제·경로·상태) — 진도의 단일 출처 |
| `templates/day-template/*` | 새 Day 생성용 빈 4종 템플릿 |
| `utils/io_helper.py` | 빠른 입출력 등 공용 유틸 + 사용 예시 |
| `phase-0-python-basics/day-01-fast-io/*` | Day 1 콘텐츠 (빠른 입출력) |
| `phase-0-python-basics/day-02-collections/*` | Day 2 콘텐츠 (자료형·컬렉션) |
| `phase-0-python-basics/day-03-stdlib-tools/*` | Day 3 콘텐츠 (컴프리헨션·표준 라이브러리) |
| `scripts/daily_prompt.md` | 매일 8시 스케줄 루틴이 실행할 프롬프트(자기완결적) |

---

## Task 1: 디렉토리 골격 + 공용 유틸

**Files:**
- Create: `utils/io_helper.py`
- Create: `.gitignore`

- [ ] **Step 1: `utils/io_helper.py` 작성**

```python
"""코딩 테스트용 빠른 입출력 및 공용 유틸리티.

사용법:
    from utils.io_helper import input, write
    n = int(input())
    write(n * 2)
출력 버퍼를 한 번에 비우려면 프로그램 끝에서 flush()를 호출한다.
"""
import sys
from typing import Iterable

# 빠른 입력(fast input): input()을 sys.stdin.readline으로 교체.
# 개행 문자가 포함되므로 .rstrip()로 제거한다.
input = lambda: sys.stdin.readline().rstrip("\n")

_out_buffer: list[str] = []


def write(value: object) -> None:
    """출력을 버퍼에 모은다(매 print의 I/O 비용을 줄이기 위함)."""
    _out_buffer.append(str(value))


def write_line(values: Iterable[object], sep: str = " ") -> None:
    """여러 값을 sep으로 join해 한 줄로 버퍼에 추가한다."""
    _out_buffer.append(sep.join(map(str, values)))


def flush() -> None:
    """버퍼에 모인 출력을 한 번에 표준 출력으로 내보낸다."""
    sys.stdout.write("\n".join(_out_buffer) + ("\n" if _out_buffer else ""))
    _out_buffer.clear()


if __name__ == "__main__":
    # 자체 검증(self-test): 표준 라이브러리만으로 동작 확인.
    write(42)
    write_line([1, 2, 3])
    flush()
```

- [ ] **Step 2: `.gitignore` 작성**

```
__pycache__/
*.pyc
.omc/
```

- [ ] **Step 3: io_helper 실행 검증**

Run: `python utils/io_helper.py`
Expected 출력:
```
42
1 2 3
```

---

## Task 2: Day 템플릿 4종

**Files:**
- Create: `templates/day-template/concept.md`
- Create: `templates/day-template/examples.py`
- Create: `templates/day-template/problems.md`
- Create: `templates/day-template/solutions.py`

- [ ] **Step 1: `templates/day-template/concept.md` 작성**

```markdown
# Day NN — <주제> (English Term)

> Phase: <phase> | 난이도: <기초/중급/심화> | 예상 학습 시간: <분>

## 1. 정의와 직관 (Definition & Intuition)

<무엇인지, 한 문단으로. 일상 비유 포함.>

## 2. 동작 원리 (How It Works)

<내부 동작을 단계별로. 그림이 필요하면 ASCII 다이어그램.>

## 3. 복잡도 (Time / Space Complexity)

| 연산 | 시간복잡도 | 설명 |
|---|---|---|
| ... | O(?) | 왜 그런지 |

## 4. 파이썬 관용구 (Pythonic Usage)

\`\`\`python
# 표준 라이브러리/문법 사용 예
\`\`\`

## 5. 💡 이해를 돕는 팁 (Tips)

<웹 서칭으로 수집한 비유·암기법·시각화. 출처 링크 포함.>

## 6. ⚠️ 개발자 필수 상식 (Must-Know)

<길어도 반드시 알아야 하는 내용. 흔한 버그·함정·면접 단골 포인트.>

## 7. 언제 쓰는가 (When to Use / Avoid)

- ✅ 적합: ...
- ❌ 부적합: ...
```

- [ ] **Step 2: `templates/day-template/examples.py` 작성**

```python
"""Day NN — <주제> 예제 코드.

각 예제는 단독 실행 가능하며, 개념을 단계별 주석으로 설명한다.
실행: python examples.py
"""


def example_1() -> None:
    """<예제 1 설명>"""
    pass


if __name__ == "__main__":
    example_1()
```

- [ ] **Step 3: `templates/day-template/problems.md` 작성**

```markdown
# Day NN 연습문제 — <주제>

> 난이도 표기: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출(대기업)

## 🟢 문제 1. <제목>
- 출처: <백준/프로그래머스/LeetCode> #<번호> — <링크>
- 카테고리: <유형>
- 요약: <문제 요약>
- 💭 힌트: <접근 힌트>

## 🟡 문제 2. <제목>
- 출처: ...
- 💭 힌트: ...

## ⚫ 문제 3. <제목> (기출)
- 출처: <기업/시험명> — <링크>
- 💭 힌트: ...
```

- [ ] **Step 4: `templates/day-template/solutions.py` 작성**

```python
"""Day NN 해설 — <주제>.

각 문제마다 접근 방식을 주석으로 먼저 설명하고,
가능하면 여러 접근(브루트포스 → 최적화)을 함께 제시한다.
"""


# ── 문제 1: <제목> ───────────────────────────────────────
# 접근 1) <설명>  | 시간복잡도: O(?)
def solve_1_approach_a():
    pass


# 접근 2) <설명, 더 빠른 방법>  | 시간복잡도: O(?)
def solve_1_approach_b():
    pass


if __name__ == "__main__":
    pass
```

- [ ] **Step 5: 템플릿 파일 존재 검증**

Run: `python -c "import os; print(all(os.path.exists(f'templates/day-template/{f}') for f in ['concept.md','examples.py','problems.md','solutions.py']))"`
Expected: `True`

---

## Task 3: curriculum.md (진도 단일 출처)

**Files:**
- Create: `curriculum.md`

- [ ] **Step 1: `curriculum.md` 작성** — 전체 Day 인덱스. Phase 0~3(개념 집중기 ~30일)은 Day 주제까지 명시, Phase 4~5는 영역만 명시(2단계에서 세부 확정).

```markdown
# 전체 커리큘럼 (Curriculum Index)

> 이 파일은 **진도의 단일 출처(single source of truth)** 입니다.
> 매일 아침 8시 스케줄 루틴이 첫 번째 `⬜ 예정` Day를 찾아 콘텐츠를 생성하고
> 상태를 `✅ 완료`로 바꿉니다.
> 상태 범례: ⬜ 예정 / 🛠 생성중 / ✅ 완료

## 1단계 — 개념 집중기 (Concept Sprint)

### Phase 0. 파이썬 코테 기초
| Day | 주제 | 경로 | 상태 |
|---|---|---|---|
| 01 | 빠른 입출력 (Fast I/O) | phase-0-python-basics/day-01-fast-io | ⬜ 예정 |
| 02 | 자료형과 컬렉션 (Types & Collections) | phase-0-python-basics/day-02-collections | ⬜ 예정 |
| 03 | 컴프리헨션·표준 라이브러리 (Comprehension & Stdlib) | phase-0-python-basics/day-03-stdlib-tools | ⬜ 예정 |
| 04 | 문자열 다루기 (String Handling) | phase-0-python-basics/day-04-strings | ⬜ 예정 |
| 05 | 수학·진법·비트 기초 (Math & Bits) | phase-0-python-basics/day-05-math | ⬜ 예정 |

### Phase 1. 자료구조 기초
| Day | 주제 | 경로 | 상태 |
|---|---|---|---|
| 06 | 배열과 동적 리스트 (Array & List) | phase-1-data-structures/day-06-array-list | ⬜ 예정 |
| 07 | 스택 (Stack) | phase-1-data-structures/day-07-stack | ⬜ 예정 |
| 08 | 큐와 덱 (Queue & Deque) | phase-1-data-structures/day-08-queue-deque | ⬜ 예정 |
| 09 | 해시: dict/set (Hashing) | phase-1-data-structures/day-09-hashing | ⬜ 예정 |
| 10 | 연결 리스트 (Linked List) | phase-1-data-structures/day-10-linked-list | ⬜ 예정 |
| 11 | 트리 기본 (Tree Basics) | phase-1-data-structures/day-11-tree-basics | ⬜ 예정 |
| 12 | 힙·우선순위 큐 (Heap & Priority Queue) | phase-1-data-structures/day-12-heap | ⬜ 예정 |
| 13 | 해시맵 응용 (Hashmap Patterns) | phase-1-data-structures/day-13-hashmap-patterns | ⬜ 예정 |
| 14 | 구간 자료구조 입문 (Prefix Sum) | phase-1-data-structures/day-14-prefix-sum | ⬜ 예정 |
| 15 | 자료구조 종합 복습 (Review) | phase-1-data-structures/day-15-review | ⬜ 예정 |

### Phase 2. 알고리즘 기초
| Day | 주제 | 경로 | 상태 |
|---|---|---|---|
| 16 | 시간복잡도와 Big-O | phase-2-core-algorithms/day-16-big-o | ⬜ 예정 |
| 17 | 정렬 (Sorting) | phase-2-core-algorithms/day-17-sorting | ⬜ 예정 |
| 18 | 이분 탐색 (Binary Search) | phase-2-core-algorithms/day-18-binary-search | ⬜ 예정 |
| 19 | 투 포인터 (Two Pointers) | phase-2-core-algorithms/day-19-two-pointers | ⬜ 예정 |
| 20 | 슬라이딩 윈도우 (Sliding Window) | phase-2-core-algorithms/day-20-sliding-window | ⬜ 예정 |
| 21 | 그리디 (Greedy) | phase-2-core-algorithms/day-21-greedy | ⬜ 예정 |
| 22 | 재귀와 분할정복 (Recursion & Divide-Conquer) | phase-2-core-algorithms/day-22-recursion | ⬜ 예정 |
| 23 | 알고리즘 기초 복습 (Review) | phase-2-core-algorithms/day-23-review | ⬜ 예정 |

### Phase 3. 탐색·그래프
| Day | 주제 | 경로 | 상태 |
|---|---|---|---|
| 24 | 완전 탐색 (Brute Force) | phase-3-search-graph/day-24-brute-force | ⬜ 예정 |
| 25 | DFS (깊이 우선 탐색) | phase-3-search-graph/day-25-dfs | ⬜ 예정 |
| 26 | BFS (너비 우선 탐색) | phase-3-search-graph/day-26-bfs | ⬜ 예정 |
| 27 | 백트래킹 (Backtracking) | phase-3-search-graph/day-27-backtracking | ⬜ 예정 |
| 28 | 그래프 표현과 순회 (Graph Representation) | phase-3-search-graph/day-28-graph | ⬜ 예정 |
| 29 | 트리 순회·응용 (Tree Traversal) | phase-3-search-graph/day-29-tree-traversal | ⬜ 예정 |
| 30 | 개념 집중기 종합 복습 (Final Review) | phase-3-search-graph/day-30-review | ⬜ 예정 |

## 2단계 — 문제 풀이기 (Problem Drilling, Day 31~)

> Day 31부터는 매일 **유형·난이도별 문제 풀이** 중심으로 진행하며,
> Phase 4 심화 개념(DP, 최단 경로, MST, 위상 정렬, Union-Find, 트라이,
> 세그먼트 트리, 비트마스킹)을 기출 문제와 섞어 도입한다.
> 이후 대기업 코테 기출(삼성 SW역량·카카오 블라인드·라인·쿠팡 등)로 지속 성장.
> 각 Day는 스케줄 루틴이 진행 시점에 주제를 확정해 이 표에 추가한다.

| Day | 주제 | 경로 | 상태 |
|---|---|---|---|
| 31 | (스케줄 루틴이 추가) | - | ⬜ 예정 |
```

- [ ] **Step 2: 존재 검증**

Run: `python -c "print(open('curriculum.md', encoding='utf-8').read().count('⬜ 예정'))"`
Expected: 31 이상의 숫자 출력 (모든 예정 Day 카운트)

---

## Task 4: README.md (소개 + 진도 체크리스트 + 학습법)

**Files:**
- Create: `README.md`

- [ ] **Step 1: `README.md` 작성**

````markdown
# 파이썬 알고리즘 with 매일 학습 (Algorithm with Python)

파이썬 알고리즘·자료구조를 **기초부터 대기업 공채 코딩테스트 기출까지** 매일 한 단계씩 학습하는 저장소입니다.

## 학습 방법

1. **1단계 개념 집중기 (Day 1~30, 약 한 달):** 자료구조·핵심 알고리즘 개념을 매우 자세하게 학습합니다.
2. **2단계 문제 풀이기 (Day 31~):** 매일 유형·난이도별 문제를 풀고, 대기업 기출로 실전 감각을 키웁니다.

매일 하나의 Day 폴더에는 4개의 파일이 있습니다.

| 파일 | 내용 |
|---|---|
| `concept.md` | 개념 설명 (한국어 + 영어 용어 병기) |
| `examples.py` | 실행 가능한 예제 코드 |
| `problems.md` | 난이도·카테고리별 연습문제 (출처 링크 포함) |
| `solutions.py` | 해설 — 여러 접근 방식을 코드로 비교 |

## 자동 생성

매일 아침 8시, Claude 스케줄 루틴이 [curriculum.md](curriculum.md)에서 다음 Day를 찾아 자동으로 콘텐츠를 생성합니다.

## 전체 로드맵

- **Phase 0** 파이썬 코테 기초 (Day 1~5)
- **Phase 1** 자료구조 기초 (Day 6~15)
- **Phase 2** 알고리즘 기초 (Day 16~23)
- **Phase 3** 탐색·그래프 (Day 24~30)
- **Phase 4** 심화 알고리즘 (Day 31~, 문제 풀이기에 통합)
- **Phase 5** 대기업 코테 실전 (지속)

전체 일자별 목록은 [curriculum.md](curriculum.md)를 참고하세요.

## 진도 체크리스트

### Phase 0. 파이썬 코테 기초
- [ ] Day 01 — 빠른 입출력 (Fast I/O)
- [ ] Day 02 — 자료형과 컬렉션 (Types & Collections)
- [ ] Day 03 — 컴프리헨션·표준 라이브러리
- [ ] Day 04 — 문자열 다루기
- [ ] Day 05 — 수학·진법·비트 기초

### Phase 1. 자료구조 기초
- [ ] Day 06 — 배열과 동적 리스트
- [ ] Day 07 — 스택
- [ ] Day 08 — 큐와 덱
- [ ] Day 09 — 해시 (dict/set)
- [ ] Day 10 — 연결 리스트
- [ ] Day 11 — 트리 기본
- [ ] Day 12 — 힙·우선순위 큐
- [ ] Day 13 — 해시맵 응용
- [ ] Day 14 — 누적 합
- [ ] Day 15 — 자료구조 종합 복습

### Phase 2. 알고리즘 기초
- [ ] Day 16 — 시간복잡도와 Big-O
- [ ] Day 17 — 정렬
- [ ] Day 18 — 이분 탐색
- [ ] Day 19 — 투 포인터
- [ ] Day 20 — 슬라이딩 윈도우
- [ ] Day 21 — 그리디
- [ ] Day 22 — 재귀와 분할정복
- [ ] Day 23 — 알고리즘 기초 복습

### Phase 3. 탐색·그래프
- [ ] Day 24 — 완전 탐색
- [ ] Day 25 — DFS
- [ ] Day 26 — BFS
- [ ] Day 27 — 백트래킹
- [ ] Day 28 — 그래프 표현과 순회
- [ ] Day 29 — 트리 순회·응용
- [ ] Day 30 — 개념 집중기 종합 복습

### 2단계 — 문제 풀이기 (Day 31~)
- 스케줄 루틴이 진행하며 추가합니다.

## 디렉토리 구조

```
.
├─ README.md
├─ curriculum.md
├─ phase-0-python-basics/ ~ phase-5-real-coding-test/
├─ templates/day-template/
├─ utils/io_helper.py
└─ scripts/daily_prompt.md
```
````

- [ ] **Step 2: 존재 검증**

Run: `python -c "print('Day 01' in open('README.md', encoding='utf-8').read())"`
Expected: `True`

---

## Task 5: Day 1 콘텐츠 — 빠른 입출력 (Fast I/O)

**Files:**
- Create: `phase-0-python-basics/day-01-fast-io/concept.md`
- Create: `phase-0-python-basics/day-01-fast-io/examples.py`
- Create: `phase-0-python-basics/day-01-fast-io/problems.md`
- Create: `phase-0-python-basics/day-01-fast-io/solutions.py`

- [ ] **Step 1: `concept.md` 작성** — 템플릿 7개 섹션을 모두 채운다. 반드시 포함할 핵심 내용:
  - 정의/직관: `input()` vs `sys.stdin.readline()`의 차이 (전자는 매 호출마다 프롬프트 처리·플러시 비용).
  - 동작 원리: 표준 입력 버퍼링, `readline()`이 개행 포함 반환 → `.rstrip()` 필요, `sys.stdin` 한 번에 읽기(`read().split()`).
  - 복잡도 표: N줄 입력 시 `input()`은 상수배 느림(상수 차이지만 10^6 줄에서 시간 초과 유발).
  - Pythonic: `input = sys.stdin.readline`, `map(int, input().split())`, `sys.stdout.write`, 출력 모아서 `'\n'.join`.
  - 💡 팁(웹 서칭): "PyPy 제출", "여러 줄 한 번에 읽기" 패턴, 출처 링크. → **WebSearch 사용**: "백준 파이썬 입력 시간초과 sys.stdin.readline" 등으로 최신 팁 2~3개 수집해 링크와 함께 기재.
  - ⚠️ 필수 상식: `readline()`의 개행 처리 함정, 공백/빈 줄 처리, EOF 처리, `int(input())` vs `input().split()`, 출력 시 `print`를 반복 호출하면 느린 이유.
  - 언제: 입력이 큰 경우(수만~수백만 줄) 필수 / 소규모면 `input()`로 충분.

- [ ] **Step 2: `examples.py` 작성** — 실행 가능한 예제 3개 이상:

```python
"""Day 01 — 빠른 입출력(Fast I/O) 예제.

실제 stdin이 없을 때도 동작을 보이기 위해 io.StringIO로 입력을 흉내낸다.
실행: python examples.py
"""
import sys
import io


def example_slow_vs_fast() -> None:
    """느린 input() vs 빠른 sys.stdin.readline() 비교 설명."""
    sample = "3\n10 20\n30 40\n50 60\n"
    sys.stdin = io.StringIO(sample)

    # 빠른 입력: readline은 개행을 포함하므로 split()이 알아서 처리.
    read = sys.stdin.readline
    n = int(read())
    pairs = [tuple(map(int, read().split())) for _ in range(n)]
    print("읽은 쌍:", pairs)


def example_read_all_at_once() -> None:
    """모든 입력을 한 번에 읽어 토큰 단위로 처리하는 패턴."""
    sample = "5\n1 2 3 4 5\n"
    data = io.StringIO(sample).read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    nums = [int(data[idx + i]) for i in range(n)]
    print("합계:", sum(nums))


def example_buffered_output() -> None:
    """출력을 모아 한 번에 내보내는 패턴 (sys.stdout.write)."""
    results = [str(i * i) for i in range(1, 6)]
    sys.stdout.write("\n".join(results) + "\n")


if __name__ == "__main__":
    example_slow_vs_fast()
    example_read_all_at_once()
    example_buffered_output()
```

- [ ] **Step 3: `problems.md` 작성** — 🟢🟡⚫ 난이도별 3문제 이상. 실제 출처·번호·링크 매핑. **WebSearch로 입출력 관련 대표 문제 확인**(예: 백준 15552 "빠른 A+B", 백준 11720, 10951 EOF 입력 등). 각 문제에 카테고리·힌트 포함.

- [ ] **Step 4: `solutions.py` 작성** — 각 문제 해설. 가능한 문제는 **여러 접근**(예: `input()` 방식 vs `sys.stdin` 방식)을 함수로 나눠 복잡도와 함께 제시. 코드는 stdin 의존이므로 상단 주석에 입력 예시를 적고, 핵심 로직 함수는 인자로 테스트 가능하게 작성.

- [ ] **Step 5: examples.py 실행 검증**

Run: `python phase-0-python-basics/day-01-fast-io/examples.py`
Expected: 에러 없이 "읽은 쌍", "합계", 제곱 값들이 출력됨.

- [ ] **Step 6: curriculum.md / README.md 진도 갱신**

`curriculum.md`의 Day 01 상태를 `⬜ 예정` → `✅ 완료`로, `README.md`의 `- [ ] Day 01` → `- [x] Day 01`로 변경.

---

## Task 6: Day 2 콘텐츠 — 자료형과 컬렉션 (Types & Collections)

**Files:**
- Create: `phase-0-python-basics/day-02-collections/{concept.md,examples.py,problems.md,solutions.py}`

- [ ] **Step 1: `concept.md` 작성** — 반드시 포함:
  - list/tuple/dict/set 각각의 정의·가변성(mutability)·해시 가능성(hashable).
  - 복잡도 표: list 인덱싱 O(1)/`in` 검색 O(n)/`append` 분할상환 O(1)/맨앞 삽입 O(n); set·dict의 `in`/삽입/삭제 평균 O(1) **(왜인지: 해시 테이블)**; 최악 O(n)(해시 충돌).
  - ⚠️ 필수 상식: 리스트 슬라이싱은 **새 리스트 복사**(O(k) 비용·메모리), 가변 기본 인자(mutable default argument) 함정, `list.insert(0, x)`가 느린 이유, 튜플 언패킹, `dict`는 삽입 순서 보존(3.7+).
  - 💡 팁(WebSearch): dict/set이 빠른 이유의 직관, "리스트로 큐 쓰지 말 것(deque 사용)" 등 — 출처 링크.
  - 언제 무엇을 쓰는가 (검색 많으면 set/dict, 순서 필요 + 인덱싱이면 list).

- [ ] **Step 2: `examples.py` 작성** — list/dict/set 동작, 슬라이싱 복사 증명(`a[:]` is 비교), 가변 기본 인자 함정 시연. 모두 `print`로 결과 확인 가능하게, `if __name__ == "__main__"`에서 호출.

- [ ] **Step 3: `problems.md` 작성** — 🟢🟡⚫ 3문제 이상. 컬렉션 활용 대표 문제(예: 백준 10815 숫자 카드=set/이분탐색, 백준 1764 듣보잡=set 교집합, 프로그래머스 해시 카테고리 문제). WebSearch로 링크·번호 확인.

- [ ] **Step 4: `solutions.py` 작성** — 여러 접근 비교(예: 숫자 카드 문제를 `set` vs 이분 탐색 두 방식으로). 핵심 로직은 인자 받는 함수로.

- [ ] **Step 5: 실행 검증**

Run: `python phase-0-python-basics/day-02-collections/examples.py`
Expected: 에러 없이 결과 출력.

- [ ] **Step 6: curriculum.md / README.md Day 02 진도 갱신** (Task 5 Step 6과 동일 방식, Day 02 대상).

---

## Task 7: Day 3 콘텐츠 — 컴프리헨션·표준 라이브러리 (Comprehension & Stdlib)

**Files:**
- Create: `phase-0-python-basics/day-03-stdlib-tools/{concept.md,examples.py,problems.md,solutions.py}`

- [ ] **Step 1: `concept.md` 작성** — 반드시 포함:
  - 리스트/딕셔너리/셋 컴프리헨션, 제너레이터 표현식(메모리 차이).
  - `collections`: `deque`(양끝 O(1)), `Counter`, `defaultdict`; `heapq`(최소 힙, 우선순위 큐); `itertools`(`permutations`/`combinations`/`product`/`accumulate`); `bisect`(이분 삽입 위치).
  - 복잡도/용도 표.
  - ⚠️ 필수 상식: `heapq`는 최소 힙뿐(최대 힙은 부호 반전), `deque`로 BFS 큐 구현, `Counter.most_common`, 컴프리헨션이 `for`+`append`보다 빠른 이유.
  - 💡 팁(WebSearch): "코테에서 자주 쓰는 파이썬 표준 라이브러리" 정리 글 1~2개 출처와 함께.

- [ ] **Step 2: `examples.py` 작성** — 각 모듈 대표 사용 예 실행 가능하게(`deque` BFS 스케치, `Counter`, `heapq` push/pop, `combinations`, `bisect_left`). `print`로 결과 확인.

- [ ] **Step 3: `problems.md` 작성** — 🟢🟡⚫ 3문제 이상. 예: 백준 2587(정렬), 프로그래머스 완전탐색(itertools), 힙 문제(백준 1927). WebSearch로 확인.

- [ ] **Step 4: `solutions.py` 작성** — 여러 접근 비교(예: 조합 문제를 `itertools.combinations` vs 직접 재귀 두 방식). 핵심 로직 함수화.

- [ ] **Step 5: 실행 검증**

Run: `python phase-0-python-basics/day-03-stdlib-tools/examples.py`
Expected: 에러 없이 결과 출력.

- [ ] **Step 6: curriculum.md / README.md Day 03 진도 갱신.**

---

## Task 8: 매일 스케줄 루틴 프롬프트 + 스케줄 등록

**Files:**
- Create: `scripts/daily_prompt.md`

- [ ] **Step 1: `scripts/daily_prompt.md` 작성** — 스케줄 루틴이 매일 실행할 자기완결적 프롬프트.

```markdown
# 매일 Day 콘텐츠 생성 루틴 프롬프트

작업 디렉토리: 이 저장소 루트.

수행 절차:
1. `curriculum.md`를 읽고 위에서부터 첫 번째 `⬜ 예정` 상태의 Day를 찾는다.
   (없으면: 2단계 문제 풀이기이므로, 직전 Day들의 주제를 보고 다음 적절한
   유형/기출 Day 주제를 정해 `curriculum.md` 2단계 표에 새 행을 추가한 뒤 그 Day를 대상으로 한다.)
2. 해당 Day의 상태를 `🛠 생성중`으로 바꾼다.
3. `templates/day-template/`의 4개 파일을 양식으로 삼아, 해당 Day 경로에
   `concept.md`, `examples.py`, `problems.md`, `solutions.py`를 생성한다.
   - 개념 집중기(Phase 0~3): concept.md의 7개 섹션을 매우 자세히 채운다.
     개발자 필수 상식은 길어도 모두 포함한다.
   - 💡 팁 섹션과 problems.md 문제 출처는 **WebSearch로 최신 정보·문제 번호·링크를 수집**해 반영한다.
   - solutions.py는 가능하면 한 문제에 여러 접근 방식을 코드로 비교한다.
4. `examples.py`를 `python`으로 실행해 에러가 없는지 확인한다.
5. 해당 Day 상태를 `✅ 완료`로, `README.md`의 체크박스를 `- [x]`로 갱신한다.
6. 무엇을 만들었는지 1~2줄로 요약 보고한다.

품질 기준: 한국어 설명 + 핵심 용어 영어 병기. 코드는 표준 라이브러리만 사용.
```

- [ ] **Step 2: 스케줄 등록** — `schedule` 스킬을 호출해 위 프롬프트를 **매일 아침 8시(Asia/Seoul)** 실행하도록 루틴을 등록한다. 루틴 프롬프트는 "이 저장소의 `scripts/daily_prompt.md` 절차를 그대로 수행하라"로 지정한다.

- [ ] **Step 3: 등록 확인** — 스케줄 목록을 조회해 매일 8시 루틴이 등록되었는지 확인하고 사용자에게 보고한다.

---

## Self-Review (작성자 확인 완료)

- **Spec 커버리지:** 2단계 구조(Task 3,4 진도 표 + Day1~3 개념 집중), 4종 파일(Task 2,5~7), 다중 해법(각 solutions.py 단계에 명시), 웹 서칭 팁(각 concept 💡 단계 + daily_prompt), 출처/난이도/카테고리 분리(각 problems 단계), 매일 8시 자동화(Task 8) 모두 대응됨.
- **Placeholder:** 템플릿 파일 내부의 `<...>`는 "빈 템플릿"이라는 의도된 산출물이며 플랜 지시가 아님. 플랜 스텝 자체에는 실제 코드/지시가 들어 있음.
- **타입/명명 일관성:** `io_helper`의 `write/write_line/flush`, curriculum 상태값 `⬜ 예정/🛠 생성중/✅ 완료`가 Task 전반에서 일관됨.

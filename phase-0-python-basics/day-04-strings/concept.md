---
day: 4
phase: 0-python-basics
title: 문자열 다루기 (String Handling)
category: [문자열]
difficulty: 기초
status: done
prev: "[[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]]"
next: "[[day-05-math/concept|Day 05 — 수학·진법·비트 기초]]"
related:
  - "[[day-02-collections/concept|Day 02 — 자료형과 컬렉션]]"
  - "[[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/lessons/12918
  - https://leetcode.com/problems/valid-palindrome/
  - https://leetcode.com/problems/valid-anagram/
  - https://school.programmers.co.kr/learn/courses/30/lessons/17682
  - https://school.programmers.co.kr/learn/courses/30/lessons/72410
tags: [phase/0, topic/string]
---

# Day 04 — 문자열 다루기 (String Handling)

> [!abstract] 한눈 요약 (TL;DR)
> 파이썬 문자열은 **불변(immutable)** 객체다. 모든 "수정" 메서드는 새 객체를 반환한다. 루프 안에서 `+=`로 누적하면 O(n²) — **리스트 버퍼 + `join`** 으로 O(n)으로 낮춘다. 슬라이싱 `s[::-1]` 로 뒤집고, `ord`/`chr` 로 ASCII 변환하고, 복잡한 패턴만 `re` 모듈을 쓴다.

> [!note]- 1. 정의와 직관
> ### 문자열은 불변(Immutable)이다
>
> 파이썬 문자열은 한 번 만들어지면 내부 문자를 **바꿀 수 없다**. 비유하자면 종이에 인쇄된 글자와 같아서,
> 한 글자만 고치려 해도 새 종이에 전체를 다시 인쇄(새 객체 생성)해야 한다.
>
> ```python
> s = "hello"
> # s[0] = "H"   # TypeError: 'str' object does not support item assignment
> s = "H" + s[1:]   # 새 문자열을 만들어 다시 바인딩 -> "Hello"
> ```
>
> ### 인덱싱과 슬라이싱 (Indexing & Slicing)
>
> ```python
> s = "algorithm"
> s[0]      # 'a'   (앞에서 0번째)
> s[-1]     # 'm'   (뒤에서 1번째)
> s[2:5]    # 'gor' (인덱스 2 이상 5 미만)
> s[:3]     # 'alg' (처음부터 3 미만)
> s[3:]     # 'orithm' (3부터 끝까지)
> s[::2]    # 'agrtm' (2칸씩 건너뛰기)
> s[::-1]   # 'mhtirogla' (문자열 뒤집기 reverse)
> ```
>
> 슬라이싱 `s[a:b:c]`는 시작 `a`, 끝 `b`(미포함), 간격 `c`다. **`s[::-1]`이 문자열을 뒤집는 가장 빠른
> 관용구**다. 슬라이싱은 항상 **새 문자열**을 만들며 길이에 비례한 O(k) 비용이 든다.
>
> ### 코딩 테스트 단골 메서드
>
> | 메서드 | 설명 | 예시 |
> |---|---|---|
> | `split(sep)` | 구분자로 분리해 리스트 반환. 인수 없으면 공백 기준 | `"a b c".split()` -> `['a','b','c']` |
> | `"sep".join(iter)` | 문자열 리스트를 구분자로 연결 | `",".join(['a','b'])` -> `'a,b'` |
> | `strip()` | 양끝 공백/지정 문자 제거 (`lstrip`/`rstrip`) | `"  hi  ".strip()` -> `'hi'` |
> | `replace(a, b)` | a를 b로 모두 치환 | `"aaa".replace("a","b")` -> `'bbb'` |
> | `find(x)` / `index(x)` | x의 첫 위치. find는 없으면 -1, index는 예외 | `"abc".find("b")` -> `1` |
> | `count(x)` | x 등장 횟수 | `"banana".count("a")` -> `3` |
> | `startswith` / `endswith` | 접두/접미 검사 (bool) | `"file.py".endswith(".py")` -> `True` |
> | `upper`/`lower`/`swapcase`/`title` | 대소문자 변환 | `"Abc".lower()` -> `'abc'` |
> | `isdigit`/`isalpha`/`isalnum` | 문자 종류 판별 (bool) | `"123".isdigit()` -> `True` |
> | `zfill(n)` | 왼쪽을 0으로 채워 길이 n | `"7".zfill(3)` -> `'007'` |
>
> ### 문자 <-> 숫자 변환 (ASCII)
>
> 문자 하나는 내부적으로 정수 코드(유니코드 코드 포인트)를 가진다. `ord`와 `chr`로 오간다.
>
> ```python
> ord('A')      # 65
> ord('a')      # 97
> ord('0')      # 48
> chr(65)       # 'A'
> chr(97 + 2)   # 'c'
> ```
>
> 알파벳 인덱스(0~25)를 구하는 관용구:
>
> ```python
> ord('c') - ord('a')   # 2  (소문자 c는 a로부터 2칸)
> ord('C') - ord('A')   # 2  (대문자도 동일 오프셋)
> ```
>
> 문자열 <-> 정수 변환은 `int()`와 `str()`을 쓰고, `int(s, base)`로 진법 변환도 된다.
>
> ```python
> int("42")        # 42
> int("ff", 16)    # 255 (16진수)
> int("1010", 2)   # 10  (2진수)
> str(255)         # '255'
> ```
>
> ### f-string과 포매팅 (Formatting)
>
> ```python
> name, score = "kim", 95
> f"{name}: {score}점"          # 'kim: 95점'
> f"{score:05d}"                 # '00095' (5자리, 0 채움)
> f"{3.14159:.2f}"               # '3.14' (소수 둘째 자리)
> f"{255:b}"                     # '11111111' (2진수)
> f"{255:x}"                     # 'ff' (16진수)
> f"{42:>6}"                     # '    42' (오른쪽 정렬 6칸)
> ```
>
> f-string(파이썬 3.6+)은 가독성과 속도 모두 좋아 코테에서 출력 포매팅에 적극 권장된다.
>
> ### 정규표현식 기초 (Regular Expression)
>
> 복잡한 문자 패턴을 다룰 때는 `re` 모듈이 강력하다.
>
> ```python
> import re
>
> re.sub(r"[^a-z0-9]", "", "He-llo_99!")   # 'ello99'  (소문자/숫자 외 제거)
> re.findall(r"\d+", "a12b345")             # ['12', '345']  (연속 숫자 묶음)
> bool(re.fullmatch(r"[a-z]+", "abc"))       # True (전체가 소문자인지)
> ```
>
> 자주 쓰는 패턴 요소:
>
> | 패턴 | 의미 |
> |---|---|
> | `\d` | 숫자 한 글자 `[0-9]` |
> | `\w` | 단어 문자 `[a-zA-Z0-9_]` |
> | `\s` | 공백류 |
> | `[^...]` | 대괄호 안 문자를 **제외**한 것 |
> | `+` / `*` | 1번 이상 / 0번 이상 반복 |
> | `.` | 임의의 한 글자 |

> [!gear]- 2. 동작 원리
> ### 불변성과 반복 누적의 차이
>
> 이 불변성 때문에 생기는 가장 중요한 함정이 **반복 문자열 누적**이다. 아래 두 코드는 결과가 같지만
> 시간복잡도가 다르다.
>
> ```python
> # (나쁨) 매 반복마다 새 문자열 생성 -> 전체 O(n^2)
> result = ""
> for ch in source:
>     result += ch          # 매번 기존 길이만큼 복사 발생
>
> # (좋음) 리스트에 모아두고 마지막에 한 번만 합침 -> 전체 O(n)
> buf = []
> for ch in source:
>     buf.append(ch)        # append는 평균 O(1)
> result = "".join(buf)     # join은 전체 길이만큼 한 번만 복사 O(n)
> ```
>
> 문자열 `a + b`는 `a`와 `b`를 모두 복사해 새 문자열을 만들므로 비용이 `len(a) + len(b)`다.
> 루프 안에서 누적하면 1+2+3+...+n = O(n^2)이 된다. 코딩 테스트에서 입력이 크면 이 차이가 시간 초과를 가른다.
>
> ### 언제 쓰는가 (When to Use / Avoid)
>
> - 적합: 회문/애너그램 판별, 토큰 파싱, 입력 전처리(공백·구분자 정리), 문자 빈도 분석, 간단한 암호화/디코딩, 문자열 패턴 검증
> - 적합: 누적이 필요하면 리스트 버퍼 + `join`, 복잡한 패턴 검증/추출이면 `re`
> - 부적합: 거대한 텍스트를 루프에서 `+=`로 이어 붙이기(반드시 `join`). 단순 치환에 과도한 정규식 사용
> - 부적합: 문자열 중간을 빈번히 수정해야 하는 알고리즘(이럴 땐 처음부터 `list`로 다루자)
>
> ### 파이썬 관용구 (Pythonic Usage)
>
> ```python
> # 1) 문자열 뒤집기
> rev = s[::-1]
>
> # 2) 회문(palindrome) 판별
> is_pal = (s == s[::-1])
>
> # 3) 공백 제거 후 단어 리스트
> words = sentence.split()
>
> # 4) 리스트를 문자열로 (성능 안전)
> text = "".join(char_list)
>
> # 5) 문자 빈도 세기
> from collections import Counter
> freq = Counter("banana")        # {'a':3, 'n':2, 'b':1}
>
> # 6) 알파벳 여부 / 숫자 여부 한 번에
> clean = [c for c in s if c.isalnum()]
>
> # 7) 대소문자 통일 후 비교
> a.lower() == b.lower()
>
> # 8) 정수 자릿수 합
> digit_sum = sum(int(d) for d in str(number))
> ```

> [!chart]- 3. 복잡도 (시간/공간)
>
> | 연산 | 시간복잡도 | 설명 |
> |---|---|---|
> | `s[i]` 인덱싱 | O(1) | 위치 직접 접근 |
> | `s[a:b]` 슬라이싱 | O(b-a) | 잘린 길이만큼 복사 |
> | `s[::-1]` 뒤집기 | O(n) | 전체 복사 |
> | `a + b` 연결 | O(len a + len b) | 두 문자열 모두 복사 |
> | 루프 내 `+=` 누적 | **O(n^2)** | 매번 전체 복사 -> 사용 금지 |
> | `"".join(list)` | O(n) | 전체 한 번만 복사 -> 권장 |
> | `x in s` 부분 검색 | O(n*m) 최악 | 부분 문자열 탐색 |
> | `s.count(x)` | O(n) | 전체 1회 스캔 |
> | `s.replace(a,b)` | O(n) | 전체 스캔 후 새 문자열 |
> | `s.split()` | O(n) | 전체 스캔 |

> [!tip]- 💡 이해를 돕는 팁
> - **불변성 핵심 비유**: 문자열을 "수정"하는 모든 메서드(`replace`, `upper`, `strip` 등)는 사실 원본을 바꾸지 않고 **새 문자열을 반환**한다. `s.upper()`만 호출하고 `s = s.upper()`로 다시 받지 않으면 아무 변화도 없다. 이는 초보자가 가장 많이 하는 실수다.
>   - 참고: [파이썬 코딩테스트 팁 — 문자열 조작 (fuzzysound)](https://fuzzysound.github.io/string-manipulation-in-python)
>
> - **`+` 대신 `join`**: 문자열을 반복해서 이어 붙일 때 `+=`는 O(n^2), 리스트 `append` 후 `join`은 O(n)이다. 입력이 수만 자 이상이면 이 차이로 시간 초과가 난다.
>   - 참고: [Python 문자열 붙이기 성능 비교 (join, +)](https://restato.github.io/posts/python-string-concat/)
>
> - **슬라이싱 뒤집기 `s[::-1]`**: `reversed(s)`나 루프보다 짧고 빠른 관용구로 기억해 두면 회문 문제를 한 줄로 푼다.
>   - 참고: [코딩테스트를 위한 Python 정리 (choiiis)](https://choiiis.github.io/python/for-coding-test/)
>
> - **ASCII 오프셋**: `ord(ch) - ord('a')`로 알파벳 위치(0~25)를 얻는 패턴은 암호화/빈도 배열 문제에서 단골이다. 대문자는 `ord('A')`, 숫자는 `ord('0')`을 기준으로 쓴다.
>
> - **정규식은 최후의 수단**: 단순 치환·분리는 메서드로, "여러 문자종류를 한 번에 거르기/패턴 추출"만 정규식으로. 카카오 "신규 아이디 추천" 문제가 정규식 연습의 대표 사례다.
>   - 참고: [신규 아이디 추천 (프로그래머스 72410)](https://school.programmers.co.kr/learn/courses/30/lessons/72410)

> [!warning]- ⚠️ 개발자 필수 상식
> 1. **문자열은 불변(immutable)** — `s[0] = 'x'`는 `TypeError`. 바꾸려면 리스트로 변환(`lst = list(s)`) 후 수정하고 `"".join(lst)`로 되돌린다.
>
> 2. **모든 "수정" 메서드는 새 객체 반환** — `s.replace(...)`, `s.strip()` 등의 반환값을 반드시 변수에 다시 받아야 한다. 원본은 절대 변하지 않는다.
>
> 3. **루프 안 `+=` 문자열 누적은 O(n^2)** — 큰 입력에서 시간 초과의 주범. 리스트에 모아 `join` 한다.
>
> 4. **`split()` vs `split(' ')`** — 인수 없는 `split()`은 연속 공백을 하나로 보고 양끝 공백을 버린다. `split(' ')`는 연속 공백마다 빈 문자열을 만든다. 의도에 맞는 쪽을 골라야 한다.
>
> 5. **`find` vs `index`** — 둘 다 첫 위치를 찾지만, 없을 때 `find`는 `-1`을 반환하고 `index`는 `ValueError`를 던진다. 존재 여부가 불확실하면 `in` 또는 `find`를 쓴다.
>
> 6. **`is...` 판별 메서드의 함정** — `"".isalpha()`처럼 **빈 문자열은 모든 is 검사에서 False**. `"3.5".isdigit()`도 점 때문에 False다. 음수/실수 판별엔 부족하므로 주의.
>
> 7. **대소문자 비교** — 사용자 입력 비교 시 `s.lower()`(또는 `casefold()`)로 통일한 뒤 비교한다. `casefold()`는 `lower()`보다 더 공격적인 정규화로 다국어에 안전하다.
>
> 8. **유니코드 한 글자 = `len` 1** — 파이썬 3의 문자열은 유니코드라 한글 `'가'`도 `len('가') == 1`이다. 바이트 수와 글자 수를 혼동하지 말 것.
>
> 9. **`str.translate`와 `maketrans`** — 여러 문자를 한 번에 매핑/삭제할 때 `replace`를 여러 번 호출하는 것보다 빠르다: `s.translate(str.maketrans("abc", "xyz"))`.

> [!example]- 예제 코드
> ```python
> csv = "kim,lee,park"
> names = csv.split(",")        # ['kim', 'lee', 'park']
> back  = "-".join(names)        # 'kim-lee-park'
>
> "  trim me  ".strip()          # 'trim me'
> "banana".replace("a", "o")     # 'bonono'
> "Hello".find("l")              # 2 (첫 번째 l)
> "Hello".find("z")              # -1 (없음)
>
> # 카이사르 암호 (글자를 n칸 미는 처리)
> def shift(ch, n):
>     base = ord('a')
>     return chr((ord(ch) - base + n) % 26 + base)
>
> shift('z', 1)   # 'a'  (모듈로 26으로 순환)
>
> # 정규표현식
> import re
> re.sub(r"[^a-z0-9]", "", "He-llo_99!")   # 'ello99'
> re.findall(r"\d+", "a12b345")             # ['12', '345']
> ```
>
> 전체 실행 예제: [examples.py](examples.py)

> [!question]- 연습문제
> | 난이도 | 문제 | 출처 | 핵심 개념 |
> |---|---|---|---|
> | 🟢 | [문자열 다루기 기본 (12918)](https://school.programmers.co.kr/learn/courses/30/lessons/12918) | 프로그래머스 Lv.1 | len, isdigit |
> | 🟢 | [Valid Palindrome (LC 125)](https://leetcode.com/problems/valid-palindrome/) | LeetCode Easy | 슬라이싱/투 포인터, isalnum |
> | 🟡 | [Valid Anagram (LC 242)](https://leetcode.com/problems/valid-anagram/) | LeetCode Easy~Med | Counter / 정렬 |
> | 🟡 | [다트 게임 (17682)](https://school.programmers.co.kr/learn/courses/30/lessons/17682) | 프로그래머스 Lv.1 (카카오) | 파싱, 정규식, 상태 처리 |
> | ⚫ | [신규 아이디 추천 (72410)](https://school.programmers.co.kr/learn/courses/30/lessons/72410) | 프로그래머스 Lv.1 (카카오) | 정규식, 단계별 치환 |
>
> 전체 문제 목록 및 힌트: [problems.md](problems.md)

> [!check]- 해설
> 각 문제의 해설 및 다중 접근 방식 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ 이전: [[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]]
- ➡️ 다음: [[day-05-math/concept|Day 05 — 수학·진법·비트 기초]]
- 🧭 관련:
  - [[day-02-collections/concept|Day 02 — 자료형과 컬렉션]] — 문자열을 다룰 때 자주 변환하는 `list`, `tuple`, `set`의 기본 동작을 알아야 `list(s)` <-> `"".join()` 패턴을 자연스럽게 쓴다 (문자열↔리스트 변환)
  - [[day-03-stdlib-tools/concept|Day 03 — 컴프리헨션·표준 라이브러리]] — 문자 빈도 분석에 쓰는 `Counter`, 컴프리헨션 기반 필터링이 문자열 처리와 직접 연결된다 (join·컴프리헨션)
- 🗺️ 지도: [[Phase-0 MOC]] · [[00 Algorithm MOC]]

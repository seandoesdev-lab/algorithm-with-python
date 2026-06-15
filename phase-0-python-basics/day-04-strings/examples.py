"""
Day 4 - 문자열 다루기 데모 (String Handling Demo)

실행 방법: python examples.py

cp949 콘솔 안전: 특수기호/이모지 미사용, 한글 및 ASCII 기호만 사용.
"""

import re
from collections import Counter


# ---------------------------------------------
# 1. 불변성(Immutable)과 누적 성능
# ---------------------------------------------
def demo_immutable():
    print("=" * 50)
    print("[1] 문자열 불변성 (Immutable)")
    print("=" * 50)

    s = "hello"
    # s[0] = "H"  -> TypeError: 문자열은 수정 불가
    new_s = "H" + s[1:]   # 새 문자열을 만들어야 한다
    print(f"원본 s: {s}")
    print(f"첫 글자만 대문자로(새 객체): {new_s}")

    # '수정' 메서드는 새 문자열을 반환할 뿐 원본을 바꾸지 않는다
    upper_result = s.upper()
    print(f"s.upper() 반환값: {upper_result}, 원본 s는 그대로: {s}")

    # 누적: 나쁜 방식(+=) vs 좋은 방식(join)
    source = "abcdef"

    bad = ""
    for ch in source:
        bad += ch          # 매번 새 문자열 복사 -> O(n^2)

    buf = []
    for ch in source:
        buf.append(ch)     # append O(1)
    good = "".join(buf)    # 한 번만 복사 O(n)

    print(f"+= 누적 결과:   {bad}")
    print(f"join 누적 결과: {good}  (둘 다 같지만 join이 O(n)으로 빠름)")
    print()


# ---------------------------------------------
# 2. 인덱싱 & 슬라이싱
# ---------------------------------------------
def demo_slicing():
    print("=" * 50)
    print("[2] 인덱싱 & 슬라이싱 (Indexing & Slicing)")
    print("=" * 50)

    s = "algorithm"
    print(f"s = {s}")
    print(f"s[0]    = {s[0]}      (앞에서 0번째)")
    print(f"s[-1]   = {s[-1]}      (뒤에서 1번째)")
    print(f"s[2:5]  = {s[2:5]}    (2 이상 5 미만)")
    print(f"s[:3]   = {s[:3]}    (처음부터 3 미만)")
    print(f"s[3:]   = {s[3:]} (3부터 끝까지)")
    print(f"s[::2]  = {s[::2]}    (2칸씩)")
    print(f"s[::-1] = {s[::-1]}  (문자열 뒤집기)")
    print()


# ---------------------------------------------
# 3. 단골 메서드 (split, join, strip, replace ...)
# ---------------------------------------------
def demo_methods():
    print("=" * 50)
    print("[3] 코딩테스트 단골 메서드")
    print("=" * 50)

    csv = "kim,lee,park"
    names = csv.split(",")
    print(f"split(','): {names}")
    print(f"join('-'):  {'-'.join(names)}")

    print(f"strip():    '{'  trim me  '.strip()}'")
    print(f"replace:    {'banana'.replace('a', 'o')}")
    print(f"find('l'):  {'Hello'.find('l')}  (첫 번째 l 위치)")
    print(f"find('z'):  {'Hello'.find('z')}  (없으면 -1)")
    print(f"count('a'): {'banana'.count('a')}")
    print(f"endswith('.py'): {'file.py'.endswith('.py')}")
    print(f"isdigit('123'):  {'123'.isdigit()}")
    print(f"zfill(3):   {'7'.zfill(3)}")

    # split() vs split(' ') 차이
    spaced = "a  b"   # 사이에 공백 2개
    print(f"'a  b'.split():    {spaced.split()}   (연속 공백 무시)")
    print(f"'a  b'.split(' '): {spaced.split(' ')} (빈 문자열 생김)")
    print()


# ---------------------------------------------
# 4. 문자 <-> 숫자 변환 (ASCII)
# ---------------------------------------------
def demo_ascii():
    print("=" * 50)
    print("[4] 문자 <-> 숫자 변환 (ord, chr, int)")
    print("=" * 50)

    print(f"ord('A') = {ord('A')}")
    print(f"ord('a') = {ord('a')}")
    print(f"chr(99)  = {chr(99)}")
    print(f"알파벳 위치 ord('c')-ord('a') = {ord('c') - ord('a')}")

    # 카이사르 암호: 글자를 n칸 미는 처리
    def shift(ch, n):
        base = ord('a')
        return chr((ord(ch) - base + n) % 26 + base)

    print(f"shift('z', 1) = {shift('z', 1)}  (모듈로 26 순환)")
    print(f"shift('a', 3) = {shift('a', 3)}")

    # 진법 변환
    print(f"int('ff', 16)   = {int('ff', 16)}")
    print(f"int('1010', 2)  = {int('1010', 2)}")
    print()


# ---------------------------------------------
# 5. f-string 포매팅
# ---------------------------------------------
def demo_format():
    print("=" * 50)
    print("[5] f-string 포매팅 (Formatting)")
    print("=" * 50)

    name, score = "kim", 95
    print(f"기본:        {name}: {score}점")
    print(f"0 채움 05d:  {score:05d}")
    print(f"소수 .2f:    {3.14159:.2f}")
    print(f"2진수 :b:    {255:b}")
    print(f"16진수 :x:   {255:x}")
    print(f"우정렬 >6:   '{42:>6}'")
    print()


# ---------------------------------------------
# 6. 회문 & 애너그램 & 빈도
# ---------------------------------------------
def demo_palindrome_anagram():
    print("=" * 50)
    print("[6] 회문(palindrome) / 애너그램 / 빈도")
    print("=" * 50)

    word = "level"
    print(f"'{word}' 회문 여부: {word == word[::-1]}")

    a, b = "listen", "silent"
    print(f"'{a}' vs '{b}' 애너그램(정렬 비교): {sorted(a) == sorted(b)}")
    print(f"'{a}' vs '{b}' 애너그램(Counter):  {Counter(a) == Counter(b)}")

    freq = Counter("banana")
    print(f"Counter('banana'): {dict(freq)}")
    print()


# ---------------------------------------------
# 7. 정규표현식 기초
# ---------------------------------------------
def demo_regex():
    print("=" * 50)
    print("[7] 정규표현식 기초 (re)")
    print("=" * 50)

    cleaned = re.sub(r"[^a-z0-9]", "", "He-llo_99!")
    print(f"sub 소문자/숫자만 남김: {cleaned}")

    nums = re.findall(r"\d+", "a12b345c6")
    print(f"findall 숫자 묶음:     {nums}")

    print(f"fullmatch 전체 소문자: {bool(re.fullmatch(r'[a-z]+', 'abc'))}")
    print(f"fullmatch 전체 소문자: {bool(re.fullmatch(r'[a-z]+', 'ab3'))}")
    print()


# ---------------------------------------------
# 메인 실행
# ---------------------------------------------
if __name__ == "__main__":
    demo_immutable()
    demo_slicing()
    demo_methods()
    demo_ascii()
    demo_format()
    demo_palindrome_anagram()
    demo_regex()
    print("모든 데모 완료!")

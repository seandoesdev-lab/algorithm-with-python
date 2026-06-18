"""Day 7 — 스택 (Stack) 예제 코드.

각 예제는 단독 실행 가능하며, 개념을 단계별 주석으로 설명한다.
실행: python examples.py
(cp949 콘솔 안전: print 문자열에는 ASCII 기호만 사용)
"""

import sys
from collections import deque


def example_1_basic_ops() -> None:
    """스택 기본 연산: push(append), pop, peek(s[-1]), isEmpty."""
    print("=== 예제 1) 기본 연산 (LIFO) ===")
    stack = []
    stack.append(10)            # push 10
    stack.append(20)            # push 20
    stack.append(30)            # push 30
    print("push 후 :", stack)    # [10, 20, 30]
    print("peek    :", stack[-1])           # 30 (제거 안 함)
    print("pop     :", stack.pop())         # 30 반환
    print("pop 후  :", stack)    # [10, 20]
    print("isEmpty :", not stack)           # False
    print("size    :", len(stack))          # 2


def example_2_empty_guard() -> None:
    """빈 스택 pop 방어: IndexError 예방."""
    print("=== 예제 2) 빈 스택 방어 ===")
    stack = []
    # 위험: 빈 스택에서 stack.pop() 하면 IndexError 발생
    safe = stack.pop() if stack else None
    print("빈 스택 안전 pop :", safe)         # None
    # 실제로 에러가 나는지 확인 (잡아서 출력)
    try:
        empty = []
        empty.pop()
    except IndexError as e:
        print("IndexError 발생 :", e)         # pop from empty list


def example_3_reverse_with_stack() -> None:
    """스택으로 문자열 뒤집기: 전부 push 후 전부 pop 하면 역순."""
    print("=== 예제 3) 스택으로 뒤집기 ===")
    text = "STACK"
    stack = list(text)         # 각 글자를 push 한 것과 동일
    out = []
    while stack:
        out.append(stack.pop())    # 맨 위부터 빼면 역순
    print("원본 :", text)            # STACK
    print("역순 :", "".join(out))    # KCATS


def example_4_paren_match() -> None:
    """괄호 매칭: 여는 괄호 push, 닫는 괄호에서 짝 확인 후 pop."""
    print("=== 예제 4) 괄호 매칭 ===")
    pairs = {")": "(", "]": "[", "}": "{"}

    def is_valid(s: str) -> bool:
        st = []
        for ch in s:
            if ch in "([{":
                st.append(ch)
            elif ch in ")]}":
                if not st or st[-1] != pairs[ch]:
                    return False        # 짝 불일치 또는 닫기만 들어옴
                st.pop()
        return not st                   # 끝에 남으면 실패

    for s in ["()[]{}", "(]", "([{}])", "(()", "{[()]}"]:
        print("is_valid(", s, ") =", is_valid(s))


def example_5_deque_as_stack() -> None:
    """deque 도 스택으로 쓸 수 있다 (양끝 O(1))."""
    print("=== 예제 5) deque 를 스택으로 ===")
    st = deque()
    st.append("a")             # push
    st.append("b")
    print("deque 스택 :", list(st))     # ['a', 'b']
    print("pop       :", st.pop())      # b (맨 뒤)
    print("pop 후    :", list(st))      # ['a']
    # 결론: 순수 스택은 list 가 직관적, deque 는 큐/덱(Day 8)에서 진가 발휘


def example_6_monotonic_stack() -> None:
    """모노토닉 스택: 각 원소의 '다음 큰 값까지 거리'를 O(n)에 계산."""
    print("=== 예제 6) 모노토닉 스택 ===")
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    ans = [0] * len(temps)
    st = []                    # 아직 더 따뜻한 날을 못 만난 인덱스들
    for i, t in enumerate(temps):
        while st and temps[st[-1]] < t:
            j = st.pop()        # i 가 j 의 '다음 큰 값'
            ans[j] = i - j      # 며칠 뒤인지
        st.append(i)
    print("온도         :", temps)
    print("며칠 뒤 따뜻 :", ans)   # [1, 1, 4, 2, 1, 1, 0, 0]


def example_7_recursion_is_a_stack() -> None:
    """재귀의 실체는 호출 스택. 깊으면 RecursionError."""
    print("=== 예제 7) 재귀 = 호출 스택 ===")
    print("현재 재귀 한계 :", sys.getrecursionlimit())   # 보통 1000 부근

    def depth(n: int) -> int:
        if n == 0:
            return 0
        return 1 + depth(n - 1)   # 호출마다 스택에 프레임 쌓임

    print("depth(100) =", depth(100))   # 100
    # depth(100000) 같이 너무 깊으면 RecursionError 가 난다 (여기선 실행 안 함)


if __name__ == "__main__":
    example_1_basic_ops()
    print()
    example_2_empty_guard()
    print()
    example_3_reverse_with_stack()
    print()
    example_4_paren_match()
    print()
    example_5_deque_as_stack()
    print()
    example_6_monotonic_stack()
    print()
    example_7_recursion_is_a_stack()
    print()
    print("=== 모든 예제 실행 완료 ===")

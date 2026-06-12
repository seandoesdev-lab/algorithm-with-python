"""Day 01 - 빠른 입출력(Fast I/O) 예제.

실제 stdin이 없을 때도 동작을 보이기 위해 io.StringIO로 입력을 흉내낸다.
실행: python examples.py
"""
import sys
import io


def example_slow_vs_fast() -> None:
    """느린 input() vs 빠른 sys.stdin.readline() 비교 설명."""
    sample = "3\n10 20\n30 40\n50 60\n"
    sys.stdin = io.StringIO(sample)
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


def example_input_reassign() -> None:
    """input = sys.stdin.readline 재정의 패턴 시연.

    코딩테스트에서 가장 널리 쓰이는 관용구다.
    파일 상단에 한 줄만 추가하면 기존 input() 호출이 모두 빨라진다.
    """
    sample = "4\n100 200\n300 400\n500 600\n700 800\n"
    sys.stdin = io.StringIO(sample)
    # ↓ 이 한 줄이 핵심 - input을 빠른 readline으로 대체
    _input = sys.stdin.readline

    n = int(_input())
    total = 0
    for _ in range(n):
        a, b = map(int, _input().split())
        total += a + b
    print("재정의 패턴 합계:", total)


def example_rstrip_trap() -> None:
    """readline()이 개행(\\n)을 포함해 반환하는 함정과 rstrip() 해결책."""
    sample = "hello\nworld\n"
    sys.stdin = io.StringIO(sample)

    raw = sys.stdin.readline()
    print("raw repr:", repr(raw))            # 'hello\n' 포함
    print("rstrip 결과:", repr(raw.rstrip())) # 'hello'
    print("int 변환 시 개행 무관:", int("42\n"))  # 42 - 파이썬이 자동 처리


if __name__ == "__main__":
    # sys.stdin 을 StringIO 로 교체하므로 각 함수마다 독립적으로 동작
    print("=" * 40)
    print("[1] example_slow_vs_fast")
    print("=" * 40)
    example_slow_vs_fast()

    print()
    print("=" * 40)
    print("[2] example_read_all_at_once")
    print("=" * 40)
    example_read_all_at_once()

    print()
    print("=" * 40)
    print("[3] example_buffered_output")
    print("=" * 40)
    example_buffered_output()

    print()
    print("=" * 40)
    print("[4] example_input_reassign")
    print("=" * 40)
    example_input_reassign()

    print()
    print("=" * 40)
    print("[5] example_rstrip_trap")
    print("=" * 40)
    example_rstrip_trap()

    # stdin 원복 (이후 테스트 환경 오염 방지)
    sys.stdin = sys.__stdin__

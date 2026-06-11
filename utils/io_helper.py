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

"""프로젝트 경로. 경로 문자열은 여기서만 쓴다.

사용법 (노트북 첫 셀):
    import sys
    from pathlib import Path
    ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "CLAUDE.md").exists())
    sys.path.insert(0, str(ROOT / "src"))
    from paths import RAW, EXT, PROC, REPORTS
"""
from pathlib import Path


def find_root(start: Path = None) -> Path:
    """CLAUDE.md가 있는 폴더를 프로젝트 ROOT로 본다."""
    start = Path(start or Path.cwd()).resolve()
    for p in [start, *start.parents]:
        if (p / "CLAUDE.md").exists():
            return p
    raise FileNotFoundError("CLAUDE.md를 못 찾음 — 프로젝트 안에서 실행해야 한다")


ROOT = find_root(Path(__file__).parent)

RAW = ROOT / "data" / "raw"            # 실습 원본 csv (수정 금지)
EXT = ROOT / "data" / "external"       # 외부에서 받은 csv
PROC = ROOT / "data" / "processed"     # 노트북이 만든 csv
REPORTS = ROOT / "reports"             # 보고서 md
SRC = ROOT / "src"                     # 공통 함수
NOTEBOOKS = ROOT / "notebooks"

# 원본 파일명 (공백·점이 들어가 있어 상수로 둔다)
BUS_BOARDING = RAW / "1.1 BUS_STATION_BOARDING_MONTH_202204.csv"
BUS_STATION = RAW / "1.1 bus_station.csv"
MOVING = RAW / "1.2 seoul_moving_month_4.csv"
PEOPLE = RAW / "1.3 seoul_people.csv"
BUSINESS = RAW / "1.4 business_type.csv"

# 외부 파일명
BUS_POS = EXT / "2022년각월1일기준_서울시버스정류소위치정보.csv"
SUBWAY = EXT / "subway_station.csv"

for _p in (RAW, EXT, PROC, REPORTS):
    _p.mkdir(parents=True, exist_ok=True)

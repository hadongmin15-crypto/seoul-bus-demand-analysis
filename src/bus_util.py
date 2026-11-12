"""버스 분석 공통 상수·함수 (여러 노트북이 같이 쓴다)."""
import re

import numpy as np

GU_ORDER = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구",
            "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구",
            "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구"]

# ARS 앞 2자리 -> 구 / 생활이동 시군구 코드 -> 구
ARS2GU = {f"{i + 1:02d}": g for i, g in enumerate(GU_ORDER)}
MOVE2GU = {f"11{(i + 1) * 10:03d}": g for i, g in enumerate(GU_ORDER)}
GU2MOVE = {v: k for k, v in MOVE2GU.items()}

FAR = ["간선", "지선", "광역"]                      # 멀리 가는 노선
FAR_WIDE = FAR + ["맞춤", "순환", "심야"]

P75 = 13482.5          # 서울 정류장 월승차 75퍼센타일 (보정 전, 고정)
P90 = 30418.0          # 90퍼센타일
D_MAIN = 300           # 의존 정류장 지하철역 제외 거리(m)


def route_type(no) -> str:
    """노선번호 패턴으로 노선 종류 분류."""
    s = str(no).strip()
    if s.upper().startswith("N"):
        return "심야"
    if re.fullmatch(r"[가-힣]+\d+(-\d+)?", s):
        return "마을"
    if s.startswith("0"):
        return "순환"
    if re.fullmatch(r"9\d{3}[AB]?", s):
        return "광역"
    if re.fullmatch(r"8\d{3}[AB]?", s):
        return "맞춤"
    if re.fullmatch(r"\d{3}[AB]?", s):
        return "간선"
    if re.fullmatch(r"[1-7]\d{3}[AB]?", s):
        return "지선"
    return "기타"


def haversine_m(lat1, lon1, lat2, lon2):
    """미터 단위 직선거리. 브로드캐스트 가능."""
    R = 6_371_000.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    a = (np.sin((p2 - p1) / 2) ** 2
         + np.cos(p1) * np.cos(p2) * np.sin(np.radians(lon2 - lon1) / 2) ** 2)
    return 2 * R * np.arcsin(np.sqrt(a))

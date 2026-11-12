"""이변량 분석 공통 함수.

규칙:
- p값 숫자는 절대 반환·출력하지 않는다. 'p<0.05' / 'p>0.05' 와 별표(*, **)만.
- 검정 전 정규성(Shapiro) 먼저 보고 방법을 고른다.
- mannwhitneyu는 "순위합 검정(W)" 으로 적는다.
"""
import numpy as np
import pandas as pd
from scipy import stats

SHAPIRO_MAX = 5000      # scipy shapiro는 n>5000에서 p가 부정확해 표본추출
SEED = 42


def ptxt(p: float) -> str:
    return "p<0.05" if p < 0.05 else "p>0.05"


def star(p: float) -> str:
    return "**" if p < 0.01 else ("*" if p < 0.05 else "")


def normal(x) -> tuple:
    """Shapiro 정규성. (정규인가, 표시문구, 사용한 n)"""
    s = pd.Series(x).dropna()
    n = len(s)
    if n < 3:
        return False, "n<3 판단불가", n
    used = s
    note = ""
    if n > SHAPIRO_MAX:
        used = s.sample(SHAPIRO_MAX, random_state=SEED)
        note = f" (n>{SHAPIRO_MAX}라 {SHAPIRO_MAX}개 표본추출)"
    if used.nunique() < 3:
        return False, "값 종류<3 판단불가", n
    p = stats.shapiro(used)[1]
    return p >= 0.05, f"{ptxt(p)}{note}", n


def corr2(x, y, xname="x", yname="y") -> dict:
    """두 변수 상관. 둘 다 정규면 Pearson, 아니면 Spearman."""
    d = pd.DataFrame({xname: x, yname: y}).dropna()
    nx, tx, _ = normal(d[xname])
    ny, ty, _ = normal(d[yname])
    if nx and ny:
        method, (coef, p) = "Pearson r", stats.pearsonr(d[xname], d[yname])
    else:
        method, (coef, p) = "Spearman rho", stats.spearmanr(d[xname], d[yname])
    return {"x": xname, "y": yname, "n": len(d), "방법": method,
            "계수": round(float(coef), 3), "p표시": ptxt(p), "별표": star(p),
            f"정규성_{xname}": tx, f"정규성_{yname}": ty,
            "유의": p < 0.05}


def group2(a, b, label_a="A", label_b="B", vname="값") -> dict:
    """두 그룹 비교. 둘 다 정규면 Levene 보고 t검정, 아니면 순위합 검정(W)."""
    sa, sb = pd.Series(a).dropna(), pd.Series(b).dropna()
    na, ta, _ = normal(sa)
    nb, tb, _ = normal(sb)

    if na and nb:
        pv_lev = stats.levene(sa, sb)[1]
        eq = pv_lev >= 0.05
        method = f"t검정({'등분산' if eq else 'Welch'})"
        stat, p = stats.ttest_ind(sa, sb, equal_var=eq)
        lev = ptxt(pv_lev)
    else:
        method = "순위합 검정(W)"
        stat, p = stats.mannwhitneyu(sa, sb, alternative="two-sided")
        lev = "-"

    return {"변수": vname, "방법": method,
            f"n_{label_a}": len(sa), f"n_{label_b}": len(sb),
            f"중앙값_{label_a}": round(float(sa.median()), 4),
            f"중앙값_{label_b}": round(float(sb.median()), 4),
            f"평균_{label_a}": round(float(sa.mean()), 4),
            f"평균_{label_b}": round(float(sb.mean()), 4),
            "p표시": ptxt(p), "별표": star(p), "유의": p < 0.05,
            f"정규성_{label_a}": ta, f"정규성_{label_b}": tb, "Levene": lev}


def groupk(groups: dict, vname="값") -> dict:
    """여러 그룹 비교. 전부 정규면 분산분석(ANOVA), 아니면 Kruskal-Wallis."""
    items = {k: pd.Series(v).dropna() for k, v in groups.items()}
    items = {k: v for k, v in items.items() if len(v) >= 3}
    flags = {k: normal(v) for k, v in items.items()}
    all_normal = all(f[0] for f in flags.values())

    if all_normal:
        method, (stat, p) = "분산분석(ANOVA)", stats.f_oneway(*items.values())
    else:
        method, (stat, p) = "Kruskal-Wallis", stats.kruskal(*items.values())

    return {"변수": vname, "방법": method, "그룹수": len(items),
            "그룹별n": {k: len(v) for k, v in items.items()},
            "그룹별정규성": {k: f[1] for k, f in flags.items()},
            "p표시": ptxt(p), "별표": star(p), "유의": p < 0.05}


def strength(coef: float) -> str:
    """관계 세기 (|계수| 기준)"""
    a = abs(coef)
    if a >= 0.5:
        return "강"
    if a >= 0.3:
        return "중"
    return "약"

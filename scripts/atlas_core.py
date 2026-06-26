from pathlib import Path
from datetime import date
import argparse

ROOT = Path(__file__).resolve().parents[1]

COMPANY_FILES = [
    "00_Summary.md",
    "01_Bear_First.md",
    "02_Business.md",
    "03_Products.md",
    "04_Industry.md",
    "05_Competitors.md",
    "06_Technology.md",
    "07_Financial.md",
    "08_Valuation.md",
    "09_Risks.md",
    "10_Tracking.md",
    "11_Investment_Thesis.md",
    "Timeline.md",
]

def write_if_missing(path: Path, content: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")

def create_company(name: str):
    company_dir = ROOT / "03_Companies" / name
    for filename in COMPANY_FILES:
        title = filename.replace("_", " ").replace(".md", "")
        write_if_missing(
            company_dir / filename,
            f"# {name} - {title}\n\n## Status\n\n待研究。\n"
        )
    print(f"Created company: {name}")

def create_industry(name: str):
    industry_dir = ROOT / "02_Industries" / name
    write_if_missing(
        industry_dir / "00_Summary.md",
        f"# {name}\n\n## 一句话定义\n\n待研究。\n\n## Bear First\n\n这个产业为什么可能不值得长期研究？\n"
    )
    write_if_missing(industry_dir / "01_Value_Chain.md", f"# {name} - Value Chain\n")
    write_if_missing(industry_dir / "02_Company_Map.md", f"# {name} - Company Map\n")
    write_if_missing(industry_dir / "03_Tracking.md", f"# {name} - Tracking\n")
    print(f"Created industry: {name}")

def create_daily():
    today = date.today().isoformat()
    path = ROOT / "06_Tactical" / "Daily_Radar" / f"Daily_Radar_{today}.md"
    write_if_missing(
        path,
        f"""# Atlas Daily Radar - {today}

## 01 今日最重要变化

## 02 产业信号

| 产业 | 事件 | 重要性 | 证据等级 | 影响 |
|---|---|---:|---|---|

## 03 公司信号

| 公司 | 事件 | 战略影响 | 战术影响 | 是否需要跟踪 |
|---|---|---|---|---|

## 04 Tactical Watch

| 标的 | 催化 | 介入逻辑 | 失效条件 | 仓位上限 |
|---|---|---|---|---|

## 05 Bear First Alert

今天有哪些信息可能推翻我们已有观点？

## 06 Action

- 需要加入 Atlas 的信息：
- 需要深入研究的问题：
- 今日不行动理由：
"""
    )
    print(f"Created daily radar: {path}")

def main():
    parser = argparse.ArgumentParser(description="Atlas Core")
    sub = parser.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("company")
    c.add_argument("name")

    i = sub.add_parser("industry")
    i.add_argument("name")

    sub.add_parser("daily")

    args = parser.parse_args()

    if args.cmd == "company":
        create_company(args.name)
    elif args.cmd == "industry":
        create_industry(args.name)
    elif args.cmd == "daily":
        create_daily()

if __name__ == "__main__":
    main()

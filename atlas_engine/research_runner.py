from pathlib import Path
from datetime import datetime
import argparse

ROOT = Path(__file__).resolve().parents[1]

ENTRY_PATHS = {
    "公司入口": "公司 → 价值节点 → 价值流 → 根本约束 → 再回到公司",
    "价值节点入口": "价值节点 → 价值流 → 根本约束 → 竞争格局 → 公司",
    "价值流入口": "价值流 → 根本约束 → 价值节点 → 公司 → 组合影响",
    "技术入口": "技术 → 根本约束 → 商业成熟 → 价值流 → 新瓶颈",
    "事件入口": "事件 → 影响层级 → Bear First → 证据分析 → 更新 Atlas",
    "未知入口": "事件 → 初步判断 → 补充信息 → 再定位入口",
}

def create_research_task(
    title: str,
    entry: str,
    trigger_reason: str,
    event_content: str = "",
    output_dir: str = "04_Research/Notes",
):
    today = datetime.now().strftime("%Y-%m-%d")
    safe_title = title.replace("/", "_").replace(" ", "_")[:40]
    path = ROOT / output_dir / f"{today}_Research_{safe_title}.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    research_path = ENTRY_PATHS.get(entry, ENTRY_PATHS["未知入口"])

    content = f"""# Research Task - {title}

> Status: Draft
> Created: {today}
> Entry: {entry}

---

# 0. Event

## 事件内容

{event_content}

## 触发原因

{trigger_reason}

---

# 1. Research Entry

本次研究入口：

**{entry}**

研究路径：

{research_path}

---

# 2. Core Question

本次研究需要回答的核心问题：

> 这个事件是否改变了 Atlas 对价值流、价值节点或公司的长期判断？

---

# 3. Layer Positioning

## 根本约束层

该事件是否影响某个人类根本约束？

结论：

证据：

## 价值流层

该事件是否影响某条价值流？

结论：

证据：

## 价值节点层

该事件是否影响某个价值节点？

结论：

证据：

## 公司层

该事件是否影响某家公司长期逻辑？

结论：

证据：

---

# 4. Bear First

## 最强反方观点

如果该事件并不重要，最可能的原因是什么？

## 可能被市场误读的地方

## 哪些事实会推翻本次研究假设？

---

# 5. Evidence

## S级证据

## A级证据

## B级证据

## C级证据

---

# 6. Preliminary Conclusion

## 当前结论

## 置信度

## 是否需要更新 Atlas

- [ ] 更新价值流
- [ ] 更新价值节点
- [ ] 更新公司研究
- [ ] 加入 Discovery
- [ ] 加入 Validation Queue
- [ ] 不更新

---

# 7. Follow-up

## 下一步跟踪指标

## 下一次验证时间

## 备注
"""
    path.write_text(content, encoding="utf-8")
    return path

def main():
    parser = argparse.ArgumentParser(description="Atlas Research Runner")
    parser.add_argument("--title", required=True)
    parser.add_argument("--entry", default="未知入口")
    parser.add_argument("--reason", default="")
    parser.add_argument("--content", default="")
    args = parser.parse_args()

    path = create_research_task(
        title=args.title,
        entry=args.entry,
        trigger_reason=args.reason,
        event_content=args.content,
    )
    print(f"Created research task: {path}")

if __name__ == "__main__":
    main()

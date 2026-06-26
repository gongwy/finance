from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import argparse
import json


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "atlas_engine" / "config" / "trigger_rules.json"

def load_rules():
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

RULES = load_rules()
KEYWORDS = RULES["keywords"]

@dataclass
class Event:
    title: str
    source: str = "manual"
    event_type: str = "unknown"
    content: str = ""
    related_companies: list[str] = None
    related_nodes: list[str] = None
    related_flows: list[str] = None

@dataclass
class TriggerResult:
    trigger_level: int
    trigger_name: str
    should_research: bool
    research_entry: str
    score: int
    reason: str
    review_required: bool
    review_note: str
    next_action: str
    output_path: str

def infer_event_type(text: str) -> str:
    for event_type, words in KEYWORDS.items():
        if any(w in text for w in words):
            return event_type
    return "unknown"

def score_event(event: Event) -> tuple[int, list[str]]:
    text = f"{event.title}\n{event.content}"
    reasons = []
    score = 0

    if event.related_flows:
        score += 2
        reasons.append("影响已知价值流")

    if event.related_nodes:
        score += 2
        reasons.append("影响已知价值节点")

    if event.related_companies:
        score += 1
        reasons.append("影响已知公司")

    event_type = event.event_type if event.event_type != "unknown" else infer_event_type(text)

    if event_type in ["technology", "policy", "risk"]:
        score += 2
        reasons.append(f"事件类型重要：{event_type}")

    if event_type in ["company", "market"]:
        score += 1
        reasons.append(f"事件类型需跟踪：{event_type}")

    if any(w in text for w in ["推翻", "重估", "重大变化", "首次", "商业化", "限制升级"]):
        score += 2
        reasons.append("可能改变既有判断")

    return score, reasons

def decide_level(score: int):

    for item in RULES["levels"]:

        if score <= item["max_score"]:

            return item

    return RULES["levels"][-1]

def decide_entry(event: Event) -> str:
    text = f"{event.title}\n{event.content}"
    event_type = event.event_type if event.event_type != "unknown" else infer_event_type(text)

    if event_type == "technology":
        return "技术入口"
    if event.related_flows:
        return "价值流入口"
    if event.related_nodes:
        return "价值节点入口"
    if event.related_companies:
        return "公司入口"
    if event_type in ["policy", "risk", "market"]:
        return "事件入口"
    return "未知入口"

def trigger(event: Event) -> TriggerResult:
    score, reasons = score_event(event)
    entry = decide_entry(event)

    level_rule = decide_level(score)
    level = level_rule["level"]
    name = level_rule["name"]
    should = level_rule["should_research"]
    action = level_rule["action"]

    today = datetime.now().strftime("%Y-%m-%d")
    safe_title = event.title.replace("/", "_").replace(" ", "_")[:40]
    output_path = f"04_Research/Notes/{today}_{safe_title}.md"

    review_required = level >= 2
    review_note = "需要人工确认事件是否真的影响价值流/价值节点" if review_required else "无需人工确认"

    return TriggerResult(
        trigger_level=level,
        trigger_name=name,
        should_research=should,
        research_entry=entry,
        score=score,
        reason="；".join(reasons) if reasons else "未发现明显价值流影响",
        review_required=review_required,
        review_note=review_note,
        next_action=action,
        output_path=output_path,
    )

def save_result(event: Event, result: TriggerResult):
    path = ROOT / result.output_path
    path.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# Trigger Result - {event.title}

## Event

- Title: {event.title}
- Source: {event.source}
- Type: {event.event_type}

## Content

{event.content}

## Trigger Decision

- Level: {result.trigger_level}
- Name: {result.trigger_name}
- Should Research: {result.should_research}
- Research Entry: {result.research_entry}
- Reason: {result.reason}
- Next Action: {result.next_action}
- Score: {result.score}
- Review Required: {result.review_required}
- Review Note: {result.review_note}

## Related

- Value Flows: {event.related_flows or []}
- Value Nodes: {event.related_nodes or []}
- Companies: {event.related_companies or []}

"""
    path.write_text(content, encoding="utf-8")
    return path

def main():
    parser = argparse.ArgumentParser(description="Atlas Trigger Machine")
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", default="")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--type", default="unknown")
    parser.add_argument("--companies", default="")
    parser.add_argument("--nodes", default="")
    parser.add_argument("--flows", default="")
    parser.add_argument("--save", action="store_true")

    args = parser.parse_args()

    event = Event(
        title=args.title,
        source=args.source,
        event_type=args.type,
        content=args.content,
        related_companies=[x for x in args.companies.split(",") if x],
        related_nodes=[x for x in args.nodes.split(",") if x],
        related_flows=[x for x in args.flows.split(",") if x],
    )

    result = trigger(event)

    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))

    if args.save:
        path = save_result(event, result)
        print(f"Saved to: {path}")

if __name__ == "__main__":
    main()

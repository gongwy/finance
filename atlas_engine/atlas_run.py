import argparse
import json
from dataclasses import asdict

from trigger_machine import Event, trigger, save_result
from research_runner import create_research_task

def main():
    parser = argparse.ArgumentParser(description="Atlas Run: Trigger + Research Task")
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", default="")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--type", default="unknown")
    parser.add_argument("--companies", default="")
    parser.add_argument("--nodes", default="")
    parser.add_argument("--flows", default="")
    parser.add_argument("--save-trigger", action="store_true")
    parser.add_argument("--create-research", action="store_true")

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

    print("=== Trigger Result ===")
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))

    if args.save_trigger:
        trigger_path = save_result(event, result)
        print(f"Trigger saved to: {trigger_path}")

    if args.create_research:
        if result.should_research:
            research_path = create_research_task(
                title=event.title,
                entry=result.research_entry,
                trigger_reason=result.reason,
                event_content=event.content,
            )
            print(f"Research task created: {research_path}")
        else:
            print("Research task not created: trigger level is below Level 3.")

if __name__ == "__main__":
    main()

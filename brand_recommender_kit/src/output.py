"""
File creates the report for brand marketing
"""
def format_report(state: dict) -> str:
    lines = []
    lines.append("BRAND MARKETING REPORT")
    lines.append("")

    lines.append("BRAND DIAGNOSIS")
    lines.append(state.get("research_brief", "(no research brief available)"))
    lines.append("")

    lines.append("RECOMMENDED STRATEGY")
    lines.append(state.get("strategy", "(no strategy available)"))
    lines.append("")
    lines.append("WHY THIS STRATEGY")
    lines.append(state.get("strategy_rationale", ""))
    lines.append("")

    critique = state.get("critique")
    if critique:
        lines.append("VALIDATION")
        lines.append(f"Approved after {state.get('revision_count', 0)} revision(s).")
        checks = {
            "Fits brand": critique.brand_alignment,
            "Evidence-supported": critique.evidence_support,
            "Commercially viable": critique.commercial_viability,
            "Differentiated": critique.differentiability,
            "Feasible": critique.feasibility,
        }
        for label, passed in checks.items():
            mark = "PASS" if passed else "FAIL"
            lines.append(f"  [{mark}] {label}")
        lines.append("")

    content_ideas = state.get("content_ideas")
    if content_ideas:
        lines.append("CONTENT IDEAS")
        for i, idea in enumerate(content_ideas.ideas, 1):
            lines.append(f"{i}. {idea.idea} ({idea.format})")
            lines.append(f"   Hook: {idea.highlight}")
            lines.append(f"   Concept: {idea.concept}")
            lines.append(f"   CTA: {idea.cta}")
            lines.append(f"   Why: {idea.purpose}")
            lines.append("")

    return "\n".join(lines)
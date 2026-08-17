"""
Brand Marketing Kit

Ties the whole pipeline together

Usage:
    python main.py --brand-url https://example.com
    python main.py --brand-url https://example.com --output report.txt
"""

import argparse

from src.graph import build_graph
from src.ingestion.brand_scraper import scrape_brand_site, search_competitors
from src.output import format_report
def main():
    parser = argparse.ArgumentParser(description="Brand Recommender KI -- marketing strategy agent")
    parser.add_argument("--brand-url", required=True, help="URL of the brand's website")
    parser.add_argument("--max-revisions", type=int, default=3, help="Max automatic revision loops")
    parser.add_argument("--output", default=None, help="Optional file path to save the report")
    args = parser.parse_args()

    print(f"Scraping {args.brand_url} ...")
    brand_site_data = scrape_brand_site(args.brand_url)
    if brand_site_data.get("error"):
        print(f"  Warning: {brand_site_data['error']}")

    print("Searching for competitors ...")
    competitor_results = search_competitors(f"{brand_site_data.get('title') or args.brand_url} competitors")

    initial_state = {
        "brand_url": args.brand_url,
        "brand_site_data": brand_site_data,
        "competitor_results": competitor_results,
        "max_revisions": args.max_revisions,
        "revision_count": 0,
        "critique_history": [],
    }

    print("Running the agent pipeline (this may take a minute)...")
    graph = build_graph()
    final_state = graph.invoke(initial_state)

    report = format_report(final_state)
    print("\n" + report)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\nReport saved to {args.output}")


if __name__ == "__main__":
    main()
"""
cli.py — Command-line entry point for flux-scraper.

Usage:
    python3 -m src.flux_scraper.cli <command> [options]
    flux-scraper <command> [options]   (when installed via pip)
"""

import argparse
import asyncio
import sys

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flux-scraper",
        description="Data extraction and ETL flow orchestration",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    # ── run ──────────────────────────────────────────────────────────────────
    p = sub.add_parser("run", help="Execute a specific scraping flow")
    p.add_argument("flow_name", help="Name of the flow to execute (e.g., 'sales-comparison')")
    p.add_argument(
        "--output", 
        default="data", 
        help="Directory to save the output files (default: 'data')"
    )

    # ── list ─────────────────────────────────────────────────────────────────
    sub.add_parser("list", help="List all available scraping flows")

    return parser

async def async_main(args: argparse.Namespace) -> None:
    match args.command:
        case "run":
            print(f"Executing flow: {args.flow_name}")
            # TODO: Dynamically load and run flow based on name
            print("Not implemented yet.")
        case "list":
            print("Available flows:")
            # TODO: Iterate through src/flux_scraper/flows and list them
            print("  - None yet (migrate BaseID flows here).")
        case _:
            pass

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        asyncio.run(async_main(args))
    except KeyboardInterrupt:
        print("\nFlow execution cancelled by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()

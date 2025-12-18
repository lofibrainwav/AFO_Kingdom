"""
Dream Hub Integration for SixXon CLI
眞善美孝永 - Complete Energy Flow Vision Integration

Integrates Dream Protocol, Enhanced Dream Hub, and Dream Contracts
into SixXon CLI for complete human dream AI execution.
"""

import argparse
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "trinity-os"))

# Import all Dream Hub components
try:
    import contracts.dream_contract as dream_contract_module
    import graphs.dream_protocol as dream_protocol_module
    import graphs.enhanced_dream_hub as enhanced_dream_hub_module
    from sixxon import _calculate_trinity_score
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all Dream Hub components are installed")
    sys.exit(1)


def run_dream_hub_command(args):
    """Execute dream hub command"""
    print("🧠 SixXon Dream Hub - Human Dream AI Execution")
    print("眞善美孝永 - Energy Flow Vision Complete")
    print("=" * 60)

    if not args.dream:
        print("❌ Error: Please provide a dream description with --dream")
        return 1

    human_dream = args.dream

    try:
        # Step 1: Create Dream Contract
        print("📋 Creating Dream Contract...")
        execution_plan = [
            "Analyze human dream and extract core requirements",
            "Design AI implementation strategy with multi-agent collaboration",
            "Validate Trinity Score compatibility and energy flow",
            "Execute with continuous audit monitoring",
            "Complete with comprehensive Bridge logging and feedback",
        ]

        contract_id = dream_contract_module.create_dream_contract_manager(
            human_party=args.human_party or "Human Creator",
            dream_description=human_dream,
            execution_plan=execution_plan,
            truth=args.truth or 85.0,
            goodness=args.goodness or 80.0,
            risk_threshold=args.risk_threshold or 25.0,
        )
        print(f"✅ Contract created: {contract_id}")

        # Step 2: Run Enhanced Dream Hub
        print("🚀 Executing Dream through Enhanced Dream Hub...")
        thread_id = "dream_safe_thread"

        result = enhanced_dream_hub_module.run_enhanced_dream_hub(human_dream, thread_id)

        if result["status"] == "ERROR":
            print(f"❌ Dream execution failed: {result['error']}")
            return 1

        # Step 3: Validate Contract Compliance
        print("📋 Validating Contract Compliance...")
        trinity_score = result.get("trinity_score", {})
        risk_score = result.get("risk_score", 0.0)

        validation = dream_contract_module.contract_manager.validate_execution(contract_id, trinity_score, risk_score)

        if not validation["valid"]:
            print(f"❌ Contract violation: {validation['reason']}")
            print(f"   Violations: {validation.get('violations', [])}")
            return 1

        print("✅ Contract compliance verified")

        # Step 4: Complete Contract
        print("🏁 Completing Dream Contract...")
        final_result = {
            "status": "SUCCESS",
            "trinity_score": trinity_score,
            "risk_score": risk_score,
            "audit_history": result.get("audit_history", []),
            "bridge_logs": result.get("bridge_logs", []),
            "final_message": result.get("final_message", ""),
        }

        if dream_contract_module.contract_manager.complete_contract(contract_id, final_result):
            print("✅ Dream contract completed successfully")

        # Step 5: Display Results (3-line output philosophy)
        print("\n" + "=" * 60)
        print("🎯 DREAM EXECUTION RESULTS")
        print("=" * 60)

        status = "OK" if validation["valid"] else "BLOCK"
        decision = "COMPLETED" if result["status"] == "COMPLETED" else "INCOMPLETE"

        avg_score = sum(trinity_score.values()) / len(trinity_score) if trinity_score else 0
        next_action = "View Bridge logs" if result.get("bridge_logs") else "Check audit history"
        receipt_info = f"Dream ID: {result.get('dream_id', 'N/A')}"

        print(f"Status: {status} | Decision: {decision} | Trinity: {avg_score:.1f}")
        print(f"Next: {next_action}")
        print(f"Receipt: {receipt_info}")

        # Additional details
        if args.verbose:
            print("\n📊 Detailed Results:")
            print(f"   Contract ID: {contract_id}")
            print(f"   Dream ID: {result.get('dream_id', 'N/A')}")
            print(f"   Trinity Score: {trinity_score}")
            print(f"   Risk Score: {risk_score}")
            print(f"   Bridge Events: {len(result.get('bridge_logs', []))}")
            print(f"   Audit Steps: {len(result.get('audit_history', []))}")

        return 0

    except Exception as e:
        print(f"❌ Dream Hub execution failed: {e}")
        import traceback

        if args.verbose:
            traceback.print_exc()
        return 1


def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="SixXon Dream Hub - Human Dream AI Execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dream_hub_integration.py --dream "Build a starship navigation system"
  python dream_hub_integration.py --dream "Create emotion-based music composer" --truth 90 --verbose
        """,
    )

    parser.add_argument("--dream", "-d", required=True, help="Human dream description to execute through AI")

    parser.add_argument("--human-party", default="Human Creator", help="Name of the human party in the dream contract")

    parser.add_argument("--truth", type=float, default=85.0, help="Minimum truth score requirement (0-100)")

    parser.add_argument("--goodness", type=float, default=80.0, help="Minimum goodness score requirement (0-100)")

    parser.add_argument("--risk-threshold", type=float, default=25.0, help="Maximum risk threshold (0-100)")

    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed execution information")

    return parser


def main():
    """Main entry point for Dream Hub CLI"""
    parser = create_parser()
    args = parser.parse_args()

    return run_dream_hub_command(args)


if __name__ == "__main__":
    sys.exit(main())

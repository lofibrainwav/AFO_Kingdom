# scripts/verify_phase_4.py
import pathlib
import sys


def verify_graph_naming():
    print("[Phase 4 Verification] Checking Chancellor Graph Naming...")
    try:
        content = pathlib.Path("packages/afo-core/chancellor_graph.py").read_text(encoding="utf-8")

        required_names = [
            "zhuge_liang",
            "sima_yi",
            "zhou_yu",
            "zhuge_liang_node",
            "sima_yi_node",
            "zhou_yu_node",
        ]

        forbidden_names = [
            "jegalryang",
            "samaui",
            "juyu_node",  # "juyu" might exist in comments, checking specific node/key usage is harder with pure grep
        ]

        missing = [name for name in required_names if name not in content]
        found_forbidden = [name for name in forbidden_names if name in content]

        if missing:
            print(f"❌ Missing required official names: {missing}")
            sys.exit(1)

        if found_forbidden:
            print(f"❌ Found forbidden Korean-based names: {found_forbidden}")
            # Note: If found in comments it's okay, but better to be clean
            sys.exit(1)

        print("✅ Official Naming (Zhuge Liang, Sima Yi, Zhou Yu) verified in code.")

    except FileNotFoundError:
        print("❌ chancellor_graph.py not found")
        sys.exit(1)


def verify_base_module():
    print("[Phase 4 Verification] Checking Base Module...")
    if pathlib.Path("packages/afo-core/strategists/base.py").exists():
        print("✅ base.py exists.")
    else:
        print("❌ base.py missing.")
        sys.exit(1)


if __name__ == "__main__":
    verify_base_module()
    verify_graph_naming()
    print("🎉 Phase 4 Verification Complete!")

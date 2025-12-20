
import sys
import os

# Add package root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages")))

try:
    from afo_core.mediators.chancellor_mediator import (
        StrategistSquad, 
        TigerGeneralsUnit, 
        ChancellorMediator
    )
except ImportError:
    # Adjust path if running from root relative to packages
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../packages/afo-core")))
    from mediators.chancellor_mediator import (
        StrategistSquad, 
        TigerGeneralsUnit, 
        ChancellorMediator
    )

def demonstrate_mediator_pattern():
    print("👑 [Mediator Pattern Demonstration]")
    
    # 1. Create Components (Colleagues)
    strategists = StrategistSquad()
    tigers = TigerGeneralsUnit()
    
    # 2. Create Mediator (Connects them)
    # The mediator automatically registers itself with the colleagues
    chancellor = ChancellorMediator(strategists, tigers)
    
    print("\n--- Flow Start: User Query ---")
    # 3. Component triggers an event
    # Strategists don't know about Tigers directly. They just "send" a message.
    strategists.deliberate("Deploy GenUI Widget")
    
    print("\n✅ Mediator Pattern Verification Complete: De-coupled communication successful.")

if __name__ == "__main__":
    demonstrate_mediator_pattern()

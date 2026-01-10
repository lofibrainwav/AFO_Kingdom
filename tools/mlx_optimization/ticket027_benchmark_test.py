#!/usr/bin/env python3
"""
TICKET-027 QLoRA-AdaLoRA Hybrid Benchmark Test
Tests memory usage, parameter count, and basic functionality
"""

import os
import sys
import time
from pathlib import Path

import psutil
import torch

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "packages" / "afo-core"))

try:
    from afo.qlora_adalora_hybrid_service import (
        QLoRAAdaLoRAHybridService,
        initialize_hybrid_qlora_adalora,
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Trying alternative import...")
    try:
        from packages.afo_core.afo.qlora_adalora_hybrid_service import (
            QLoRAAdaLoRAHybridService,
            initialize_hybrid_qlora_adalora,
        )
    except ImportError as e2:
        print(f"Alternative import failed: {e2}")
        sys.exit(1)


def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def benchmark_hybrid_service():
    """Benchmark QLoRA-AdaLoRA hybrid service"""
    print("=" * 60)
    print("TICKET-027 QLoRA-AdaLoRA Hybrid Benchmark Test")
    print("=" * 60)

    results = {
        "timestamp": time.time(),
        "memory_before": get_memory_usage(),
        "memory_after_init": 0,
        "memory_after_load": 0,
        "memory_after_hybrid": 0,
        "trainable_params": 0,
        "total_params": 0,
        "gpu_available": torch.cuda.is_available(),
        "gpu_memory_allocated": 0,
        "gpu_memory_reserved": 0,
        "success": False,
        "error": None,
    }

    try:
        print("1. Initializing hybrid service...")
        service = QLoRAAdaLoRAHybridService()
        results["memory_after_init"] = get_memory_usage()
        print(".1f")

        print("2. Loading base model with 4-bit quantization...")
        service.load_base_model()
        results["memory_after_load"] = get_memory_usage()
        print(".1f")

        if torch.cuda.is_available():
            results["gpu_memory_allocated"] = torch.cuda.memory_allocated() / 1024**3
            results["gpu_memory_reserved"] = torch.cuda.memory_reserved() / 1024**3
            print(".2f")
            print(".2f")

        print("3. Applying QLoRA-AdaLoRA hybrid optimization...")
        service.apply_hybrid_optimization()
        results["memory_after_hybrid"] = get_memory_usage()
        results["trainable_params"] = service.get_trainable_params()
        print(".1f")
        print(f"   Trainable parameters: {results['trainable_params']}")

        print("4. Preparing for training...")
        service.prepare_for_training()
        print("   ✓ Training preparation complete")

        print("5. Testing text generation...")
        test_prompt = "Hello, this is a test prompt for"
        generated = service.generate_text(test_prompt, max_length=20)
        print(f"   Generated: {generated}")

        results["success"] = True
        print("\n✅ Benchmark completed successfully!")

    except Exception as e:
        results["error"] = str(e)
        print(f"\n❌ Benchmark failed: {e}")

    # Calculate memory differences
    results["memory_init_delta"] = (
        results["memory_after_init"] - results["memory_before"]
    )
    results["memory_load_delta"] = (
        results["memory_after_load"] - results["memory_after_init"]
    )
    results["memory_hybrid_delta"] = (
        results["memory_after_hybrid"] - results["memory_after_load"]
    )

    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Success: {results['success']}")
    print(".1f")
    print(".1f")
    print(".1f")
    print(".1f")
    print(f"Trainable params: {results['trainable_params']}")
    print(f"GPU available: {results['gpu_available']}")

    if results["gpu_available"]:
        print(".2f")
        print(".2f")

    if results["error"]:
        print(f"Error: {results['error']}")

    # Save results
    import json

    output_file = f"artifacts/ticket027_benchmark_{int(time.time())}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n📊 Results saved to: {output_file}")

    return results


if __name__ == "__main__":
    results = benchmark_hybrid_service()

    # Exit with appropriate code
    sys.exit(0 if results["success"] else 1)

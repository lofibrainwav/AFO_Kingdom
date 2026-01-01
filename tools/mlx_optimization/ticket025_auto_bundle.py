import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


ARTIFACTS = "artifacts"


class ReleaseHandler(FileSystemEventHandler):
    def on_created(self, event):
        src_path = str(event.src_path)
        if "release_" in src_path and src_path.endswith("Z"):
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] New release detected: {src_path}")
            print("Rebuilding bundle...")
            # 기존 ticket024_build_dashboard_bundle.py 호출
            result = os.system("python tools/mlx_optimization/ticket024_build_dashboard_bundle.py")
            if result == 0:
                print("Bundle updated successfully! Dashboard SSOT synced.")
            else:
                print("Bundle update failed!")
            print("-" * 50)


# 모니터링 시작 (왕국 부팅 시 실행)
if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ReleaseHandler(), ARTIFACTS, recursive=False)
    observer.start()
    print(
        f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] TICKET-025 Auto Pipeline ACTIVE - Eternal Sync ON"
    )
    print(f"Monitoring {ARTIFACTS} for new release directories...")
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        print("Auto pipeline stopped.")
    observer.join()

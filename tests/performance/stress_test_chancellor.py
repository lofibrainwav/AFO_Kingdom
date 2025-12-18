# tests/performance/stress_test_chancellor.py
from locust import HttpUser, task, between, constant

class ChancellorUser(HttpUser):
    wait_time = between(1, 3) # Wait 1-3 seconds between tasks
    
    @task(3)
    def health_check(self):
        """Monitor health endpoint under load."""
        self.client.get("/api/health")
        
    @task(1)
    def invoke_chancellor_simple(self):
        """Simple dry-run query to Chancellor."""
        self.client.post("/api/chancellor/invoke", json={
            "query": "Status Report",
            "dry_run": True
        })

    @task(1)
    def invoke_chancellor_complex(self):
        """Complex query simulating ToT trigger."""
        # Note: This might be slow and resource intensive. Lower weight.
        self.client.post("/api/chancellor/invoke", json={
            "query": "Analyze the kingdom architecture and propose improvements.",
            "dry_run": True
        })

# To run: locust -f tests/performance/stress_test_chancellor.py --host http://localhost:8010

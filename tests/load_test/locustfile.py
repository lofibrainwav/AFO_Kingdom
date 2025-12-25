"""
AFO Kingdom Load Testing with Locust

This script performs comprehensive load testing on AFO Kingdom API endpoints.
Tests various scenarios including basic health checks, skills API, and concurrent user loads.
"""

import random
import time

from locust import HttpUser, between, events, task


class AFOKingdomUser(HttpUser):
    """AFO Kingdom API Load Test User"""

    # Wait time between tasks (1-3 seconds)
    wait_time = between(1, 3)

    # Test configuration
    host = "http://localhost:8010"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skills_list = []  # Cache skills list for detail requests

    @task(4)
    def health_check(self):
        """Test health endpoint"""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")

    @task(3)
    def skills_list(self):
        """Test skills list endpoint"""
        with self.client.get("/api/skills/list", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "skills" in data:
                        # Cache some skill IDs for detail requests
                        self.skills_list = [skill["id"] for skill in data["skills"][:5]]
                        response.success()
                    else:
                        response.failure("Invalid response format")
                except ValueError:
                    response.failure("Invalid JSON response")
            else:
                response.failure(f"Skills list failed: {response.status_code}")

    @task(2)
    def skills_detail(self):
        """Test skills detail endpoint"""
        if self.skills_list:
            skill_id = random.choice(self.skills_list)
            with self.client.get(
                f"/api/skills/detail/{skill_id}", catch_response=True
            ) as response:
                if response.status_code == 200:
                    response.success()
                elif response.status_code == 404:
                    # Skill not found - remove from cache
                    if skill_id in self.skills_list:
                        self.skills_list.remove(skill_id)
                    response.success()  # 404 is acceptable for this test
                else:
                    response.failure(f"Skills detail failed: {response.status_code}")
        else:
            # Skip if no skills cached yet
            time.sleep(0.1)

    @task(1)
    def trinity_current(self):
        """Test Trinity current scores endpoint"""
        with self.client.get("/api/5pillars/current", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Trinity current failed: {response.status_code}")

    @task(1)
    def skills_execute(self):
        """Test skills execute endpoint (light usage to avoid resource exhaustion)"""
        if self.skills_list:
            skill_id = random.choice(self.skills_list)
            payload = {
                "skill_id": skill_id,
                "parameters": {"test": True},
                "timeout_seconds": 5,
            }
            with self.client.post(
                "/api/skills/execute", json=payload, catch_response=True
            ) as response:
                if response.status_code in {200, 400, 404}:  # Accept various responses
                    response.success()
                else:
                    response.failure(f"Skills execute failed: {response.status_code}")
        else:
            time.sleep(0.1)


class LoadTestShape:
    """
    Dynamic load testing shape
    Gradually increases load, then maintains peak load, then decreases
    """

    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 2},  # Warm up: 10 users over 1 min
        {"duration": 120, "users": 50, "spawn_rate": 5},  # Ramp up: 50 users over 2 min
        {
            "duration": 180,
            "users": 100,
            "spawn_rate": 10,
        },  # Peak load: 100 users over 3 min
        {
            "duration": 120,
            "users": 100,
            "spawn_rate": 10,
        },  # Sustained load: 100 users for 2 min
        {
            "duration": 60,
            "users": 50,
            "spawn_rate": 5,
        },  # Cool down: 50 users over 1 min
        {
            "duration": 30,
            "users": 10,
            "spawn_rate": 2,
        },  # Final cool down: 10 users over 30s
    ]

    def tick(self):
        """Return the current number of users and spawn rate"""
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])

            run_time -= stage["duration"]

        # Test completed
        return None

    def get_run_time(self):
        """Get total run time"""
        return time.time() - self.start_time

    def set_start_time(self, start_time):
        """Set test start time"""
        self.start_time = start_time


# Custom event handlers
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """Initialize test environment"""

    # Set up test shape if configured
    if hasattr(environment, "shape_class"):
        environment.shape_class.set_start_time(time.time())


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Test start event"""


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Test stop event"""

    # Generate summary report
    if environment.runner:
        pass


@events.spawning_complete.add_listener
def on_spawning_complete(user_count, **kwargs):
    """Spawning complete event"""


@events.request_success.add_listener
def on_request_success(request_type, name, response_time, response_length, **kwargs):
    """Request success event - detailed logging"""
    if response_time > 2000:  # Log slow requests (>2s)
        pass


@events.request_failure.add_listener
def on_request_failure(request_type, name, response_time, exception, **kwargs):
    """Request failure event"""

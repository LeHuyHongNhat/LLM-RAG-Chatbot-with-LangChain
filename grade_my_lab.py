#!/usr/bin/env python3
"""
Automated grading script for Day 12 Lab
Adjusted for LLM-RAG-Chatbot-with-LangChain structure.
Usage: python grade.py <student-repo-path> <public-url> <api-key>
"""

import sys
import os
import subprocess
import requests
import time
from pathlib import Path

class Grader:
    def __init__(self, repo_path, public_url, api_key):
        self.repo_path = Path(repo_path)
        self.public_url = public_url.rstrip('/')
        self.api_key = api_key
        self.score = 0
        self.max_score = 60
        self.results = []
    
    def test(self, name, points, func):
        """Run a test and record result"""
        print(f"Testing: {name}...", end=" ", flush=True)
        try:
            func()
            self.score += points
            self.results.append(f"✅ {name}: {points}/{points}")
            print("PASSED")
            return True
        except AssertionError as e:
            self.results.append(f"❌ {name}: 0/{points} - {e}")
            print(f"FAILED - {e}")
            return False
        except Exception as e:
            if "Target URL" in str(e) or "Connection" in str(e):
                 print(f"ERROR - Could not reach API: {e}")
                 self.results.append(f"❌ {name}: 0/{points} - Connection Error")
                 return False
            self.results.append(f"❌ {name}: 0/{points} - Error: {e}")
            print(f"ERROR - {e}")
            return False
    
    def check_file_exists(self, filepath):
        """Check if file exists"""
        assert (self.repo_path / filepath).exists(), f"{filepath} not found"
    
    def check_dockerfile(self):
        """Check Dockerfile quality"""
        # API Dockerfile
        df_path = self.repo_path / "chatbot_api" / "Dockerfile"
        assert df_path.exists(), "chatbot_api/Dockerfile not found"
        dockerfile = df_path.read_text()
        assert "FROM" in dockerfile, "No FROM instruction"
        assert "as builder" in dockerfile.lower(), "Not multi-stage build"
        assert "slim" in dockerfile.lower(), "Not using slim image for optimization"
    
    def check_docker_compose(self):
        """Check docker-compose.yml"""
        compose = (self.repo_path / "docker-compose.yml").read_text()
        assert "redis:" in compose, "No redis service found in compose"
        assert "api:" in compose, "No api service found in compose"
    
    def check_no_secrets(self):
        """Check for hardcoded secrets"""
        # Search in chatbot_api/src
        src_path = self.repo_path / "chatbot_api" / "src"
        result = subprocess.run(
            ["grep", "-r", "sk-", str(src_path)],
            capture_output=True, text=True
        )
        assert result.returncode != 0, f"Found hardcoded API keys in {result.stdout}"
    
    def test_health_endpoint(self):
        """Test /health endpoint"""
        r = requests.get(f"{self.public_url}/health", timeout=15)
        assert r.status_code == 200, f"Health check failed: {r.status_code}"
    
    def test_ready_endpoint(self):
        """Test /ready endpoint"""
        r = requests.get(f"{self.public_url}/ready", timeout=15)
        assert r.status_code == 200, f"Ready check failed: {r.status_code}"
    
    def test_auth_required(self):
        """Test authentication is required"""
        r = requests.post(
            f"{self.public_url}/hospital-rag-agent",
            json={"text": "test"}
        )
        assert r.status_code == 401, f"Should require authentication (Got {r.status_code})"
    
    def test_auth_works(self):
        """Test authentication works"""
        r = requests.post(
            f"{self.public_url}/hospital-rag-agent",
            headers={"X-API-Key": self.api_key},
            json={"user_id": "grader", "text": "Hello Agent"}
        )
        assert r.status_code == 200, f"Auth failed with valid key: {r.status_code} - {r.text}"
    
    def test_rate_limiting(self):
        """Test rate limiting"""
        print("(Stress testing...)", end=" ", flush=True)
        # Send requests quickly to trigger the 15 req/min limit
        status_codes = []
        for i in range(20):
            r = requests.post(
                f"{self.public_url}/hospital-rag-agent",
                headers={"X-API-Key": self.api_key},
                json={"user_id": "grader_rate_test", "text": f"stress test {i}"}
            )
            status_codes.append(r.status_code)
            if r.status_code == 429:
                break
            time.sleep(0.05)
        
        assert 429 in status_codes, f"Rate limiting not triggered. Status codes: {status_codes}"
    
    def test_conversation_history(self):
        """Test conversation history (Stateless using Redis)"""
        # Logic: First message, then check if it remembers the name
        # Note: This depends on the agent implementation being stateless (session_id or user_id)
        # Assuming the agent uses the session state from memory/Redis.
        return True # Placeholder as actual chat test depends on LLM response
    
    def run_all_tests(self):
        """Run all tests and output report"""
        print("\n" + "="*60)
        print("🧪 STARTING AUTOMATED GRADING FOR DAY 12 LAB")
        print(f"Target URL: {self.public_url}")
        print("="*60 + "\n")
        
        # File structure tests
        self.test("chatbot_api/Dockerfile exists", 2, lambda: self.check_file_exists("chatbot_api/Dockerfile"))
        self.test("docker-compose.yml exists", 2, lambda: self.check_file_exists("docker-compose.yml"))
        self.test("chatbot_api/pyproject.toml exists", 1, lambda: self.check_file_exists("chatbot_api/pyproject.toml"))
        
        # Docker quality tests
        self.test("Multi-stage Dockerfile", 5, self.check_dockerfile)
        self.test("Docker Compose setup (Redis)", 4, self.check_docker_compose)
        
        # Security tests
        self.test("No hardcoded secrets", 5, self.check_no_secrets)
        self.test("Authentication required (401)", 5, self.test_auth_required)
        self.test("Authentication functional (200)", 5, self.test_auth_works)
        self.test("Rate limiting (Ex 4.3)", 5, self.test_rate_limiting)
        
        # Reliability tests
        self.test("Health check endpoint", 3, self.test_health_endpoint)
        self.test("Readiness check endpoint", 3, self.test_ready_endpoint)
        
        # Summary
        print("\n" + "="*60)
        print("📊 AUTOMATED GRADING RESULTS SUMMARY")
        print("="*60)
        for result in self.results:
            print(result)
        print("="*60)
        print(f"🎯 AUTOMATED SCORE: {self.score}/60")
        print("="*60 + "\n")
        
        return self.score

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python grade_my_lab.py <repo-path> <public-url> <api-key>")
        sys.exit(1)
    
    repo = sys.argv[1]
    url = sys.argv[2]
    key = sys.argv[3]
    
    grader = Grader(repo, url, key)
    grader.run_all_tests()

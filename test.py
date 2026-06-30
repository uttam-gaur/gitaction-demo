#!/usr/bin/env python3

print("🚀 GitHub Actions Workflow Started\n")

# Build Stage
print("🔨 Building the application...")
print("Build completed successfully.\n")

# Lint Stage
print("🧹 Running lint checks...")
print("No linting errors found.\n")
# Test Stage
print("🧪 Running tests...")
def add(a, b):
    return a + b

assert add(2, 3) == 5
assert add(10, 5) == 15

print("All tests passed.\n")

# Deploy Simulation
print("🚀 Deploying application...")
print("Deployment successful.\n")

print("✅ GitHub Actions Workflow Completed Successfully!")

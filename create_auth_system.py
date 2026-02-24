import os

class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}CREATING LOGIN & LOGOUT SYSTEM{Colors.END}")
print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

created_files = []

# Create templates directory
os.makedirs('templates', exist_ok=True)

# ============================================================================
# 1. LOGIN PAGE
# ============================================================================
print(f"{Colors.CYAN}Creating login.html...{Colors.END}")

LOGIN_PAGE = """{% extends 'base.html' %}

{% block title %}Login - Event Social Network{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white text-center">
                    <h3 class="mb-0">
                        <i class="fas fa-sign-in-alt me-2"></i>
                        Login
                    </h3>
                </div>
                <div class="card-body p-4">
                    
                    <form method="POST" action="/login">
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Email Address</label>
                            <div class="input-group">
                                <span class="input-group-text">
                                    <i class="fas fa-envelope"></i>
                                </span>
                                <input type="email" name="email" class="form-control" 
                                       placeholder="your@email.com" required autofocus>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label fw-bold">Password</label>
                            <div class="input-group">
                                <span class="input-group-text">
                                    <i class="fas fa-lock"></i>
                                </span>
                                <input type="password" name="password" class="form-control" 
                                       placeholder="Enter password" required>
                            </div>
                        </div>
                        
                        <div class="mb-3 form-check">
                            <input type="checkbox" class="form-check-input" id="remember">
                            <label class="form-check-label" for="remember">
                                Remember me
                            </label>
                        </div>
                        
                        <button type="submit" class="btn btn-primary btn-lg w-100 mb-3">
                            <i class="fas fa-sign-in-alt me-2"></i>
                            Login
                        </button>
                        
                        <hr>
                        
                        <div class="text-center">
                            <p class="mb-2">
                                <a href="/forgot-password" class="text-decoration-none">
                                    <i class="fas fa-question-circle me-1"></i>
                                    Forgot Password?
                                </a>
                            </p>
                            <p class="mb-0">
                                Don't have an account? 
                                <a href="/register" class="text-decoration-none fw-bold">
                                    Register here
                                </a>
                            </p>
                        </div>
                        
                    </form>
                    
                </div>
            </div>
            
            <div class="text-center mt-3">
                <small class="text-muted">
                    <i class="fas fa-shield-alt me-1"></i>
                    Secure Login • SSL Encrypted
                </small>
            </div>
            
        </div>
    </div>
</div>
{% endblock %}
"""

with open('templates/login.html', 'w', encoding='utf-8') as f:
    f.write(LOGIN_PAGE.strip())
created_files.append('templates/login.html')

print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}✅ LOGIN PAGE CREATED!{Colors.END}")
print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}\n")

print(f"{Colors.CYAN}Created files:{Colors.END}")
for file in created_files:
    print(f"  {Colors.GREEN}✓{Colors.END} {file}")

print(f"\n{Colors.BOLD}{Colors.YELLOW}NEXT: ADD LOGIN/LOGOUT ROUTES{Colors.END}\n")
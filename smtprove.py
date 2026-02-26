import smtplib
import argparse
import sys

def test_smtp_login(host, port, user, password):
    print(f"[*] Connecting to {host}:{port}...")

    try:
        # Connect to the SMTP server — use implicit SSL for port 465, plain for everything else
        if port == 465:
            print("[*] Using implicit SSL (SMTP_SSL)...")
            server = smtplib.SMTP_SSL(host, port, timeout=10)
        else:
            server = smtplib.SMTP(host, port, timeout=10)
        
        # Identify ourselves to the server
        server.ehlo()
        
        # If using port 587, switch to STARTTLS (standard for modern SMTP auth)
        if port == 587:
            print("[*] Starting TLS...")
            server.starttls()
            server.ehlo()

        print(f"[*] Attempting login with user: {user}")

        # Attempt 1: Try the username exactly as provided
        try:
            server.login(user, password)
            print(f"[+] SUCCESS! Logged in as: {user}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            print(f"[-] Failed with '{user}': {e.smtp_code} {e.smtp_error.decode()}")
            
            # Attempt 2: Try appending the domain if it looks like a bare username
            if '@' not in user:
                # Extract domain from the hostname (basic heuristic)
                domain = host
                if '.' in host and not host.replace('.', '').isdigit():
                    # simple extraction for 'mail.domain.com' -> 'domain.com'
                    parts = host.split('.')
                    if len(parts) > 2:
                        domain = '.'.join(parts[1:])
                
                user_with_domain = f"{user}@{domain}"
                print(f"[*] Retrying with full email address: {user_with_domain}")
                
                try:
                    server.login(user_with_domain, password)
                    print(f"[+] SUCCESS! Logged in as: {user_with_domain}")
                    return True
                except smtplib.SMTPAuthenticationError as e2:
                    print(f"[-] Failed with '{user_with_domain}': {e2.smtp_code} {e2.smtp_error.decode()}")
            return False

    except Exception as e:
        print(f"[!] Connection error: {e}")
        return False
    finally:
        try:
            server.quit()
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SMTP Credential Tester")
    parser.add_argument("host", help="SMTP server hostname or IP")
    parser.add_argument("-p", "--port", type=int, default=587, help="SMTP port (default: 587)")
    parser.add_argument("-u", "--user", required=True, help="Username")
    parser.add_argument("-P", "--password", required=True, help="Password")
    
    args = parser.parse_args()

    if not test_smtp_login(args.host, args.port, args.user, args.password):
        sys.exit(1)

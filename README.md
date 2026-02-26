# SMTProbe 

A lightweight SMTP credential tester built for one thing netexec can't do — **testing credentials against the email domain format (`user@domain.com`)**.

When a mail server requires full email address authentication, netexec fails silently. smtprobe automatically retries with the domain appended, so you don't miss valid creds just because of how the server expects the username formatted.

---

## The Problem with netexec

netexec passes the username exactly as you give it. If the server requires `user@domain.com` instead of just `user`, it just fails — no fallback, no retry. You might be sitting on valid credentials and walking away empty handed.

smtprobe fixes that. It tries the bare username first, and if that fails it automatically retries with the domain appended — extracted from the hostname. Two shots at every login attempt.

---

## What it does

- **Auto-retries with full email format** — the main reason this exists
- Handles implicit SSL (465), STARTTLS (587), and plain SMTP
- Clean output with SMTP response codes so you know *why* something failed
- Exits with code `0`/`1` so it plays nicely in scripts

---

## Installation

No dependencies outside the standard library. Just clone and run.

```bash
git clone https://github.com/youruser/smtprobe.git
cd smtprobe
python smtprobe.py --help
```

---

## Usage

```bash
python smtprobe.py <host> -u <user> -P <password> [-p <port>]
```

### Examples

```bash
# Standard STARTTLS (default port 587)
python smtprobe.py mail.example.com -u admin -P hunter2

# Implicit SSL
python smtprobe.py mail.example.com -p 465 -u admin -P hunter2

# Plain SMTP (no TLS)
python smtprobe.py 192.168.1.50 -p 25 -u admin -P hunter2
```

### Arguments

| Argument | Description | Default |
|---|---|---|
| `host` | SMTP server hostname or IP | required |
| `-p / --port` | SMTP port | `587` |
| `-u / --user` | Username | required |
| `-P / --password` | Password | required |

---

## Output

```
[*] Connecting to mail.example.com:587...
[*] Starting TLS...
[*] Attempting login with user: admin
[-] Failed with 'admin': 535 Authentication failed
[*] Retrying with full email address: admin@example.com
[+] SUCCESS! Logged in as: admin@example.com
```

---

## When to use this

- netexec's SMTP module fails and you suspect the server wants `user@domain.com` format
- You want to make sure you're not missing valid creds due to username formatting
- You need something simple you can read and modify on the fly during an engagement

---

## Disclaimer

For authorized security testing only. Don't be that guy.

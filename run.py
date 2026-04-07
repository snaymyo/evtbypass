import core  # 
import os
import sys
import time
import hashlib

# UI Colors
C_RED, C_CYAN, C_GREEN, C_YELLOW, C_RESET, C_BOLD = '\033[91m', '\033[96m', '\033[92m', '\033[93m', '\033[0m', '\033[1m'
SECRET_SALT = "ohmygod@123"
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".turbo_license")

if __name__ == "__main__":
    try:
        did = core.get_device_id()
        
        # 
        if not core.check_time_manipulation():
            os.system('clear')
            print(f"{C_RED}[!] FATAL ERROR: System time manipulation detected!{C_RESET}")
            sys.exit(1)

        authorized, expiry, status = False, None, "PENDING"
        
        # 
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, "r") as f:
                saved_key = f.read().strip()
            
            is_valid, msg, expiry = core.validate_key(did, saved_key)
            if is_valid:
                authorized, status = True, msg
            elif core.verify_legacy_user(saved_key):
                # Legacy Migration Logic
                lt_exp = "212601010000"
                raw_new = f"{did}{lt_exp}{SECRET_SALT}"
                new_k = f"{hashlib.sha256(raw_new.encode()).hexdigest()[:12].upper()}{lt_exp}"
                
                with open(LICENSE_FILE, "w") as f:
                    f.write(new_k)
                
                authorized, status = True, "VERIFIED_LIFETIME"
                core.print_banner(did, None, "VERIFIED_LIFETIME")
                print(f"{C_YELLOW}╔══════════════════════════════════════════════════════╗")
                print(f"║ {C_CYAN}LEGACY USER DETECTED! NEW LIFETIME KEY GENERATED:{C_RESET}    {C_YELLOW}║")
                print(f"║ {C_BOLD}{C_GREEN}{new_k:<52}{C_RESET} {C_YELLOW}║")
                print(f"{C_YELLOW}╚══════════════════════════════════════════════════════╝{C_RESET}")
                time.sleep(5)

        core.print_banner(did, expiry, status)
        
        # 
        if not authorized:
            print(f"{C_CYAN}[?] Activation Key: {C_RESET}")
            key = input(f"\033[92mroot@turbo:~# \033[0m").strip().upper()
            
            v, m, e = core.validate_key(did, key)
            if v:
                with open(LICENSE_FILE, "w") as f: f.write(key)
                core.print_banner(did, e, m)
                authorized = True
            elif core.verify_legacy_user(key):
                lt_exp = "212601010000"
                raw_new = f"{did}{lt_exp}{SECRET_SALT}"
                new_k = f"{hashlib.sha256(raw_new.encode()).hexdigest()[:12].upper()}{lt_exp}"
                with open(LICENSE_FILE, "w") as f: f.write(new_k)
                core.print_banner(did, None, "VERIFIED_LIFETIME")
                print(f"{C_YELLOW}╔══════════════════════════════════════════════════════╗")
                print(f"║ {C_CYAN}NEW LIFETIME KEY GENERATED (SAVE THIS):{C_RESET}              {C_YELLOW}║")
                print(f"║ {C_BOLD}{C_GREEN}{new_k:<52}{C_RESET} {C_YELLOW}║")
                print(f"{C_YELLOW}╚══════════════════════════════════════════════════════╝{C_RESET}")
                time.sleep(5)
                authorized = True
            else:
                print(f"{C_RED}[X] Invalid Activation Key!{C_RESET}")
                sys.exit(1)

        if authorized:
            core.start_process()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] STOPPED BY USER.{C_RESET}")
        

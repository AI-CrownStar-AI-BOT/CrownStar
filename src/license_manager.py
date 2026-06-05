import hashlib
import os
import json
from pathlib import Path

LICENSE_FILE = Path.home() / ".crownstar_license"
SECRET = "CrownStarAI-2026-PROD-KEY"   # change to a random string

def generate_key(machine_id):
    """Generate a license key from machine ID and tier."""
    return hashlib.sha256(f"{SECRET}{machine_id}".encode()).hexdigest()[:20]

def get_machine_id():
    """Simple machine identifier (Windows volume serial or hostname)."""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        product_id = winreg.QueryValueEx(key, "ProductId")[0]
        return product_id
    except:
        return os.environ.get("COMPUTERNAME", "unknown")

def save_license(license_key, tier):
    data = {"key": license_key, "tier": tier}
    LICENSE_FILE.write_text(json.dumps(data))
    os.chmod(LICENSE_FILE, 0o600)

def load_license():
    if LICENSE_FILE.exists():
        return json.loads(LICENSE_FILE.read_text())
    return None

def verify_license(required_tier):
    """Returns (valid, message, tier)."""
    license_data = load_license()
    if not license_data:
        return False, "No license found. Please purchase a license.", None
    key = license_data.get("key")
    tier = license_data.get("tier")
    # Simple verification: check if key matches expected format
    # For production, you'd call an online API or use asymmetric crypto.
    machine_id = get_machine_id()
    expected = generate_key(machine_id)
    if key == expected:
        # Tier hierarchy: Free < Basic < Pro < Enterprise
        tier_order = {"Free":0, "Basic":1, "Pro":2, "Enterprise":3}
        if tier_order.get(tier,0) >= tier_order.get(required_tier,0):
            return True, f"Valid {tier} license", tier
        else:
            return False, f"License tier ({tier}) insufficient for {required_tier}", tier
    return False, "Invalid license key", None

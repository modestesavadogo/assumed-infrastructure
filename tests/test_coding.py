"""Unit tests for the lexicon coder. Run: python tests/test_coding.py"""
import sys
sys.path.insert(0, "src")
from coding import code_text

BS = chr(92)
src = open("src/coding.py", encoding="utf-8").read()
assert not any(ord(c) < 32 and c not in "\n\r\t" for c in src), "control characters in coding.py (a bad escape?)"
assert (BS + BS + "w") not in src, "double-escaped backslash-w in coding.py"

t = code_text("No international credit card, so no online subscriptions. Avoid platforms that need a credit card.")
assert t["pay_D"] == 0, t            # restated or avoided constraints are not dependence
t = code_text("Pay the fee via credit card, check, or online payment.")
assert t["pay_D"] == 2, t
t = code_text("If online payment is only possible via mobile money, note the amount.")
assert t["pay_D"] == 0 and t["pay_A"] == 1, t
t = code_text("Use Wi-Fi at the hotel, search LinkedIn and book flights.")
assert t["net_D"] == 1 and t["online_D"] == 1 and t["trans_D"] == 1, t
t = code_text("Apply online, download the app and send an email to the virtual team.")
assert t["digital_generic"] == 5 and t["D_total"] == 0, t
t = code_text("Download once for offline use and plan for power cuts; pay by mobile money.")
assert t["net_A"] == 2 and t["power_A"] == 1 and t["pay_A"] == 1, t
print("all coding tests passed")

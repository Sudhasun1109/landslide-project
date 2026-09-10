from send_alert import send_sms

message = """
LANDSLIDE TEST ALERT 🚨

This is a test message from
AI Landslide Early Warning System.

No emergency action is required.
"""

receiver = "+919043116274"

try:
    sid = send_sms(message, receiver)
    print("SMS SENT SUCCESSFULLY!")
    print("Message SID:", sid)

except Exception as e:
    print("SMS FAILED!")
    print("Error:", e)
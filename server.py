from http.server import HTTPServer, BaseHTTPRequestHandler  # HTTP 서버 생성 및 응답 처리을 위해 사용
import ssl  # TLS 설정을 위해 사용
import json # JSON 파싱/생성을 위해 사용
import os   # 환경변수를 읽기 위해 사용

# HTTP 요청을 처리하기 위한 클래스를 정의
# BaseHTTPRequestHandler 클래스를 상속
class MyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """CORS 설정을 처리하기 위한 함수"""
        self.send_response(200) # 200 OK 응답 코드를 설정
        self.send_header('Access-Control-Allow-Origin', '*')    # 모든 도메인을 허용
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')   # POST, OPTIONS 메서드 허용
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')    # Content-type 헤더 허용
        self.end_headers()

    def do_POST(self):
        """클라이언트가 보낸 요청을 처리하는 함수"""
        content_length = int(self.headers.get('Content-Length', 0)) # 본문 길이를 파싱
        body = self.rfile.read(content_length).decode('utf-8')  # 본문 길이만큼 바이트를 읽음
        
        # 메시지를 파싱
        try:
            data = json.loads(body)
            message = data.get('message', 'Hello World')    # 기본값은 'Hello World'
        except:
            message = body if body else 'Empty'
        
        # 응답 헤더를 설정
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 응답 본문을 설정
        response = json.dumps({
            'received': message,
            'protocol': 'HTTPS' if USE_TLS else 'HTTP',
            'encrypted': USE_TLS
        })

        # 응답을 전송
        self.wfile.write(response.encode('utf-8'))

# 서버 객체를 생성하는 함수
def run_server(port, use_tls=False):
    global USE_TLS
    USE_TLS = use_tls
    
    # 모든 네트워크 인터페이스에서 접속을 허용하고, 입력한 포트를 매핑
    # 요청을 처리할 클래스를 설정
    server = HTTPServer(('0.0.0.0', port), MyHandler)
    
    # 만약에 TLS 를 사용한다면 적용
    if use_tls:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)   # SSLContext 객체 생성, 서버용 TLS 프로토콜 사용
        context.load_cert_chain('/app/cert.pem', '/app/key.pem')    # 해당 객체에 인증서, 개인키를 로드
        server.socket = context.wrap_socket(server.socket, server_side=True)    # 암호화 통신을 위해 일반 TCP 소켓을 래핑
        print(f"HTTPS 서버 동작! 포트:{port}")
    else:
        print(f"HTTP 서버 동작! 포트:{port}")
    
    # 서버가 요청을 대기함. 한 번에 하나의 클라이언트만 처리 가능하며 blocking 방식을 사용
    server.serve_forever()

# 프로그램 진입점
if __name__ == '__main__':
    # 환경변수를 읽음
    port = int(os.environ.get('PORT', 8080))    # 기본값은 HTTP 포트
    use_tls = os.environ.get('USE_TLS', 'false').lower() == 'true'  # 기본값은 false, 대소문자 상관없이 처리 가능
    run_server(port, use_tls)
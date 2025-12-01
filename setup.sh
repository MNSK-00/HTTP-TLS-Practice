#!/bin/bash

echo "================================"
echo "HTTP/HTTPS 실습 환경 설정"
echo "================================"

# 1. 자체 서명 인증서 생성
echo ""
echo "[1/3] TLS 인증서 생성 중..."
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes \
    -subj "/CN=localhost"

if [ -f cert.pem ] && [ -f key.pem ]; then
    echo "[완료] 인증서 생성 완료: cert.pem, key.pem"
else
    echo "[실패] 인증서 생성 실패"
    exit 1
fi

# 2. Docker 이미지 빌드
echo ""
echo "[2/3] Docker 이미지 빌드 중..."
docker-compose build

# 3. 컨테이너 실행
echo ""
echo "[3/3] 서버 시작 중..."
docker-compose up -d

echo ""
echo "================================"
echo "[완료] 설정 완료!"
echo "================================"
echo ""
echo "서버 정보:"
echo "   HTTP  서버: http://localhost:8080"
echo "   HTTPS 서버: https://localhost:8443"
echo ""
echo "클라이언트 GUI:"
echo "   브라우저에서 client.html 파일을 열어주세요"
echo ""
echo "[주의] HTTPS 첫 접속 시:"
echo "   https://localhost:8443 직접 접속 후"
echo "   브라우저 인증서 경고를 수락해주세요"
echo ""
echo "종료: docker-compose down"
echo ""
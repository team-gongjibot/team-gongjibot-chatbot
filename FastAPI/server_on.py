import nest_asyncio
import uvicorn
from pyngrok import ngrok

nest_asyncio.apply()

port = 8000

#ngrok 인증 토큰 설정
ngrok.set_auth_token("2xdX9EYng3EDack7QZyiBvF2ZQE_5oCPcm3n9NmxARS4DM2tv")

#고정 도메인 설정 (유료 플랜에서 예약한 경우만 가능)
try:
    public_url = ngrok.connect(addr=port, domain="vervet-upright-pony.ngrok-free.app")
    print(f"FastAPI 서버 공개 주소: {public_url}")

    uvicorn.run("chat:app", host="0.0.0.0", port=port, reload=False)

except Exception as e:
    print(f"오류 발생: {e}")
#  Flask API를 완성하세요.
# 요구사항:
# - 데이터 파일 경로: /app/data/data.json  (초기 내용: [])
# - GET  /api/records   : 저장된 데이터를 JSON으로 반환
# - POST /api/records   : {height, weight}를 받아 유효성 검사 후 누적 저장
# - GET  /api/download  : data.json 파일 다운로드
#


from flask import Flask, request, jsonify, send_file
from pathlib import Path
import json, os

app = Flask(__name__)

DATA_PATH = Path("/app/data/data.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]", encoding="utf-8")

@app.get("/healthz")
def healthz():
    return "ok", 200

# 아래 엔드포인트들을 구현하세요.
# @app.get("/api/records")
# def get_records():
#     raise NotImplementedError
@app.get("/api/records")
def get_records():
    json_text = DATA_PATH.read_text(encoding="utf-8")

    if not json_text:
        return jsonify([]), 200
    
    data = json.loads(json_text)
    return jsonify(data), 200

# @app.post("/api/records")
# def add_record():
#     raise NotImplementedError
@app.post("/api/records")
def add_record():
    payload = request.get_json()

    if not payload:
        return jsonify({"error": "JSON 데이터가 비어있습니다."}), 400

    height = payload.get("height")
    weight = payload.get("weight")

    if not height or not weight:
         return jsonify({"error": "'height'와 'weight' 값은 필수입니다."}), 400  
    if not (isinstance(height, (int, float)) and height > 0):
         return jsonify({"error": "'height'는 0보다 큰 숫자여야 합니다."}), 400
    if not (isinstance(weight, (int, float)) and weight > 0):
         return jsonify({"error": "'weight'는 0보다 큰 숫자여야 합니다."}), 400

    new_record = {"height": height, "weight": weight}

    current_data = []
    json_text = DATA_PATH.read_text(encoding="utf-8")

    if json_text:
        current_data = json.loads(json_text)

        if not isinstance(current_data, list):
            currnet_data = []

    current_data.append(new_record)

    DATA_PATH.write_text(json.dumps(current_data, indent=2, ensure_ascii=False), encoding="utf-8")

    return jsonify(new_record), 201
# @app.get("/api/download")
# def download_json():
#     raise NotImplementedError
@app.get("/api/download")
def download_json():
    
    return send_file(
        DATA_PATH,
        as_attachment=True,
        download_name="records.json"
    )

if __name__ == "__main__":
    # 적절한 포트(예: 5000)로 0.0.0.0 에서 실행
    app.run(host="0.0.0.0", port=5000)
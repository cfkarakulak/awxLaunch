from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    data = request.get_json(force=False)
    
    try:
        tag = data['tag']
    except:
        return jsonify({
            "success": False,
            "error": "Missing parameter: tag"
        })

    headers = {
        "User-agent": "zinc-awx-client",
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46YWs2NGNrOTQ="
    }

    templates = requests.get("http://34.123.174.145/api/v2/job_templates", headers=headers)
    
    try:
        job_id = [x['id'] for x in templates.json()['results'] if x['name'] == 'JL2 Goto'][0]
    except:
        return jsonify({
            "success": False,
            "error": "Can't find job id for JL2 Goto"
        })
        
    launch = requests.post(
        url=f"http://34.123.174.145/api/v2/job_templates/{job_id}/launch",
        headers=headers,
        data={
            "extra_vars": {
                "tag": tag,
            }
        },
    )
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

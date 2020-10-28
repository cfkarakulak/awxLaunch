from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

URL = "http://34.123.174.145"

@app.route('/', methods=['POST'])
def home():
    text = request.form.get('text', None)
    
    if not text:
        return jsonify({
            "success": False,
            "error": "Missing parameter: text"
        })
        
    params = text.split(' ')
    
    try:
        JOB = str(params[0])
        TAG = str(params[1])
    except:
        return jsonify({
            "success": False,
            "error": "Missing parameter: JOB or TAG"
        })

    headers = {
        "User-Agent": "zinc-awx-client",
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46YWs2NGNrOTQ=" # dont store it like this on production
    }

    templates = requests.get(
        url=f"{URL}/api/v2/job_templates",
        headers=headers,
    )
    
    try:
        job_id = [x['id'] for x in templates.json()['results'] if x['name'] == (JOB + 'Jump')][0]
    except:
        return jsonify({
            "success": False,
            "error": f"Can't find job id for {JOB}Jump"
        })
        
    awx_data = {
        "extra_vars": {
            "tag": TAG
        }
    }    
    
    launch = requests.post(
        url=f"{AWX}/api/v2/job_templates/{job_id}/launch/",
        headers=headers,
        json=awx_data,
    )
    
    return jsonify({
        "response_type": "in_channel",
        "text": f"Goto {TAG} command for {JOB} received, will run shortly", 
    })
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

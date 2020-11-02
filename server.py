from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

URL = "http://34.123.174.145"

ALLOWED_CHANNELS = {
    'jl-deploys': 'G01D6U7BWTW',
}

ALLOWED_USERS = {
    'cemre': 'U010V29AVSA',
    'eric': 'U0ELWGVGT',
    'oz': 'UJ0A0J4LX',
}

@app.route('/', methods=['POST'])
def home():
    user_id = request.form.get('user_id')
    channel_id = request.form.get('channel_id')
    
    if not user_id in ALLOWED_USERS.values():
        return jsonify({
            "response_type": "in_channel",
            "text": f"You do not have permission to run this command",
        })
    
    if not channel_id in ALLOWED_CHANNELS.values():
        return jsonify({
            "response_type": "in_channel",
            "text": f"This command is only available in #jl-deploys channel",
        })
        
    text = request.form.get('text', None)
        
    if not text:
        return jsonify({
            "response_type": "in_channel",
            "error": "Missing parameter: text",
        })
        
    params = text.split(' ')
    
    try:
        JOB = str(params[0])
        TAG = str(params[1])
    except:
        return jsonify({
            "response_type": "in_channel",
            "error": "Missing parameter: JOB or TAG"
        })

    headers = {
        "User-Agent": "zinc-awx-client",
        "Content-Type": "application/json",
        "Authorization": "Basic ZGVwbG95Ym90OjQ4TG1XdnJSOTZhTXhhUkh1bVE3VldqOUZ1eVVVUHVE" # deploybot cant do much tho @cemre change it pls.
    }

    templates = requests.get(
        url=f"{URL}/api/v2/job_templates",
        headers=headers,
    )
    
    try:
        job_id = [x['id'] for x in templates.json()['results'] if x['name'] == (JOB + 'JumpToSpecificVersion')][0]
    except:
        return jsonify({
            "response_type": "in_channel",
            "error": f"Can't find job id for {JOB}JumpToSpecificVersion"
        })
        
    awx_data = {
        "extra_vars": {
            "tag": TAG
        }
    }    
    
    launch = requests.post(
        url=f"{URL}/api/v2/job_templates/{job_id}/launch/",
        headers=headers,
        json=awx_data,
    )
    
    return jsonify({
        "response_type": "in_channel",
        "text": f"Goto {TAG} command for {JOB} received, will run shortly", 
    })
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

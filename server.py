from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    data = request.get_json(force=True)
    
    tag = data['tag']
    
    return tag
    
    headers = {
        "User-agent": "zinc-awx-client",
        "Content-Type": "application/json",
        "Authorization": "Basic YWRtaW46YWs2NGNrOTQ="
    }

    templates = requests.get("http://34.123.174.145/api/v2/job_templates", headers=headers)
    
    job_id = [x['id'] for x in templates.json()['results'] if x['name'] == 'JL2 Goto'][0]
    
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
    app.run(debug=True)

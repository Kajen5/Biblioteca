import urllib3
import requests
import json
import requests

# Paste your Watson Machine Learning service apikey here
if __name__ == '__main__':
    # Use the rest of the code sample as written
    credent = {
        "apikey": "b65j918SA224fVMJYxBPdEs_2FNlZqiYkNdIBZrBOMFm",
        "iam_apikey_description": "Auto-generated for key 1b27e835-49af-4704-a556-609b43a30ff3",
        "iam_apikey_name": "wdp-writer",
        "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
        "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/373bdd43af874dffb94e80914f533390::serviceid:ServiceId-b712216b-c9d2-4f31-958f-8115ebf58258",
        "instance_id": "73af7d75-f76e-4e28-81fc-b2e11cdd00ea",
        "url": "https://us-south.ml.cloud.ibm.com"
    }
    apikey = credent['apikey']

    # Get an IAM token from IBM Cloud
    url = "https://iam.bluemix.net/oidc/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = "apikey=" + apikey + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    IBM_cloud_IAM_uid = "bx"
    IBM_cloud_IAM_pwd = "bx"
    response = requests.post(url, headers=headers, data=data, auth=(
        IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd))
    iam_token = response.json()["access_token"]
# NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' +
              iam_token, 'ML-Instance-ID': credent['instance_id']}
    array_of_values_to_be_scored = [
        6000, 'Spain', 'Male', 37, 3555, 56454.5, 55, 0, 0, 50000.5]
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance",
                                                  "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"], "values": [array_of_values_to_be_scored]}]}

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/v4/deployments/72c5d66b-384d-4cd3-afc1-2a38b01855d1/predictions', json=payload_scoring, headers=header)
    print("Scoring response")
    print(json.loads(response_scoring.text))

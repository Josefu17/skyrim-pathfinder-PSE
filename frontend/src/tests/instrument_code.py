import requests

# TODO: since such a server does not exist -> find alternative
# url of an instrumenting online-service
api_url = "https://your-instrumentation-api.example.com"

# Local file path
input_file = "./frontend/src/js/path_finder.js"
output_file = "./frontend/src/tests/instrumented/path_finder.instrumented.js"

# Read the original file
with open(input_file, "r") as file:
    code = file.read()

# Send the code to the API
response = requests.post(api_url, data={"code": code})
if response.status_code == 200:
    # Save the instrumented code
    with open(output_file, "w") as file:
        file.write(response.text)
    print(f"Instrumented code saved to {output_file}")
else:
    print("Instrumentation failed:", response.text)

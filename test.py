from flask import Flask, request

app = Flask(__name__)

@app.route('/esp32-data', methods=['POST'])
def handle_post_request():
    data = request.get_json()  # Assuming JSON data is sent in the request
    # Process and respond to the data as needed
    print("Received data:", data)
    return "Data received and processed successfully."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 

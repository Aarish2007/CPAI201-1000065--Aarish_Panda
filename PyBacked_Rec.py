from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/start-streamlit', methods=['GET'])
def start_streamlit():
    try:
        # Command to start Streamlit
        streamlit_cmd = ['streamlit', 'run', os.path.join("C:\Users\AARISH\OneDrive\Desktop\capstone123", "app.py")]
        subprocess.Popen(streamlit_cmd, shell=True)  # Run as a background process
        return jsonify({"status": "success", "message": "Streamlit server started"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)

pp = Flask(__name__)
from flask import Flask, request, jsonify
from captions import get_video_id, print_captions
import io
import sys
from contextlib import redirect_stdout

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/transcript', methods=['POST'])
def get_transcript():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "URL is required"}), 400
        
        url = data['url']
        
        # Capture the output from print_captions
        output = io.StringIO()
        with redirect_stdout(output):
            print_captions(url)
        
        transcript_text = output.getvalue()
        
        return jsonify({
            "success": True,
            "transcript": transcript_text,
            "url": url
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

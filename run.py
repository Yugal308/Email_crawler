from app import app

if __name__ == '__main__':
    print("Starting Flask application...")
    print("Please visit http://127.0.0.1:8000 in your browser")
    app.run(debug=True, port=8000) 
from app import create_app

app = create_app()

# flask run --port 3001

if __name__ == "__main__":
    app.run(debug=True)
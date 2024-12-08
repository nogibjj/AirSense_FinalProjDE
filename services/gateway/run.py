from app import create_app

# Create the app using the factory
app = create_app()

if __name__ == "__main__":
    # Run the app
    app.run(debug=True)

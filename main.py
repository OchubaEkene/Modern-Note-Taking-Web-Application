from website import create_App

app = create_App() # Create the Flask application instance

if __name__ == '__main__': # Run the application
    app.run(debug=True, port=5001)
    


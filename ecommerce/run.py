from app import create_app

app = create_app()

@app.route('/')
def welcome():
    return 'Welcome User!'

if __name__ == '__main__':
    app.run()
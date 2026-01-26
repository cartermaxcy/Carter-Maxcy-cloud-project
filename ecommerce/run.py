from app import create_app

app = create_app()

@app.route('/')
def welcome():
    return """
    Welcome User!
    Register, login, select inventory, then checkout on the products page. Append the following to the URL to view each page:
    /browser/register,
    /browser/login,
    /browser/inventory,
    /browser/products
    """

if __name__ == '__main__':
    app.run()
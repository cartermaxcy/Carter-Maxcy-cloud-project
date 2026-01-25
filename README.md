# Carter-Maxcy-cloud-project

For the eccomerce application please cd into that directory and run:

python -m venv venv

source venv/bin/activate

## Features
This is a product inventory and managment Flask application.

Users register and login and are able to view an inventory of items that can be added to a cart.

After adding items the user can view the contents of the cart formatted with each item. When they select the
checkout button the contents of the cart are written to cloud storage and the current cart is claered, allowing
for more items to be added to a separate cart and the process repeated.

The browser is the primary way the app is intended to be used however there are pure API ways access some app
functionality as well such as registering, logging in, and viewing products. Please ensure the usage here is 
consistent. Cookies saved when using the pure API version via Curl commands won't be accesible when switching
over to the browser for example.

pytest is utilized for the unit tests where the API paths have fake inputs constructed and the expected output
verified. The setup can be extended so that other API endpoints can be tested via unit tests in a way that is
fast and simple.

Cart managment is implimented with a local DB. An in memory SQLite DB can be considered as this DB's use is 
just to track the user's products at the time they are creating the cart. The in memory SQLite DB is also 
used for unit testing to ensure the endpoints work as expected. Flask SQLAlchemy is used and the DB setup
passed via .env (covered below).

HTML forms are used to enable a browser interface. This is used to render the register, login, inventory,
product page with checkout. Buttons in the HTML are embedded that invoke the API command used to checkout
and send the user's products over to the AWS storage. For login and register HTML forms are used then the
data parsed on the Flask side to perform these functions.

Rate limiting is implimented for API calls to prevent these from being spammed. Values are chosen so that
the intuitive usage of the app are able to work just fine. Only when manually testing out features quickly
is when these are expected to be triggered assuming normal app usage, and any bad usage should be caught 
and slowed by these limits.

An example of load balancing can be found in the standalone loadbalancer folder. This demonstrates how 
load balancing could be applied to the eccomerce or similar apps to prevent server overload.

## Challenges
During development a number of challenges were encountered.

I wanted to make sure the actual code paths that were being used in the browser were being tested as much
as possible while still not manually spinning up the browser for every last bit of behavior verification.
By abstracting logic into a get_products_internal() that means that the API tests go through almost all
of the code paths that are used for the browser and provides some assurance of correctness.

When midway through setting up the browser support I ran into issues testing. Before a browser I was
testing API calls all through the terminal using Curl. This was keeping cookies for the login data 
on the backend, so when I tried to impliment half of the browser then go through the Curl commands,
I didn't see the expected results in the browser. I went ahead and got all of the browser functionality
working and testing through there so that the cookies remain in the expected place (staying on the browser
when this is what is expected).

The Jinja syntax requires a mix of HTML and Python like code blocks to access the data sent. Once I
reviewed the API guide and examples I saw how this was to be done but this was not intuitive to me 
at first. I do however see the flexibility this gives you to be able to display data that has been
packed on the python side while staying largely in HTML syntax.

Python's logging module required setting:

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

in each file where the module is imported. This prevented interference with Flask's use of logging
and afterwards the console shows every manual invocation of logging and every API call in a clear
way.

While a production setup would benefit from Docker, this app was developed using Codio. The venv
setup in this case handles package versioning and the app runs on a Codio server whose web page
can be viewed on others' browsers. Codio settings do not appear to allow Docker to be used here
but for a custom hosting setup this should be straightforward to add.

The Python virtual enviroment sets up a venv/ folder and this must be included in the gitignore
to prevent the verbose files from being committed as well. After doing this iteration does not 
require reverting that folder. 

## Configurations

An AWS account is expected, with a DynamoDB named Orders created. The purpose of this is to enable
downstream processing of the contents of this DB to facilitate actual order processing. The region,
AWS access key, and secret access key are to be included in the .env provided (see the example).

In addition to the above users should provide Flask environment variables:

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///:memory:

as can be found in the .env_example which should be changed to .env and that will be picked up by the app.

# Ecommerce-rest-api

Ecommerce-rest-api is an authenticated rest api which supports CRUD operation of products and sellers.

**Endpoints**

| HTTP     | Path           | Action  | Used for|
| ------------- |:-------------:| -----:|-----:|
| POST      | /sellers | create | creating a seller |
| POST      | /sellers      |   update |  update the seller mentioning the id |
| GET | /sellers      |    get |    get seller details |
| GET | /token      |    get |    get token for seller |
| POST      | /products | get | get product details |
| POST      | /products      |   create |  create a new product |
| POST | /products      |    update |    updating an existing product specifying id |
| DELETE | /products      |    delete |    delete product specifying id |

### Tech

Dillinger uses a number of open source projects to work properly:
* [Flask] - Flask is a micro web framework written in Python
* [Mysql] - an open-source relational database management system
* [sqlalchemy] - An object-relational mapper (ORM) for Python
* Other flask extensions mentioned in requirements.

### Installation


```sh
$ git clone  https://github.com/eternalfool/ecommerce-rest-api.git
$ cd ecommerce-rest-api/
$ python setup.py
```
To run application:
```
python run.py
```

### Requirements
* pip install Flask-Testing
* pip install Flask-BasicAuth
* pip install Flask-HTTPAuth
* pip install passlib
* pip install MySQL-python
* pip install Flask-SQLAlchemy
* pip install SQLAlchemy
* pip install flask-mysqldb
* pip install flask-restful
* pip install flask
* pip install python-tk
* sudo apt-get install python-dev python-pip python3-dev python3-pip


### Schema Design

![Schema Design](https://cloud.githubusercontent.com/assets/5109996/16544181/087eb2c0-4119-11e6-9892-afbb2f4c648c.png)

### Usage

**Post request to /sellers to create a new seller**

    curl http://0.0.0.0:5000/sellers -j -H "Content-Type: application/json" --data '{"username": "shashwat", "password":"shashwat", "name": "brotherNero"}'

Response:

    { "id": 44, "isSuccessful": true}

**Get api-token for the seller**

    curl -u shashwat:shashwat "http://0.0.0.0:5000/token"


***Note:*** Passing just the username without the colon (`:`) will cause you to be prompted for your account password. This avoids having your password in your command line history
Response:

    { "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2ODAwNDg2MiwiaWF0IjoxNDY3NDA0ODYyfQ.eyJpZCI6Mzd9.bxhrdVc-KSRbbirv_BG0PnHUdewCy0_mkeeTe7k3sOc"}


**Make a post request to create a new product**

    curl -X POST -H "Content-Type: application/json" -u shashwat:shashwat -d @./create_product.json "http://0.0.0.0:5000/products" 

***Contents of create_product.json***

    {
	"name": "Lifebouy",
	"description1": "Tandarusti ki raksha karta hai lifebouy",
	"description2": "Lifebouy hai jahan tandarusti hai wahan",
	"sku_id": "SKU-86e467-UKS",
	"price": "99.95",
	"image_urls": "['http://www.lifebuoy.co.za/Resources/Images/logo.gif']",
	"video_urls": "['https://www.youtube.com/watch?v=VsnP_6kdtDY', 'https://www.youtube.com/watch?v=AOU3ZIrUiVM']",
	"discount": "7.50",
	"coupons": "['WNG50', 'FP40']",
	"available_colors": "['RED', '0x454']",
	"weight": "45.76 gms"
}

Response:

    { "id": 41, "isSuccessful": true}

**Make a post request update an existing product**

    curl -X POST -H "Content-Type: application/json" -u shashwat:shashwat -d @./update_product.json "http://0.0.0.0:5000/products" 

***Contents of update_product.json***

    {
    "id": 41,
    "name": "Dettol",
    "description1": "Dettol Dettol Dettol Dettol",
    "description2": "Dettol Dettol Dettol Dettol Ho",
    "sku_id": "SKU-96ghi7-UKS",
    "price": "95.95",
    "image_urls": "['http://www.dettol.co.in/media/1463092/Dettol-original-Soap-Packshot-300-X-600.jpg']",
    "video_urls": "['https://www.youtube.com/watch?v=iiGAPr9Vl0U']",
    "discount": "5.50",
    "coupons": "['DD50', 'FP40']",
    "available_colors": "['BLUE', '0x454']",
    "weight": "75.46 gms" 
    }

Response:

    { "id": 41, "isSuccessful": true}
    
**Get request to get product details**

    curl -u shashwat:shashwat "http://0.0.0.0:5000/products"

Response:

    {
	"data": [{
		"available_colors": null,
		"coupons": null,
		"creation_date": "Fri, 01 Jul 2016 13:45:22 -0000",
		"description1": null,
		"description2": null,
		"discount": null,
		"id": 31,
		"image_urls": null,
		"is_active": true,
		"last_update": "Fri, 01 Jul 2016 13:45:22 -0000",
		"name": "new Poduct",
		"price": null,
		"seller_id": 37,
		"sku_id": null,
		"video_urls": null,
		"weight": "500 pounds"
	}, {
		"available_colors": "['BLUE', '0x454']",
		"coupons": "['DD50', 'FP40']",
		"creation_date": "Sat, 02 Jul 2016 02:06:01 -0000",
		"description1": "Dettol Dettol Dettol Dettol",
		"description2": "Dettol Dettol Dettol Dettol Ho",
		"discount": "5.50",
		"id": 41,
		"image_urls": "['http://www.dettol.co.in/media/1463092/Dettol-original-Soap-Packshot-300-X-600.jpg']",
		"is_active": true,
		"last_update": "Sat, 02 Jul 2016 02:29:48 -0000",
		"name": "Dettol",
		"price": "95.95",
		"seller_id": 37,
		"sku_id": "SKU-96ghi7-UKS",
		"video_urls": "['https://www.youtube.com/watch?v=iiGAPr9Vl0U']",
		"weight": "75.46 gms"
	}]
}
    
    
**Delete a product**

    curl -X DELETE -u shashwat:shashwat "http://0.0.0.0:5000/products?id=41" 

Response:

    { "id": 44, "isSuccessful": true}

### Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantanously see your updates!

Open your favorite Terminal and run these commands.

First Tab:
```sh
$ node app
```

Second Tab:
```sh
$ gulp watch
```

(optional) Third:
```sh
$ karma start
```
### Docker
Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 80, so change this within the Dockerfile if necessary. When ready, simply use the Dockerfile to build the image.

```sh
cd dillinger
docker build -t <youruser>/dillinger:latest .
```
This will create the dillinger image and pull in the necessary dependencies. Once done, run the Docker and map the port to whatever you wish on your host. In this example, we simply map port 80 of the host to port 80 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 80:80 --restart="always" <youruser>/dillinger:latest
```

Verify the deployment by navigating to your server address in your preferred browser.

### N|Solid and NGINX

More details coming soon.

#### docker-compose.yml

Change the path for the nginx conf mounting path to your full path, not mine!

### Todos
 - Read log configurations from a file.
 - Pagination on get_products.
 - bulk creation / deletion of products.
 - add more information to unauthorized requests (get token by invalid username, duplicate username while creating seller)
 - Write negative test cases.


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [Flask]: <http://flask.pocoo.org/>
   [Mysql]: <https://www.mysql.com/>
   [Sqlalchemy]: <http://www.sqlalchemy.org/>
   [@thomasfuchs]: <http://twitter.com/thomasfuchs>


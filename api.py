from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from flask_restx import Api, Namespace, Resource
import pandas as pd

user = "root"
passw = ''
host = ""
database = "main"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = host

# Authentication
auth_db = {
    "xxxxxx"
}

api = Api(app, version = '1.0',
    title = 'Rodrigo Escolar API',
    description = """
        Load and obtain data from the H&M dataset
        """,
    contact = "rescolar@student.ie.edu",
    endpoint = "/api/v1"
)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

def query_all(query):
    conn = connect()
    result = conn.execute(text(query)).mappings().all()
    disconnect(conn)
    return jsonify({'result': [dict(row) for row in result]})


## LOAD DATA
load_data = Namespace('Load Data',
    description = 'Load Tables to SQL Database',
    path='/api/v1')
api.add_namespace(load_data)
@load_data.route('/load_table/<table_name>',methods=['POST'])
class load_table(Resource):
    def post(self, table_name):
        if "Authorization" not in request.headers:
            return jsonify({"error": "unauthorized access"})
        else:
            token = request.headers['Authorization'].split()[1]
            if token in auth_db:
                table_json = request.get_json()
                df = pd.read_json(table_json)
                print(df.info())
                df.to_sql(name = f'{table_name}', con = connect(), if_exists = 'replace', index = False)
                return  201
            else:
                return jsonify({'error': 'token provided is incorrect'})


## CUSTOMERS DATA
customers = Namespace('Customers',
    description = 'All operations related to customers',
    path='/api/v1')
api.add_namespace(customers)
@customers.route("/customers")
class get_all_customers(Resource):
    def get(self):
        if "Authorization" not in request.headers:
            return jsonify({"error": "unauthorized access"})
        else:
            token = request.headers['Authorization'].split()[1]
            if token in auth_db:
                select = """
                SELECT *
                FROM customers
                LIMIT 100000;
                """
           
                return query_all(select)
            else:
                return jsonify({'error': 'token provided is incorrect'})

## ARTICLES DATA
articles = Namespace('Articles',
    description = 'All information related to articles',
    path='/api/v1')
api.add_namespace(articles)
@articles.route("/articles")
class get_all_articles(Resource):
    def get(self):
        if "Authorization" not in request.headers:
            return jsonify({"error": "unauthorized access"})
        else:
            token = request.headers['Authorization'].split()[1]
            if token in auth_db:
                select = """
                    SELECT *
                    FROM articles
                    LIMIT 100000;"""
                return query_all(select)
            else:
                 return jsonify({'error': 'token provided is incorrect'})


# SEARCH ARTICLE
@articles.route("/articles/<article_name>")
class search_article(Resource):
    def get(self, article_name):
        if "Authorization" not in request.headers:
            return jsonify({"error": "unauthorized access"})
        else:
            token = request.headers['Authorization'].split()[1]
            if token in auth_db:
                select = f"""
                    SELECT product_code, product_type_name, product_group_name, colour_group_name
                    FROM articles
                    WHERE product_type_name = '{article_name}';"""
                return query_all(select)
            else:
                return jsonify({'error': 'token provided is incorrect'})

## TRANSACTIONS DATA
transactions = Namespace('Transactions',
    description = 'All information related to transactions',
    path='/api/v1')
api.add_namespace(transactions)

@transactions.route("/transactions")
class get_all_transactions(Resource):
    def get(self):
        if "Authorization" not in request.headers:
            return jsonify({"error": "unauthorized access"})
        else:
            token = request.headers['Authorization'].split()[1]
            if token in auth_db:
                select = """
                    SELECT *
                    FROM transactions
                    LIMIT 100000;"""
                return query_all(select)
            else:
                return jsonify({'error': 'token provided is incorrect'})
   


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True, port=8080)

from flask import Flask, jsonify, request
from functools import wraps

# Dados fictícios de produtos
products = [
    {
        "name": "Protetor Solar Facial Anthelios XL-Protect Cor Morena FPS 60 Gel Creme 40g",
        "description": "PROTETOR SOLAR FACIAL ANTHELIOS XL-PROTECT COR MORENA FPS 60 GEL CREME Pele extremamente sensível a queimadura solar.",
        "originalValue": 69.29,
        "currentValue": 45.29,
        "category": "Protetor Solar",
        "brand": "Anthelios",
        "unitType": "",
        "unitQuantity": 150,
        "extras": None,
        "images": [
            {
                "imageUrl": "https://s3-sa-east-1.amazonaws.com/i.imgtake.takenet.com.br/ieq09onpj2/ieq09onpj2.png",
                "order": 1
            }
        ],
        "sku": "abc"
    },
    {
        "name": "Lavitan Cabelos e Unhas 60 Cápsulas",
        "description": "Suplemento vitamínico-mineral. Auxilia no crescimento e fortalecimento de cabelos e unhas. Lavitan Cabelos e Unhas é um suplemento que possui ação antioxidante, além de ajudar a evitar a queda e na manutenção da saúde dos cabelos, além de deixar suas unhas muito mais fortes e saudáveis.",
        "originalValue": 41.29,
        "currentValue": 34.99,
        "category": "Nutricosméticos",
        "brand": "Lavitan",
        "unitType": "",
        "unitQuantity": 150,
        "extras": None,
        "images": [
            {
                "imageUrl": "https://s3-sa-east-1.amazonaws.com/i.imgtake.takenet.com.br/indh43e088/indh43e088.png",
                "order": 1
            }
        ],
        "sku": "cde"
    },
    {
        "name": "Protetor Solar Facial Isdin Fusion Water Oil Control FPS 60 com 30ml",
        "description": "Fusion Water 5 Stars é um protetor solar facial especialmente criado para o uso diário. Com FPS 60 garante muito alta proteção.",
        "originalValue": 69.99,
        "currentValue": 69.99,
        "category": "Protetor Solar",
        "brand": "Isdin",
        "unitType": "",
        "unitQuantity": 150,
        "extras": None,
        "images": [
            {
                "imageUrl": "https://s3-sa-east-1.amazonaws.com/i.imgtake.takenet.com.br/ii0mntjaiq/ii0mntjaiq.png",
                "order": 1
            }
        ],
        "sku": "egv"
    },
    {
        "name": "Toalhas Umedecidas MamyPoko Dia e Noite 200 Unidades",
        "description": "",
        "originalValue": 25.49,
        "currentValue": 24.49,
        "category": "Lenços Umedecidos",
        "brand": "Mamypoko",
        "unitType": "",
        "unitQuantity": 150,
        "extras": None,
        "images": [
            {
                "imageUrl": "https://s3-sa-east-1.amazonaws.com/i.imgtake.takenet.com.br/isldfab19m/isldfab19m.png",
                "order": 1
            }
        ],
        "sku": "eghv"
    },
    {
        "name": "Cadeira Gamer Reclinável e Giratória com Apoio Retrátil para Pés Azul GT13 - DPX",
        "description": "Desenvolvida especialmente para quem busca ter muito mais conforto, a Cadeira Gamer da DPX conta com o design sofisticado e a segurança que você necessita no dia a dia. Ideal para quem é apaixonado por games, trabalha em casa ou necessita de mais conforto para desempenhar o melhor dos dias, possui estrutura com alta qualidade. Com o design moderno, essa cadeira gamer deixa a lombar no conforto que você merece para passar por longas horas sentado. Com ela você tem muito mais segurança, ergonomia e conforto. A Cadeira Gamer da DPX deixará o seu ambiente muito mais moderno e preparado para as horas de diversão ou de trabalho. Conte com a comodidade na sua casa. DPX é uma marca própria da Americanas. Desenvolvemos produtos pensando em você, com MAIS qualidade e MENOS preço. Temos tuuudo o que você precisa! Uma boa estrutura com equipamentos de qualidade é o diferencial que todo gamer precisa. Escolha a DPX para o seu set up e veja sua performance decolar! Com mouses ergonômicos, cadeiras gamers, fones e teclados de alta tecnologia, o seu tempo de jogo, além de divertido, será confortável e de qualidade. Você vai subir o nível do seu game! Imagens meramente ilustrativas. Todas as informações divulgadas são de responsabilidade do Fabricante/Fornecedor.",
        "originalValue": 1899.99,
        "currentValue": 1899.99,
        "category": "cadeira gamer",
        "brand": "DPX",
        "unitType": "",
        "unitQuantity": 150,
        "extras": {
            "option1": "Cores",
            "values1": [
                {
                    "name": "Cadeira Gamer Reclinável e Giratória com Apoio Retrátil para Pés Vermelha GT13 - DPX",
                    "valueAddition": 150.0
                }
            ],
            "option2": None,
            "values2": None
        },
        "images": [
            {
                "imageUrl": "https://s3-sa-east-1.amazonaws.com/i.imgtake.takenet.com.br/i0py2w0mir/i0py2w0mir.png",
                "order": 1
            }
        ],
        "sku": "44333212"
    }
]

# Token de acesso para controle de autenticação
api_token = "abcde"

# Criando a aplicação Flask
app = Flask(__name__)

# Middleware para verificar o token de acesso
def verify_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Token')

        if not token or token != api_token:
            return jsonify({"message": "Acesso não autorizado"}), 401

        return f(*args, **kwargs)

    return decorated_function

# Configurando os endpoints protegidos com verificação de token

# Endpoint /api/products (GET) para retornar a lista de produtos
@app.route('/api/products', methods=['GET'])
@verify_token
def get_products():
    return jsonify({"products": products})

# Endpoint /api/products (POST) para filtrar produtos
@app.route('/api/products', methods=['POST'])
@verify_token
def filter_products():
    req_data = request.json
    filter_keyword = req_data.get('filter', '')
    brands_filter = req_data.get('brands', [])
    categories_filter = req_data.get('categories', [])

    filtered_products = []
    for product in products:
        # Verifica se o filtro está presente no nome, descrição, categoria ou marca do produto
        if (filter_keyword.lower() in product['name'].lower() or
            filter_keyword.lower() in product['description'].lower() or
            filter_keyword.lower() in product['category'].lower() or
            filter_keyword.lower() in product['brand'].lower()):

            # Verifica se a marca está presente nos filtros ou se a lista de marcas filtradas está vazia
            if not brands_filter or product['brand'] in brands_filter:
                # Verifica se a categoria está presente nos filtros ou se a lista de categorias filtradas está vazia
                if not categories_filter or product['category'] in categories_filter:
                    filtered_products.append(product)

    return jsonify({"products": filtered_products})

# Endpoint /api/products/categories (GET) para retornar categorias de produtos únicas
@app.route('/api/products/categories', methods=['GET'])
@verify_token
def get_categories():
    categories = set(product['category'] for product in products)
    categories_list = [{"name": category} for category in categories]
    return jsonify({"categories": categories_list})

# Endpoint /api/products/brands (GET) para retornar marcas de produtos únicas
@app.route('/api/products/brands', methods=['GET'])
@verify_token
def get_brands():
    brands = set(product['brand'] for product in products)
    brands_list = [{"name": brand} for brand in brands]
    return jsonify({"brands": brands_list})

# Endpoint /api/products/{sku} (GET) para retornar detalhes de um produto específico
@app.route('/api/products/<string:sku>', methods=['GET'])
@verify_token
def get_product_by_sku(sku):
    for product in products:
        if product['sku'] == sku:
            return jsonify(product)
    return jsonify({"message": "Produto não encontrado"}), 404

# Endpoint /api/products/relatedProducts/{sku} (GET) para retornar produtos relacionados
@app.route('/api/products/relatedProducts/<string:sku>', methods=['GET'])
@verify_token
def get_related_products(sku):
    related_products = []
    for product in products:
        if product['sku'] == sku:
            related_category = product['category']
            related_products = [p for p in products if p['category'] == related_category]

    if related_products:
        return jsonify({
            "relatedProducts": [
                {
                    "title": "Mais Vistos",
                    "products": related_products[:10]  # Limitando a 10 produtos apenas para exemplo
                }
            ]
        })
    else:
        return jsonify({"message": "Não há produtos relacionados disponíveis"}), 404

# Executando a aplicação Flask
app.run(debug=True)
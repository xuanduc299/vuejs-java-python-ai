# from transformers import GPT2LMHeadModel, GPT2Tokenizer

# # Load tokenizer và model
# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# model = GPT2LMHeadModel.from_pretrained("gpt2")

# # Hàm sinh câu trả lời từ mô hình
# def generate_response(user_input):
#     inputs = tokenizer.encode(user_input, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=50, do_sample=True, top_p=0.95, top_k=60)
#     response = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return response


##### ver 2 app.py

# import pandas as pd
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from fuzzywuzzy import fuzz

# # Đọc dữ liệu từ file Excel
# df = pd.read_csv('dataset_nike2.csv')
# # Đọc dữ liệu từ file Excel
# # df = pd.read_excel('dataset_nike2.xlsx')
# # df.to_csv('dataset_nike2.csv', encoding='utf-8', index=False)

# app = Flask(__name__)
# CORS(app)

# def get_description(product_name):
#     # Lấy mô tả với độ tương tự cao nhất
#     best_match = None
#     highest_ratio = 0
    
#     # Duyệt qua từng hàng trong DataFrame để tìm câu hỏi khớp nhất
#     for index, row in df.iterrows():
#         # Tính toán tỷ lệ tương tự giữa câu hỏi của người dùng và câu hỏi trong file
#         ratio = fuzz.partial_ratio(product_name.lower(), row['product_name'].lower())
        
#         # Nếu tỷ lệ cao hơn giá trị đã có, lưu câu hỏi và tỷ lệ này
#         if ratio > highest_ratio:
#             highest_ratio = ratio
#             best_match = row['description']  # Lấy mô tả của sản phẩm này
    
#     # Nếu tỷ lệ tương tự lớn hơn ngưỡng (ở đây là 70%), trả về mô tả
#     if highest_ratio > 70:
#         return best_match
#     else:
#         return "Sản phẩm không được tìm thấy."

# @app.route('/chatbot/', methods=['POST'])
# def api_get_description():
#     # Lấy dữ liệu JSON từ yêu cầu
#     data = request.json
#     product_name = data.get('message', '')
    
#     # Gọi hàm tìm mô tả sản phẩm
#     description = get_description(product_name)
    
#     # Trả về kết quả dưới dạng JSON
#     return jsonify({"response": description})

# if __name__ == '__main__':
#     app.run(debug=True)


#### verr 3 
# import pandas as pd
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from fuzzywuzzy import fuzz
# import json

# # Đọc dữ liệu từ file CSV
# df = pd.read_csv('dataset_nike2.csv')
# # df = pd.read_excel('dataset_nike2.xlsx')
# # df.to_csv('dataset_nike2.csv', encoding='utf-8', index=False)

# # Khởi tạo ứng dụng Flask
# app = Flask(__name__)
# CORS(app)

# def get_top_products():
#     # Sắp xếp theo cột "rating" giảm dần và lấy 5 sản phẩm đầu tiên
#     top_products = df.sort_values(by='rating', ascending=False).head(5)
    
#     # Danh sách kết quả sản phẩm
#     top_product_list = []
#     for _, row in top_products.iterrows():
#         # Kiểm tra nếu cột 'images' không phải là NaN và là chuỗi hợp lệ
#         if pd.notna(row['images']) and isinstance(row['images'], str):
#             try:
#                 # Chuyển đổi chuỗi JSON của images thành danh sách
#                 images = json.loads(row['images'])
                
#                 # Lấy ảnh đầu tiên nếu danh sách không rỗng
#                 image_url = images[0] if images else None
#             except json.JSONDecodeError:
#                 image_url = None
#         else:
#             image_url = None
        
#         # Thêm sản phẩm vào danh sách với tên và ảnh đầu tiên
#         top_product_list.append({
#             "product_name": row['product_name'],
#             "image_url": image_url
#         })
    
#     # Trả về danh sách sản phẩm dưới dạng JSON
#     return top_product_list

# def get_sale_price(product_name):
#     # Tìm kiếm sản phẩm theo tên trong cột "product_name"
#     for index, row in df.iterrows():
#         if fuzz.partial_ratio(product_name.lower(), row['product_name'].lower()) > 70:
#             return row['sale_price']
#     return None

# def get_description(product_name):
#     # Nếu người dùng nhắc đến "sản phẩm nổi bật", trả về danh sách top 5 sản phẩm
#     if "sản phẩm nổi bật" in product_name.lower():
#         top_products = get_top_products()
#         return {"top_products": top_products}
    
#     # Nếu người dùng nhắc đến "giá", trả về giá sản phẩm
#     if "giá" in product_name.lower():
#         # Loại bỏ từ "giá" để chỉ lấy tên sản phẩm
#         product_name_cleaned = product_name.lower().split("giá", 1)[1].strip()
        
#         # Tìm kiếm giá của sản phẩm
#         sale_price = get_sale_price(product_name_cleaned)
        
#         if sale_price:
#             return {"response": f"Giá của {product_name_cleaned} là {sale_price} VND."}
#         else:
#             return {"response": "Sản phẩm không được tìm thấy."}
    
#     # Lấy mô tả với độ tương tự cao nhất
#     best_match = None
#     highest_ratio = 0
    
#     # Duyệt qua từng hàng trong DataFrame để tìm câu hỏi khớp nhất
#     for index, row in df.iterrows():
#         # Tính toán tỷ lệ tương tự giữa câu hỏi của người dùng và câu hỏi trong file
#         ratio = fuzz.partial_ratio(product_name.lower(), row['product_name'].lower())
        
#         # Nếu tỷ lệ cao hơn giá trị đã có, lưu câu hỏi và tỷ lệ này
#         if ratio > highest_ratio:
#             highest_ratio = ratio
#             best_match = row['description']  # Lấy mô tả của sản phẩm này
    
#     # Nếu tỷ lệ tương tự lớn hơn ngưỡng (ở đây là 70%), trả về mô tả
#     if highest_ratio > 70:
#         return {"response": best_match}
#     else:
#         return {"response": "Sản phẩm không được tìm thấy."}

# @app.route('/chatbot/', methods=['POST'])
# def api_get_description():
#     # Lấy dữ liệu JSON từ yêu cầu
#     data = request.json
#     product_name = data.get('message', '')
    
#     # Gọi hàm tìm mô tả sản phẩm
#     description = get_description(product_name) 
    
#     # Trả về kết quả dưới dạng JSON
#     return jsonify(description)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0') 




# import pandas as pd
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from fuzzywuzzy import fuzz
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import MultinomialNB
# import joblib
# import json
# import nltk
# from nltk.corpus import wordnet

# # Đọc dữ liệu từ file CSV
# df = pd.read_excel('dataset_nike2.xlsx')

# # Kiểm tra và loại bỏ giá trị NaN trong cột 'product_name' và 'description'
# df.dropna(subset=['product_name', 'description'], inplace=True)

# # Chuẩn bị dữ liệu để huấn luyện mô hình
# X = df['product_name']
# y = df['description']

# # Chuyển đổi văn bản thành vectơ TF-IDF
# vectorizer = TfidfVectorizer()
# X_tfidf = vectorizer.fit_transform(X)

# # Chia tập dữ liệu thành tập huấn luyện và tập kiểm tra
# X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# # Huấn luyện mô hình Naive Bayes
# model = MultinomialNB()
# model.fit(X_train, y_train)

# # Lưu mô hình đã huấn luyện và vectorizer
# joblib.dump(model, 'product_model.pkl')
# joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

# # Khởi tạo ứng dụng Flask
# app = Flask(__name__)
# CORS(app)

# # Hàm lấy sản phẩm nổi bật (không thay đổi)
# def get_top_products():
#     top_products = df.sort_values(by='rating', ascending=False).head(5)
#     top_product_list = []
#     for _, row in top_products.iterrows():
#         if pd.notna(row['images']) and isinstance(row['images'], str):
#             try:
#                 images = json.loads(row['images'])
#                 image_url = images[0] if images else None
#             except json.JSONDecodeError:
#                 image_url = None
#         else:
#             image_url = None
#         top_product_list.append({
#             "product_name": row['product_name'],
#             "image_url": image_url,
#             "product_id": row['product_id'],
#             "slug": row['slug']
#         })
#     return top_product_list

# # Hàm lấy danh sách từ đồng nghĩa
# def get_synonyms(word):
#     synonyms = set()
    
#     for syn in wordnet.synsets(word):
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name())  # Lấy tên của từ đồng nghĩa
    
#     return synonyms

# # Hàm kiểm tra và bổ sung đồng nghĩa vào từ khóa tìm kiếm
# def enhance_with_synonyms(product_name):
#     words = product_name.split()
#     enhanced_words = set(words)  # Tạo một tập các từ (set) để tránh trùng lặp
    
#     # Tìm đồng nghĩa cho mỗi từ và bổ sung vào bộ từ khóa
#     for word in words:
#         synonyms = get_synonyms(word)
#         enhanced_words.update(synonyms)
    
#     return list(enhanced_words)

# # Hàm tìm kiếm mô tả sản phẩm với từ đồng nghĩa
# def get_description_with_synonyms(product_name):
#     enhanced_keywords = enhance_with_synonyms(product_name.lower())  # Tìm từ đồng nghĩa và kết hợp
    
#     best_match = None
#     highest_ratio = 0
    
#     # Duyệt qua các từ đồng nghĩa và tìm sản phẩm khớp nhất
#     for index, row in df.iterrows():
#         # Kiểm tra các từ khóa mở rộng với đồng nghĩa
#         for keyword in enhanced_keywords:
#             ratio = fuzz.partial_ratio(keyword.lower(), row['product_name'].lower())
#             if ratio > highest_ratio:
#                 highest_ratio = ratio
#                 best_match = row['description']  # Lấy mô tả của sản phẩm khớp nhất
    
#     if highest_ratio > 70:
#         return {"response": best_match}
    
#     # Nếu không tìm thấy mô tả phù hợp, sử dụng mô hình học máy dự đoán
#     predicted_description = predict_description(product_name)
    
#     return {"response": predicted_description}

# # Hàm dự đoán mô tả từ mô hình học máy
# def predict_description(product_name):
#     vectorized_input = vectorizer.transform([product_name])
#     prediction = model.predict(vectorized_input)
#     return prediction[0]

# # API Flask để xử lý yêu cầu từ người dùng
# @app.route('/chatbot/', methods=['POST'])
# def api_get_description():
#     data = request.json
#     product_name = data.get('message', '')
    
#     description = get_description_with_synonyms(product_name)
    
#     return jsonify(description)

# if __name__ == '__main__':
#     app.run(debug=True)


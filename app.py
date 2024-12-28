##############ver 4

import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import joblib
import json

# Đọc dữ liệu từ file CSV
# df = pd.read_csv('dataset_nike2.csv')
df = pd.read_excel('dataset_nike2.xlsx')
df.to_csv('dataset_nike2.csv', encoding='utf-8', index=False)

# Kiểm tra và loại bỏ giá trị NaN trong cột 'product_name' và 'description'
df.dropna(subset=['product_name', 'description'], inplace=True)

# Chuẩn bị dữ liệu để huấn luyện mô hình
X = df['product_name']
y = df['description']

# Chuyển đổi văn bản thành vectơ TF-IDF
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)

# Chia tập dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình Naive Bayes
model = MultinomialNB()
model.fit(X_train, y_train)

# Lưu mô hình đã huấn luyện và vectorizer
joblib.dump(model, 'product_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app)

# Hàm lấy sản phẩm nổi bật (không thay đổi)
def get_top_products():
    top_products = df.sort_values(by='rating', ascending=False).head(5)
    
    top_product_list = []
    for _, row in top_products.iterrows():
        if pd.notna(row['images']) and isinstance(row['images'], str):
            try:
                images = json.loads(row['images'])
                image_url = images[0] if images else None
            except json.JSONDecodeError:
                image_url = None
        else:
            image_url = None
        
        top_product_list.append({
            "product_name": row['product_name'],
            "image_url": image_url,
            "product_id": row['product_id'],
            "slug": row['slug']
        })
    
    return top_product_list

def get_top_nike_products():
    # Lọc các sản phẩm có nhãn hàng "Nike"
    nike_products = df[df['brand'].str.contains('Nike', case=False, na=False)]
    
    # Sắp xếp theo cột "rating" giảm dần và lấy 2 sản phẩm đầu tiên
    top_nike_products = nike_products.sort_values(by='rating', ascending=False).head(2)
    
    # Danh sách kết quả sản phẩm
    top_product_list = []
    for _, row in top_nike_products.iterrows():
        # Kiểm tra nếu cột 'images' không phải là NaN và là chuỗi hợp lệ
        if pd.notna(row['images']) and isinstance(row['images'], str):
            try:
                # Chuyển đổi chuỗi JSON của images thành danh sách
                images = json.loads(row['images'])
                
                # Lấy ảnh đầu tiên nếu danh sách không rỗng
                image_url = images[0] if images else None
            except json.JSONDecodeError:
                image_url = None
        else:
            image_url = None
        
        # Thêm sản phẩm vào danh sách với tên và ảnh đầu tiên
        top_product_list.append({
            "product_name": row['product_name'],
            "image_url": image_url,
            "product_id": row['product_id'],
            "slug": row['slug']
        })
    
    # Trả về danh sách sản phẩm dưới dạng JSON
    return top_product_list

def get_top_adidas_products():
    # Lọc các sản phẩm có nhãn hàng "Adidas"
    adidas_products = df[df['brand'].str.contains('Adidas', case=False, na=False)]
    
    # Sắp xếp theo cột "rating" giảm dần và lấy 2 sản phẩm đầu tiên
    top_adidas_products = adidas_products.sort_values(by='rating', ascending=False).head(2)
    
    # Danh sách kết quả sản phẩm
    top_product_list = []
    for _, row in top_adidas_products.iterrows():
        # Kiểm tra nếu cột 'images' không phải là NaN và là chuỗi hợp lệ
        if pd.notna(row['images']) and isinstance(row['images'], str):
            try:
                # Chuyển đổi chuỗi JSON của images thành danh sách
                images = json.loads(row['images'])
                
                # Lấy ảnh đầu tiên nếu danh sách không rỗng
                image_url = images[0] if images else None
            except json.JSONDecodeError:
                image_url = None
        else:
            image_url = None
        
        # Thêm sản phẩm vào danh sách với tên và ảnh đầu tiên
        top_product_list.append({
            "product_name": row['product_name'],
            "image_url": image_url,
            "product_id": row['product_id'],
            "slug": row['slug']
        })
    
    # Trả về danh sách sản phẩm dưới dạng JSON
    return top_product_list

# Hàm lấy giá sản phẩm (không thay đổi)
def get_sale_price(product_name):
    for index, row in df.iterrows():
        if fuzz.partial_ratio(product_name.lower(), row['product_name'].lower()) > 70:
            return row['sale_price']
    return None

def get_tong_sp(product_name):
    for index, row in df.iterrows():
        if fuzz.partial_ratio(product_name.lower(), row['product_name'].lower()) > 70:
            return row['tong_sp']
    return None

def get_chat_lieu(product_name):
    for index, row in df.iterrows():
        if fuzz.partial_ratio(product_name.lower(), row['product_name'].lower()) > 70:
            return row['chat_lieu']
    return None

def get_cong_nghe(product_name):
    for index, row in df.iterrows():
        if fuzz.partial_ratio(product_name.lower(), row['product_name'].lower()) > 70:
            return row['cong_nghe']
    return None

# Hàm sử dụng mô hình học máy để dự đoán mô tả sản phẩm
def predict_description(product_name):
    # Tải mô hình và vectorizer đã lưu
    model = joblib.load('product_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    
    # Chuyển tên sản phẩm thành vectơ TF-IDF
    product_name_vector = vectorizer.transform([product_name])
    
    # Dự đoán mô tả sản phẩm
    predicted_description = model.predict(product_name_vector)
    
    return predicted_description[0]

def get_product_info_by_name(product_name):
    # Tìm kiếm sản phẩm theo tên với fuzzy search
    _product_list = []
    for index, row in df.iterrows():
        if fuzz.partial_ratio(product_name.lower(), row['product_name'].lower()) > 70:
            # Kiểm tra nếu cột 'images' không phải là NaN và là chuỗi hợp lệ
            if pd.notna(row['images']) and isinstance(row['images'], str):
                try:
                    # Chuyển đổi chuỗi JSON của images thành danh sách
                    images = json.loads(row['images'])
                    image_url = images[0] if images else None  # Lấy ảnh đầu tiên nếu có
                except json.JSONDecodeError:
                    image_url = None
            else:
                image_url = None
            _product_list.append({
                "product_name": row['product_name'],
                "image_url": image_url,
                "product_id": row['product_id'],
                "slug": row['slug']
            })
            # Trả về thông tin sản phẩm
            return _product_list
    return None  # Không tìm thấy sản phẩm


def get_description(product_name):
    # Kiểm tra từ khóa "sản phẩm nổi bật"
    # if "" in product_name.lower():
    if any(keyword in product_name.lower() for keyword in ["sản phẩm nổi bật", "mẫu giày nổi bật"]):
        top_products = get_top_products()
        return {"top_products": top_products}
    
    # Kiểm tra từ khóa "giá"
    if "giá" in product_name.lower():
        product_name_cleaned = product_name.lower().split("giá", 1)[1].strip()
        sale_price = get_sale_price(product_name_cleaned)
        
        if sale_price:
            return {"response": f"Giá của {product_name_cleaned} là {sale_price} VND."}
        else:
            return {"response": "Sản phẩm không được tìm thấy."}
        
    if  any(keyword in product_name.lower() for keyword in ["số lượng", "còn"]):
        product_name_cleaned = product_name.lower()
        tong_sp = get_tong_sp(product_name_cleaned)
        
        if tong_sp:
            return {"response": "Sản phẩm này hiện đang còn hàng, bạn có muốn biết thêm thông tin gì về sản phẩm này không?"}
        else:
            return {"response": "Hiện tại sản phẩm này đã hết hàng, cảm ơn quý khách"}
        
    if  any(keyword in product_name.lower() for keyword in ["chất liệu giày"]):
        product_name_cleaned = product_name.lower()
        chat_lieu = get_chat_lieu(product_name_cleaned)
        
        if chat_lieu:
            return {"response": f"Chất liệu của {product_name_cleaned}là {chat_lieu}."}
        else:
            return {"response": "Sản phẩm chưa dc tìm thấy chất liệu."}
    
    if  any(keyword in product_name.lower() for keyword in ["công nghệ giày"]):
        product_name_cleaned = product_name.lower()
        cong_nghe = get_cong_nghe(product_name_cleaned)
        
        if cong_nghe:
            return {"response": f"Công nghệ của {product_name_cleaned}là {cong_nghe}."}
        else:
            return {"response": "Sản phẩm chưa dc tìm thấy công nghệ."}
        
    
      # Kiểm tra từ khóa "mô tả"
    if "mô tả" in product_name.lower():
        product_name_cleaned = product_name.lower().split("mô tả", 1)[1].strip()
        for index, row in df.iterrows():
            if fuzz.partial_ratio(product_name_cleaned.lower(), row['product_name'].lower()) > 70:
                return {"response": f"Mô tả của {row['product_name']} là: {row['description']}"}
        return {"response": "Sản phẩm không được tìm thấy."}
    
     # Kiểm tra từ khóa "Nike" và "bán chạy" hoặc "nổi bật"
    if "nike" in product_name.lower() and any(keyword in product_name.lower() for keyword in ["bán chạy", "yêu thích"]):
        top_nike_products = get_top_nike_products()
        return {"top_nike_products": top_nike_products}
    
     # Kiểm tra từ khóa "Adidas" và "bán chạy" hoặc "nổi bật"
    if "adidas" in product_name.lower() and any(keyword in product_name.lower() for keyword in ["bán chạy", "yêu thích"]):
        top_adidas_products = get_top_adidas_products()
        return {"top_adidas_products": top_adidas_products}
    
    
   # Nếu không có từ khóa "giá" hay "mô tả", kiểm tra tên sản phẩm
    if any(keyword in product_name.lower() for keyword in ["mẫu", "sản phẩm"]):  # Thêm từ khóa phù hợp
        product_info = get_product_info_by_name(product_name)
        
        if product_info:
            return {"select_products": product_info}
    
    # Tìm kiếm mô tả sản phẩm bằng fuzzy search
    best_match = None
    highest_ratio = 0
    
    for index, row in df.iterrows():
        ratio = fuzz.partial_ratio(product_name.lower(), row['product_name'].lower())
        
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = row['description']  # Lấy mô tả của sản phẩm khớp nhất
    
    # Nếu fuzzy search tìm thấy tỷ lệ phù hợp cao (trên 70%)
    if highest_ratio > 70:
        return {"response": best_match}
    
    # Nếu không tìm thấy mô tả phù hợp, sử dụng mô hình học máy dự đoán
    predicted_description = predict_description(product_name)
    
    return {"response": predicted_description}

# API Flask để xử lý yêu cầu từ người dùng
@app.route('/chatbot/', methods=['POST'])
def api_get_description():
    data = request.json
    product_name = data.get('message', '')
    
    description = get_description(product_name) 
    
    return jsonify(description)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


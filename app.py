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


####################ver 2

import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from fuzzywuzzy import fuzz
import json

# Đọc dữ liệu từ file CSV
df = pd.read_csv('dataset_nike2.csv')
# df = pd.read_excel('dataset_nike2.xlsx')
# df.to_csv('dataset_nike2.csv', encoding='utf-8', index=False)

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app)

# def get_top_products():
#     # Sắp xếp theo cột "rating" giảm dần và lấy 5 sản phẩm đầu tiên
#     top_products = df.sort_values(by='rating', ascending=False).head(5)
    
#     # Lấy danh sách tên sản phẩm từ cột "product_name"
#     top_product_names = top_products['product_name'].tolist()
    
#     # Trả về danh sách sản phẩm nổi bật
#     return top_product_names
def get_top_products():
    # Sắp xếp theo cột "rating" giảm dần và lấy 5 sản phẩm đầu tiên
    top_products = df.sort_values(by='rating', ascending=False).head(5)
    
    # Danh sách kết quả sản phẩm
    top_product_list = []
    for _, row in top_products.iterrows():
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
            "image_url": image_url
        })
    
    # Trả về danh sách sản phẩm dưới dạng JSON
    return top_product_list

def get_sale_price(product_name):
    # Tìm kiếm sản phẩm theo tên trong cột "product_name"
    for index, row in df.iterrows():
        if fuzz.partial_ratio(product_name.lower(), row['product_name'].lower()) > 70:
            return row['sale_price']
    return None

def get_description(product_name):
    # Nếu người dùng nhắc đến "sản phẩm nổi bật", trả về danh sách top 5 sản phẩm
    if "sản phẩm nổi bật" in product_name.lower():
        top_products = get_top_products()
        return {"top_products": top_products}
    
    # Nếu người dùng nhắc đến "giá", trả về giá sản phẩm
    if "giá" in product_name.lower():
        # Loại bỏ từ "giá" để chỉ lấy tên sản phẩm
        product_name_cleaned = product_name.lower().split("giá", 1)[1].strip()
        
        # Tìm kiếm giá của sản phẩm
        sale_price = get_sale_price(product_name_cleaned)
        
        if sale_price:
            return {"response": f"Giá của {product_name_cleaned} là {sale_price} VND."}
        else:
            return {"response": "Sản phẩm không được tìm thấy."}
    
    # Lấy mô tả với độ tương tự cao nhất
    best_match = None
    highest_ratio = 0
    
    # Duyệt qua từng hàng trong DataFrame để tìm câu hỏi khớp nhất
    for index, row in df.iterrows():
        # Tính toán tỷ lệ tương tự giữa câu hỏi của người dùng và câu hỏi trong file
        ratio = fuzz.partial_ratio(product_name.lower(), row['product_name'].lower())
        
        # Nếu tỷ lệ cao hơn giá trị đã có, lưu câu hỏi và tỷ lệ này
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = row['description']  # Lấy mô tả của sản phẩm này
    
    # Nếu tỷ lệ tương tự lớn hơn ngưỡng (ở đây là 70%), trả về mô tả
    if highest_ratio > 70:
        return {"response": best_match}
    else:
        return {"response": "Sản phẩm không được tìm thấy."}

@app.route('/chatbot/', methods=['POST'])
def api_get_description():
    # Lấy dữ liệu JSON từ yêu cầu
    data = request.json
    product_name = data.get('message', '')
    
    # Gọi hàm tìm mô tả sản phẩm
    description = get_description(product_name) 
    
    # Trả về kết quả dưới dạng JSON
    return jsonify(description)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 

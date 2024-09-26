import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from fuzzywuzzy import fuzz

# Đọc dữ liệu từ file Excel
df = pd.read_excel('dataset_nike2.xlsx')

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app)

def get_description(product_name):
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
        return best_match
    else:
        return "Sản phẩm không được tìm thấy."

@app.route('/chatbot/', methods=['POST'])
def api_get_description():
    # Lấy dữ liệu JSON từ yêu cầu
    data = request.json
    product_name = data.get('message', '')
    
    # Gọi hàm tìm mô tả sản phẩm
    description = get_description(product_name)
    
    # Trả về kết quả dưới dạng JSON
    return jsonify({"response": description})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

class PlayfairCipher:
    def __init__(self):
        pass

    # Hàm tạo ma trận 5x5 từ Khóa (Key)
    def create_matrix(self, key: str) -> list:
        key = key.upper().replace('J', 'I')  # Gom J vào I
        seen = set()
        matrix_chars = []
        
        # Đưa các ký tự của Key vào trước
        for char in key:
            if char.isalpha() and char not in seen:
                seen.add(char)
                matrix_chars.append(char)
                
        # Điền các ký tự còn lại trong bảng chữ cái (bỏ J)
        for i in range(26):
            char = chr(ord('A') + i)
            if char != 'J' and char not in seen:
                seen.add(char)
                matrix_chars.append(char)
                
        # Chia thành ma trận 5 hàng, mỗi hàng 5 cột
        return [matrix_chars[i:i+5] for i in range(0, 25, 5)]

    # Tìm tọa độ (hàng, cột) của một chữ cái trong ma trận
    def find_coords(self, matrix: list, char: str):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == char:
                    return r, c
        return None

    # Chuẩn hóa bản rõ: tách thành từng cặp, nếu trùng nhau hoặc lẻ thì thêm 'X'
    def prepare_text(self, text: str) -> str:
        text = text.upper().replace('J', 'I')
        pure_text = [char for char in text if char.isalpha()]
        
        prepared = []
        i = 0
        while i < len(pure_text):
            char1 = pure_text[i]
            char2 = pure_text[i+1] if (i + 1) < len(pure_text) else 'X'
            
            if char1 == char2:
                prepared.append(char1)
                prepared.append('X')
                i += 1
            else:
                prepared.append(char1)
                prepared.append(char2)
                i += 2
        return "".join(prepared)

    def playfair_encrypt(self, plain_text: str, key: str) -> str:
        matrix = self.create_matrix(key)
        prepared_text = self.prepare_text(plain_text)
        ciphertext = []
        
        for i in range(0, len(prepared_text), 2):
            r1, c1 = self.find_coords(matrix, prepared_text[i])
            r2, c2 = self.find_coords(matrix, prepared_text[i+1])
            
            if r1 == r2:  # Cùng hàng: dịch phải 1 ô
                ciphertext.append(matrix[r1][(c1 + 1) % 5])
                ciphertext.append(matrix[r2][(c2 + 1) % 5])
            elif c1 == c2:  # Cùng cột: dịch xuống 1 ô
                ciphertext.append(matrix[(r1 + 1) % 5][c1])
                ciphertext.append(matrix[(r2 + 1) % 5][c2])
            else:  # Khác hàng khác cột: đổi góc hình chữ nhật
                ciphertext.append(matrix[r1][c2])
                ciphertext.append(matrix[r2][c1])
                
        return "".join(ciphertext)

    def playfair_decrypt(self, cipher_text: str, key: str) -> str:
        matrix = self.create_matrix(key)
        cipher_text = cipher_text.upper().replace('J', 'I')
        plaintext = []
        
        for i in range(0, len(cipher_text), 2):
            r1, c1 = self.find_coords(matrix, cipher_text[i])
            r2, c2 = self.find_coords(matrix, cipher_text[i+1])
            
            if r1 == r2:  # Cùng hàng: dịch trái 1 ô
                plaintext.append(matrix[r1][(c1 - 1 + 5) % 5])
                plaintext.append(matrix[r2][(c2 - 1 + 5) % 5])
            elif c1 == c2:  # Cùng cột: dịch lên 1 ô
                plaintext.append(matrix[(r1 - 1 + 5) % 5][c1])
                plaintext.append(matrix[(r2 - 1 + 5) % 5][c2])
            else:  # Khác hàng khác cột: đổi góc ngược lại
                plaintext.append(matrix[r1][c2])
                plaintext.append(matrix[r2][c1])
                
        return "".join(plaintext)
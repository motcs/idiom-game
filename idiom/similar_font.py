# -*- coding: utf-8 -*-
import random
import numpy as np
import cv2
import os
from operator import itemgetter
import pygame


def cosine_similarity(vector1, vector2):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a, b in zip(vector1, vector2):
        dot_product += a * b
        normA += a ** 2
        normB += b ** 2
    if normA == 0.0 or normB == 0.0:
        return 0
    else:
        return dot_product / ((normA ** 0.5) * (normB ** 0.5))


def read_img_2_list(img_path):
    # 读取图片
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    # 把图片转换为灰度模式
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).reshape(-1, 1)
    return [_[0] for _ in img.tolist()]


class CharacterMatcher:
    def __init__(self):
        self.chars = []
        self.img_vector_dict = self.get_all_char_vectors()

    def match_char_int(self, _match_char):
        # 获取最接近的汉字
        similarity_dict = {}
        if _match_char in self.img_vector_dict.keys():
            match_vector = self.img_vector_dict[_match_char]
            for char, vector in self.img_vector_dict.items():
                cosine_similar = cosine_similarity(match_vector, vector)
                similarity_dict[char] = cosine_similar
            # 按相似度排序，取前10个
            sorted_similarity = sorted(similarity_dict.items(), key=itemgetter(1), reverse=True)
            return [[char, round(similarity, 4)] for char, similarity in sorted_similarity[:10]]
        else:
            return [[_match_char, 1.0]]

    def if_char_get(self, at, char):
        ft = random.choice(self.chars)
        if ft in at or ft == char:
            self.if_char_get(at, char)
        return ft

    def if_char(self, at, result, char):
        # 结果为空时，从文字中随机选取一个放进去保证不重复
        if result is None or result == []:
            for _ in range(3):
                at.append(self.if_char_get(at, char))
        elif len(result) < 3:
            for _ in range(len(result)):
                at.append(result[_])
            for _ in range(3 - len(result)):
                at.append(self.if_char_get(at, char))
        else:
            for _ in range(3):
                self.if_char_three(at, result, char)

    def if_char_three(self, at, result, char):
        pt = random.choice(result)[0]
        if pt != char and pt not in at:
            at.append(pt)
        else:
            self.if_char_three(at, result, char)

    def find_match_char(self, char):
        at = []
        result = self.match_char_int(char)
        self.if_char(at, result, char)
        return at

    def get_all_char_vectors(self):
        # image_paths = [_ for _ in os.listdir(font_directory) if _.endswith("png")]
        image_paths = self.get_all_files_in_font_directory(1)
        img_vector = {}
        for image_path in image_paths:
            # 提取文件名
            file_name = os.path.basename(image_path)
            # 获取文件名的第一个字符
            first_char = file_name[0]
            img_vector[first_char] = read_img_2_list(img_path=image_path)

        return img_vector

    def get_all_files_in_font_directory(self, int_num):
        script_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录的绝对路径
        font_directory = os.path.join(script_directory, "font")  # 构建 "font" 目录的路径
        if os.path.exists(font_directory) and os.path.isdir(font_directory):
            file_paths = [os.path.join(font_directory, file) for file in os.listdir(font_directory) if
                          os.path.isfile(os.path.join(font_directory, file))]
            return file_paths
        else:
            if int_num <= 3:
                print('没有图片信息，开始生成文字图片:' + int_num)
                self.image_save()
                return self.get_all_files_in_font_directory(int_num + 1)
            else:
                return []

    def image_save(self):
        # 获取3500个汉字
        with open("chinese_characters.txt", "r", encoding="utf-8") as f:
            read = f.read().strip()
            for r in read:
                self.chars.append(r)
        pygame.init()
        # 通过pygame将汉字转化为黑白图片
        for char in self.chars:
            font = pygame.font.Font("C://Windows/Fonts/simkai.ttf", 100)
            rtext = font.render(char, True, (0, 0, 0), (255, 255, 255))
            pygame.image.save(rtext, "font/{}.png".format(char))

    def main_loop(self):
        while True:
            match_char = input("输入汉字: ")
            print(self.find_match_char(match_char))


if __name__ == '__main__':
    character_matcher = CharacterMatcher()
    character_matcher.main_loop()

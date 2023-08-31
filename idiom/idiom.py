import os
import random
import mysql.connector
from similar_font import CharacterMatcher

# 所有的成语全局使用
global_idioms = []


# 从数据库初始化所有的成语
def select_idioms_from_database():
    conn = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="motcs")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT idiom FROM idiom_library")
        idioms = cursor.fetchall()
        global global_idioms
        global_idioms = [idiom[0] for idiom in idioms]

    except mysql.connector.Error as e:
        print("数据库查询出错：", e)

    finally:
        conn.close()


# 随机返回一个成语
def select_random_idiom():
    return random.choice(global_idioms)


# 修改成语返回
def modify_idiom(idiom):
    num_replacements = 1 if len(idiom) == 4 else ((len(idiom) - 4) // 4) * 2 + random.randint(1, 2)
    indices_to_replace = random.sample(range(len(idiom)), num_replacements)

    idiom_new = ''
    correct_options = {}
    for index in range(len(idiom)):
        if index in indices_to_replace:
            idiom_new += '_'
            if idiom[index] not in correct_options:
                correct_options[idiom[index]] = index
        else:
            idiom_new += idiom[index]

    return idiom_new, correct_options


# 生成答案
def generate_similar_options(correct_options):
    options = []
    result = []
    result1 = []
    result2 = []
    result3 = []
    for char, index in correct_options.items():
        result.append(char)
        similar_chars = character_matcher.find_match_char(char)
        if similar_chars is not None:
            result1.append(similar_chars[0])
            result2.append(similar_chars[1])
            result3.append(similar_chars[2])

    options.append(''.join(result))
    options.append(''.join(result1))
    options.append(''.join(result2))
    options.append(''.join(result3))
    random.shuffle(options)
    return options


# 游戏入口
def play_idiom_game():
    while True:
        idiom = select_random_idiom()
        idiom_new, correct_options = modify_idiom(idiom)
        options = generate_similar_options(correct_options)

        print("欢迎来到成语拼接游戏！")
        print(f"以下是一个被改动的成语：{idiom_new}")

        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")

        player_choice = int(input("请输入你认为正确的选项数字："))

        if options[player_choice - 1] == ''.join(correct_options):
            print("恭喜！你猜对了，成语是正确的。")
        else:
            print(f"很遗憾，你猜错了。正确的选项是：{''.join(correct_options)}")


if __name__ == "__main__":
    character_matcher = CharacterMatcher()
    select_idioms_from_database()
    play_idiom_game()

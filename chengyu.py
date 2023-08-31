import os

import mysql.connector


def create_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idiom_library (
                id INT AUTO_INCREMENT PRIMARY KEY,
                idiom VARCHAR(255)  comment '成语',
                pinyin VARCHAR(255) comment '拼音',
                remark TEXT comment '解释'
            )
        ''')
        print("表格创建成功！")

    except mysql.connector.Error as e:
        print("创建表格出错：", e)


def insert_data(conn, idiom, pinyin, remark):
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO idiom_library (idiom, pinyin, remark) VALUES (%s, %s, %s)',
                       (idiom, pinyin, remark))
        conn.commit()
        print("数据插入成功！")

    except mysql.connector.Error as e:
        print("数据插入出错：", e)


if __name__ == "__main__":
    connect = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user="root",
        password=os.environ["MYSQL_PASSWORD"],
        database="motcs")

    create_table(connect)  # 创建表格
    with open('idiom.txt', 'r', encoding='utf-8') as file:
        entries = file.read().split("\n\n")  # 假设每条数据之间有一个空行分隔
        for entry in entries:
            print(entry)
            parts = entry.strip().split(",")
            idiom_s = parts[0].strip()
            pinyin_s = parts[1].split("：")[1].strip()
            remark_s = parts[2].split("：")[1].strip()

            # 调用函数插入数据
            insert_data(connect, idiom_s, pinyin_s, remark_s)

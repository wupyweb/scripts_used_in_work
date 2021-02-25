import csv
import json
import argparse

import requests

# 单次请求可批量解析100个坐标
# x:经度 y:纬度

def read_csv():
    # 输入为文件
    # 输出为二维列表，大列表里面是一对对小的经纬度列表
    rows = []
    with open(INPUT, newline="",mode="r") as f:
        row_data = csv.reader(f)
        next(row_data)
        for row in row_data:
            # 如果为空行，那么给row赋值[0,0]，防止空行造成格式错误
            if row == ['', '']:
                row = ['0', '0']
            rows.append(row)
    print(rows)
    return rows


def write_csv(data):
    # 输入为列表，列表元素为经纬度组成的字典，x是经度，y是纬度
    # 输出为文件
    # with open("output4.csv", "w", newline="") as f:
    #     file = csv.writer(f)
    #     file.writerow(["经度", "纬度"])
    #     for row in data:
    #         file.writerow([row["x"], row["y"]])
    header = ["x", "y"]
    with open(OUTPUT, "w", newline="") as f:
        file = csv.DictWriter(f, header)
        file.writeheader()
        file.writerows(data)


def gen_coords(rows):
    # 输入为一对对经纬度组成的二维列表
    # 输出为请求url中的coords
    coords = ""
    for item in rows:
        i = "{},{}".format(item[0], item[1])
        coords = coords + i + ";"
    return coords.strip(";")


def convert(coords):
    # 输入是url中的coords
    # 输出[{'x': 114.17544613746104, 'y': 22.832490084732502},
    kw = {
        'coords': coords,
        'from': '1',
        'to': '5',
        'ak': 'HUQSyZIIXZe0uNnSSAzDhwD9mwuBB4un'
    }
    result = requests.get(base_url, params=kw)
    # 跟据返回的状态码抛出异常
    if json.loads(result.text)["status"] == 0:
        x_y = json.loads(result.text)["result"]
    elif json.loads(result.text)["status"] == 1:
        raise Exception("API内部错误！")
    elif json.loads(result.text)["status"] == 24:
        raise Exception("coords格式非法！")
    else:
        raise Exception("未知错误！")
    return x_y


def split_rows(rows):
    # 每次取100组经纬度
    # 返回coords组成的列表
    temp = []
    flag = 1
    coords_list = []
    for row in rows:
        temp.append(row)
        if len(temp) == 100:
            coords = gen_coords(temp)
            temp = []
            coords_list.append(coords)
        elif flag == len(rows):
            coords = gen_coords(temp)
            coords_list.append(coords)
        flag += 1
    return coords_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="your input file name.")
    parser.add_argument("-o", "--output", help="your output file name.")
    args = parser.parse_args()
    if args.input and args.output:
        INPUT = args.input
        OUTPUT = args.output
    else:
        INPUT = "input.csv"
        OUTPUT = "output.csv"

    base_url = 'http://api.map.baidu.com/geoconv/v1/'
    rows = read_csv()
    result = []
    for coords in split_rows(rows):
        print(coords)
        result += convert(coords)
    write_csv(result)

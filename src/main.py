import requests
import json
import time

data = []


def get_content(id: str) -> str:
    url = "https://thanhnien.vn/ajax/diemthi.aspx"
    data = {
        "kythi": "THPT",
        "nam": "2021",
        "city": "",
        "text": id,
        "top": "no"
    }
    response = requests.get(url, params=data)
    return str(response.content)


def get_mark_to_list(content: str) -> list:
    content = content.split("<td")

    for _ in range(4):
        content.pop(0)

    for _ in range(2):
        content.pop(1)

    for i in range(len(content)):
        content[i] = content[i].split("</td>")

    arr = []

    for i in content:
        tmp = ""
        for j in reversed(i[0]):
            if j == ">":
                break
            tmp += j

        arr.append(tmp[::-1])
    return arr


def make_dictionary_for_mark(arr: list, province_id: str) -> dict:
    mark_dict = {}
    mark_dict["SBD"] = arr[0]
    mark_dict["Cum_thi"] = province_id
    mark_dict["Toan"] = arr[1]
    mark_dict["Ngu_van"] = arr[2]
    mark_dict["Vat_li"] = arr[3]
    mark_dict["Hoa_hoc"] = arr[4]
    mark_dict["Sinh_hoc"] = arr[5]
    mark_dict["KHTN"] = arr[6]
    mark_dict["Lich_su"] = arr[7]
    mark_dict["Dia_li"] = arr[8]
    mark_dict["GDCD"] = arr[9]
    mark_dict["KHXH"] = arr[10]
    mark_dict["Ngoai_ngu"] = arr[11]
    return mark_dict


def main() -> None:
    for i in range(1, 64+1):
        province_id = str(i)
        while len(province_id) < 2:
            province_id = "0" + province_id

        for j in range(1, 999999 + 1):
            if j % 5000 == 0:
                loading_char = ["\\", "|", "/", "-"]
                loading_char_index = 0
                print("Start to sleep")
                for k in range(300):
                    time_left = 300 - (k + 1)
                    for _ in range(5):
                        current_loading_char = loading_char[loading_char_index]
                        print(
                        "Time left: {}... {}".format(time_left, current_loading_char),
                        end="\r"
                        )
                        if loading_char_index != 3:
                            loading_char_index += 1
                        else:
                            loading_char_index = 0
                        time.sleep(0.2)
                print("Finish")
            student_id = str(j)
            while len(student_id) < 6:
                student_id = "0" + student_id

            id = province_id + student_id
            content = get_content(id)

            if content == "b'\\n'":
                continue

            mark_list = get_mark_to_list(content)
            mark_dictionary = make_dictionary_for_mark(mark_list, province_id)
            print(mark_dictionary)
            data.append(mark_dictionary)

    with open("data.json", "w") as file:
        json.dump(data, file)


if __name__ == "__main__":
    main()

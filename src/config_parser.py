#!/usr/bin/env python3


def validate_format(line: str) -> bool:
    """
    =が１つだけか
    =の左右が空でないか

    ==== 正しいフォーマット(それ以外はエラー) ====

    KEY = VALUE ('='は1つ)
    空行・コメント(#)は無視

    """
    if line.count("=") != 1:
        return (False)
    key_value = line.split("=", 1)

    if key_value[0].strip() == "" or key_value[1].strip() == "":
        return (False)
    return (True)


# argvのリストが渡される
def config_parser(arguments: list) -> dict:
    """
    config.txtを検証
    値の名前が違ったり、存在しない場合にエラーメッセージを表示
    →そのvalueを初期化
    返り値: dict
    """
    valid_list = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                  "OUTPUT_FILE", "PERFECT", "SEED"]
    try:
        print(arguments)
        if len(arguments) != 2:
            print("no name")
            print("~tets data~")
            return {}
        config_dict = {}
        line_counter = 1
        with open(arguments[1], "r") as f:
            for line in f:
                line = line.strip()
                # 空行 or # だけならスキップ
                if not line or line.startswith("#"):
                    continue
                # 以降を削除（コメント除去）
                line = line.split("#", 1)[0]
                line = line.strip()
                if validate_format(line):
                    key, value = line.split("=", 1)
                    if key not in valid_list:
                        print(f"Invalid key name in line"
                              f"{line_counter}: {key}")
                    config_dict[key.strip()] = value.strip()
                else:
                    print(f"Invalid format in line {line_counter}: {line}")
                line_counter += 1
            if line_counter != 8:
                print("Invalid format. You need 7 elements")
        return config_dict
    except Exception as e:
        print(e)
        return {}


if __name__ == "__main__":
    pass

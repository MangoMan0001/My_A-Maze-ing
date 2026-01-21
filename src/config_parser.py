#!/usr/bin/env python3
# from src import error_caller


def validate_format(line) -> bool:
    """
    =が１つだけか
    =の左右が空でないか

    ==== 正しいフォーマット(それ以外はエラー) ====

    KEY = VALUE ('='は1つ)
    空行・コメント(#)は無視

    """
    if line.count("=") != 1:
        return (False)
    line = line.split("=", 1)

    if line[0].strip() == "" or line[1].strip() == "":
        return (False)
    return (True)


# argvのリストが渡される
def config_parser(arguments: list) -> dict:
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
                    config_dict[key.strip()] = value.strip()
                else:
                    raise ValueError(f"Invalid format in line"
                                     f" {line_counter}: {line}")
                line_counter += 1
        return config_dict
    except Exception as e:
        pass
        # error_caller(e)


if __name__ == "__main__":
    pass

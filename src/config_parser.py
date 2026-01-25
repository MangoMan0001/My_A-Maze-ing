#!/usr/bin/env python3
"""設定ファイル(.txt)の解析を行うモジュール."""

VALID_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
              "OUTPUT_FILE", "PERFECT", "SEED"}


def validate_format(line: str) -> bool:
    """設定行のフォーマットが正しいか検証します.

    正しい形式: 'KEY = VALUE'
    - '=' は行内に1つだけであること
    - '=' の左右（キーと値）が空でないこと

    Args:
        line (str): 検証対象の行文字列.

    Returns:
        bool: フォーマットが正しければTrue、不正ならFalse.
    """
    # '='が一つか
    if line.count("=") != 1:
        return False

    key, value = line.split("=", 1)

    # キーと値が空文字じゃないか
    if key.strip() == "" or value.strip() == "":
        return False
    return True


def config_parser(arguments: list[str]) -> dict[str, str]:
    """設定ファイルを読み込み、解析結果を辞書形式で返します.

    コマンドライン引数で指定されたファイルを読み込み、
    定義済みのキー（WIDTH, HEIGHTなど）に対応する値を抽出します。
    不正なキーやフォーマットエラーがある場合はエラーメッセージを表示します。

    Args:
        arguments (list): コマンドライン引数のリスト（通常はsys.argv）.
            arguments[1] に設定ファイルのパスが含まれていることを想定しています。

    Returns:
        dict: 解析された設定値の辞書 (key: value).
            引数エラーやファイル読み込みエラーが発生した場合は空の辞書を返します。
    """
    if len(arguments) != 2:
        print(f"Usage: {arguments[0]} <config_file>")
        print()
        return {}

    config_dict = {}
    file_path = arguments[1]

    try:

        with open(file_path, "r") as f:
            for line_num, line in enumerate(f, 1):
                # 前後の空白削除
                line = line.strip()

                # 空行 or # で始まる行はスキップ
                if not line or line.startswith("#"):
                    continue

                # 行の途中にあるコメントを削除("KEY = VAL # comment"に対応)
                clean_line = line.split("#", 1)[0].strip()

                if validate_format(clean_line):
                    key, value = clean_line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if key not in VALID_KEYS:
                        print(f"Error ({line_num}): Invalid key '{key}'")
                        continue

                    config_dict[key] = value

                else:
                    print(f"Error ({line_num}): Invalid format '{line}'")
                    continue

        if len(config_dict) != len(VALID_KEYS):
            missing = VALID_KEYS - config_dict.keys()
            print(f"Error: Missing configuration keys: {missing}")

        return config_dict

    except FileNotFoundError:
        print(f"Error: file not found '{file_path}'")
        return {}
    except Exception as e:
        print(f"Error: {e}")
        return {}


if __name__ == "__main__":
    pass

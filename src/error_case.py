#!/usr/bin/env python3


def error_case(error: Exception) -> None:
    """
    例外発生時に呼び出される。
    例外オブジェクトを受けとり、適切な例外処理を行う。
    """

    print("new error!! Pleas put in new error case!!!")
    print(f"new error_case: {error.__class__.__name__}")
    print(f"          args: {error.args}")


if __name__ == "__main__":
    error_case()

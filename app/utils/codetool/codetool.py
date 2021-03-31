import random
import time
from typing import Union

from hashids import Hashids


class CodeTool:
    def create_serial_number(number: int, length=6) -> str:
        fix_number = 10**length

        number += 1
        ret = fix_number + number

        return str(ret)[1:length + 1]

    def create_random_number(length=6) -> str:
        start_number = 10**(length - 1)
        end_number = 10**length - 1

        ret = random.sample(range(start_number, end_number), 1)

        return ret[0]

    def create_random_str(length=6, base_str='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789') -> str:
        base_length = len(base_str) - 1
        str_list = [base_str[random.randint(0, base_length)]
                    for i in range(length)]

        return ''.join(str_list)

    def create_hashids_str(number: int, salt='5ebe2294ecd0e0f08eab7690d2a6ee69', min_length: int=6):
        """
        number 转换的字符
        salt 加密盐 默认 md5(secret)
        min_length 最小长度 6位
        """
        hashids = Hashids(salt=salt, min_length=min_length)
        return hashids.encode(number)
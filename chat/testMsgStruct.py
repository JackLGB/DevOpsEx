import json


class MessageStruct:
    """
    接收的信息结构体
    """
    msgType = None
    megInfo = {}

    def __init__(self, *args: str, **kwargs) -> None:
        """
        构造函数
        :param args:
        :param kwargs:
        """
        if args:
            _msg = json.loads(args[0])
        else:
            _msg = kwargs
        for key, value in _msg.items():
            if key == "msgType":
                self.msgType = value
            else:
                self.megInfo[key] = value

    def __call__(self, *args, **kwargs) -> dict:
        """
        调用时返回数据字典
        :param args:
        :param kwargs:
        :return:
        """
        return {
            "type": self.msgType,
            "info": self.megInfo,
        }


if __name__ == '__main__':
    msg = MessageStruct(key=2, ke3=[9, 34, "dasd"])
    print(msg())

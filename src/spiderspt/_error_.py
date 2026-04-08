class GetWebTimeError(Exception):
    def __init__(self, message: str = "获取网页时间失败"):
        super().__init__(message)

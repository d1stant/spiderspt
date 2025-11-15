import sys
from pathlib import Path

from loguru import logger

log_dir: Path = Path("./logs")
log_dir.mkdir(parents=True, exist_ok=True)
log_max_num: int = 20  # 最大日志文件数
log_files: list[Path] = sorted(
    log_dir.glob("*.log"), key=lambda x: x.stat().st_ctime
)  # 对日志文件进行排序
# 删除多余的
if len(log_files) > log_max_num:
    for old_log in log_files[:-19]:
        old_log.unlink()

logger.remove()  # 移除默认日志处理器

# 为每个日志级别设置颜色
logger.level("DEBUG", color="<fg #8B658B>")
logger.level("INFO", color="<fg #228B22>")
logger.level("WARNING", color="<fg #FFD700>")
logger.level("ERROR", color="<fg #ff00cc>")
logger.level("CRITICAL", color="<fg #CD0000><bold>")

# 日志格式
__console_log_format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:^8}</level> : <level>{message}</level>"
__file_log_format: str = "{time:YYYY-MM-DD HH:mm:ss} | {process.name} | {thread.name} | {file:>10}:{line}:{function}() | {level} : {message}"

# 添加文件日志处理器
logger.add(
    sink=log_dir / "log_{time:YYYY-MM-DD HH-mm-ss}.log",
    # sink=sys.stdout,
    level="DEBUG",  # 级别
    format=__file_log_format,
    rotation="10 MB",  # 设置大小
    retention=log_max_num,  # 最多保留20个日志文件
    encoding="utf-8",
    enqueue=True,
    backtrace=True,  # 记录堆栈
    diagnose=True,  # 堆栈跟踪
    mode="w",  # 每次运行新建
)

# 添加控制台日志处理器
logger.add(
    sink=sys.stdout,
    level="INFO",
    format=__console_log_format,
    colorize=True,
    enqueue=True,
)


class PrintLogger:
    def info(self, *args) -> None:
        msg: str = " ".join(map(str, args))
        logger.info(msg)

    def debug(self, *args) -> None:
        msg: str = " ".join(map(str, args))
        logger.debug(msg)

    def warning(self, *args) -> None:
        msg: str = " ".join(map(str, args))
        logger.warning(msg)

    def error(self, *args) -> None:
        msg: str = " ".join(map(str, args))
        logger.error(msg)

    def critical(self, *args) -> None:
        msg: str = " ".join(map(str, args))
        logger.critical(msg)

    def exception(self, err) -> None:
        # msg: str = " ".join(map(str, args))
        logger.exception(err)


print_log: PrintLogger = PrintLogger()

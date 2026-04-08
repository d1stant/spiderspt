from concurrent.futures import ProcessPoolExecutor

from loguru._logger import Logger

from spiderspt.logger_ import init_logger

print_log: Logger = init_logger()


def work(n):
    print_log.info(f"子进程, {n}")


if __name__ == "__main__":
    print_log.info("主进程")
    with ProcessPoolExecutor(max_workers=2) as executor:
        for i in range(10):
            executor.submit(work, i)

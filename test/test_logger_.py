from concurrent.futures import ProcessPoolExecutor

from spiderspt.logger_ import print_log


def work():
    print_log.info("子进程")


if __name__ == "__main__":
    print_log.info("主进程")
    with ProcessPoolExecutor(max_workers=2) as executor:
        for i in range(1):
            executor.submit(work)

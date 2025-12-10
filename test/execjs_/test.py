from spiderspt.execjs_ import ExecJS

execjs = ExecJS("./test/test.js")
print(execjs.run_without_wasm("add", (1, 2)))

from pathlib import Path
from typing import Any

import exejs
from exejs.runtimes import RuntimeCompileContext


class ExecJS:
    def __init__(self, js_file: str | Path) -> None:
        """执行JS

        Args:
            js_file (str | Path): js文件的路径
        """
        self.js_file: Path = Path(js_file) if isinstance(js_file, str) else js_file
        self.js_code: str = self.js_file.read_text(encoding="utf-8")

    def run_without_wasm(self, func: str, args: tuple = ()) -> None | Any:
        """无WASM需求, 执行JS并返回结果

        Args:
            func (str): 要调用的JS函数
            args (tuple, optional): JS函数的参数. Defaults to ().

        Returns:
            None | Any: JS函数返回的值
        """
        runtime: RuntimeCompileContext = exejs.compile(self.js_code)
        result: None | Any = runtime.call(func, *args)
        return result

    def __build_js_with_wasm(
        self,
        wasm_path: str,
        export_var: str,
        import_code: str = "",
        import_var: str = "",
    ) -> str:
        """构建加载WASM的JS代码

        Args:
            wasm_path (str): WASM文件的路径
            export_var (str): WASM导出的变量名
            import_code (str, optional): WASM实例化时要import的对象的JS代码. Defaults to "".
            import_var (str, optional): WASM实例化时要import的对象的变量名. Defaults to "".

        Returns:
            str: 构建好的新JS代码
        """
        if import_code:
            new_js_code: str = f"const fs = require('fs');{import_code};const wasmBuffer = fs.readFileSync('{wasm_path}');const wasmModule = new WebAssembly.Module(wasmBuffer);const wasmInstance = new WebAssembly.Instance(wasmModule, {import_var});const {export_var} = wasmInstance.exports;{self.js_code};"
        else:
            new_js_code: str = f"const fs = require('fs');const wasmBuffer = fs.readFileSync({wasm_path});const wasmModule = new WebAssembly.Module(wasmBuffer);const wasmInstance = new WebAssembly.Instance(wasmModule);const {export_var} = wasmInstance.exports;{self.js_code};"
        return new_js_code

    def run_with_wasm(
        self,
        wasm_file: str,
        wasm_export_var: str,
        func: str,
        wasm_import_file: str = "",
        wasm_import_var: str = "",
        args: tuple = (),
    ) -> None | Any:
        """加载WASM文件的同时执行JS代码并获取返回值

        Args:
            wasm_file (str): WASM文件的路径
            wasm_export_var (str): WASM导出的变量名
            func (str): JS要调用的函数
            args (tuple, optional): JS要调用的的函数的参数. Defaults to ().
            wasm_import_file (str, optional): WASM实例化时要import的对象的JS代码文件路径. Defaults to "".
            wasm_import_var (str, optional): WASM实例化时要import的对象的变量名. Defaults to "".

        Returns:
            None | Any: JS函数返回的值
        """
        if wasm_import_file:
            import_code: str = Path(wasm_import_file).read_text(encoding="utf-8")
        else:
            import_code: str = ""
        new_js_code: str = self.__build_js_with_wasm(
            wasm_file, wasm_export_var, import_code, wasm_import_var
        )
        runtime: RuntimeCompileContext = exejs.compile(new_js_code)
        result: None | Any = runtime.call(func, *args)
        return result

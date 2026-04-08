# SPIDERSPT
为了写爬虫脚本时写更少的代码而生！
## 1.安装
`pip install spiderspt`
## 2.模块
```
spiderspt
|
|- _error_.py
|- _type_.py
|- auth_.py
|- captcha_.py
|- decrypt_.py
|- encrypt.py
|- execjs_.py
|- logger_.py
|- machine_.py
|- captcha_.py
|- time_.py
```
## 3.模块功能
### auth_.py
1. 根据机器码生成带期限的离线授权文件
2. 验证授权文件是否合法
### captcha_.py
1. 识别滑块验证码
2. 识别字符验证码
### decrypt_.py
1. AES解密
### encrypt.py
1. MD5加密 ☑️
2. AES CBC加密 ☑️
3. AES GCM加密 ☑️
4. AES其他类型加密
5. 生成RAS密钥对 ☑️
6. RSA私钥签名 ☑️
7. RSA公钥验签 
### execjs_.py
1. 执行JS代码 ☑️
2. 执行调用WASM的JS代码 ☑️
### logger_.py
1. 初始化日志器 ☑️
### machine_.py
1. 获取机器码 ☑️
### time_.py
1. 时间戳格式化 ☑️
2. 格式化时间字符串转换为时间戳 ☑️
3. 获取当前网络时间 ☑️

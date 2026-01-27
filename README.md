# CloudRaiser Admin 登录客户端

Windows 桌面客户端，用于快速登录 CloudRaiser Admin 平台。

## 功能

- 输入用户名和密码
- 点击登录后自动打开浏览器并填充表单
- 自动提交登录

## 下载

从 [Releases](../../releases) 或 [Actions](../../actions) 页面下载最新的 `CloudRaiser-Login.exe`。

## 使用说明

1. 运行 `CloudRaiser-Login.exe`
2. 输入 ID 和 Password
3. 点击 Login 按钮
4. 程序会自动打开 Edge 浏览器并完成登录

## 系统要求

- Windows 10/11
- Microsoft Edge 浏览器（系统自带）

## 开发

```bash
pip install -r requirements.txt
python login_client.py
```

## 构建

推送到 main 分支后，GitHub Actions 会自动构建 Windows exe 文件。

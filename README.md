# Python 在线计算器

这是一个使用 Python + Streamlit 实现的在线计算器项目，适合作为测试开发岗位的小考核作品。项目不使用 HTML、CSS、JavaScript 前端文件，也没有使用 `eval()` 或 `exec()` 执行用户输入，而是自行实现了安全的表达式解析、逆波兰表达式转换和求值逻辑。

## 已实现功能

- 支持加法、减法、乘法、除法。
- 支持整数、小数、括号、百分号和负数。
- 支持复杂表达式，例如 `1+2*3`、`(1+2)*3`、`200*10%`、`5*-2`。
- 使用 Streamlit 提供在线网页界面。
- 支持文本框直接输入表达式。
- 支持数字、运算符、括号、百分号、清空、退格和等号按钮。
- 成功计算后保存最近 10 条历史记录。
- 支持清空历史记录。
- 对表达式错误和除以 0 进行友好提示。
- 对浮点数结果进行合理处理，例如 `0.1+0.2` 显示为 `0.3`。

## 本地运行方式

```bash
pip install -r requirements.txt
streamlit run app.py
```

运行后，终端会显示本地访问地址，通常是：

```text
http://localhost:8501
```

## 测试运行方式

```bash
pytest
```

## 部署到 Streamlit Cloud

1. 将 `python-online-calculator` 项目上传到 GitHub。
2. 登录 Streamlit Cloud。
3. 点击 New app，选择对应的 GitHub 仓库。
4. Main file path 填写：

```text
app.py
```

5. 点击 Deploy。
6. 部署完成后，Streamlit Cloud 会生成一个公网访问链接。

## 推荐提交给招聘方的话术

您好，在线计算器小考核我这边已经完成，访问链接如下：

项目链接：xxx

该项目使用 Python + Streamlit 实现，支持四则运算、括号、小数、百分号、负数、历史记录和异常处理。核心计算逻辑未使用 eval 或 exec，而是通过表达式解析、逆波兰表达式转换和求值完成，安全性和可维护性更好。

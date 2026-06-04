import json
import os
import smtplib
import sys
from email.mime.text import MIMEText
from pathlib import Path

import requests


CONFIG_PATH = Path(os.environ.get("CONFIG_PATH", "stocks.json"))
MAIL_HOST = os.environ.get("MAIL_HOST", "smtp.qq.com")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "465"))
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASS = os.environ.get("MAIL_PASS")
RECEIVER = os.environ.get("RECEIVER")


def send_email(title, content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = MAIL_USER
    msg["To"] = RECEIVER
    msg["Subject"] = title

    try:
        with smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT) as server:
            server.login(MAIL_USER, MAIL_PASS)
            server.sendmail(MAIL_USER, [RECEIVER], msg.as_string())
        print("邮件发送成功")
    except Exception as exc:
        print(f"邮件发送失败: {exc}")


def load_stocks():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"找不到配置文件: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        stocks = json.load(file)

    if not isinstance(stocks, list) or not stocks:
        raise ValueError("stocks.json 必须是非空数组")

    return stocks


def fetch_price(stock_code):
    url = f"https://qt.gtimg.cn/q={stock_code}"
    response = requests.get(url, timeout=10)
    response.encoding = "gbk"

    data = response.text.split("~")
    if len(data) < 4:
        raise ValueError(f"获取股价数据失败: {stock_code}")

    name = data[1]
    current_price = float(data[3])
    quote_time = data[30] if len(data) > 30 else ""
    return name, current_price, quote_time


def is_triggered(current_price, target):
    target_price = float(target["price"])
    direction = target.get("direction", "below").lower()

    if direction == "below":
        return current_price <= target_price
    if direction == "above":
        return current_price >= target_price

    raise ValueError(f"不支持的 direction: {direction}")


def check_stock(stock):
    code = stock["code"]
    display_name = stock.get("name", code)
    targets = stock.get("targets", [])

    if not targets:
        print(f"{display_name} ({code}) 未配置目标价格，跳过")
        return

    actual_name, current_price, quote_time = fetch_price(code)
    name = display_name or actual_name
    print(f"{name} ({code}) 当前价格: {current_price} 行情时间: {quote_time}")

    for target in targets:
        if not is_triggered(current_price, target):
            continue

        target_price = float(target["price"])
        direction = target.get("direction", "below").lower()
        direction_text = "低于或等于" if direction == "below" else "高于或等于"
        label = target.get("label", "价格提醒")

        send_email(
            f"【股价警报】{name} {label}",
            (
                f"您监控的股票 {name} ({code}) 当前价格为 {current_price}，"
                f"已{direction_text}目标价 {target_price}。\n"
                f"行情时间: {quote_time}"
            ),
        )


def main():
    if not all([MAIL_USER, MAIL_PASS, RECEIVER]):
        print("未配置邮箱环境变量，请设置 MAIL_USER、MAIL_PASS、RECEIVER")
        sys.exit(1)

    try:
        for stock in load_stocks():
            try:
                check_stock(stock)
            except Exception as exc:
                print(f"检查股票失败: {stock.get('code', 'UNKNOWN')} {exc}")
    except Exception as exc:
        print(f"程序执行出错: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()

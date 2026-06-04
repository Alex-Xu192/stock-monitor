# A-Share Stock Monitor

GitHub Actions 定时监控 A 股价格，触发目标价格后发送邮件提醒。

## 配置股票

修改 `stocks.json` 即可添加股票和目标价。

```json
[
  {
    "code": "sz300024",
    "name": "机器人",
    "targets": [
      {
        "price": 14.0,
        "direction": "below",
        "label": "第一档提醒"
      },
      {
        "price": 11.0,
        "direction": "below",
        "label": "第二档提醒"
      },
      {
        "price": 8.0,
        "direction": "below",
        "label": "第三档提醒"
      }
    ]
  }
]
```

字段说明：

- `code`: 腾讯行情接口股票代码。深市用 `sz` 开头，沪市用 `sh` 开头。
- `name`: 自定义显示名称。
- `targets`: 一只股票可以配置多个提醒价格。
- `price`: 目标价格。
- `direction`: `below` 表示当前价低于或等于目标价时提醒，`above` 表示当前价高于或等于目标价时提醒。
- `label`: 邮件标题中的提醒标签。

## 邮箱密钥

在 GitHub 仓库页面进入 `Settings` -> `Secrets and variables` -> `Actions`，添加：

- `MAIL_USER`: 发件邮箱，例如 `232631653@qq.com`
- `MAIL_PASS`: 邮箱 SMTP 授权码，不是邮箱登录密码
- `RECEIVER`: 收件邮箱，例如 `alex653@163.com`

当前工作流默认使用 QQ 邮箱 SMTP：

```yaml
MAIL_HOST: smtp.qq.com
MAIL_PORT: "465"
```

如果以后改用 163 邮箱发信，把 `.github/workflows/monitor.yml` 中的 `MAIL_HOST` 改成 `smtp.163.com`。

## 本地测试

PowerShell:

```powershell
$env:MAIL_USER="232631653@qq.com"
$env:MAIL_PASS="你的SMTP授权码"
$env:RECEIVER="alex653@163.com"
python -m pip install -r requirements.txt
python monitor.py
```

## 推送到 GitHub

```powershell
git init
git add .
git commit -m "Add stock monitor"
git branch -M main
git remote add origin https://github.com/YOUR_NAME/YOUR_REPO.git
git push -u origin main
```

GitHub Actions 的定时任务可能有排队延迟，适合低频提醒，不适合高频交易。

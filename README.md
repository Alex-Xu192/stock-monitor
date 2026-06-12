# Price Monitor

GitHub Actions 定时监控价格，触发目标价格后发送邮件提醒。

当前监控标的：

- 新洋丰（000902）：11 元、10 元、9 元
- 机器人（300024）：14 元、11 元、9 元
- 现货黄金：900 元/克、800 元/克、700 元/克
- 现货白银：12 元/克、10 元/克、8 元/克

## 配置标的

修改 `stocks.json` 即可添加股票、黄金、白银和目标价格。

```json
[
  {
    "type": "stock",
    "code": "sz000902",
    "name": "新洋丰",
    "targets": [
      {
        "price": 11.0,
        "direction": "below",
        "label": "11元提醒"
      }
    ]
  },
  {
    "type": "stock",
    "code": "sz300024",
    "name": "机器人",
    "targets": [
      {
        "price": 14.0,
        "direction": "below",
        "label": "14元提醒"
      }
    ]
  },
  {
    "type": "gold",
    "code": "hf_XAU",
    "name": "现货黄金",
    "targets": [
      {
        "price": 900.0,
        "direction": "below",
        "label": "900元/克提醒"
      }
    ]
  },
  {
    "type": "silver",
    "code": "hf_XAG",
    "name": "现货白银",
    "targets": [
      {
        "price": 12.0,
        "direction": "below",
        "label": "12元/克提醒"
      }
    ]
  }
]
```

字段说明：

- `type`: `stock` 表示 A 股，`gold` 表示现货黄金，`silver` 表示现货白银。
- `code`: 股票使用腾讯行情接口代码，深市用 `sz` 开头，沪市用 `sh` 开头；现货黄金使用 `hf_XAU`，现货白银使用 `hf_XAG`。
- `name`: 自定义显示名称。
- `targets`: 一个标的可以配置多个提醒价格。
- `price`: 目标价格。股票单位为元，黄金和白银单位为元/克。
- `direction`: `below` 表示当前价低于或等于目标价时提醒，`above` 表示当前价高于或等于目标价时提醒。
- `label`: 邮件标题中的提醒标签。
- `position_hint`: 可选，邮件正文里的加仓/操作建议。

黄金和白银价格来源为腾讯美元/盎司报价，并使用公开 USD/CNY 汇率折算为人民币/克。该价格与上海黄金交易所、上海期货交易所人民币报价可能存在少量价差，适合作为提醒参考。

脚本会把已经通知过的点位记录到 `.monitor-state.json`，避免 GitHub Actions 每次运行都重复发送同一个点位的邮件。

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

GitHub Actions 的定时任务可能有排队延迟，适合低频提醒，不适合高频交易。

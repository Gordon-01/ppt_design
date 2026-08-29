<div align="center">

# 🎨 ppt_design

**PPT 设计与美化工作区** — 素材 · 脚本 · 技能收集

</div>

---

## 📁 目录结构

| 路径 | 说明 |
| --- | --- |
| `8.28/` | 8.28 项目：市场大调研复盘会、北大楼的钟声、项目痛点等素材与美化结果 |
| `8.28/暑假生活6p/` | 《我的暑假生活》6 页 PPT 制作工程 |
| `.codex-ppt-polish/` | codex PPT 美化工作目录（脚本、模板检查产物；`node_modules` 不入库） |
| `my_skills/` | 个人技能包（ppt-beautify 等） |
| `github_skills/` | 第三方技能收集，上游地址与同步方法见 [UPSTREAM.md](github_skills/UPSTREAM.md) |

---

## ⚠️ 换电脑必读：先配置提交身份

本仓库所有提交统一使用 **Gordon-01** 账号。

> **不要**使用电脑全局 git 配置里的其他账号（如 `wuzhaoguo` + QQ 邮箱）提交——
> 那个邮箱绑定在另一个 GitHub 账号上，提交的头像和归属会显示错误。

新电脑上 `git clone` 本仓库后，**在仓库根目录执行一次**：

```bash
git config user.name "Gordon-01"
git config user.email "321310107+Gordon-01@users.noreply.github.com"
```

配置写在 `.git/config` 里，本仓库永久生效；重启电脑不受影响。

> 💡 如果是直接拷贝整个文件夹（含 `.git` 目录），配置会跟着走，无需重设。
> 用了错误的身份提交也没关系，见下方「修正提交身份」。

### 🛠 修正提交身份

若某条提交已经用了错误账号，改完配置后执行：

```bash
git commit --amend --no-edit --reset-author   # 修正最近一条
git push --force-with-lease                    # 会重写远程历史，仅限个人仓库
```

---

## 🔗 上游同步

`github_skills/` 下的三个仓库（Powerpoint-fancy-design、ergouzi-agent-skills、slide-master）
已去除内嵌 `.git`，完整保存文件内容。需要同步上游更新时，
按 [github_skills/UPSTREAM.md](github_skills/UPSTREAM.md) 中的步骤操作。

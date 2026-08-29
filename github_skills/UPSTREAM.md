# github_skills 上游记录

本目录下的三个文件夹是从 GitHub 克隆来的第三方技能仓库，为了让本仓库能完整保存其内容，提交前已删除各自的 `.git`（它们只是克隆元数据，历史都在上游仓库里）。因此这些文件夹不再与上游保持 git 关联，需要同步时按下方方法手动操作。

## 上游地址

| 本地文件夹 | 上游仓库 | 说明 |
| --- | --- | --- |
| `Powerpoint-fancy-design/` | https://github.com/Phlegonlabs/Powerpoint-fancy-design | PPT 设计技能（ppt-design skill），支持 Codex / Claude Code |
| `ergouzi-agent-skills/` | https://github.com/aiman-labs/ergouzi-agent-skills | 社区维护的 Agent Skills 与 Claude Code / Codex 插件合集 |
| `slide-master/` | https://github.com/byungjunjang/slide-master | 韩语定制版 PPT 生成工作区，基于 [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)（MIT） |

## 如何同步上游更新

在每个文件夹内重新关联上游并强制对齐（会丢弃该文件夹内的本地改动，如有修改先备份）：

```bash
cd github_skills/slide-master
git init
git remote add origin https://github.com/byungjunjang/slide-master.git
git fetch origin
git reset --hard origin/main   # 若上游默认分支是 master，把 main 换成 master
```

同步完成后，把本文件夹的 `.git` 删掉再回到本仓库根目录提交，保持本仓库只存文件内容：

```bash
rm -rf github_skills/slide-master/.git
cd ../..
git add github_skills/slide-master
git commit -m "chore(skills): 同步 slide-master 上游更新"
```

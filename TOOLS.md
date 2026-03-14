# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific
- **技能清单与能力范围**（本段新增）

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod

### Skills & Capabilities

- 可读写工作空间文件（read, write, edit）
- 执行 Shell 命令（exec）
- 管理 git 版本控制
- 创建部署 GitHub Pages 和 Hugging Face Spaces
- 使用 Gradio + Folium 构建交互式地图
- 集成多种 API（GitHub, Hugging Face, 天气等）
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## 📚 已具备的核心技能

- **文件操作**: read, write, edit, mkdir
- **命令执行**: exec（支持 pty、后台、超时）
- **Git 版本控制**: init, add, commit, push, pull, branch 管理
- **GitHub 部署**: GitHub Pages Actions workflow 创建与推送
- **Hugging Face 部署**: Spaces 创建与文件推送（gradio SDK）
- **Web 开发**: 静态 HTML + CSS + JS 快速原型
- **Python 应用**: Gradio + Folium 交互式地图应用
- **API 集成**: GitHub API, Hugging Face Hub API
- **多语言**: 繁體中文優先回應，可切換語言
- **记忆管理**: memory_search, memory_get, 日誌記錄
- **子代理管理**: sessions_spawn, subagents 協調
- **消息發送**: 多通道支援（Telegram, Discord 等）

## 🔧 常用工作流模板

### GitHub Pages 部署
1. 建立 index.html
2. 建立 `.github/workflows/deploy.yml`
3. git push 到 GitHub
4. Settings → Pages → Source: GitHub Actions

### Hugging Face Space 部署
1. 创建 Space（Gradio SDK）
2. 准备 `app.py`, `requirements.txt`, `README.md`（带 front matter）
3. git remote add space (HF token URL)
4. git push -u space main

### Gradio + Folium 地图模板
- 使用 `folium.Map` 创建底图
- `MarkerCluster` 聚合标记
- 用 `m._repr_html_()` 嵌入 Gradio HTML 组件
- JSON 存储数据，实时更新

## 📁 环境变量（安全储存）

- `GITHUB_TOKEN`: GitHub 个人访问令牌（repo, workflow 权限）
- `HUGGING_FACE_TOKEN`: Hugging Face 访问令牌
- 务必加入 `.gitignore`，勿外洩

## 🧠 记忆与上下文

- 主会话可加载 `MEMORY.md`（长期记忆）
- 日誌存于 `memory/YYYY-MM-DD.md`
- 使用 `memory_search` 检索过往决策

## ⚠️ 安全边界

- 不暴露憑證
- 外部操作（郵件、社交媒體）先詢問
-  destructive 操作需確認
- 尊重用戶隱私，不擴散敏感資訊

---
title: 防災即時資訊 API
emoji: ⚡
colorFrom: yellow
colorTo: red
sdk: docker
pinned: false
---

# 防災即時資訊 API 服務

此空間專門提供防災系統的 API 服務，使用 FastAPI 所建構。第一線防災人員可透過 Openclaw 傳送訊息後，透過此 API 介面即時向指揮中心或後台查詢最新的分析統計數據。

- **資料來源**: [GitHub Repository](https://github.com/cwbdayi638/disaster_dashboard)
- **架構**: Python + FastAPI
- **存取端點**: 
  - `GET /api/reports`
  - `GET /api/stats`

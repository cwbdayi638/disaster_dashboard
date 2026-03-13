import gradio as gr
import requests
import pandas as pd
import plotly.express as px
import folium

DATA_URL = "https://raw.githubusercontent.com/cwbdayi638/disaster_dashboard/main/data/reports.json"

def load_data():
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def get_stats():
    data = load_data()
    if not data:
        return "尚無通報數據", None
    
    df = pd.json_normalize(data)
    
    # 建立 Plotly 嚴重程度圓餅圖
    fig = px.pie(
        df, 
        names='incident.severity', 
        title='災情嚴重程度分布',
        color='incident.severity',
        hole=0.4, # 採用甜甜圈設計比較美觀
        color_discrete_map={'嚴重':'red', '重度':'orange', '中度':'yellow', '輕度':'green'}
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14)
    )
    
    summary = f"### 目前共有 {len(df)} 筆即時通報資料 🌊"
    return summary, fig

def generate_map(severity):
    data = load_data()
    if not data: 
        m = folium.Map(location=[23.5, 121.0], zoom_start=7)
        return m._repr_html_()
        
    filtered_data = data if severity == "全部" else [r for r in data if r['incident']['severity'] == severity]
    
    if not filtered_data:
        m = folium.Map(location=[23.5, 121.0], zoom_start=7)
        return m._repr_html_()

    # 計算中心點
    lats = [d['location']['latitude'] for d in filtered_data]
    lons = [d['location']['longitude'] for d in filtered_data]
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    
    # 建立地圖
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles='CartoDB positron')
    
    # 設定顏色對應
    color_map = {
        '嚴重': 'darkred',
        '重度': 'red',
        '中度': 'orange',
        '輕度': 'green',
        'Critical': 'darkred',
        'High': 'red', 
        'Medium': 'orange', 
        'Low': 'green'
    }
    
    # 繪製地標
    for d in filtered_data:
        sev = d['incident'].get('severity', '中度')
        cat = d['incident'].get('category', '未知')
        desc = d['incident'].get('description', '無描述')
        dist = d['location'].get('district', '')
        
        html_popup = f"""
        <div style="width:200px">
            <b>{dist} - {cat}</b><br>
            <i>嚴重度: {sev}</i><br>
            <p>{desc}</p>
        </div>
        """
        
        folium.Marker(
            location=[d['location']['latitude'], d['location']['longitude']],
            popup=folium.Popup(html_popup, max_width=300),
            tooltip=f"{cat} ({sev})",
            icon=folium.Icon(color=color_map.get(sev, 'blue'), icon='info-sign')
        ).add_to(m)
        
    return m._repr_html_()

def filter_reports(severity):
    data = load_data()
    if not data: return []
    if severity == "全部":
        return data
    return [r for r in data if r['incident']['severity'] == severity]

def update_ui(severity):
    return filter_reports(severity), generate_map(severity)

# 自定義 CSS
custom_css = """
.gradio-container {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
}
.map-container iframe {
    width: 100%;
    height: 600px;
    border: none;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
"""

with gr.Blocks(title="防災智慧核心展示", css=custom_css, theme=gr.themes.Soft(primary_hue="blue", secondary_hue="indigo")) as demo:
    gr.Markdown("# 🌊 即時防災資訊智慧展示中心")
    gr.Markdown("此儀表板自動提取來自各地的即時災情報告，提供即時的嚴重程度分析與地理分佈，協助防災指揮官迅速做出決策。")
    
    with gr.Row():
        with gr.Column(scale=1):
            stats_text = gr.Markdown("載入中...")
            stats_plot = gr.Plot()
        
        with gr.Column(scale=2):
            severity_filter = gr.Radio(
                ["全部", "嚴重", "重度", "中度", "輕度"], 
                label="快速篩選嚴重程度", 
                value="全部"
            )
            map_output = gr.HTML(elem_classes="map-container")

    with gr.Accordion("展開原始通報數據", open=False):
        report_output = gr.JSON(label="最新通報紀錄")
        
    # 事件綁定
    severity_filter.change(
        update_ui, 
        inputs=[severity_filter], 
        outputs=[report_output, map_output]
    )

    # 初始化載入
    demo.load(
        get_stats, 
        outputs=[stats_text, stats_plot]
    ).then(
        update_ui,
        inputs=[severity_filter],
        outputs=[report_output, map_output]
    )

if __name__ == "__main__":
    demo.launch()

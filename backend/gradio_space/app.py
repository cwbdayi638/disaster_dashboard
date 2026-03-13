import gradio as gr
import requests
import pandas as pd
import plotly.express as px

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
    fig = px.pie(df, names='incident.severity', title='災情嚴重程度分布',
                 color='incident.severity',
                 color_discrete_map={'Critical':'red', 'High':'orange', 'Medium':'yellow', 'Low':'green'})
    
    summary = f"目前共有 {len(df)} 筆即時通報資料。"
    return summary, fig

def filter_reports(severity):
    data = load_data()
    if not data: return []
    if severity == "全部":
        return data
    return [r for r in data if r['incident']['severity'] == severity]

with gr.Blocks(title="防災智慧核心展示") as demo:
    gr.Markdown("# 🌊 即時防災資訊智慧展示 (視覺展示)")
    
    with gr.Row():
        stats_text = gr.Label(label="系統概況")
        stats_plot = gr.Plot(label="比例分佈")
    
    with gr.Tab("通報清單"):
        severity_filter = gr.Radio(["全部", "Critical", "High", "Medium", "Low"], label="嚴重程度篩選", value="全部")
        report_output = gr.JSON(label="原始數據")
        
        severity_filter.change(filter_reports, severity_filter, report_output)

    demo.load(get_stats, outputs=[stats_text, stats_plot])

if __name__ == "__main__":
    demo.launch()

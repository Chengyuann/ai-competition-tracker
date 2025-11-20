# app.py
import streamlit as st
import pandas as pd
import os
from main import run_scrapers

# 页面配置
st.set_page_config(
    page_title="AI 竞赛聚合平台",
    page_icon="🏆",
    layout="wide"
)

# 侧边栏样式
st.sidebar.title("🔍 筛选与控制")

# --- 功能 1: 手动更新数据 ---
if st.sidebar.button("🔄 立即抓取最新数据"):
    with st.spinner("正在连接各大平台API，请稍候..."):
        run_scrapers()
    st.success("数据更新完成！请刷新页面。")

# --- 功能 2: 读取数据 ---
data_file = "competitions.csv"
if os.path.exists(data_file):
    df = pd.read_csv(data_file)
    
    # 数据清洗：确保 NaN 处理
    df.fillna("", inplace=True)

    # --- 侧边栏筛选器 ---
    # 1. 平台筛选
    all_platforms = list(df['platform'].unique())
    selected_platforms = st.sidebar.multiselect(
        "选择竞赛平台", 
        all_platforms, 
        default=all_platforms
    )
    
    # 2. 搜索框
    search_query = st.sidebar.text_input("搜索比赛 (支持标题/标签)", "")
    
    # --- 数据过滤逻辑 ---
    filtered_df = df[df['platform'].isin(selected_platforms)]
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df['title'].str.contains(search_query, case=False) | 
            filtered_df['tags'].str.contains(search_query, case=False)
        ]

    # --- 主页面展示 ---
    st.title(f"🏆 全球 AI 算法竞赛聚合")
    st.markdown(f"**当前收录:** {len(filtered_df)} 个正在进行的比赛 | **最后更新:** {datetime.now().strftime('%Y-%m-%d')}")
    st.divider()

    # 使用 Streamlit 的高级表格展示
    st.dataframe(
        filtered_df,
        column_config={
            "title": "比赛名称",
            "url": st.column_config.LinkColumn("比赛链接", display_text="点击跳转"),
            "prize": "奖金池",
            "deadline": "截止日期",
            "platform": "平台",
            "tags": st.column_config.ListColumn("标签"),
            "status": "状态"
        },
        hide_index=True,
        use_container_width=True,
        height=600
    )

else:
    st.warning("⚠️ 本地暂无数据。请点击左侧侧边栏的【立即抓取最新数据】按钮初始化。")
    st.info("如果是第一次运行，请确保网络畅通。")

# 页脚
st.markdown("---")
st.markdown("*这是一个 AI 辅助开发的开源项目 demo*")
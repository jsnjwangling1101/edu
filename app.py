import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="新加坡留学‘防破产’计算器",
    page_icon="🇸🇬",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Main App ---

# --- Header ---
st.title("🇸🇬 2026新加坡留学‘防破产’生存计算器")
st.markdown("一个帮你提前规划、避免“吃土”的实用工具。请真实填写，让我们看看你的留学之路是‘生存模式’还是‘度假模式’。")
st.markdown("---")

# --- Constants & Dictionaries ---
ACCOMMODATION_COSTS = {
    "HDB组屋普通房 (S$1,000/月)": 1000,
    "公寓普通房 (S$1,800/月)": 1800,
    "寄宿家庭 (S$2,200/月, 含餐)": 2200
}

FOOD_COSTS = {
    "仅食阁 (S$600/月)": 600,
    "偶尔下馆子 (S$1,000/月)": 1000
}

MISC_TRANSPORT_COST = 200  # 固定杂项与交通费 (SGD/月)
INSURANCE_COST = 500       # 固定医疗保险费 (SGD/年)
GUARDIANSHIP_COST = 1500   # 监护人费 (SGD/月)
GST_RATE = 0.09            # 商品及服务税 (GST)

# --- Input Form ---
with st.form(key="calculator_form"):
    st.header("Step 1: 填写你的基本情况")

    # 1. 学费预算
    tuition_fee = st.number_input(
        label="学费预算 (年/SGD)",
        min_value=0,
        value=30000,
        step=1000,
        help="请输入你预计的年度学费总额，单位为新币(SGD)。"
    )

    # 2. 住宿选择
    accommodation_choice = st.radio(
        label="住宿选择",
        options=list(ACCOMMODATION_COSTS.keys()),
        index=0,
        help="选择你的住宿类型，这是生活费的大头。"
    )

    # 3. 餐饮消费习惯
    food_choice = st.radio(
        label="餐饮消费习惯",
        options=list(FOOD_COSTS.keys()),
        index=0,
        help="“食阁”是新加坡的大众食堂，经济实惠。"
    )

    # 4. 未成年人监护
    is_under_18 = st.checkbox(
        label="是否未满18岁且父母不陪读？",
        value=False,
        help="根据新加坡法律，未满18岁的国际学生若父母不陪读，通常需要指定一位本地监护人。"
    )

    st.header("Step 2: 确认汇率")
    # 5. 汇率
    exchange_rate = st.number_input(
        label="新币(SGD) 到 人民币(CNY) 的汇率",
        min_value=0.1,
        value=5.4,
        step=0.01,
        help="你可以根据最新汇率进行调整。"
    )
    
    # Submit Button
    submit_button = st.form_submit_button(label="开始计算 🧮")


# --- Calculation & Output ---
if submit_button:
    # --- Calculation Logic ---

    # 1. 获取用户选择对应的费用
    accommodation_monthly_cost = ACCOMMODATION_COSTS[accommodation_choice]
    food_monthly_cost = FOOD_COSTS[food_choice]
    
    # 2. 计算监护人费用
    guardianship_monthly_cost = GUARDIANSHIP_COST if is_under_18 else 0

    # 3. 计算每月总生活费 (新币)
    monthly_living_cost_sgd = (
        accommodation_monthly_cost +
        food_monthly_cost +
        MISC_TRANSPORT_COST +
        guardianship_monthly_cost
    )

    # 4. 计算年度总生活费 (新币)
    annual_living_cost_sgd = monthly_living_cost_sgd * 12

    # 5. 计算含9% GST的学费
    tuition_with_gst = tuition_fee * (1 + GST_RATE)

    # 6. 计算年度总成本 (新币)
    # 总成本 = (学费*1.09) + (住宿+餐饮+杂项+监护费)*12 + 500
    total_annual_cost_sgd = tuition_with_gst + annual_living_cost_sgd + INSURANCE_COST

    # 7. 转换为人民币
    first_year_funds_rmb = total_annual_cost_sgd * exchange_rate
    monthly_remittance_rmb = monthly_living_cost_sgd * exchange_rate

    # --- Display Results ---
    st.markdown("---")
    st.header("📊 计算结果分析")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="首年启动资金 (人民币)",
            value=f"¥ {first_year_funds_rmb:,.2f}",
            help=f"这是第一年所需的总费用，包括学费、全年生活费和保险。计算公式: (总成本SGD {total_annual_cost_sgd:,.2f}) * 汇率 {exchange_rate}"
        )
    with col2:
        st.metric(
            label="家长每月需打款 (人民币)",
            value=f"¥ {monthly_remittance_rmb:,.2f}",
            help=f"这是覆盖每月基本生活开销的金额。计算公式: (每月生活费SGD {monthly_living_cost_sgd:,.2f}) * 汇率 {exchange_rate}"
        )
    
    # --- "Poison Tongue" Comments ---
    st.subheader("毒舌理财师点评 🧐")
    if first_year_funds_rmb < 300000:
        st.error(
            "**警告：** 该预算在新加坡生存极其困难，建议考虑马来西亚或泰国。这笔钱可能只够支付学费和房租，孩子将面临‘只要吸气就要花钱’的窘境。"
        )
    elif 300000 <= first_year_funds_rmb <= 450000:
        st.warning(
            "**勉强生存：** 孩子将过得像苦行僧，社交活动基本为零，经不起任何生病或意外。请确保孩子有强大的心理素质和独立生活能力。"
        )
    else: # first_year_funds_rmb > 450000
        st.success(
            "**舒适区：** 恭喜！这才是新加坡留学的正常门槛。孩子可以专注于学业，偶尔还能和朋友下馆子、看个电影，享受正常的留学生活。"
        )

    # --- Details Breakdown ---
    with st.expander("点击查看费用明细 (新币)"):
        st.markdown(f"""
        - **学费 (含9% GST)**: `S$ {tuition_with_gst:,.2f}`
        - **住宿费 (年)**: `S$ {accommodation_monthly_cost * 12:,.2f}`
        - **餐饮费 (年)**: `S$ {food_monthly_cost * 12:,.2f}`
        - **杂项与交通 (年)**: `S$ {MISC_TRANSPORT_COST * 12:,.2f}`
        - **强制医疗险 (年)**: `S$ {INSURANCE_COST:,.2f}`
        - **监护人费 (年)**: `S$ {guardianship_monthly_cost * 12:,.2f}`
        ---
        - **每月生活费总计**: `S$ {monthly_living_cost_sgd:,.2f}`
        - **年度总成本**: `S$ {total_annual_cost_sgd:,.2f}`
        """)

# --- Footer ---
st.markdown("---")
st.markdown("免责声明: 本计算器结果仅供参考，实际费用可能因个人消费习惯、通货膨胀及政策变动而有所不同。")

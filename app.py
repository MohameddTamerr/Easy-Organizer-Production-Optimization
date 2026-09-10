import streamlit as st
import cvxpy as cp
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Easy Organizer Dashboard",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# COLORS
# =========================================================
PINK = "#EC008C"
DARK_PINK = "#C60076"
LIGHT_PINK = "#FFF5FB"
SOFT_PINK = "#FCE4F1"
GREEN = "#8CC63F"
LIGHT_GREEN = "#F4FAEA"
DARK = "#1A1A1A"
TEXT = "#222222"
MUTED = "#6B7280"
WHITE = "#FFFFFF"
BORDER = "#EED7E5"
RED = "#E74C3C"


# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(circle at top left, #FFE7F4 0%, transparent 25%),
        radial-gradient(circle at bottom right, #F2FFE7 0%, transparent 20%),
        linear-gradient(135deg, #FFF8FC 0%, #FFFFFF 45%, #FCFFF8 100%);
}}

.block-container {{
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}}

#MainMenu, footer, header {{
    visibility: hidden;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: #FFFFFF !important;
    border-right: 3px solid {PINK};
}}

[data-testid="stSidebar"] * {{
    color: {TEXT} !important;
}}

.sidebar-logo-wrap {{
    text-align: center;
    padding-top: 10px;
    padding-bottom: 10px;
}}

.sidebar-title {{
    font-size: 28px;
    font-weight: 800;
    color: {TEXT};
    margin-top: 8px;
    margin-bottom: 4px;
}}

.sidebar-subtitle {{
    font-size: 14px;
    color: {PINK};
    font-weight: 600;
    margin-bottom: 12px;
}}

.sidebar-box {{
    background: linear-gradient(135deg, #FFF7FC 0%, #FFFFFF 100%);
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.04);
}}

.sidebar-box-title {{
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 6px;
    color: {TEXT};
}}

.sidebar-box-text {{
    font-size: 14px;
    color: {MUTED};
    line-height: 1.6;
}}

/* Hero */
.hero {{
    background: linear-gradient(135deg, {PINK} 0%, #FF58B6 55%, {GREEN} 140%);
    border-radius: 30px;
    padding: 35px;
    box-shadow: 0 20px 45px rgba(236, 0, 140, 0.18);
    color: white;
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
}}

.hero::after {{
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.15);
    top: -80px;
    right: -60px;
}}

.hero-title {{
    font-size: 40px;
    font-weight: 900;
    margin-bottom: 8px;
    color: white;
}}

.hero-text {{
    font-size: 16px;
    line-height: 1.7;
    color: #FFF6FB;
    max-width: 760px;
}}

.hero-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    padding: 8px 14px;
    border-radius: 999px;
    margin-top: 14px;
    margin-right: 8px;
    font-size: 13px;
    font-weight: 700;
}}

/* Section */
.section-card {{
    background: rgba(255,255,255,0.92);
    border: 1px solid {BORDER};
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 15px 32px rgba(0,0,0,0.05);
    margin-bottom: 22px;
}}

.section-title {{
    font-size: 24px;
    font-weight: 850;
    color: {TEXT};
    margin-bottom: 5px;
}}

.section-subtitle {{
    font-size: 14px;
    color: {MUTED};
    margin-bottom: 8px;
}}

/* KPI cards */
.kpi-card {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 14px 28px rgba(0,0,0,0.05);
    position: relative;
    overflow: hidden;
    min-height: 165px;
}}

.kpi-card::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: linear-gradient(90deg, {PINK}, {GREEN});
}}

.kpi-icon {{
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background: {SOFT_PINK};
    color: {PINK};
    margin-bottom: 12px;
}}

.kpi-icon .material-symbols-outlined {{
    font-size: 28px;
}}

.kpi-value {{
    font-size: 28px;
    font-weight: 900;
    color: {TEXT};
    margin-bottom: 4px;
}}

.kpi-label {{
    font-size: 14px;
    font-weight: 700;
    color: {MUTED};
}}

.kpi-chip {{
    display: inline-block;
    margin-top: 10px;
    padding: 6px 10px;
    border-radius: 999px;
    background: {LIGHT_GREEN};
    color: #4F7F18;
    font-size: 12px;
    font-weight: 700;
}}

/* insight */
.insight-card {{
    background: white;
    border-radius: 24px;
    border-left: 6px solid {PINK};
    padding: 24px;
    box-shadow: 0 14px 28px rgba(0,0,0,0.05);
}}

.insight-note {{
    background: {LIGHT_GREEN};
    border: 1px solid #D8EDBB;
    padding: 14px;
    border-radius: 16px;
    color: #436B17;
    font-weight: 700;
    margin-top: 12px;
}}

/* recommendation cards */
.rec-card {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 14px 28px rgba(0,0,0,0.05);
    min-height: 190px;
}}

.rec-icon {{
    width: 46px;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background: {SOFT_PINK};
    color: {PINK};
    margin-bottom: 12px;
}}

.rec-icon .material-symbols-outlined {{
    font-size: 26px;
}}

.rec-title {{
    font-size: 18px;
    font-weight: 800;
    color: {TEXT};
    margin-bottom: 8px;
}}

.rec-text {{
    font-size: 14px;
    color: {MUTED};
    line-height: 1.6;
}}

/* buttons */
.stButton > button {{
    background: linear-gradient(90deg, {PINK}, {DARK_PINK}) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 0.8rem 1rem !important;
    font-weight: 800 !important;
    width: 100% !important;
    box-shadow: 0 10px 22px rgba(236,0,140,0.2) !important;
}}

.stButton > button:hover {{
    background: linear-gradient(90deg, {DARK_PINK}, {PINK}) !important;
    color: white !important;
}}

/* metric progress */
.progress-wrap {{
    margin-bottom: 18px;
}}

.progress-label {{
    display: flex;
    justify-content: space-between;
    font-weight: 700;
    margin-bottom: 6px;
    color: {TEXT};
}}

.progress-bg {{
    height: 12px;
    background: #F2F2F2;
    border-radius: 999px;
    overflow: hidden;
}}

.progress-fill {{
    height: 12px;
    border-radius: 999px;
    background: linear-gradient(90deg, {GREEN}, {PINK});
}}

/* table */
[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 18px;
    overflow: hidden;
}}

/* tabs if used */
.stTabs [data-baseweb="tab-list"] {{
    gap: 10px;
}}

.stTabs [data-baseweb="tab"] {{
    background: white;
    border-radius: 14px;
    border: 1px solid {BORDER};
    font-weight: 700;
    padding: 10px 16px;
}}

.stTabs [aria-selected="true"] {{
    background: {PINK};
    color: white;
}}

/* input labels */
label, .stSlider label, .stNumberInput label {{
    font-weight: 600 !important;
    color: {TEXT} !important;
}}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA
# =========================================================
sizes = ["S", "M", "L", "XL", "XXL"]

profit = np.array([55, 75, 100, 120, 140])
pvc_usage = np.array([0.45, 0.70, 0.95, 1.30, 1.75])
fabric_usage = np.array([0.30, 0.50, 0.75, 1.00, 1.40])
production_time = np.array([10, 15, 20, 28, 35])
storage_space = np.array([1, 2, 3, 5, 7])


# =========================================================
# SESSION STATE DEFAULTS
# =========================================================
defaults = {
    "MAX_PVC": 500,
    "MAX_FABRIC": 400,
    "MAX_TIME": 15000,
    "MAX_STORAGE": 1000,
    "demand_S": 120,
    "demand_M": 100,
    "demand_L": 80,
    "demand_XL": 55,
    "demand_XXL": 35,
    "alpha": 1.0,
    "beta": 0.5,
    "gamma": 0.2,
    "delta": 0.1,
    "epsilon": 10.0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown('<div class="sidebar-logo-wrap">', unsafe_allow_html=True)
    st.image("logo.png", width=160)
    st.markdown('<div class="sidebar-title">Easy Organizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Smart production planning</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=[
            "Overview",
            "Optimization Inputs",
            "Production Results",
            "Visual Analysis",
            "Business Insights"
        ],
        icons=[
            "house-door",
            "sliders",
            "boxes",
            "bar-chart-line",
            "lightbulb"
        ],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#FFFFFF",
            },
            "icon": {
                "color": PINK,
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "17px",
                "text-align": "left",
                "margin": "6px 0px",
                "padding": "12px 14px",
                "border-radius": "14px",
                "color": TEXT,
                "font-weight": "600",
                "--hover-color": "#FFF3FA",
            },
            "nav-link-selected": {
                "background": f"linear-gradient(90deg, {PINK}, {DARK_PINK})",
                "color": "white",
                "font-weight": "700",
                "box-shadow": "0 8px 18px rgba(236,0,140,0.18)",
            },
        }
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sidebar-box">
        <div class="sidebar-box-title">Project Type</div>
        <div class="sidebar-box-text">
            Optimization Techniques<br>
            Python + CVXPY + Streamlit
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# HERO SECTION
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">Easy Organizer Optimization Dashboard</div>
    <div class="hero-text">
        A smart dashboard for production planning that helps determine the best quantity to produce
        for each organizer size while balancing profit, waste, storage, labor time, and shortages.
    </div>
    <span class="hero-badge">Optimization Model</span>
    <span class="hero-badge">Production Planning</span>
    <span class="hero-badge">Decision Support</span>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SOLVE MODEL
# =========================================================
def solve_model():
    demand = np.array([
        st.session_state["demand_S"],
        st.session_state["demand_M"],
        st.session_state["demand_L"],
        st.session_state["demand_XL"],
        st.session_state["demand_XXL"]
    ])

    MAX_PVC = st.session_state["MAX_PVC"]
    MAX_FABRIC = st.session_state["MAX_FABRIC"]
    MAX_TIME = st.session_state["MAX_TIME"]
    MAX_STORAGE = st.session_state["MAX_STORAGE"]

    alpha = st.session_state["alpha"]
    beta = st.session_state["beta"]
    gamma = st.session_state["gamma"]
    delta = st.session_state["delta"]
    epsilon = st.session_state["epsilon"]

    x = cp.Variable(len(sizes), integer=True)
    shortage = cp.Variable(len(sizes))
    waste_pvc = cp.Variable()
    waste_fabric = cp.Variable()

    total_profit = profit @ x
    used_pvc = pvc_usage @ x
    used_fabric = fabric_usage @ x
    total_time = production_time @ x
    total_storage = storage_space @ x
    total_waste = waste_pvc + waste_fabric
    total_shortage = cp.sum(shortage)

    constraints = [
        x >= 0,
        x <= demand,
        shortage >= 0,
        shortage >= demand - x,
        used_pvc <= MAX_PVC,
        used_fabric <= MAX_FABRIC,
        total_time <= MAX_TIME,
        total_storage <= MAX_STORAGE,
        waste_pvc == MAX_PVC - used_pvc,
        waste_fabric == MAX_FABRIC - used_fabric,
        waste_pvc >= 0,
        waste_fabric >= 0
    ]

    objective = cp.Maximize(
        alpha * total_profit
        - beta * total_waste
        - gamma * total_time
        - delta * total_storage
        - epsilon * total_shortage
    )

    problem = cp.Problem(objective, constraints)

    try:
        problem.solve()
    except:
        problem.solve(solver=cp.SCIPY)

    if problem.status not in ["optimal", "optimal_inaccurate"]:
        return None

    production = np.round(x.value).astype(int)
    shortages = np.round(shortage.value).astype(int)

    result_df = pd.DataFrame({
        "Size": sizes,
        "Demand": demand,
        "Produced": production,
        "Shortage": shortages,
        "Profit / Unit": profit,
        "Total Profit": production * profit,
        "PVC Usage": np.round(production * pvc_usage, 2),
        "Fabric Usage": np.round(production * fabric_usage, 2),
        "Production Time": production * production_time,
        "Storage Used": production * storage_space
    })

    resources_df = pd.DataFrame({
        "Resource": ["PVC", "Fabric", "Labor Time", "Storage"],
        "Used": [
            float(used_pvc.value),
            float(used_fabric.value),
            float(total_time.value),
            float(total_storage.value)
        ],
        "Available": [
            MAX_PVC,
            MAX_FABRIC,
            MAX_TIME,
            MAX_STORAGE
        ]
    })

    resources_df["Utilization %"] = (
        resources_df["Used"] / resources_df["Available"] * 100
    )

    bottleneck_row = resources_df.loc[resources_df["Utilization %"].idxmax()]

    return {
        "status": problem.status,
        "objective_value": float(problem.value),
        "total_profit": float(total_profit.value),
        "total_shortage": float(total_shortage.value),
        "used_pvc": float(used_pvc.value),
        "used_fabric": float(used_fabric.value),
        "total_time": float(total_time.value),
        "total_storage": float(total_storage.value),
        "production": production,
        "shortages": shortages,
        "demand": demand,
        "result_df": result_df,
        "resources_df": resources_df,
        "bottleneck": bottleneck_row["Resource"],
        "bottleneck_util": float(bottleneck_row["Utilization %"])
    }


solution = solve_model()

if solution is None:
    st.error("No feasible solution found. Try increasing the available resources or reducing demand.")
    st.stop()


# =========================================================
# HELPERS
# =========================================================
def kpi_card(icon_name, value, label, chip):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">
            <span class="material-symbols-outlined">{icon_name}</span>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-chip">{chip}</div>
    </div>
    """, unsafe_allow_html=True)


def rec_card(icon_name, title, text):
    st.markdown(f"""
    <div class="rec-card">
        <div class="rec-icon">
            <span class="material-symbols-outlined">{icon_name}</span>
        </div>
        <div class="rec-title">{title}</div>
        <div class="rec-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def progress_bar(name, value):
    width = min(value, 100)
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label">
            <span>{name}</span>
            <span>{value:.1f}%</span>
        </div>
        <div class="progress-bg">
            <div class="progress-fill" style="width:{width}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# PAGE: OVERVIEW
# =========================================================
if selected == "Overview":

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Executive Overview</div>
        <div class="section-subtitle">
            A quick summary of the optimal solution and the current business performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        kpi_card("track_changes", f"{solution['objective_value']:,.1f}", "Objective Value", "Model Output")

    with c2:
        kpi_card("payments", f"{solution['total_profit']:,.0f}", "Total Profit", "Revenue Result")

    with c3:
        kpi_card("inventory_2", f"{solution['total_storage']:,.0f}", "Storage Used", "Capacity Usage")

    with c4:
        kpi_card("warning", f"{solution['total_shortage']:,.0f}", "Total Shortage", "Demand Gap")

    with c5:
        kpi_card("factory", solution["bottleneck"], "Main Bottleneck", f"{solution['bottleneck_util']:.1f}% Utilized")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.4, 1])

    with left:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Production Snapshot</div>
            <div class="section-subtitle">
                Produced quantity compared with demand for each organizer size.
            </div>
        </div>
        """, unsafe_allow_html=True)

        snapshot_df = solution["result_df"][["Size", "Demand", "Produced", "Shortage", "Total Profit"]]
        st.dataframe(snapshot_df, use_container_width=True, hide_index=True)

    with right:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Resource Health</div>
            <div class="section-subtitle">
                Current utilization percentage for every major resource.
            </div>
        </div>
        """, unsafe_allow_html=True)

        for _, row in solution["resources_df"].iterrows():
            progress_bar(row["Resource"], row["Utilization %"])


# =========================================================
# PAGE: INPUTS
# =========================================================
elif selected == "Optimization Inputs":

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Optimization Inputs</div>
        <div class="section-subtitle">
            Adjust the resources, demand, and objective weights, then run the optimization again.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Factory Resources")
        st.slider("PVC Available", 100, 800, key="MAX_PVC")
        st.slider("Fabric Available", 100, 700, key="MAX_FABRIC")
        st.slider("Labor Time", 1000, 20000, key="MAX_TIME")
        st.slider("Storage Capacity", 500, 1500, key="MAX_STORAGE")

    with col2:
        st.markdown("### Demand by Size")
        st.number_input("Demand S", min_value=0, key="demand_S")
        st.number_input("Demand M", min_value=0, key="demand_M")
        st.number_input("Demand L", min_value=0, key="demand_L")
        st.number_input("Demand XL", min_value=0, key="demand_XL")
        st.number_input("Demand XXL", min_value=0, key="demand_XXL")

    with col3:
        st.markdown("### Objective Weights")
        st.slider("Profit Weight", 0.0, 5.0, key="alpha")
        st.slider("Waste Weight", 0.0, 5.0, key="beta")
        st.slider("Time Weight", 0.0, 5.0, key="gamma")
        st.slider("Storage Weight", 0.0, 5.0, key="delta")
        st.slider("Shortage Penalty", 0.0, 20.0, key="epsilon")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Run Optimization"):
        st.success("The optimization inputs were updated successfully.")


# =========================================================
# PAGE: PRODUCTION RESULTS
# =========================================================
elif selected == "Production Results":

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Optimal Production Plan</div>
        <div class="section-subtitle">
            The recommended quantities for each size based on the current constraints.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(solution["result_df"], use_container_width=True, hide_index=True)

    csv = solution["result_df"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="easy_organizer_results.csv",
        mime="text/csv"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    most_produced_idx = int(np.argmax(solution["production"]))
    highest_profit_idx = int(np.argmax(solution["production"] * profit))
    highest_shortage_idx = int(np.argmax(solution["shortages"]))

    r1, r2, r3 = st.columns(3)

    with r1:
        rec_card(
            "inventory",
            "Most Produced Size",
            f"Size {sizes[most_produced_idx]} has the highest production quantity with {solution['production'][most_produced_idx]} units."
        )

    with r2:
        rec_card(
            "paid",
            "Highest Profit Contribution",
            f"Size {sizes[highest_profit_idx]} contributes the highest total profit with {(solution['production'] * profit)[highest_profit_idx]:,.0f}."
        )

    with r3:
        rec_card(
            "report_problem",
            "Highest Shortage",
            f"Size {sizes[highest_shortage_idx]} has the highest shortage with {solution['shortages'][highest_shortage_idx]} units."
        )


# =========================================================
# PAGE: VISUAL ANALYSIS
# =========================================================
elif selected == "Visual Analysis":

    st.markdown("""
    <div class="section-card">
        <div class="section-title">Visual Analysis</div>
        <div class="section-subtitle">
            Interactive charts for better understanding of production, profit, shortages, and resource usage.
        </div>
    </div>
    """, unsafe_allow_html=True)

    result_df = solution["result_df"]
    resources_df = solution["resources_df"]

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=result_df["Size"],
            y=result_df["Demand"],
            name="Demand",
            marker_color="#F8B7DD"
        ))
        fig.add_trace(go.Bar(
            x=result_df["Size"],
            y=result_df["Produced"],
            name="Produced",
            marker_color=PINK
        ))
        fig.update_layout(
            title="Production vs Demand",
            barmode="group",
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color=TEXT)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            resources_df,
            x="Utilization %",
            y="Resource",
            orientation="h",
            text=resources_df["Utilization %"].round(1),
            color="Utilization %",
            color_continuous_scale=[GREEN, PINK]
        )
        fig.update_layout(
            title="Resource Utilization",
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color=TEXT),
            coloraxis_showscale=False
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig = px.pie(
            result_df,
            names="Size",
            values="Total Profit",
            hole=0.55,
            color_discrete_sequence=[PINK, "#FF5AB8", "#F7A7D4", GREEN, "#B8E06D"]
        )
        fig.update_layout(
            title="Profit Contribution by Size",
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color=TEXT)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.bar(
            result_df,
            x="Size",
            y="Shortage",
            text="Shortage",
            color_discrete_sequence=[RED]
        )
        fig.update_layout(
            title="Shortage by Size",
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color=TEXT)
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)


# =========================================================
# PAGE: BUSINESS INSIGHTS
# =========================================================
elif selected == "Business Insights":

    bottleneck = solution["bottleneck"]
    util = solution["bottleneck_util"]

    if bottleneck == "Storage":
        recommendation = "Increase storage capacity or reduce the production of larger sizes because they consume more space."
    elif bottleneck == "PVC":
        recommendation = "Increase PVC availability or prioritize sizes that create better profit with lower PVC usage."
    elif bottleneck == "Fabric":
        recommendation = "Increase fabric supply or improve cutting efficiency to reduce waste."
    else:
        recommendation = "Increase labor hours or improve scheduling to handle time-consuming production more efficiently."

    st.markdown(f"""
    <div class="insight-card">
        <h2 style="margin-top:0; color:{TEXT};">Main Business Insight</h2>
        <p style="font-size:16px; color:{MUTED}; line-height:1.7;">
            The optimization model indicates that the main bottleneck is <b>{bottleneck}</b>
            with a utilization rate of <b>{util:.2f}%</b>.
        </p>
        <p style="font-size:16px; color:{MUTED}; line-height:1.7;">
            This means that <b>{bottleneck}</b> is the most limiting resource in the production system.
            Improving this resource can help reduce shortages and increase profit.
        </p>
        <div class="insight-note">
            Recommendation: {recommendation}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        rec_card(
            "trending_up",
            "Increase High-Profit Production",
            "Focus more on the sizes that generate the strongest profit contribution when resources are available."
        )

    with b:
        rec_card(
            "assignment_late",
            "Reduce Shortages",
            "Monitor recurring demand gaps and improve the resources needed for the most affected sizes."
        )

    with c:
        rec_card(
            "manufacturing",
            "Improve Resource Efficiency",
            "Track usage of PVC, fabric, labor, and storage to avoid unnecessary bottlenecks."
        )


# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<br><br>
<div style="text-align:center; color:#666; font-size:14px; padding:20px;">
    <b>Easy Organizer</b> | Smart Production Planning<br>
    Created for Optimization Techniques Project
</div>
""", unsafe_allow_html=True)
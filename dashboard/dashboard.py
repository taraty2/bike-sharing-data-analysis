
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. PAGE CONFIGURATION

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM CSS

st.markdown("""
<style>
    .stApp {
        background-color: #9FB4D0;
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    [data-testid="stSidebar"] {
        background-color: #17233F;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    .dashboard-header {
        background-color: #17233F;
        padding: 24px;
        border-radius: 18px;
        margin-bottom: 20px;
        color: white;
    }

    .dashboard-header h1 {
        color: #FFFFFF;
        margin-bottom: 5px;
    }

    .dashboard-header p {
        color: #B9D8EE;
        margin-bottom: 0;
    }

    [data-testid="stMetric"] {
        background-color: #F2F6FC;
        border-radius: 16px;
        padding: 18px;
        border: 1px solid #DCE6F2;
    }

    [data-testid="stMetricLabel"] {
        color: #52627D;
    }

    [data-testid="stMetricValue"] {
        color: #17233F;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #F2F6FC;
        border-radius: 16px;
        border: 1px solid #DCE6F2;
        padding: 12px;
    }

    h1, h2, h3 {
        color: #17233F;
    }

    .section-caption {
        color: #52627D;
        font-size: 13px;
        margin-top: -10px;
        margin-bottom: 15px;
    }

    hr {
        border-color: #C4D1E2;
    }

    /* Year Filter Dropdown */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #304565 !important;
        border: 1px solid #77A9D8 !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #42D6E8 !important;
    }

    /* Dropdown Options */
    [data-baseweb="popover"] {
        background-color: #203456 !important;
    }

    [role="option"] {
        background-color: #203456 !important;
        color: #FFFFFF !important;
    }

    [role="option"]:hover {
        background-color: #304565 !important;
    }



</style>
""", unsafe_allow_html=True)

# 3. LOAD DATA

BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    day = pd.read_csv(
        BASE_DIR / "day_data.csv",
        parse_dates=["dteday"]
    )

    hour = pd.read_csv(
        BASE_DIR / "hour_data.csv",
        parse_dates=["dteday"]
    )

    return day, hour


day_df, hour_df = load_data()


# 4. SIDEBAR FILTER

st.sidebar.title("🚲 Bike Sharing")
st.sidebar.caption("Rental Data Analysis")
st.sidebar.divider()

selected_year = st.sidebar.selectbox(
    "Select Year",
    options=[2011, 2012]
)

year_code = selected_year - 2011

filtered_day = day_df[
    day_df["yr"] == year_code
].copy()

filtered_hour = hour_df[
    hour_df["yr"] == year_code
].copy()

st.sidebar.divider()
st.sidebar.caption("Dataset Period")
st.sidebar.write("January 2011 - December 2012")

# 5. COLOR PALETTE

NAVY = "#17233F"
DARK_BLUE = "#203456"
SOFT_BLUE = "#77A9D8"
CYAN = "#42D6E8"
LIGHT_BLUE = "#A5B5D0"
PALE_BLUE = "#D3DCEB"
BACKGROUND = "#F2F6FC"

WEATHER_COLORS = [
    CYAN,
    SOFT_BLUE,
    LIGHT_BLUE,
    PALE_BLUE
]


def style_chart(ax):
    ax.set_facecolor(BACKGROUND)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#C4D1E2")
    ax.spines["bottom"].set_color("#C4D1E2")
    ax.tick_params(colors=NAVY)
    ax.xaxis.label.set_color(NAVY)
    ax.yaxis.label.set_color(NAVY)
    ax.title.set_color(NAVY)
    ax.grid(axis="y", linestyle="--", alpha=0.3)


# 6. DASHBOARD HEADER

st.markdown(f"""
<div class="dashboard-header">
    <h1>🚲 Bike Sharing Dashboard</h1>
    <p>Explore bike rental patterns based on time,
    weather conditions, and user characteristics.</p>
    <p><b>Selected Year:</b> {selected_year}</p>
</div>
""", unsafe_allow_html=True)


# 7. KEY PERFORMANCE INDICATORS

total_rentals = filtered_day["cnt"].sum()
daily_average = filtered_day["cnt"].mean()
total_casual = filtered_day["casual"].sum()
total_registered = filtered_day["registered"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Rentals",
    f"{total_rentals:,.0f}"
)

col2.metric(
    "Daily Average",
    f"{daily_average:,.0f}"
)

col3.metric(
    "Casual Users",
    f"{total_casual:,.0f}"
)

col4.metric(
    "Registered Users",
    f"{total_registered:,.0f}"
)

st.markdown("---")


# 8. MONTHLY RENTAL TRENDS & MONTHLY GROWTH

st.subheader("Monthly Rental Overview")
st.caption("Monthly rental trends and percentage growth")

monthly_rentals = (
    filtered_day
    .groupby(filtered_day["dteday"].dt.month)["cnt"]
    .sum()
)

monthly_growth = monthly_rentals.pct_change() * 100

month_names = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

monthly_rentals.index = [
    month_names[i - 1] for i in monthly_rentals.index
]

monthly_growth.index = monthly_rentals.index

col1, col2 = st.columns([1.5, 1])

with col1:
    with st.container(border=True):
        st.markdown("#### Monthly Rental Trends")

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            monthly_rentals.index,
            monthly_rentals.values,
            color=SOFT_BLUE,
            marker="o",
            linewidth=2.5,
            markersize=6
        )

        ax.fill_between(
            range(len(monthly_rentals)),
            monthly_rentals.values,
            color=SOFT_BLUE,
            alpha=0.12
        )

        style_chart(ax)
        ax.set_ylabel("Total Rentals")
        ax.set_xlabel("Month")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

with col2:
    with st.container(border=True):
        st.markdown("#### Monthly Growth")

        growth_data = monthly_growth.dropna()

        fig, ax = plt.subplots(figsize=(6, 4))

        growth_colors = [
            CYAN if value >= 0 else "#E58B8B"
            for value in growth_data.values
        ]

        ax.bar(
            growth_data.index,
            growth_data.values,
            color=growth_colors,
            width=0.65
        )

        ax.axhline(0, color=NAVY, linewidth=0.8)

        style_chart(ax)
        ax.set_ylabel("Growth (%)")
        ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


# =====================================================
# 9. HOURLY RENTAL PATTERNS
# =====================================================

st.markdown("---")
st.subheader("Hourly Rental Patterns")
st.caption("Average bike rentals across 24 hours")

hourly_rentals = (
    filtered_hour
    .groupby("hr")["cnt"]
    .mean()
)

with st.container(border=True):
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        hourly_rentals.index,
        hourly_rentals.values,
        color=CYAN,
        marker="o",
        linewidth=2.5,
        markersize=5
    )

    ax.fill_between(
        hourly_rentals.index,
        hourly_rentals.values,
        color=CYAN,
        alpha=0.12
    )

    style_chart(ax)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Rentals")
    ax.set_xticks(range(24))

    peak_hour = hourly_rentals.idxmax()
    lowest_hour = hourly_rentals.idxmin()

    ax.scatter(
        [peak_hour],
        [hourly_rentals.loc[peak_hour]],
        color="#E58B8B",
        s=70,
        zorder=5
    )

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

peak_col, low_col = st.columns(2)

peak_col.metric(
    "Peak Rental Hour",
    f"{peak_hour:02d}:00",
    f"{hourly_rentals.loc[peak_hour]:.2f} rentals"
)

low_col.metric(
    "Lowest Rental Hour",
    f"{lowest_hour:02d}:00",
    f"{hourly_rentals.loc[lowest_hour]:.2f} rentals"
)


# 10. WEATHER ANALYSIS

st.markdown("---")
st.subheader("Weather Analysis")
st.caption("Rental distribution and average rentals by weather condition")

weather_labels = {
    1: "Clear / Few clouds",
    2: "Mist / Cloudy",
    3: "Light rain / snow",
    4: "Heavy rain / snow"
}

weather_data = (
    filtered_hour
    .groupby("weathersit")["cnt"]
    .agg(["sum", "mean"])
    .reindex([1, 2, 3, 4], fill_value=0)
)

col1, col2 = st.columns([1.2, 1])

# Donut Chart and Legend
with col1:
    with st.container(border=True):
        st.markdown("#### Weather Rental Distribution")

        fig, ax = plt.subplots(figsize=(7, 4))

        valid_weather = weather_data[
            weather_data["sum"] > 0
        ]

        wedges, _ = ax.pie(
            valid_weather["sum"],
            colors=[
                WEATHER_COLORS[int(i) - 1]
                for i in valid_weather.index
            ],
            startangle=90,
            wedgeprops={
                "width": 0.38,
                "edgecolor": BACKGROUND
            }
        )

        total_weather_rentals = valid_weather["sum"].sum()

        ax.text(
            0, 0,
            f"{total_weather_rentals / 1_000_000:.2f}M\nRentals",
            ha="center",
            va="center",
            fontsize=13,
            fontweight="bold",
            color=NAVY
        )

        ax.legend(
            wedges,
            [
                f"{weather_labels[i]}  "
                f"{weather_data.loc[i, 'sum'] / total_weather_rentals * 100:.1f}%"
                for i in valid_weather.index
            ],
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            frameon=False,
            fontsize=8
        )

        ax.set_aspect("equal")
        plt.tight_layout()

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

# Weather Average Bar Chart
with col2:
    with st.container(border=True):
        st.markdown("#### Average Rentals by Weather")

        fig, ax = plt.subplots(figsize=(6, 4))

        weather_means = weather_data["mean"]

        ax.bar(
            [str(i) for i in weather_means.index],
            weather_means.values,
            color=WEATHER_COLORS,
            width=0.6
        )

        style_chart(ax)
        ax.set_xlabel("Weather Condition")
        ax.set_ylabel("Average Rentals")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

# Weather Legend
with st.container(border=True):
    st.markdown("#### Weather Conditions")

    legend_cols = st.columns(4)

    for i, col in enumerate(legend_cols, start=1):
        with col:
            st.markdown(
                f"""
                <div style="
                    background-color: {WEATHER_COLORS[i-1]};
                    color: #17233F;
                    padding: 8px;
                    border-radius: 8px;
                    text-align: center;
                    font-weight: bold;
                    font-size: 20px;
                    margin-bottom: 5px;
                ">{i}</div>
                """,
                unsafe_allow_html=True
            )
            st.caption(weather_labels[i])


# 11. USER TYPE COMPARISON

st.markdown("---")
st.subheader("User Type Comparison")
st.caption("Casual and registered rentals by day type")

user_data = (
    filtered_day
    .groupby("workingday")[["casual", "registered"]]
    .sum()
    .reindex([0, 1], fill_value=0)
)

user_data.index = [
    "Non-working Day",
    "Working Day"
]

with st.container(border=True):
    fig, ax = plt.subplots(figsize=(10, 4))

    x = range(len(user_data))
    width = 0.34

    ax.bar(
        [i - width / 2 for i in x],
        user_data["casual"],
        width,
        label="Casual",
        color=SOFT_BLUE
    )

    ax.bar(
        [i + width / 2 for i in x],
        user_data["registered"],
        width,
        label="Registered",
        color=CYAN
    )

    style_chart(ax)
    ax.set_xticks(list(x))
    ax.set_xticklabels(user_data.index)
    ax.set_ylabel("Total Rentals")
    ax.legend(frameon=False)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# 12. TEMPERATURE ANALYSIS

st.markdown("---")
st.subheader("Advanced Analysis: Temperature Binning")
st.caption("Average bike rentals based on temperature categories")

if "temp_category" not in filtered_day.columns:
    filtered_day["temp_celsius"] = filtered_day["temp"] * 41

    filtered_day["temp_category"] = pd.cut(
        filtered_day["temp_celsius"],
        bins=[0, 10, 20, 30, 41],
        labels=["Dingin", "Sejuk", "Hangat", "Panas"],
        include_lowest=True
    )

temperature_order = [
    "Dingin",
    "Sejuk",
    "Hangat",
    "Panas"
]

temperature_data = (
    filtered_day
    .groupby("temp_category", observed=False)["cnt"]
    .mean()
    .reindex(temperature_order)
)

with st.container(border=True):
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.bar(
        temperature_data.index.astype(str),
        temperature_data.values,
        color=[
            SOFT_BLUE,
            CYAN,
            "#55B9C7",
            "#77A9D8"
        ],
        width=0.6
    )

    style_chart(ax)
    ax.set_xlabel("Temperature Category")
    ax.set_ylabel("Average Rentals")

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# 13. FOOTER

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align: center;
        color: #52627D;
        padding: 15px;
        font-size: 13px;
    ">
        🚲 <b>Bike Sharing Dashboard</b><br>
        Data Analysis Project · 2011–2012
    </div>
    """,
    unsafe_allow_html=True
)

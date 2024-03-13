import pandas as pd
import streamlit as st
from mplsoccer import PyPizza
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import math
from scipy import stats
import requests

# Function to embed Google Analytics tracking code
def google_analytics():
    google_analytics_code = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-8GYL51JTS7"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-8GYL51JTS7');
    </script>
    """
    return google_analytics_code


# add png image centered on the column
st.image("laliga.svg", use_column_width=True)

# Load data from GitHub repository
medios_url = "https://raw.githubusercontent.com/imjoseba/player_profile/main/medios.csv"
medios = pd.read_csv(medios_url)

# Define font paths from GitHub repository
fonts_base_url = "https://raw.githubusercontent.com/imjoseba/player_profile/main/fonts/"
font_normal_path = fonts_base_url + "Cousine-Regular.ttf"
font_italic_path = fonts_base_url + "Cousine-Italic.ttf"
font_bold_path = fonts_base_url + "Cousine-Bold.ttf"

# Download fonts
font_normal = requests.get(font_normal_path).content
font_italic = requests.get(font_italic_path).content
font_bold = requests.get(font_bold_path).content

# Write fonts to temporary files
with open("Cousine-Regular.ttf", "wb") as f:
    f.write(font_normal)
with open("Cousine-Italic.ttf", "wb") as f:
    f.write(font_italic)
with open("Cousine-Bold.ttf", "wb") as f:
    f.write(font_bold)

# Create FontProperties objects for each font
font_normal_prop = FontProperties(fname="Cousine-Regular.ttf")
font_italic_prop = FontProperties(fname="Cousine-Italic.ttf")
font_bold_prop = FontProperties(fname="Cousine-Bold.ttf")

# Create select boxes and radar plots for both players
selected_player_1, selected_player_2 = st.columns(2)
with selected_player_1:
    player_1_name = st.selectbox("Select the first player:", medios['player'])

    # Get the first selected player's data
    player_data_1 = medios[medios['player'] == player_1_name].iloc[0]
    params = list(medios.columns[4:])
    player_1_values = list(player_data_1.values[4:])
    values_1 = [math.floor(stats.percentileofscore(medios[param], value)) for param, value in zip(params, player_1_values)]

    # Plot radar chart for the first player
    baker = PyPizza(
        params=params,
        background_color="#FFFFFF",
        straight_line_color="#FFFFFF",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=30
    )
    fig1, ax1 = baker.make_pizza(
        values_1,
        figsize=(12, 12),
        color_blank_space="same",
        slice_colors=["#1A78CF"] * 5 + ["#FF9300"] * 5 + ['#d70232'] * 5,
        value_colors=["#000000"] * 15,
        value_bck_colors=["#1A78CF"] * 5 + ["#FF9300"] * 5 + ['#d70232'] * 5,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
        kwargs_params=dict(color="#000000", fontsize=11, fontproperties=font_normal_prop, va="center"),
        kwargs_values=dict(color="#000000", fontsize=11, fontproperties=font_normal_prop, zorder=3,
                            bbox=dict(edgecolor="#000000", facecolor="cornflowerblue", boxstyle="round,pad=0.2", lw=1))
    )
    fig1.text(0.5, 0.975, player_1_name, size=30, ha="center", fontproperties=font_bold_prop, color="#000000")
    fig1.text(0.99, 0.005, "data: fbref\ninspired by: @Lanus Stats\nJoseba Moreno: imjoseba@hotmail.com", size=12,
              color="#000000", ha="right", fontproperties=font_italic_prop)
    fig1.text(0.25, 0.925, "Attack contribution         Passes        Defence contribution", size=14,
              color="#000000", fontproperties=font_bold_prop)
    fig1.patches.extend([
        plt.Circle((0.23, 0.93), 0.015, fill=True, color="#1A78CF", zorder=3, clip_on=False, transform=fig1.transFigure, figure=fig1),
        plt.Circle((0.50, 0.93), 0.015, fill=True, color="#FF9300", zorder=3, clip_on=False, transform=fig1.transFigure, figure=fig1),
        plt.Circle((0.64, 0.93), 0.015, fill=True, color="#d70232", zorder=3, clip_on=False, transform=fig1.transFigure, figure=fig1)
    ])

with selected_player_2:
    player_2_name = st.selectbox("Select the second player:", medios['player'])

    # Get the second selected player's data
    player_data_2 = medios[medios['player'] == player_2_name].iloc[0]
    player_2_values = list(player_data_2.values[4:])
    values_2 = [math.floor(stats.percentileofscore(medios[param], value)) for param, value in zip(params, player_2_values)]

    # Plot radar chart for the second player
    fig2, ax2 = baker.make_pizza(
        values_2,
        figsize=(12, 12),
        color_blank_space="same",
        slice_colors=["#1A78CF"] * 5 + ["#FF9300"] * 5 + ['#d70232'] * 5,
        value_colors=["#000000"] * 15,
        value_bck_colors=["#1A78CF"] * 5 + ["#FF9300"] * 5 + ['#d70232'] * 5,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
        kwargs_params=dict(color="#000000", fontsize=11, fontproperties=font_normal_prop, va="center"),
        kwargs_values=dict(color="#000000", fontsize=11, fontproperties=font_normal_prop, zorder=3,
                            bbox=dict(edgecolor="#000000", facecolor="cornflowerblue", boxstyle="round,pad=0.2", lw=1))
    )
    fig2.text(0.5, 0.975, player_2_name, size=30, ha="center", fontproperties=font_bold_prop, color="#000000")
    fig2.text(0.99, 0.005, "data: fbref\ninspired by: @Lanus Stats\nJoseba Moreno: imjoseba@hotmail.com", size=12,
              color="#000000", ha="right", fontproperties=font_italic_prop)
    fig2.text(0.25, 0.925, "Attack contribution         Passes        Defence contribution", size=14,
              color="#000000", fontproperties=font_bold_prop)
    fig2.patches.extend([
        plt.Circle((0.23, 0.93), 0.015, fill=True, color="#1A78CF", zorder=3, clip_on=False, transform=fig2.transFigure, figure=fig2),
        plt.Circle((0.50, 0.93), 0.015, fill=True, color="#FF9300", zorder=3, clip_on=False, transform=fig2.transFigure, figure=fig2),
        plt.Circle((0.64, 0.93), 0.015, fill=True, color="#d70232", zorder=3, clip_on=False, transform=fig2.transFigure, figure=fig2)
    ])

# Display radar charts
st.pyplot(fig1)
st.pyplot(fig2)

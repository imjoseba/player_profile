
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

# add png image centered on the column 
st.image("laliga.svg", use_column_width=True)


selected_player_1, selected_player_2 = st.columns(2)
with selected_player_1:
    selected_player_1 = st.selectbox("Select the first player:", medios['player'])

# Get the first selected player's data
player_data_1 = medios[medios['player'] == selected_player_1].iloc[0]

params = list(medios.columns[4:])
player_1 = list(player_data_1.values[4:])

values_1 = []
for x in range(len(params)):   
    values_1.append(math.floor(stats.percentileofscore(medios[params[x]], player_1[x])))

with selected_player_2:
    selected_player_2 = st.selectbox("Select the second player:", medios['player'])

# Get the second selected player's data
player_data_2 = medios[medios['player'] == selected_player_2].iloc[0]

player_2 = list(player_data_2.values[4:])

values_2 = []
for x in range(len(params)):   
    values_2.append(math.floor(stats.percentileofscore(medios[params[x]], player_2[x])))

# color for the slices and text
slice_colors = ["#1A78CF"] * 5 + ["#FF9300"] * 5 + ['#d70232'] * 5 
text_colors = ["#000000"] * 5 + ["#000000"] * 5 + ["#000000"] * 5

# instantiate PyPizza class
baker = PyPizza(
    params=params,                  # list of parameters
    background_color="#FFFFFF",     # background color
    straight_line_color="#FFFFFF",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=0,               # linewidth of last circle
    other_circle_lw=0,              # linewidth for other circles
    inner_circle_size=30            # size of inner circle (increased from 20 to 30)
)

# plot pizza for the first player
fig1, ax1 = baker.make_pizza(
    values_1,                          # list of values
    figsize=(12, 12),                # increased figsize
    color_blank_space="same",        # use same color to fill blank space
    slice_colors=slice_colors,       # color for individual slices
    value_colors=text_colors,        # color for the value-text
    value_bck_colors=slice_colors,   # color for the blank spaces
    blank_alpha=0.4,                 # alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#F2F2F2", zorder=2, linewidth=1
    ),                               # values to be used when plotting slices
    kwargs_params=dict(
    color="#000000", fontsize=11, fontproperties=font_normal_prop,
    va="center"
    ),  # values to be used when adding parameter
    kwargs_values=dict(
        color="#000000", fontsize=11, fontproperties=font_normal_prop,
        zorder=3,
        bbox=dict(
        edgecolor="#000000", facecolor="cornflowerblue",
        boxstyle="round,pad=0.2", lw=1
        )
    )  # values to be used when adding parameter-values
)

# add title for the first player
fig1.text(
    0.5, 0.975, selected_player_1, size=30,
    ha="center", fontproperties=font_bold_prop, color="#000000"
)
# add credits
CREDIT_1 = "data: fbref"
CREDIT_2 = "inspired by: @Lanus Stats"
CREDIT_3 = "Joseba Moreno: imjoseba@hotmail.com"

# add credits for the first player
fig1.text(
    0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=12,
    color="#000000",
    ha="right", fontproperties=font_italic_prop
)
fig1.text(
    0.25, 0.925, "Attack contribution         Passes        Defence contribution", size=14,
    color="#000000", fontproperties=font_bold_prop
)

# Circles (Rectangles in this case) for the first player
fig1.patches.extend([
    plt.Circle(
        (0.23, 0.93), 0.015,
        fill=True, color="#1A78CF", zorder=3, clip_on=False,
        transform=fig1.transFigure, figure=fig1
    ),
    plt.Circle(
        (0.50, 0.93), 0.015,
        fill=True, color="#FF9300", zorder=3, clip_on=False,
        transform=fig1.transFigure, figure=fig1
    ),
    plt.Circle(
        (0.64, 0.93), 0.015,
        fill=True, color="#d70232", zorder=3, clip_on=False,
        transform=fig1.transFigure, figure=fig1
    ),
])

# plot pizza for the second player
fig2, ax2 = baker.make_pizza(
    values_2,                          # list of values for the second player
    figsize=(12, 12),                # increased figsize
    color_blank_space="same",        # use same color to fill blank space
    slice_colors=slice_colors,       # color for individual slices
    value_colors=text_colors,        # color for the value-text
    value_bck_colors=slice_colors,   # color for the blank spaces
    blank_alpha=0.4,                 # alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#F2F2F2", zorder=2, linewidth=1
    ),                               # values to be used when plotting slices
    kwargs_params=dict(
    color="#000000", fontsize=11, fontproperties=font_normal_prop,
    va="center"
    ),  # values to be used when adding parameter
    kwargs_values=dict(
        color="#000000", fontsize=11, fontproperties=font_normal_prop,
        zorder=3,
        bbox=dict(
        edgecolor="#000000", facecolor="cornflowerblue",
        boxstyle="round,pad=0.2", lw=1
        )
    )  # values to be used when adding parameter-values
)

# add title for the second player
fig2.text(
    0.5, 0.975, selected_player_2, size=30,
    ha="center", fontproperties=font_bold_prop, color="#000000"
)

# add credits for the second player
fig2.text(
    0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}\n{CREDIT_3}", size=12,
    color="#000000",
    ha="right", fontproperties=font_italic_prop
)
fig2.text(
    0.25, 0.925, "Attack contribution         Passes        Defence contribution", size=14,
    color="#000000", fontproperties=font_bold_prop
)

# Circles (Rectangles in this case) for the second player
fig2.patches.extend([
    plt.Circle(
        (0.23, 0.93), 0.015,
        fill=True, color="#1A78CF", zorder=3, clip_on=False,
        transform=fig2.transFigure, figure=fig2
    ),
    plt.Circle(
        (0.50, 0.93), 0.015,
        fill=True, color="#FF9300", zorder=3, clip_on=False,
        transform=fig2.transFigure, figure=fig2
    ),
    plt.Circle(
        (0.64, 0.93), 0.015,
        fill=True, color="#d70232", zorder=3, clip_on=False,
        transform=fig2.transFigure, figure=fig2
    ),
])

# Display radar charts side by side
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)

with col2:
    st.pyplot(fig2)

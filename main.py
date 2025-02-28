import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv(r"C:/Users/Dell/Downloads/quality_of_life_indices_by_country.csv", encoding='gb18030')


from pyecharts.charts import Map
from pyecharts import options as opts

name1 = "Quality of Life Index"
info = data[["Country", name1]]
info_first = info.values.tolist()

map_chart = Map(init_opts=opts.InitOpts(width="1500px", height="1000px"))
map_chart.add(
    series_name=name1,
    data_pair=info_first,
    maptype="world",
    zoom=1,
)
map_chart.set_global_opts(
    title_opts=opts.TitleOpts(
        title=f"{name1}hhkk",
        pos_right="center",
        pos_top="5%"
    ),
    visualmap_opts=opts.VisualMapOpts(
        max_=220.1,
        min_=21.5,
        range_color=["#C6E7FF", "#87CEFA", "#0044FF"]
    )
)
map_chart.render("map.html")


selected_columns = [
    "Purchasing Power Index",
    "Safety Index",
    "Health Care Index",
    "Cost of Living Index",
    "Property Price to Income Ratio",
    "Traffic Commute Time Index",
    "Pollution Index",
    "Climate Index"
]
radar_data = {}
for index, row in data.iterrows():
    country = row["Country"]
    values = [row[col] for col in selected_columns]
    radar_data[country] = values
fig = go.Figure()
for country in radar_data.keys():
    fig.add_trace(go.Scatterpolar(
        r=radar_data[country],
        theta=selected_columns,
        fill='toself',
        name=country
    ))
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 200]
        ),
    ),
    showlegend=False,
    width=800,
    height=600,
    title="Radar Chart for Countries",
    updatemenus=[{
        "buttons": [
            {
                "label": country,
                "method": "update",
                "args": [{
                    "visible": [trace.name == country for trace in fig.data]
                }]
            } for country in radar_data.keys()
        ],
        "direction": "down",
        "showactive": True,
        "x": 0.1,
        "y": 1.1,
    }]
)
fig.show()
fig.write_html("radar_chart.html")
selected_columns_corr = [
    "Purchasing Power Index",
    "Safety Index",
    "Health Care Index",
    "Cost of Living Index",
    "Property Price to Income Ratio",
    "Traffic Commute Time Index",
    "Pollution Index",
    "Climate Index"
]

data_corr = data[selected_columns_corr]
corr = data_corr.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(
    corr,
    annot=True,
    cmap='coolwarm',
    fmt=".2f",
    annot_kws={"size": 8},
    linewidths=0.5
)
plt.title("Heatmap of Quality of Life Indices")
plt.savefig("heatmap.png")
plt.show()


selected_columns_pairplot = [
    "Purchasing Power Index",
    "Safety Index",
    "Health Care Index",
    "Cost of Living Index",
    "Property Price to Income Ratio",
    "Traffic Commute Time Index",
    "Pollution Index",
    "Climate Index"
]

data_pairplot = data[selected_columns_pairplot].dropna()

sns.set_theme(style="ticks")
sns.pairplot(data_pairplot, corner=True)
plt.savefig("pairplot.png")
plt.show()
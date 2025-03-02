import plotly.io as pio

darkly_template = dict(
    layout=dict(
        paper_bgcolor="#303030",
        plot_bgcolor="#424242",
        font=dict(color="white"),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.2)",
            zerolinecolor="rgba(255,255,255,0.3)",
            tickfont=dict(color="white"),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.2)",
            zerolinecolor="rgba(255,255,255,0.3)",
            tickfont=dict(color="white"),
        )
    )
)

pio.templates["darkly"] = darkly_template
pio.templates.default = "darkly"
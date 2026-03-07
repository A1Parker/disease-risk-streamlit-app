def apply_chart_style(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="white",
            size=14
        ),

        # Proper margins (prevents cutting)
        margin=dict(
            l=60,
            r=60,
            t=70,
            b=120
        ),

        # Legend positioning
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=13)
        )
    )

    # Axis spacing
    fig.update_xaxes(
        title_standoff=25,
        automargin=True
    )

    fig.update_yaxes(
        title_standoff=25,
        automargin=True
    )

    return fig
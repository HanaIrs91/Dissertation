import pandas as pd
import networkx as nx
import plotly.graph_objects as go

file_path = '/Users/hanairshaid/Desktop/Network curatorial strategies.csv'
df_matrix = pd.read_csv(file_path, index_col=0)

edges = []
for source in df_matrix.index:
    for target in df_matrix.columns:
        weight = df_matrix.loc[source, target]
        if weight > 0:
            edges.append((source, target, weight))

G = nx.DiGraph()
G.add_weighted_edges_from(edges)

pos = nx.circular_layout(G)

edge_traces = []
for u, v, data in G.edges(data=True):
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    weight = data['weight']
    edge_traces.append(go.Scatter(
        x=[x0, x1],
        y=[y0, y1],
        line=dict(width=0.5 + weight * 1.5, color='rgba(150,150,150,0.4)'),
        hoverinfo='none',
        mode='lines'
    ))

node_x, node_y, node_labels = [], [], []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_labels.append(node)

node_degree = dict(G.degree(weight='weight'))
node_colors = [node_degree[node] for node in G.nodes()]
node_texts = [f'{node}<br>Connections: {node_degree[node]}' for node in G.nodes()]

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers+text',
    text=node_labels,
    textposition='top center',
    hoverinfo='text',
    hovertext=node_texts,
    textfont=dict(size=8),
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        color=node_colors,
        size=14,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=1,
        line_color='black'
    )
)

fig = go.Figure(data=edge_traces + [node_trace],
                layout=go.Layout(
                    title='<b>Network of Curatorial Strategies and Community Engaged Sonic Practices</b>',
                    titlefont_size=20,
                    title_x=0.5,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(t=100, b=100, l=100, r=100),
                    paper_bgcolor='rgba(240,248,255,0.8)',
                    plot_bgcolor='rgba(240,248,255,0.8)',
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                ))

fig.show()
fig.write_html("/Users/hanairshaid/Desktop/network_curatorial_strategies.html", include_plotlyjs='cdn')

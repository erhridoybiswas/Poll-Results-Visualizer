import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Set style for static plots
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

def plot_bar_overall(summary_df, save_path="outputs/figures/overall_bar.png"):
    """Static bar chart of overall results."""
    plt.figure()
    sns.barplot(data=summary_df, x="Option", y="Percentage", palette="viridis")
    plt.title("Overall Poll Results")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_pie_overall(summary_df, save_path="outputs/figures/overall_pie.png"):
    """Static pie chart."""
    plt.figure()
    plt.pie(summary_df["Count"], labels=summary_df["Option"], autopct='%1.1f%%', startangle=90)
    plt.title("Vote Share")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_stacked_bar(crosstab_df, save_path="outputs/figures/stacked_region.png"):
    """Stacked bar chart (e.g., Answer distribution by Region)."""
    ax = crosstab_df.T.plot(kind='bar', stacked=True, colormap='tab20', figsize=(10,6))
    ax.set_title("Answer Distribution by Region (%)")
    ax.set_ylabel("Percentage")
    ax.legend(title="Answer", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# Interactive Plotly charts for Streamlit
def plotly_bar(summary_df):
    fig = px.bar(summary_df, x="Option", y="Percentage", text="Percentage",
                 title="Overall Vote Share", color="Option")
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    return fig

def plotly_pie(summary_df):
    fig = px.pie(summary_df, names="Option", values="Count", title="Vote Distribution")
    return fig

def plotly_stacked_bar(df, group_col):
    crosstab = pd.crosstab(df["Answer"], df[group_col], normalize='columns') * 100
    fig = px.bar(crosstab.T, title=f"Answer Distribution by {group_col} (%)",
                 labels={"value": "Percentage", group_col: group_col},
                 barmode="stack")
    return fig

def plotly_trend(df):
    weekly = df.set_index("Date").resample('W')["Answer"].count()
    fig = px.line(weekly, title="Response Volume Over Time", labels={"value": "Responses", "Date": "Week"})
    return fig
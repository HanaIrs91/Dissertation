import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

file_path = "/Users/hanairshaid/Desktop/Likert Scale Answers.xlsx"
df = pd.read_excel(file_path)

likert_scale_order = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']
font_properties = fm.FontProperties(fname="/System/Library/Fonts/Supplemental/Times New Roman.ttf")

all_freq_tables = {}
means = {}
medians = {}
modes = {}
stds = {}

def split_text_two_lines(text):
    if len(text) <= 100:
        return text
    else:
        mid = len(text) // 2
        left_space = text.rfind(' ', 0, mid)
        right_space = text.find(' ', mid)
        split_pos = left_space if (mid - left_space) < (right_space - mid) else right_space
        if split_pos == -1:
            split_pos = mid
        return text[:split_pos] + '\n' + text[split_pos+1:]

mapping = {
    'Strongly Disagree': 1,
    'Disagree': 2,
    'Neutral': 3,
    'Agree': 4,
    'Strongly Agree': 5
}

df_numeric = df.replace(mapping)

for idx, question in enumerate(df.columns):
    response_counts = df[question].value_counts().reindex(likert_scale_order, fill_value=0)
    all_freq_tables[question] = response_counts

    question_id = f"Q{idx+1}"
    wrapped_title = split_text_two_lines(question)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=response_counts.index, y=response_counts.values, palette="coolwarm")
    plt.xlabel("Response", fontproperties=font_properties)
    plt.ylabel("Count", fontproperties=font_properties)
    plt.title(f"{question_id}: {wrapped_title}", fontproperties=font_properties, fontsize=11, loc='left', pad=20, multialignment='left')
    plt.xticks(fontproperties=font_properties)
    plt.yticks(fontproperties=font_properties)
    plt.tight_layout(rect=[0, 0, 1, 0.88])
    plt.show()

    series = df_numeric[question].dropna()
    means[question] = series.mean()
    medians[question] = series.median()
    modes[question] = series.mode().iloc[0] if not series.mode().empty else None
    stds[question] = series.std()

output_file = "/Users/hanairshaid/Desktop/Likert_Scale_Descriptive_Tables.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for question, table in all_freq_tables.items():
        df_out = pd.DataFrame({question: table})
        df_out.loc['Mean', question] = means[question]
        df_out.loc['Median', question] = medians[question]
        df_out.loc['Mode', question] = modes[question]
        df_out.loc['Std Dev', question] = stds[question]
        df_out.to_excel(writer, sheet_name=f"Q{list(df.columns).index(question)+1}", index=True)

question_labels = [f"Q{i+1}" for i in range(len(df.columns))]
mean_values = list(means.values())
std_values = list(stds.values())

plt.figure(figsize=(10, 6))
sns.barplot(x=mean_values, y=question_labels, palette="coolwarm", orient='h')
plt.xlabel("Mean Rating", fontproperties=font_properties)
plt.title("Mean Rating per Question", fontproperties=font_properties)
plt.xticks(fontproperties=font_properties)
plt.yticks(fontproperties=font_properties)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x=std_values, y=question_labels, palette="coolwarm", orient='h')
plt.xlabel("Standard Deviation", fontproperties=font_properties)
plt.title("Standard Deviation per Question", fontproperties=font_properties)
plt.xticks(fontproperties=font_properties)
plt.yticks(fontproperties=font_properties)
plt.tight_layout(rect=[0, 0, 1, 0.88])
plt.show()

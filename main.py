from flask import Flask, render_template
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3

connection = sqlite3.connect('./instance/station-database.db')
query = 'SELECT * FROM station'
df = pd.read_sql_query(query,connection)
connection.close()

# GETTING PAST DATA
connection = sqlite3.connect('./instance/station-database-past.db')
query = 'SELECT * FROM station'
df_past = pd.read_sql_query(query,connection)
connection.close()

app = Flask(__name__)

@app.route('/')
def index():
    # Create a Plotly Express chart

    # BAR CHART FUTURE
    country_counts = df['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'count']

    colours = ['#000033','blue','green','black','red','white','#E0E0E0','yellow','orange','brown','purple']

    fig = px.bar(country_counts, y='country', x='count', orientation='h', title='Number of Planned Missions by Country',color=colours)
    fig.update_layout(yaxis_title='Country', xaxis_title='Count')
    fig.update_yaxes(categoryorder='total ascending')

    plotly_html = fig.to_html()
    
    
    # PIE CHART FUTURE
    company_counts = df.owner.value_counts().reset_index()
    company_counts.columns = ['Enterprise', 'Count']

    fig2 = px.pie(company_counts, names='Enterprise', values='Count', title='Company-Mission Distribution')
    
    
    # Adjust the label distance by changing the factor (0.5 in this example)
    label_distance_factor = 0.5  # Adjust this factor to control label distance from center

    # Calculate the position of labels within the pie chart
    label_x = []
    label_y = []
    total = company_counts['Count'].sum()
    for count in company_counts['Count']:
        label_x.append(0.5 * label_distance_factor * count / total)
        label_y.append(0)

    # Update the layout to position labels within the pie slices
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(annotations=[
        dict(text=company_counts['Enterprise'][i], x=label_x[i], y=label_y[i], showarrow=False)
        for i in range(len(company_counts))
    ])

    plotly_html2 = fig2.to_html()
    
    
    
    # PAST AND FUTURE COMPARISON
    
    df['Mission Type'] = 'Future'
    df_past['Mission Type'] = 'Past'

    # Add a dummy column to both DataFrames to represent the number of missions
    df['Mission Count'] = 1
    df_past['Mission Count'] = 1

    # Concatenate the two DataFrames
    combined_df = pd.concat([df, df_past], ignore_index=True)

    # Group by country and Mission Type, and count the number of missions
    grouped_data = combined_df.groupby(['country', 'Mission Type']).size().reset_index(name='Count')

    # Sort the data frame by 'Count' column in descending order
    grouped_data = grouped_data.sort_values(by='Count', ascending=False)

    fig3 = px.bar(grouped_data, x='country', y='Count', color='Mission Type', labels={'Mission Type': 'Mission Type'})
    fig3.update_layout(title='Past and Future Missions by Country', xaxis_title='Country', yaxis_title='Number of Missions')
    
    plotly_html3 = fig3.to_html()  
    
    
    # PIE CHART PAST COMPANIES
    
    company_counts = df_past.owner.value_counts().reset_index()
    company_counts.columns = ['Enterprise', 'Count']

    fig4 = px.pie(company_counts, names='Enterprise', values='Count', title='Company-Mission Distribution (past)')


    label_distance_factor = 0.5  

    label_x = []
    label_y = []
    total = company_counts['Count'].sum()
    for count in company_counts['Count']:
        label_x.append(0.5 * label_distance_factor * count / total)
        label_y.append(0)

    fig4.update_traces(textposition='inside', textinfo='percent+label')
    fig4.update_layout(annotations=[
            dict(text=company_counts['Enterprise'][i], x=label_x[i], y=label_y[i], showarrow=False)
            for i in range(len(company_counts))
        ])
    
    plotly_html4 = fig4.to_html()  
    
    
    # SCATTER PLOT PLANNED MISSIONS
    
    fig5 = px.scatter(df, x=df.country, y=df.year, title='Years and Planned Missions by Country')
    plotly_html5= fig5.to_html()  
    
    
    # Render the HTML template with the Plotly chart embedded
    return render_template('index.html', plotly_html=plotly_html,plotly_html2=plotly_html2, plotly_html3=plotly_html3,plotly_html4=plotly_html4,plotly_html5=plotly_html5)


    

if __name__ == '__main__':
    app.run(debug=True)
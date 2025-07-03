import mysql.connector
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "95095",
    database = "crime"
)

cursor = conn.cursor()

query = "Select * from crime_data;"


#df = pd.read_sql(query, conn)

# 1. Spatial Analysis:
# Where are the geographical hotspots for reported crimes?
def Spatial_Analysis():
    query1 = """  Select 
                            Round(LAT, 3) as lat_group,
                            Round(LON, 3) as lon_group,
                            Count(*) as crime_count
                    from crime_data
                    Group By lat_group, lon_group
                    Order By crime_count Desc
                    Limit 10;
    """
    cursor.execute(query1)
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    df1 = pd.DataFrame(rows, columns = columns)
    print(df1)

    plt.figure(figsize=(10, 6))
    sns.set_style("white")


    scatter = sns.scatterplot(
        data = df1,
        x = "lon_group",
        y = "lat_group",
        size = "crime_count",
        hue = "crime_count",
        sizes = (100, 500),
        palette = 'Reds',
        legend = "brief"
    )

    for i in range(len(df1)):
        plt.text(
            df1['lon_group'][i],
            df1['lat_group'][i],
            str(df1['crime_count'][i]),
            fontsize = 9,
            ha = 'center',
            va = 'bottom'
        )

    plt.title("Top 10 Crime Hotspots by Latitude/Longitude", fontsize = 14, weight = "bold")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.show()


#Spatial_Analysis()

# Victim Demographics:
# What is the distribution of victim ages in reported crimes?

def Victim_Demographic_by_Ages():
    query2 = """
                With age_category as (
                select *,
                case
                    When Vict_Age <= 12 Then 'Children'
                    When Vict_Age > 12 and Vict_Age <= 17 Then 'Teen'
                    When Vict_Age > 17 and Vict_Age <= 24 Then 'Young Adult'
                    When Vict_Age > 24 and Vict_Age <= 44 Then 'Adult'
                    When Vict_Age > 44 And Vict_Age < 65 Then 'Mid Aged'
                    When Vict_Age >= 65 Then 'Senior'
                End as age_group
                from crime_data
                )
                select age_group, Count(*) as Total_Count from age_category
                Group By age_group
                Order By Total_Count Desc;"""
    
    cursor.execute(query2)
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    df2 = pd.DataFrame(rows, columns = columns)
    print(df2)

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")

    age_order = ["Children","Teen", "Young Adult", "Adult", "Mid Aged", "Senior"]
    df2['age_group'] = pd.Categorical(df2['age_group'], categories = age_order, ordered = True)
    df2_sorted = df2.sort_values("age_group")

    sns.barplot(data=df2_sorted, x = 'age_group', y = 'Total_Count', palette= 'viridis')

    plt.title("Victim Age Group Distribution in Reported Crimes", fontsize = 14, weight = 'bold')
    plt.xlabel("Age Group")
    plt.ylabel("Number of Victims")
    plt.xticks(rotation = 15)
    plt.tight_layout()
    plt.show()


#Victim_Demographic_by_Ages()

# Is there a significant difference in crime rates between male and female victims?
def Gender_wise_crime():
    query3 = """
                select Vict_Sex, Count(*) as Gender_Count from crime_data
                Where Vict_Sex IN ('M', 'F')
                Group By Vict_Sex
                Order By Gender_Count Desc;"""

    cursor.execute(query3)
    row = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    df3 = pd.DataFrame(row, columns = columns)
    print(df3)

    plt.figure(figsize=(6, 6))
    colors = ['#66B3FF', '#FF9999']
    explode = (0.05, 0.05)

    plt.pie(df3['Gender_Count'], labels = df3['Vict_Sex'], autopct='%1.1f%%', startangle = 140,
                                 colors = colors, explode = explode, shadow = True)
    plt.title('Crime Distribution By Victim Gender', fontsize = 14, weight = 'bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

#Gender_wise_crime()


# Location Analysis:
# Where do most crimes occur based on the "Location" column?
def Location_Analysis():
    query1 = """  Select 
                            Location, 
                            Count(*) as crime_count
                    from crime_data
                    Group By Location
                    Order By crime_count Desc
                    Limit 10;
    """
    cursor.execute(query1)
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    df1 = pd.DataFrame(rows, columns = columns)
    print(df1)

    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.barplot(data = df1, x = 'Location', y = 'crime_count', palette='viridis')

    plt.title('Top 10 Crime Locations', fontsize=14, weight='bold')
    plt.xlabel('location', fontsize = 12)
    plt.ylabel('Crime Count', fontsize = 12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

#Location_Analysis()

# Crime Code Analysis:
# What is the distribution of reported crimes based on Crime Code?
def Crime_Based_Analysis():
    query1 = """
                Select 
                    Crm_Cd, 
                    Crm_Cd_Desc, 
                    count(*) as crime_count 
                from crime_data
                Group By Crm_Cd, Crm_Cd_Desc
                Order By crime_count Desc
                Limit 10;
            """
    cursor.execute(query1)
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    df1 = pd.DataFrame(rows, columns = columns)
    print(df1)

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.barplot(data=df1, x='crime_count',y = 'Crm_Cd_Desc', palette='Reds_r')
    plt.title("Top 10 Crime Types by Frequency", fontsize=14, weight='bold')
    plt.xlabel('Number of Incidents')
    plt.ylabel('Crime Description')
    plt.tight_layout()
    plt.show()

Crime_Based_Analysis()



cursor.close()
conn.close()
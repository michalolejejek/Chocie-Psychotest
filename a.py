import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the CSV file
data = pd.read_csv('s01.csv', delimiter=';')

# Convert the 'responseTime' column to numeric
data['responseTime'] = pd.to_numeric(data['responseTime'], errors='coerce')

# Filter out rows with missing values in 'responseTime' or 'confAnswer'
filtered_data = data.dropna(subset=['responseTime', 'confAnswer'])

# Create a scatter plot
plt.scatter(filtered_data['responseTime'], filtered_data['confAnswer'])

# Set plot title and labels
plt.title('Correlation between Response Time and Confidence Answer')
plt.xlabel('Response Time')
plt.ylabel('Confidence Answer')

# Show the plot
plt.show()
# Calculate average and median for each parameter
average_response_time = filtered_data['responseTime'].mean()
median_response_time = filtered_data['responseTime'].median()
average_conf_answer = filtered_data['confAnswer'].mean()
median_conf_answer = filtered_data['confAnswer'].median()

# Write results to a text file
with open('results.txt', 'w') as file:
    file.write(f'Average Response Time: {average_response_time}\n')
    file.write(f'Median Response Time: {median_response_time}\n')
    file.write(f'Average Confidence Answer: {average_conf_answer}\n')
    file.write(f'Median Confidence Answer: {median_conf_answer}\n')
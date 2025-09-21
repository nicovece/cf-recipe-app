from io import BytesIO
import base64
import matplotlib.pyplot as plt

def get_graph():
    """Convert matplotlib plot to base64 image for HTML display"""
    # create a BytesIO buffer for the image
    buffer = BytesIO()
    # create a plot with a bytesIO object as a file-like object. Set format to png
    plt.savefig(buffer, format="png")
    # set cursor to the beginning of the stream
    buffer.seek(0)
    # retrieve the content of the file
    image_png = buffer.getvalue()
    # encode the bytes-like object
    graph = base64.b64encode(image_png)
    # decode to get the string as output
    graph = graph.decode("utf-8")
    # free up the memory of buffer
    buffer.close()
    # return the image/graph
    return graph

def get_chart(chart_type, data, **kwargs):
    """
    Generate charts based on recipe data
    
    Args:
        chart_type: Type of chart ('#1'=bar, '#2'=pie, '#3'=line)
        data: pandas DataFrame with recipe data
        **kwargs: Additional parameters like labels
    """
    # switch plot backend to AGG (Anti-Grain Geometry) - to write to file
    # AGG is preferred solution to write PNG files
    plt.switch_backend("AGG")
    # specify figure size
    fig = plt.figure(figsize=(8, 5))
    
    # select chart_type based on user input from the form
    if chart_type == "#1":
        # Bar chart: Recipe names on x-axis, cooking time on y-axis
        plt.bar(data["name"], data["cooking_time"])
        plt.title("Recipe Cooking Times")
        plt.xlabel("Recipe Name")
        plt.ylabel("Cooking Time (minutes)")
        plt.xticks(rotation=45, ha='right')
        
    elif chart_type == "#2":
        # Pie chart: Distribution of difficulty levels
        difficulty_counts = data["difficulty"].value_counts()
        plt.pie(difficulty_counts.values, labels=difficulty_counts.index, autopct='%1.1f%%')
        plt.title("Recipe Difficulty Distribution")
        
    elif chart_type == "#3":
        # Line chart: Cooking time vs ingredient count
        plt.plot(data["ingredient_count"], data["cooking_time"], marker='o')
        plt.title("Cooking Time vs Number of Ingredients")
        plt.xlabel("Number of Ingredients")
        plt.ylabel("Cooking Time (minutes)")
        
    else:
        print("unknown chart type")
    
    # specify layout details
    plt.tight_layout()
    # render the graph to file
    chart = get_graph()
    return chart

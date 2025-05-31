from IPython.display import Image, display

# from Backend.services.assistant.graph.builder import build_graph
# from Backend.services.assistant.utils import display_graph


def display_graph(graph):
    """Renders and displays a Mermaid graph as a PNG image in Jupyter/IPython."""

    try:
        image_bytes = graph.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as f:
            f.write(image_bytes)
        display(Image(data=image_bytes))
    except Exception as e:
        print("Error rendering or saving graph:", e)


# app = build_graph()

# if __name__ == "__main__":
#     display_graph(app)

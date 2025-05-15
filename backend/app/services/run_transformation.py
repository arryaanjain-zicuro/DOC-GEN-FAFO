# app/services/run_transformation.py

from workflows.transformation_graph import transformation_graph
import asyncio

def run_graph_sync(alpha_path: str, beta_word_path: str, beta_excel_path: str):
    graph = transformation_graph()
    print("Initial state being passed to graph:", {
    "alpha_path": alpha_path,
    "beta_word_path": beta_word_path,
    "beta_excel_path": beta_excel_path
    })
    return graph.invoke({
        "alpha_path": alpha_path,
        "beta_word_path": beta_word_path,
        "beta_excel_path": beta_excel_path
    })

async def run_graph_async(alpha_path, beta_word_path, beta_excel_path):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None,  # Uses default thread pool executor
        run_graph_sync, alpha_path, beta_word_path, beta_excel_path
    )
    return result
# app/services/run_transformation.py

from workflows.transformation_graph import build_transformation_graph
import concurrent.futures

def run_graph_sync(alpha_path: str, beta_word_path: str, beta_excel_path: str):
    graph = build_transformation_graph()
    return graph.invoke({
        "alpha_path": alpha_path,
        "beta_word_path": beta_word_path,
        "beta_excel_path": beta_excel_path
    })

async def run_graph_async(alpha_path: str, beta_word_path: str, beta_excel_path: str):
    loop = concurrent.futures.ThreadPoolExecutor()
    return await loop.submit(run_graph_sync, alpha_path, beta_word_path, beta_excel_path)

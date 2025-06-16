import gradio as gr
from rag_core.pipeline import rag_with_decomposition

custom_css = """[your CSS here]"""
custom_js = """[your JS here]"""

with gr.Blocks(css=custom_css, theme=gr.themes.Base()) as demo:
    gr.HTML('<div id="particles-js"></div>' + custom_js)
    gr.Markdown(
        """
        # Financial RAG Assistant with Query Decomposition
        Enter your financial query below. The system will decompose your query, retrieve context from Qdrant across multiple collections, fetch integrated annual report data, and generate a context-aware answer.
        """
    )
    with gr.Column(elem_id="response-container"):
        final_answer_output = gr.Textbox(
            label="Response",
            lines=8,
            interactive=False,
            elem_id="response-textbox"
        )
        with gr.Accordion("Show Full RAG Output (Detailed)", open=False):
            output_json = gr.JSON(label="All Details", elem_id="json-output")
    gr.Markdown("<div style='flex-grow:1'></div>")
    with gr.Column(elem_id="input-container"):
        query_input = gr.Textbox(
            label="Your Financial Query",
            placeholder="e.g., What are the recent cashflow trends for the company?",
            lines=3
        )
        company_filter_input = gr.Textbox(
            label="Company Filter (optional)",
            placeholder="e.g., Apple Inc."
        )
        submit_btn = gr.Button("Get Answer", variant="primary")
    def split_outputs(query: str, company: str):
        result = rag_with_decomposition(query, company)
        return result["Final Answer"], result
    submit_btn.click(
        fn=split_outputs,
        inputs=[query_input, company_filter_input],
        outputs=[final_answer_output, output_json]
    )
demo.launch(share=True)

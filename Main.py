import Config
import gradio as gr

with gr.Blocks(title='专有名词翻译汇总', analytics_enabled=False) as demo:
    gr.Markdown('# 添加新词条')
    gr.Markdown('此界面用于新增词条')

    with gr.Row():
        with gr.Column(scale=1, min_width=600):
            with gr.Column(variant='panel'):
                text_word = gr.Textbox(label="原词/词组")
                text_trans = gr.Textbox(label="翻译")
                text_tag = gr.Dropdown(label="Tag", choices=['a', 'b', 'c'], max_choices=2, multiselect=True)
            with gr.Accordion(label='添加Tag', open=False):
                text_new_tag = gr.Textbox(label='Tag')
                btn_tag = gr.Button('添加')

        with gr.Column(scale=2, min_width=600, variant='panel'):
            text_desc = gr.TextArea(label="描述", lines=7)
            text_example = gr.TextArea(label="示例", lines=5)
            btn_add = gr.Button('添加')

if __name__ == '__main__':
    demo.launch(auth=Config.AUTH, server_port=Config.PORT)

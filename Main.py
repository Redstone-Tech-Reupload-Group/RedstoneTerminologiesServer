# -*- coding: utf-8 -*-

import Config
import gradio as gr
import utils.Dictionary as Dic

now_index = -1

with gr.Blocks(title='专有名词翻译汇总', analytics_enabled=True) as demo:
    gr.Markdown('# 红石科技搬运组专有名词翻译汇总')
    gr.Markdown('欢迎使用红石科技专有名词词库在线维护系统！')
    with gr.Tab('新词条'):
        gr.Markdown('## 添加新词条')
        gr.Markdown('此界面用于新增词条')

        with gr.Row():
            with gr.Column(scale=1, min_width=600):
                with gr.Column(variant='panel'):
                    text_word = gr.Textbox(label="原词/词组")
                    text_trans = gr.Textbox(label="翻译")
                    text_tag = gr.Dropdown(label="Tag", choices=Dic.get_tag(), max_choices=5,
                                           multiselect=True)
                with gr.Accordion(label='添加Tag', open=False):
                    text_new_tag = gr.Textbox(label='Tag')
                    btn_tag = gr.Button('添加')
                    label_tag = gr.Markdown(value='')

            with gr.Column(scale=2, min_width=600, variant='panel'):
                text_desc = gr.TextArea(label="描述", lines=7)
                text_example = gr.TextArea(label="示例", lines=5)
                btn_add = gr.Button('添加')
                label_word = gr.Markdown('')


        def add_word(word, trans, tag, desc, example):
            fi, index = Dic.add_word(word, trans, desc, example, tag)
            if index == -1:
                return '已存在该词条，请前往修改界面进行修改'

            return f'添加了{fi}-{index}号词条'


        def add_tag(tag):
            result, tags = Dic.add_tag(tag)
            print(tags)
            # TODO 说是后续4.0版本会修复不更新的问题
            text_tag.update(choices=tags)
            if result == 1:
                demo.update()
                return 'success!'
            else:
                return '已存在'


        btn_add.click(add_word, inputs=[text_word, text_trans, text_tag, text_desc, text_example], outputs=label_word)
        btn_tag.click(add_tag, inputs=text_new_tag, outputs=label_tag)

    with gr.Tab('删改词条'):
        gr.Markdown('# 删改词条')

        with gr.Row():
            with gr.Column(scale=1):
                search_input = gr.Textbox(label='词条')
                with gr.Row():
                    clean_btn = gr.Button(value='clean')
                    search_btn = gr.Button(value='search', variant='primary')
                submit_btn = gr.Button(value='submit', variant='primary')
                del_btn = gr.Button(value='delete', variant='stop')
                label_search = gr.Markdown('')
            with gr.Column(scale=3):
                with gr.Group():
                    with gr.Row():
                        text_modify_trans = gr.Textbox(label='翻译')
                        text_modify_tag = gr.Dropdown(label='Tag', choices=Dic.get_tag(), multiselect=True,
                                                      max_choices=5)
                    text_modify_description = gr.Textbox(label='描述', lines=7)
                    text_modify_example = gr.Textbox(label='示例', lines=5)


        def clean_input():
            global now_index
            now_index = -1
            return '', '', '', '', []


        def search_word(word):
            global now_index
            index, result = Dic.search_word(word)
            if index == -1:
                return '该词条不存在', '', '', '', []
            else:
                now_index = index
                return 'success', result['Translation'], result['Description'], result['Example'], result[
                    'Tag'].split('|')


        def submit_modify(word, trans, desc, example, tag):
            Dic.modify_word(now_index, word, trans, desc, example, tag)
            return f'修改了{now_index}号词条'


        def del_word(word, tag):
            global now_index
            index = now_index
            now_index = -1
            Dic.del_word(now_index, word, tag)
            return f'删除了{word[0].upper()}-{index}号词条'


        clean_btn.click(clean_input,
                        outputs=[search_input, text_modify_trans, text_modify_description, text_modify_example,
                                 text_modify_tag])

        search_btn.click(search_word, inputs=search_input,
                         outputs=[label_search, text_modify_trans, text_modify_description, text_modify_example,
                                  text_modify_tag])
        submit_btn.click(submit_modify,
                         inputs=[search_input, text_modify_trans, text_modify_description, text_modify_example,
                                 text_modify_tag], outputs=label_search)
        del_btn.click(del_word, inputs=[search_input, text_modify_tag], outputs=label_search)

if __name__ == '__main__':
    demo.launch(auth=Config.AUTH, server_port=Config.PORT)

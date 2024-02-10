import panel as pn
import ipywidgets as widgets
import pandas as pd

from controller.controller import controller

pn.extension("ipywidgets", sizing_mode="stretch_width")
pn.extension("tabulator")


def scrap_and_analyze(event):
    if not event:
        return

    # df = pd.DataFrame({
    #     "Title": ["Sample Title 1", "Sample Title 2", "Sample Title 3"],
    #     "Summary": ["Sample Summary 1", "Sample Summary 2", "Sample Summary 3"],
    #     "Sentiment": ["-1", "0", "1"],
    #     "Resource": ["Reddit", "Youtube", "CNN"],
    #     "Date": ["2024-02-10", "2024-02-09", "2024-02-08"],
    #     "Link": ["http://example.com/link1", "http://example.com/link2", "http://example.com/link3"]
    # }, index=[1, 2, 3])
    collection_data = options_box.collect_data()
    table.value = controller.analyze_event(collection_data)

    print(controller.get_statistics())

    table.visible = True


class OptionsBox:
    def __init__(self):
        common_width = 150
        common_height = 40
        self.tags = widgets.TagsInput(value=['Enter keywords here!'],
                                      allowed_tags=[], allow_duplicates=False,
                                      layout=widgets.Layout(width='85%'))
        self.services = pn.widgets.CheckButtonGroup(name='Services', button_type='primary',
                                                    button_style='outline', options=['Reddit', 'CNN', 'DOU'],
                                                    value=['CNN'], orientation='horizontal', width=300,
                                                    height=common_height)
        self.timeperiod = pn.widgets.Select(options=['Day', 'Week', 'Month'], width=100, height=common_height)
        self.submit_btn = pn.widgets.Button(name='Analyze', button_type='warning',
                                            width=common_width, height=common_height)
        self.options_row = pn.Row(
            self.tags,
            self.services,
            self.timeperiod,
            self.submit_btn
        )

    def collect_data(self):
        return {
            'tags': self.tags.value,
            'services': self.services.value,
            'timeperiod': self.timeperiod.value
        }

    def set_on_analyze_btn_pressed(self, runnable):
        if not callable(runnable):
            raise ValueError("Cannot call the runnable argument")
        pn.bind(runnable, self.submit_btn, watch=True)


options_box = OptionsBox()
options_box.set_on_analyze_btn_pressed(scrap_and_analyze)
user_input = options_box.options_row

tabulator_formatters = {
    'Summary': {'type': 'textarea'},
    'Sentiment': {'type': 'traffic', 'min': -1, 'max': 1, 'color': ["red", "orange", "green"]},
    'Link': {'type': 'link'},
}
table = pn.widgets.Tabulator(
    pd.DataFrame(),
    layout='fit_columns',
    header_align='center',
    text_align='center',
    selectable=False,
    disabled=True,
    visible=False,
    formatters=tabulator_formatters
)

main_page = pn.Column(
    user_input,
    table,
)

template = pn.template.FastListTemplate(
    title="Web Scraping App",
    # logo="",
    header_background="#FFA500",
    accent_base_color="#00A170",
    main=[main_page],
).servable()

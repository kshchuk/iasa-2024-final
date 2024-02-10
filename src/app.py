import panel as pn
import ipywidgets as widgets

pn.extension("ipywidgets", sizing_mode="stretch_width")


def scrap_and_analyze(event):
    pass


class OptionsBox:
    def __init__(self):
        common_width = 150
        common_height = 200
        self.tags = widgets.TagsInput(value=['Enter keywords here!'],
                                      allowed_tags=[], allow_duplicates=False,
                                      layout=widgets.Layout(width='85%'))
        self.services = pn.widgets.CheckButtonGroup(name='Services', button_type='primary',
                                                    button_style='outline', options=['Reddit', 'Facebook', 'DOU'],
                                                    value=['Facebook'], orientation='horizontal', width=300)
        self.submit_btn = pn.widgets.Button(name='Analyze', button_type='warning',
                                            width=common_width)
        self.options_row = pn.Row(
            self.tags,
            self.services,
            self.submit_btn
        )

    def collect_data(self):
        return {
            'tags': self.tags.value,
            'services': self.services.value
        }

    def set_on_analyze_btn_pressed(self, runnable):
        if not callable(runnable):
            raise ValueError("Cannot call the runnable argument")
        pn.bind(runnable, self.submit_btn, watch=True)


options_box = OptionsBox()
user_input = options_box.options_row

template = pn.template.FastListTemplate(
    title="Web Scraping App",
    # logo="",
    header_background="#FFA500",
    accent_base_color="#00A170",
    main=[options_box.options_row],
).servable()
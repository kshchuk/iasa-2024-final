import panel as pn
import ipywidgets as widgets

pn.extension("ipywidgets", sizing_mode="stretch_width")

tags = widgets.TagsInput(
    value=[],
    allowed_tags=[],
    allow_duplicates=False,
)

options = pn.widgets.CheckButtonGroup(
            name='service', button_type='primary',
            button_style='outline', options=['Reddit', 'Facebook', 'DOU'],
            value=['Bar'], orientation='horizontal',
)

main_component = pn.Row(
    tags,
    options,
)
template = pn.template.FastListTemplate(
    title="Web Scraping App",
    # logo="",
    header_background="#FFA500",
    accent_base_color="#00A170",
    main=[main_component],
).servable()
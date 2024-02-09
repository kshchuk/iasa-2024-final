import panel as pn
import ipywidgets as widgets

pn.extension("ipywidgets", sizing_mode="stretch_width")

tags = widgets.TagsInput(
    value=[],
    allowed_tags=[],
    allow_duplicates=False
)

main_component = pn.Row(tags)
template = pn.template.FastListTemplate(
    title="Web Scraping App",
    # logo="",
    header_background="#023020",
    accent_base_color="#023020",
    main=[main_component],
).servable()

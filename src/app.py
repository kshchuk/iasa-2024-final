import panel as pn

main_component = pn.Row()
template = pn.template.FastListTemplate(
    title="Web Scraping App",
    # logo="",
    header_background="#AAFFAA",
    accent_base_color="#AAFFAA",
    main=[main_component],
).servable()

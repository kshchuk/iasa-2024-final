import panel as pn

main_component = pn.Row()
template = pn.template.FastListTemplate(
    title="Scrapping",
    logo="https://i.imgur.com/7NenPSk.png",
    header_background="#AAFFAA",
    accent_base_color="#AAFFAA",
    main=[main_component],
).servable()
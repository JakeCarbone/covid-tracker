import plotly.graph_objs as go
import plotly.io as pio
# from PIL import Image
# import pathlib as pl

# local_root = pl.Path(__file__).parents[0]
# watermark_img = Image.open(local_root / 'images/IM_Copyright.png')


class GraphConfig(object):
    ""
    text_colour="#1c3c4a"
    title_colour = "#73a2ab"
    subtitle_colour = "#1c3c4a"
    bold_colour = '#1c3c4a'
    axis_colour = '#1c3c4a'
    grid_colour = 'rgba(28, 60, 74, 0.5)'
    im_brand_colour = '#73a2ab'

    title_size = 26
    subtitle_size = 20
    legend_text_size = 14
    annotation_text_size = 12

    axis_text_size = 16
    axis_number_size = 12

    text_size = 12

    graph_width = 750
    graph_height = graph_width / 1.5  #1.618

    # Margin is relative to the graph not the full image
    # 1rem margin + 2rem title line height + 0.5rem margin + 1.8rem subtitle height + 1rem
    margin_top = 95 # 16 * (1 + 2 + 0.5 + 1.8 + 1)
    margin_bottom = 110 # margin_top  # tbc
    # 0.5rem margin + 1.4rem axis line height + 2rem + 1.4rem axis numbers + 0.5rem inner margin
    margin_left = 30 # 16 * (0.5 + 1.4 + 2 + 1.4 + 0.5)
    margin_right = 0 # 8
    pad = 0

    # Config options for fig.show - these apply to the in-browser render only
    list_to_remove = ["zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d",
                      "zoomOut2d", "autoScale2d", "resetScale2d -'3D': zoom3d",
                      "pan3d", "rbitRotation", "tableRotation", "handleDrag3d",
                      "resetCameraDefault3d", "resetCameraLastSave3d",
                      "hoverClosest3d -'Cartesian': hoverClosestCartesian",
                      "hoverCompareCartesian -'Geo': zoomInGeo", "zoomOutGeo",
                      "resetGeo", "hoverClosestGeo -'Other': hoverClosestGl2d",
                      "hoverClosestPie", "toggleHover", "resetViews",
                      "toImage: sendDataToCloud", "toggleSpikelines",
                      "resetViewMapbox"]



class GraphTwitterConfig(GraphConfig):
    graph_height = 500
    graph_width = 750*(500/421.0)

class Graph(object):
    ""
    def __init__(self, config=GraphConfig):
        self.config = config

    def style_graph(self,
                    fig,
                    title=False,
                    title_position = [0, 1.27],
                    subtitle_position = [0, 1.15],
                    subtitle='',
                    x_axis_title="XAxis",
                    y_axis_title=False,
                    x_axis_title_gap = 20,
                    data_source="",
                    data_source_position=[0,-0.375], # [x, y]
                    watermark=None, # "left" or "right"
                    watermark_position = [0,-0.375], # [x, y]
                    legend_position = [-0.01,-0.1875], # [x, y]
                    ytozero = True, # Y-xis to zero True or False
                    xhovermode = True, # x-axis hover mode. This means y value hover text always appears regardless if your mouse is over the value or not
                    xaxis_tickangle = 0 # xaxis text angle in degrees of rotation clockwise
                   ):

        """ apply style to an existing graph

            fig is a go.Figure instance
        """
        #plotly graph configs
        fig.update_layout(plot_bgcolor="#ffffff")  # #F9F9F9

        # Controls the font and font size
        fig.update_layout(
            font=dict(family="Libre Baskerville",
                      size=self.config.text_size,
                      color=self.config.text_colour))

        # setting the axis to IM blue
        fig.update_xaxes(showgrid=False,
                ticks="outside",
                tickson="boundaries",
                ticklen=5,
            )


        fig.update_yaxes(showgrid=True,
            ticks="outside",
            tickson="boundaries",
            ticklen=0,
        )

        if title:
            # if logo_position[1] == 0.95: logo_position[1] = 1.1
            if self.config.margin_top == 0: self.config.margin_top = 75

            # fig.update_layout(
            #     title={
            #         'text': "<span style='color:" + self.config.title_colour + ";font-size:" + str(self.config.title_size) + ";'>" + title + "</span><br><span style='font-size:" + str(self.config.subtitle_size) + ";'>" + subtitle + "</span>",
            #         'x': title_position[0], # Control title position with this
            #         'y': title_position[1]
            #     })
        else:
            self.config.margin_top = 0
            # if logo_position[1] > 1: logo_position[1] = 0.95


        # Controlling x-axis
        fig.update_layout(
            xaxis_title=x_axis_title,
            xaxis={'tickfont':{ 'size': self.config.axis_number_size},
                    'titlefont':{ 'size': self.config.axis_text_size}},
        )

        # Controlling y-axis
        if y_axis_title:
            fig.update_layout(
                yaxis_title=y_axis_title,
                yaxis={'tickfont':{ 'size': self.config.axis_number_size},
                        'titlefont':{ 'size': self.config.axis_text_size}}
            )
        else:
            # Removing axis gap if there is no y-axis
            self.config.margin_left = 0

        # You can control the X and Y axis lines with these two lines. I like not having a Y-axis line as it de-cluters the graph
        fig.update_xaxes(showline=True, linecolor=self.config.axis_colour)
        # fig.update_yaxes(showline=False, linecolor=self.axis_colour)

        # Controls the zero lines, sometimes its nice to emphaise the zero line by making it more bold or a slightly differnt colour
        fig.update_yaxes(zeroline=False,
                         zerolinewidth=1,
                         zerolinecolor=self.config.axis_colour)
        fig.update_xaxes(zeroline=False,
                         zerolinewidth=1,
                         zerolinecolor=self.config.axis_colour)

        # Controls the grid lines
        fig.update_xaxes(showgrid=False, gridwidth=1, gridcolor=self.config.grid_colour)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=self.config.grid_colour)

        # Controls the graph size. These values are defined earlier
        fig.update_layout(autosize=True,
#                           width=self.config.graph_width,
#                           height=self.config.graph_height
                         )

        # Adds logo. Mute for no logo
        # if logo:
        #     fig.add_layout_image(
        #         dict(
        #
        #             # source="https://influencemap.org/site/data/000/287/InfluenceMap_Logo_without_Name.jpg", # Chris it would be cool to get this to work from the link
        #             # Yes it would, but it's blocked by CORS cross domain origin rules
        #             # and it's only really useful for online display.
        #             source=watermark_img,
        #             xref="paper",
        #             yref="paper",
        #             x=logo_position[0],
        #             y=logo_position[1],  # control postion with these
        #             sizex=0.15,  # control size with these
        #             sizey=0.15,
        #             xanchor="center",
        #             yanchor="middle"))

        # Adding annotations This can be used for the water mark, data source explanation etc
        annotations = []

        # If watermark is set as 'left' or 'right' this code will add it
        if watermark:
            if watermark == 'right':
                if watermark_position[0] == 0:
                    watermark_position[0] = 1

            annotations.append(dict(
                name="draft watermark",
                text="Leaf",
                textangle=0,
                opacity=1,  #0.1,
                xref="paper",
                yref="paper",
                xanchor=watermark,
                x=watermark_position[0],
                y=watermark_position[1],
                showarrow=False,
                font=dict(
                    size=self.config.annotation_text_size
                    ),
            ))

            # fig.add_layout_image(
            #     dict(
            #
            #         # source="https://influencemap.org/site/data/000/287/InfluenceMap_Logo_without_Name.jpg", # Chris it would be cool to get this to work from the link
            #         # Yes it would, but it's blocked by CORS cross domain origin rules
            #         # and it's only really useful for online display.
            #         source=watermark_img,
            #         opacity=1,
            #         xref="paper",
            #         yref="paper",
            #         x=watermark_position[0],
            #         y=watermark_position[1],
            #         sizex=0.05,  # control size with these
            #         sizey=0.05,
            #         xanchor=watermark))

        # if data_source is set this code will add it
        if data_source:
            annotations.append(
            dict(
                x=data_source_position[0],
                y=data_source_position[1],
                opacity=1,
                showarrow=False,
                text="Data source: %s" % data_source,
                xref="paper",
                yref="paper",
                xanchor='left',
                font=dict(
                    size=self.config.annotation_text_size
                    ),))


        # If we wanted to make the subtitle using annotations this is where we would put it
        if title:
            # print("Title")
            annotations.append(
            dict(
                name="title",
                font = {'color': self.config.title_colour,
                         'size': self.config.title_size},
                x=title_position[0],
                y=title_position[1],
                opacity=1,
                showarrow=False,
                text=title,
                xref="paper",
                yref="paper",
                xanchor='left'))

        # If we wanted to make the subtitle using annotations this is where we would put it
        if subtitle:
            # print("Subtitle")
            annotations.append(
            dict(
                name="subtitle",
                font = {'color': self.config.subtitle_colour,
                          'size':self.config.subtitle_size},
                x=subtitle_position[0],
                y=subtitle_position[1],
                opacity=1,
                showarrow=False,
                text=subtitle,
                xref="paper",
                yref="paper",
                xanchor='left'))


        # adding all annotations set
        fig.update_layout(annotations=annotations)

        ## Control the space around the graph with this
        fig.update_layout(margin=dict(
            l=self.config.margin_left,  #left
            r=self.config.margin_right,  #right
            b=self.config.margin_bottom,  #bottom
            t=self.config.margin_top,  #top
            pad=self.config.pad))

        # bog standard
        if ytozero:
            fig.update_yaxes(rangemode='tozero')

        # Control position of legend with this
        if legend_position != 'default':
            fig.update_layout(legend=dict(x=legend_position[0],
                                          y=legend_position[1],
                                          xanchor='left',
                                          font=dict(
                                            size=self.config.legend_text_size,
                                                ),
                                        ),
                              legend_orientation="h")


        # Spacing the title away from the axis title
        fig.update_xaxes(title_standoff = x_axis_title_gap)


        fig.update_yaxes(title_standoff = (self.config.graph_width / float(self.config.graph_height))*x_axis_title_gap)

        # This makes the hover mode better
        if xhovermode:
            fig.update_layout(hovermode="x")

        # X-axis label angle
        fig.update_layout(xaxis_tickangle=xaxis_tickangle)

        return fig


    def get_config(self, remove_list = False):
        object_to_remove = self.config.list_to_remove.copy()

        if remove_list:
            object_to_remove = remove_list

        config_dict = {
        'displayModeBar': False,
        'scrollZoom': False,
        'displaylogo': False,
        'modeBarButtonsToRemove': object_to_remove,
        'toImageButtonOptions': {
            'format': 'png',  # one of png, svg, jpeg, webp
            'filename': 'Leaf Plot',
            'height': self.config.graph_height,
            'width': self.config.graph_width,
            'scale':
            2  # Multiply title/legend/axis/canvas sizes by this factor. In effect this makes the image more crisp
            }
        }

        return config_dict


    def save_graph_image(self, fig, path):
        """ Jake's demo of various ways of saving graphs

            # ## Saving the plot

            # To get this to work follow the instructions here https://plotly.com/python/static-image-export/
            #
            # Or you can just click the camera icon on the graph above

        """

        fig.write_image(path,
                        width=self.config.graph_width,
                        height=self.config.graph_height,
                        scale=2)

    # Save as html using this code. This will preserve all the interactive aspects of the plot
    def save_graph_html(self, fig, path): # web_or_test can be 'web' or 'test'
        view_path = path.replace('.html', '_view.html')
        div_path = path.replace('.html', '_web.html')

        # Preparing for viewing the html
        include_plotlyjs=True
        full_html=True

        fig.write_html(view_path,
                        full_html=full_html,
                        include_plotlyjs=include_plotlyjs,
                        config=self.get_config())


        # Preparing the html for the IM site
        include_plotlyjs=False
        full_html=False

        temp_list = self.config.list_to_remove.copy()
        temp_list.append("toImage")

        fig.write_html(div_path,
                        full_html=full_html,
                        include_plotlyjs=include_plotlyjs,
                        config=self.get_config(remove_list = temp_list))

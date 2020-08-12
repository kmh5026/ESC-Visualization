#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row
from bokeh.models import Slider, ColumnDataSource, CategoricalColorMapper

gapminder = pd.read_csv('gapminder.csv')
gapminder = gapminder.set_index('Year')

source = ColumnDataSource(data={'x':gapminder.loc[1970].fertility, 'y':gapminder.loc[1970].life,
                                'country':gapminder.loc[1970].Country, 'pop':(gapminder.loc[1970].population / 20000000) + 2,
                                'region':gapminder.loc[1970].region})

xmin, xmax = min(gapminder.fertility), max(gapminder.fertility)
ymin, ymax = min(gapminder.life), max(gapminder.life)

plot = figure(x_axis_label='Fertility (children per woman)', y_axis_label='Life Expectancy (years)',
              title='Gapminder Data for 1970', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))
plot.circle(x='x', y='y', fill_alpha=0.8, source=source)

regions_list = gapminder.region.unique().tolist()
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)
plot.circle(x='x', y='y', fill_alpha=0.8, source=source, 
            color=dict(field='region', transform=color_mapper), legend_field='region')
plot.legend.location = 'top_right'

def update_plot(attr, old, new):
    yr = slider.value
    new_data = {'x':gapminder.loc[yr].fertility, 'y':gapminder.loc[yr].life,
                'country':gapminder.loc[yr].Country, 'pop':(gapminder.loc[yr].population / 20000000) + 2,
                'region':gapminder.loc[yr].region}
    source.data = new_data
    
slider = Slider(start=1970, end=2010, step=1, value=1970, title='Year')
slider.on_change('value', update_plot)
layout = row(widgetbox(slider), plot)
curdoc().add_root(layout)
curdoc().title='Gapminder'


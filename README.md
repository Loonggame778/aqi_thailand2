<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Model-Air-Pollution-Thailand-and-South-East-Asian-Countries" data-toc-modified-id="Model-Air-Pollution-Thailand-and-South-East-Asian-Countries-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Model Air Pollution Thailand and South East Asian Countries</a></span></li><li><span><a href="#Requirements" data-toc-modified-id="Requirements-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Requirements</a></span></li><li><span><a href="#Directory-Tree" data-toc-modified-id="Directory-Tree-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Directory Tree</a></span></li><li><span><a href="#Data-Sources" data-toc-modified-id="Data-Sources-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Data Sources</a></span><ul class="toc-item"><li><span><a href="#Pollution-Data" data-toc-modified-id="Pollution-Data-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Pollution Data</a></span></li><li><span><a href="#Weather-Data" data-toc-modified-id="Weather-Data-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>Weather Data</a></span></li><li><span><a href="#Hotspot-Data" data-toc-modified-id="Hotspot-Data-4.3"><span class="toc-item-num">4.3&nbsp;&nbsp;</span>Hotspot Data</a></span></li></ul></li><li><span><a href="#AQI-Convention" data-toc-modified-id="AQI-Convention-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>AQI Convention</a></span></li><li><span><a href="#Modeling-Air-Pollution-in-Chiang-Mai-Data-:-A-Case-Study" data-toc-modified-id="Modeling-Air-Pollution-in-Chiang-Mai-Data-:-A-Case-Study-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Modeling Air Pollution in Chiang Mai Data : A Case Study</a></span><ul class="toc-item"><li><span><a href="#Casual-Diagram" data-toc-modified-id="Casual-Diagram-6.1"><span class="toc-item-num">6.1&nbsp;&nbsp;</span>Casual Diagram</a></span></li><li><span><a href="#Exploratory-Data-Analysis" data-toc-modified-id="Exploratory-Data-Analysis-6.2"><span class="toc-item-num">6.2&nbsp;&nbsp;</span>Exploratory Data Analysis</a></span></li></ul></li></ul></div>

# Model Air Pollution Thailand and South East Asian Countries

This project aims to use a machine learning model predict and identify sources of the air pollution South East Asian cities. Because this is a multi-variables problem with complex interaction among features, and time-lag, a machine learning approch has an advantage over a traditional approach. Here, random forest regressor(RF) is used to model a small particle pollution(PM2.5) level. After trying searching various machine learning model, I found that RF perform the best. In addition, the model can be easily interpreted. The model's feature of importances in combination data exploration helps identify the major sources of air pollution. In addition, I will use the model to simulate the pollution level when an environmental policies are implemented. I use Chiang Mai as a case study, but the codes works with other cities such as Bangkok, and Hanoi (Given there are enough data, of course!)

# Requirements

numpy==1.18.1<br>
matplotlib==3.1.2<br>
pandas==1.0.0<br>
geopandas==0.6.2<br>
scikit_optimize==0.7.4 <br>
scikit_learn==0.23.2<br>
TPOT==0.11.5<br>
statsmodels==0.11.1<br>
scipy==1.4.1<br>
seaborn==0.10.0<br>
joblib==0.14.1<br>
tqdm==4.43.0<br>
Shapely==1.7.0<br>
pyproj==2.4.2.post1<br>
Fiona==1.8.13<br>
bokeh==2.1.1<br>
selenium==3.141.0 <br>
wget==3.2<br>
beautifulsoup4==4.9.1<br>
requests==2.22.0<br>
swifter==1.0.3<br>
Sphinx>=1.6.0<br>

# Directory Tree

<pre>
├── README.md   
├── requirements.txt : generated by pipreqs
├── data : raw data and processed data for each cities. Please see the data section for details about how to obtains the raw data
├── docs._build.html : code documentations generated by Sphinx 
├── models : each subfolder contains a model for a each city.  
│   ├──  chiang_mai : contains random forest models for Chiang Mai and model meta file containing setting
│   └── bangkok   
├── reports : plots for each city 
│   ├── chiang_mai : data and model visualizations for Chiang Mai
│   └── bangkok   
├── notebooks   
│   ├── 1_pollutions_data.ipynb : 
│   ├── 1.1_vn_power_plants.ipynb : 
│   ├── 2_analyze_pollution_data.ipynb : 
│   ├── 5.0-ML_Chiang_mai.ipynb : 
│   ├── 6.0_vis_ChiangMai.ipynb : 
│   ├── 6.1_BKK.ipynb : 
│   ├── 6.2_vis_Jarkata.ipynb : 
│   ├── 6.3_Hanoi.ipynb : 
│   └── 7_prediction.ipynb : 
│   
└── src : the source codes are meant to be ran as a module not as .py (except for vn_data.py) 
    ├── imports.py : 
    ├── gen_functions.py : general purpose functions such as color setting, AQI conversion and coordinate Conversion
    ├── data : download and preprocess data 
    │   ├── download_data.py :  download pollution data from various sources 
    │   ├── read_data.py :  read pollution data 
    │   ├── vn_data.py : scrape pollution data from Vietnamese EPA
    │   ├── weather_data.py : scrape, process and load weather data
    │   └── fire_data.py : process and load hotspots data
    │     
    ├── features   
    │   ├── build_features.py : 
    │   └── dataset.py : Dataset object is responsible for putting raw data together, 
    │                    feature engineering and preparing matricies for machine learning models. 
    │                    Call read_data.py when loading data
    │                    Call build_features.py for feature engineering functions 
    ├── models   
    │   ├── train_model.py :  model builder and hyperparameter searcher
    │   └── predict_model.py : load model and perform statistical simulations
    │   
    └── visualization  
        ├── vis_data.py : create plots for data exploration steps   
        └── vis_model.py : create plots for visualizing model performance and simulation 
</pre>

# Data Sources

## Pollution Data
 - [Thailand Pollution Department](http://air4thai.pcd.go.th/webV2/) Data only go back 2 months! so need to run scapper once a month using `src.data.download_data.update_last_air4Thai()` . Once can also writes a letter to ask for historical data directly. The request took about a month to process. The data has to be parsed from their excel files.  
 - [Vietnamese Pollution Department](http://enviinfo.cem.gov.vn/) Pollution data for major cities such as Hanoi. Data only go back 24 hours, so need to run scapper once a day. This is done using using `src.data.vn_data.download_vn_data()`
 - [Berkeley project](http://berkeleyearth.org/) provides historical PM2.5 data back until late 2016 
 - [US Embassy](http://dosairnowdata.org/dos/historical/) US embassy in some cities collect PM2.5 data. Use `src.data.download_data.download_us_emb_data()` to download data. 
 - [Chiang Mai University Monitoring Stations](https://www.cmuccdc.org/) provides data from the University monitoring stations in the northern part of Thailand. Use `src.data.download_data..download_cdc_data()` to download this data.  
 - [The World Air
Quality Project](https://aqicn.org/) has pollutions data from many cities, but only provide daily average data  

## Weather Data 

Weather data is from two sources. 

- [OpenWeathermap](https://openweathermap.org/history) provides a bulk historial data to purchase. The data is processed using `src.data.weather_data.proc_open_weather()`
- Additional weather data is constantly scraped from [Weather Underground)(https://www.wunderground.com/) `src.data.weather_data.update_weather()` 

Both the pollution data and weather data are can be downloaded using one single command `src.data.download_data.main()`


## Hotspot Data 

Satellite data showing location of burning activities(hotspots) from NASA https://firms.modaps.eosdis.nasa.gov/download/. There are three data product. This study uses MODIS Collection 6 data because of the data available for a longer period that other products.

# AQI Convention

Countries have different standards, which convert the raw polution readings into air quality index(AQI) and interpret the harmful levels. The maximum AQIs for each pollutants (PM2.5, Pm10, SO2 etc) is reported at a single AQI. The figure belows compare US and Thailand AQI. The standards are comparable except for SO$_2$, where the US has a stricker standard. This study use US AQI conversion standard for calculating AQI for different pollutants. For example, in the PM2.5 case 
- 0 - 50 AQI is in a healthy range. This corresponds to PM2.5 level between 0 - 12 $\mu g/m^3$ (green). 
- 50 - 100 AQI is a moderate range, corresponding to PM2.5 12- 35.4  $\mu g/m^3$ (orange)
- 100 - 150 AQI is a unhealthy for sensitive group, corresponding to PM2.5 35.5- 55.4  $\mu g/m^3$ (red)
- 150 - 200 AQI is a unhealthy range, corresponding to PM2.5 55.5- 150.4  $\mu g/m^3$ (red)

For simplicity, the color code in this study groups the  100 - 150 and 150 - 200 as unhealthy range(red). 


```python
#  Load the "autoreload" extension so that code can change
%reload_ext autoreload
%autoreload 2
import src
```


```python
src.visualization.vis_data.compare_aqis(filename='../reports/chiang_mai/aqi.png')
```

![png](https://github.com/worasom/aqi_thailand2/blob/master/reports/chiang_mai/aqi.png)

#  Modeling Air Pollution in Chiang Mai Data : A Case Study

## Casual Diagram

![Casual Diagram](https://github.com/worasom/aqi_thailand2/blob/master/reports/chiang_mai/casual_di.png)

## Exploratory Data Analysis

The first step before any machine learning model is to understand the data. The file `src.visualization.vis_data.py` contains many useful functions for quick data visualization. Here, pollution data in Chiang Mai is used to illustrate visualization functions. 

![map of Chiang Mai](https://github.com/worasom/aqi_thailand2/blob/master/reports/chiang_mai/cm_map.png)

![different pollutants](https://github.com/worasom/aqi_thailand2/blob/master/reports/chiang_mai/all_pol_aqi.png)

Seasonal patterns of PM2.5 level(top), number of hotspots within 1000 km from Chiang Mai(middle), and temperature(bottom). The shaded regions are 95% confident interval from different years. (top) the horizontal lines indicate the values corresponded to AQI 100 (moderate) and 150 (unhealthy) accordingly. The number of hotspots has a similar seasonal pattern as the PM2.5’s.

![seasonal pattern](https://github.com/worasom/aqi_thailand2/blob/master/reports/chiang_mai/fire_PM25_t_season.png)

![seasonal pattern](https://github.com/worasom/aqi_thailand2/blob/master/reports/chiang_mai/fire_PM25_season.png)


```python

```


```python

```

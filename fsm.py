import numpy as np
import pandas as pd
import openpyxl
import streamlit as st
import altair as alt

import dataReader
#test

# LAYOUT
st.set_page_config(layout="wide")

st.header('🚇 Fare and Service Modeling Platform 🚇')

df_riders, df_fares, df_elasticities = dataReader.getData("data.xlsx")





# TAB STRUCTURE L0
tab0_0, tab0_1 = st.tabs(["Fare Structure", "Power User"])

with tab0_0:

	#COLUMN STRUCTURE L1

	col10, col11, col12 		= st.columns([1,1,4])

	with col10:
		with st.form(key = "railform"):
			st.text("Rail")
			v_railfare 				= st.slider("Rail fare", key="railfare", value=1.5, min_value=0., max_value=5., step=.10, format="$%.2f")
			v_railseniordiscount 	= st.slider("Senior Discount", value=50, min_value=0, max_value=100, step=10, format="%i%%")
			st.form_submit_button("Apply")
			df_fares.loc[(df_fares["Mode"] == "Rail") & (df_fares["FareClass"] == "Standard"), "NewFare"] = v_railfare
			df_fares.loc[(df_fares["Mode"] == "Rail") & (df_fares["FareClass"] == "Senior"), "NewFare"] = v_railfare * (1 - (v_railseniordiscount / 100))




	with col11:
		with st.form(key="busform"):
			st.text("Bus")
			v_busfare 				= st.slider("Base fare", key="busfare", value=1.5, min_value=0., max_value=5., step=.10, format="$%.2f")
			v_busseniordiscount 	= st.slider("Senior Discount", value=50, min_value=0, max_value=100, step=10, format="%i%%")
			st.form_submit_button("Apply")			
			df_fares.loc[(df_fares["Mode"] == "Bus") & (df_fares["FareClass"] == "Standard"), "NewFare"] = v_busfare
			df_fares.loc[(df_fares["Mode"] == "Bus") & (df_fares["FareClass"] == "Senior"), "NewFare"] = v_busfare * (1 - (v_busseniordiscount / 100))
			
					


	with col12:
		st.text("Monthly Impact")
		a_segmentation = st.radio("Segmentation", ('Mode', 'Equity', 'Jurisdiction'))

		df_fares = pd.merge(df_fares, df_elasticities, how='left', left_on=["Mode"], right_on=["Mode"])
		df_fares["FareDiff"] = df_fares["NewFare"] - df_fares["BaseFare"]
		df_fares["ElastFactor"] = df_fares["Elasticity"] * df_fares["FareDiff"]
		df_riders_ = pd.merge(df_riders, df_fares, how='left', left_on=["Mode", "FareClass"], right_on=["Mode", "FareClass"])
		df_riders_["NewRiders"] = (df_riders_["Riders"] * (1 + df_riders_["ElastFactor"])).round(0)

		df_display = df_riders_[["Mode", "Equity", "FareClass", "Jurisdiction", "Riders", "NewRiders", "BaseFare", "NewFare"]]

		df_display["BaseRevenue"] 	= df_display["Riders"] 		* df_display["BaseFare"]
		df_display["NewRevenue"] 	= df_display["NewRiders"] 	* df_display["NewFare"]

		df_display_rev = pd.melt(df_display, id_vars=["Mode", "Equity", "FareClass", "Jurisdiction"], value_vars=["BaseRevenue", "NewRevenue"])
		df_display_rid = pd.melt(df_display, id_vars=["Mode", "Equity", "FareClass", "Jurisdiction"], value_vars=["Riders", "NewRiders"])
	
		df_display_rev.columns = ["Mode", "Equity", "FareClass", "Jurisdiction", "Period", "Revenue"]
		df_display_rid.columns = ["Mode", "Equity", "FareClass", "Jurisdiction", "Period", "Riders"]

		df_display_rev["Period"] = ["Proposed" if x=="NewRevenue" 	else "Existing" for x in df_display_rev["Period"]]
		df_display_rid["Period"] = ["Proposed" if x=="NewRiders" 	else "Existing" for x in df_display_rid["Period"]]

		df_display_ = df_display_rev.merge(df_display_rid, how="left", on=["Mode", "Equity", "FareClass", "Jurisdiction", "Period"])
		df_display_ = pd.melt(df_display_, id_vars=["Mode", "Equity", "FareClass", "Jurisdiction", "Period"], value_vars=["Revenue", "Riders"])

		tooltip = ["Mode", "Equity", "Jurisdiction"]
		tooltip.remove(a_segmentation)

		c_ridership = alt.Chart(df_display_[["Mode", "Equity", "Jurisdiction", "Period", "variable", "value"]]).mark_bar().encode(
			x="Period", 
			y="value",
			column="variable",
			color=a_segmentation, 
			tooltip=tooltip)
		st.altair_chart(c_ridership)
		

with tab0_1:
	st.header("Power User")
	st.text("Congrats on being a Powerful User")
	st.image("https://static.streamlit.io/examples/dog.jpg", width=200)


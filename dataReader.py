import pandas as pd
import streamlit as st

def main():
	print(getData("data.xlsx"))

@st.cache(allow_output_mutation=True)
def getData(filename):
	_df_ridership 		= pd.read_excel(filename, sheet_name="ridership", header=0)
	_df_fares			= pd.read_excel(filename, sheet_name="fares", header=0)
	_df_elasticities 	= pd.read_excel(filename, sheet_name="elasticities", header=0)
	return _df_ridership, _df_fares, _df_elasticities


if __name__ == '__main__':
	main()